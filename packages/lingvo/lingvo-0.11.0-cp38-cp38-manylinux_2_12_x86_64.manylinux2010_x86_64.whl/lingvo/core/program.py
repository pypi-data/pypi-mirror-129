# Lint as: python3
# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Programs for interleaving execution on TPU."""

import contextlib
import multiprocessing.dummy
import os
import queue
import time

from lingvo import base_trial
import lingvo.compat as tf
from lingvo.core import base_model
from lingvo.core import checkpointer
from lingvo.core import cluster_factory
from lingvo.core import hyperparams
from lingvo.core import metrics
from lingvo.core import ml_perf_log as mlp_log
from lingvo.core import py_utils
from lingvo.core import summary_utils

# pylint:disable=g-direct-tensorflow-import
from tensorflow.core.protobuf.tpu import compilation_result_pb2 as tpu_compilation_result
from tensorflow.python.tpu import tpu
from tensorflow.python.tpu import tpu_function
from tensorflow.python.tpu import training_loop as tpu_training_loop
from tensorflow.python.tpu.ops import tpu_ops

# pylint:enable=g-direct-tensorflow-import
FLAGS = tf.flags.FLAGS


class BaseProgram:
  """A Program associated with a Task.

  This is inspired by the "program" multi-tenancy that TPUs
  support. Essentially, each program corresponds with a
  sub-graph can exist in the same Graph/Session.

  Upon first execution, it is XLA/JIT compiled and is subsequently
  available to be executed on demand without significant delay.

  Program's provides the following functionality:

    - Builds a sub-graph
    - Writes summaries
    - Runs for pre-determined `steps_per_loop` steps with appropriate infeeds
  """

  @classmethod
  def Params(cls):
    """"Defaults parameters for Programs."""
    p = hyperparams.InstantiableParams(cls)
    p.Define('task', None, 'Underlying task')
    p.Define('logdir', None, 'Log directory')
    p.Define('num_splits_per_client', None, '')
    p.Define('steps_per_loop', None, 'Number of steps to run.')
    p.Define('dataset_name', None,
             'Dataset the program is operating on, eg: "Test"')
    p.Define('name', 'base_program', 'Program name.')
    p.Define('task_name', None,
             'If multi-task, what the high-level task name is')
    p.Define('num_threads', 1, 'Number of threads in multiprocessing pool.')
    p.Define('spmd', False, 'Whether program is running under SPMD mode.')
    p.Define('write_train_input_stats', False,
             'Whether to write input data stats during training.')
    p.Define('max_metrics', 256, 'Overrides TpuEvalMetrics.max_metrics')
    p.Define('ml_perf', None, 'MLPerf config')
    return p

  def __init__(self,
               params,
               shared_model=None,
               trial=base_trial.NoOpTrial(),
               **kwargs):
    self.params = params.Copy()
    p = self.params
    p.task = trial.OverrideModelParams(p.task)
    self._task_params = p.task
    self._logdir = p.logdir
    self._task_name = p.task_name
    self._program_name = ''
    self._shared_model = shared_model
    self._tf_master = kwargs.pop('tf_master', None)
    self._write_train_input_stats = p.write_train_input_stats
    self._trial = trial

    # Program dirs are where the summaries are written to.
    if p.task_name:
      program_dir_name = (
          p.task_name + '_' + p.name + '_' + p.dataset_name.lower())
    else:
      program_dir_name = p.name + '_' + p.dataset_name.lower()
    self._program_dir = os.path.join(self._logdir, program_dir_name)
    tf.io.gfile.makedirs(self._program_dir)
    with tf.io.gfile.GFile(os.path.join(self._program_dir, 'params.txt'),
                           'w') as f:
      f.write(p.ToText())
    # Initialized on use; access via self._summary_writer property only.
    self._summary_writer_obj = None

    tf.io.gfile.makedirs(self._logdir)
    # Just a standard spot that all programs may restore from.
    self._checkpoint_dir = os.path.join(self._logdir, 'train')
    tf.io.gfile.makedirs(self._checkpoint_dir)

    self._steps_per_loop = p.steps_per_loop
    self.num_splits_per_client = p.num_splits_per_client
    self.data_parallelism = p.num_splits_per_client

    # Thread Pool for infeed.
    self._infeed_pool = multiprocessing.dummy.Pool(p.num_threads)

    self._compile_op = None
    self._status_msg_fn = None

    # Same param as in the TPU executor program schedule.
    # Used mainly for each program to check if training is scheduled.
    self.train_executions_per_eval = None
    # Set input repeat_steps to steps_per_loop, if repeat_steps was undefined
    # but available, and also 'resettable' is False.
    # This allows a repeating input TF Dataset (without reset) to take, for each
    # repeat/loop, exactly steps_per_loop batches of data.
    if (hasattr(self._task_params, 'input') and
        not getattr(self._task_params.input, 'resettable', True) and
        hasattr(self._task_params.input, 'repeat_steps') and
        self._task_params.input.repeat_steps is None and self._steps_per_loop):
      tf.logging.info('Setting input repeat_steps to %d', self._steps_per_loop)
      self._task_params.input.repeat_steps = self._steps_per_loop

    self._InitializeVizier()

  def _InitializeVizier(self):
    """Checks if this program should report metrics to vizier."""
    p = self.params
    self._should_report_metrics = False

    reporting_job = self._task_params.cluster.reporting_job
    job_split = self._task_params.cluster.reporting_job.split('/')

    if len(job_split) != 2:
      # The default setting for reporting job is 'evaler'. This is not valid
      # for use with program. We only warn only since we may not be in a vizier
      # setting.
      tf.logging.info('reporting_job should be of the form '
                      'program_name/dataset_name with exactly one / '
                      f'instead got {reporting_job}')
      return

    vizier_program_name, vizier_dataset_name = job_split
    if p.name == vizier_program_name and p.dataset_name == vizier_dataset_name:
      tf.logging.info(f'Adding reporting for {reporting_job}')
      self._should_report_metrics = True

  @property
  def _summary_writer(self):
    """Returns the FileWriter object to use for summaries."""
    # Initialize on first use, so that subclasses can override the
    # implementation without creating a default FileWriter in the constructor.
    if self._summary_writer_obj is None:
      if py_utils.IsEagerMode():
        self._summary_writer_obj = tf.compat.v2.summary.create_file_writer(
            self._program_dir)
      else:
        self._summary_writer_obj = tf.summary.FileWriter(self._program_dir)
        # Apply a custom Tensorboard layout for input data stats if writing
        # TF summaries for input data stats is enabled and a custom layout is
        # defined by the input generator.
        if (self._task.input.input_data_summary_layout is not None and
            self._write_train_input_stats):
          self._summary_writer_obj.add_summary(
              self._task.input.input_data_summary_layout)
    return self._summary_writer_obj

  def _SummarizeValue(self, steps, tag, value):
    if py_utils.IsEagerMode():
      with self._summary_writer.as_default():
        tf.compat.v2.summary.scalar(tag, value, step=steps)
    else:
      self._summary_writer.add_summary(
          metrics.CreateScalarSummary(tag, value), steps)

  def _WriteSummaries(self, job_name, global_step, summaries):
    """Write summaries to be viewed by TensorBoard.

    Args:
      job_name: The name of this job ('trainer', 'evaler', etc.)
      global_step: Integer number of trainer steps (not a tensor).
      summaries: Dict of {summary_name: tf.Summary()}.
    """
    if not summaries:
      return
    with contextlib.ExitStack() as stack:
      if py_utils.IsEagerMode():
        stack.enter_context(self._summary_writer.as_default())
      for unused_name, summary in sorted(summaries.items()):
        if py_utils.IsEagerMode():
          # TODO(laigd): make this work with v1 summaries.
          # tf.compat.v2.summary.scalar(tag, value, step=steps)
          pass
        else:
          self._summary_writer.add_summary(summary, global_step)
        if summary.value:
          for value in summary.value:
            if value.HasField('simple_value'):
              tf.logging.info('%s summary on checkpoint@%d %s = %.8g', job_name,
                              global_step, value.tag, value.simple_value)
        self._summary_writer.flush()

  def _WriteInputDataStats(self, sess=None):
    """Write input data stats for model training as TF summaries.

    Args:
      sess: The Tensorflow session.
    """
    if (self._task.input.merged_input_data_summary_op is None or
        not self._write_train_input_stats):
      return

    global_step = sess.run(self._model.global_step)
    if (global_step %
        self._task.input.params.input_stats_summary_interval_steps == 0):
      summary_str = sess.run(self._task.input.merged_input_data_summary_op)
      self._summary_writer.add_summary(summary_str, global_step)
      self._summary_writer.flush()

  def _InfeedLoop(self, sess=None):
    """Infeed loop for input generator for batched data and input data stats."""
    tf.logging.info(f'_InfeedLoop start {self._program_name} '
                    f'on dataset {self.params.dataset_name}')
    try:
      for i in range(self._steps_per_loop):
        tf.logging.vlog(1, '_InfeedLoop %d', i)
        sess.run(self._task.input.tpu_infeed_op)
      self._WriteInputDataStats(sess)
      tf.logging.info('_InfeedLoop done')
    except Exception as e:
      tf.logging.info('_InfeedLoop exception %r %s', e, e)
      raise

  def _ReportVizierMetrics(self, global_step, metrics_dict):
    """Report metrics to vizier service.

    Args:
      global_step: Int.
      metrics_dict: A dict of metric name -> metric values.

    Returns:
      vizier_early_stop: Boolean, indicates if early stopping has bee requested
        by vizier.
    """
    p = self.params
    if self._should_report_metrics:
      tf.logging.info(f'Reporting Vizier metrics for {p.name}/{p.dataset_name}')
      vizier_early_stop = self._trial.ReportEvalMeasure(global_step,
                                                        metrics_dict, '')
      if global_step >= self._task_params.train.max_steps or vizier_early_stop:
        self._trial.ReportDone()

    else:
      vizier_early_stop = False
    # Export cluster metrics as well.
    cluster_factory.Current().ExportMetrics(
        global_step, {k: metric.value for k, metric in metrics_dict.items()})
    return vizier_early_stop

  def BuildTpuSubgraph(self):
    """Sub classes should construct a model/graph to be executed by Run.

    Specific to TPU execution, this may involve a
    @tpu_function.on_device_training_loop etc.
    """
    raise NotImplementedError()

  def SetStatusMessageFn(self, fn):
    """Workaround since we instantiate programs via Params."""
    self._status_msg_fn = fn

  def SetStatusMessage(self, msg):
    """Write to borglet status."""
    if self._status_msg_fn:
      self._status_msg_fn(msg)
    else:
      tf.logging.info('Status: %s', msg)

  def Compile(self, sess=None):
    """Compile the program using the given session handle."""
    self.SetStatusMessage('Init inputs %s' % self._program_name)
    self._task.input.Initialize(sess)
    self.SetStatusMessage('Init inputs %s done.' % self._program_name)

    if not py_utils.IsEagerMode() and self._compile_op is not None:
      self.SetStatusMessage('Compiling %s' % self._program_name)
      result = sess.run(self._compile_op)
      proto = tpu_compilation_result.CompilationResultProto()
      proto.ParseFromString(result)
      if proto.status_error_message:
        tf.logging.fatal('Compilation failed: {}'.format(
            proto.status_error_message))
      tf.logging.info('Compiling %s done.', self._program_name)

  def Run(self, sess=None, threadpool=None):
    """Execute the program using the given session handle.

    Args:
      sess: TF Session.
      threadpool: A ThreadPool on the executor for running async functions.

    Returns:
      done: Whether to end all execution.
    """
    raise NotImplementedError()

  def Shutdown(self):
    """Runs any necessary cleanup (potentially blocking)."""
    pass

  def CreateCheckpointer(self, init_op=None):
    """Creates a checkpointer, whose version depends on the mode and config.

    Args:
      init_op: The initialize variables op. If unset, it will call
        tf.global_variables_initializer().

    Raises:
      TypeError: When the function is called in Eager mode.
    """
    if py_utils.IsEagerMode():
      raise TypeError('Not supported in Eager mode.')
    else:
      self._checkpointer = checkpointer.Checkpointer(
          self._checkpoint_dir, self._model, init_op=init_op)

  def RestoreIfNeeded(self, sess=None):
    if py_utils.IsEagerMode():
      raise TypeError('Not supported in Eager mode.')
    else:
      self._checkpointer.RestoreIfNeeded(sess)

  def SaveProgramState(self, sess=None, global_step=None):
    """Saves program state information that need to be loaded during restore."""
    pass

  def _InstantiateTaskModel(self, task_params):
    """Instantiates a model object for a particular task.

    MultiTaskModels can accept a shared_model parameter, but SingleTaskModels
    cannot, so we handle them separately here.

    Args:
      task_params: An params instance that constructs either a SingleTaskModel
        or a MultiTaskSubModel.

    Returns:
      An instantiated object based on task_params.
    """
    if issubclass(task_params.cls, base_model.MultiTaskSubModel):
      return task_params.Instantiate(shared_model=self._shared_model)
    return task_params.Instantiate()

  def _OutfeedEnqueue(self, per_example_tensors):
    if not per_example_tensors:
      return tf.constant(0.0)
    per_example_tensors = py_utils.NestedMap(per_example_tensors)
    device = tpu.core(0) if self.spmd else ''
    with tf.device(device):
      return tpu_ops.outfeed_enqueue_tuple(per_example_tensors.Flatten())

  def GetModel(self):
    return self._model


class InputBenchmark(BaseProgram):
  """Measures input generation steps/sec depending on the params below."""

  @classmethod
  def Params(cls):
    p = super().Params()
    p.Define('warmup_loops', 1,
             'How many loops to warmup before measuring elapsed time.')
    p.Define('measurement_loops', 5, 'How many loops to measure across.')
    return p

  def __init__(self, params, shared_model=None, **kwargs):
    super().__init__(
        params, shared_model=shared_model, input_benchmark_only=True, **kwargs)
    self._program_name = 'InputBenchmark'

  def BuildTpuSubgraph(self):
    with py_utils.OpportunisticVariableReuseScope(True):
      self._model = self._InstantiateTaskModel(self._task_params)
    self._task = self._model.GetTask()
    self._task.input.CreateTpuEnqueueOps(benchmark_only=True)

  def Run(self, sess=None):
    p = self.params
    # Input benchmark doesn't work with eager yet.
    assert not py_utils.IsEagerMode()

    for _ in range(p.warmup_loops):
      self._InfeedLoop(sess)

    start_time = time.time()
    for _ in range(p.measurement_loops):
      self._InfeedLoop(sess)
    elapsed_secs = time.time() - start_time

    steps_per_sec = p.measurement_loops * self._steps_per_loop / elapsed_secs
    tf.logging.info('Input benchmark: steps/sec %f', steps_per_sec)
    return True


class TrainProgram(BaseProgram):
  """TrainProgram trains a single task and handles checkpoints."""

  def __init__(self, params, shared_model=None, **kwargs):
    super().__init__(params, shared_model=shared_model, **kwargs)
    self._step_rate_tracker = summary_utils.StepRateTracker()
    self._program_name = 'TrainProgram'
    p = self.params
    if (p.ml_perf is not None and p.ml_perf.benchmark_name is not None and
        p.ml_perf.steps_per_epoch is not None):
      self._ml_perf = p.ml_perf
    else:
      self._ml_perf = None

  def _OutfeedDequeueLoop(self, per_example_tensors, num_loops, num_devices):
    """Process all per-example tensor outfeed data for a TPU sess.run.

    Args:
      per_example_tensors: dict of key -> tensor as generated by TpuTrainStep.
      num_loops: number of times that TpuTrainStep will be executed by TpuTrain.
      num_devices: number of TPU cores assigned to this process.

    Returns:
      A dict of per-example tensors from the latest TpuTrainStep.
    """
    if not per_example_tensors:
      return tf.constant(0.0)

    tensor_shapes = [
        py_utils.GetShape(per_example_tensors[key])
        for key in sorted(per_example_tensors)
    ]
    tensor_types = [
        tf.as_dtype(per_example_tensors[key].dtype)
        for key in sorted(per_example_tensors)
    ]

    def LoopBody(i, *input_arrays):
      """Process outfeed data for a single TpuTrainStep.

      Args:
        i: current loop index.
        *input_arrays: One tf.TensorArray per outfeed tensor.

      Returns:
        i+1 (new index) plus post-write tf.TensorArray handles.
      """
      # Outfeed ops execute on each JF node, so they must be located on the
      # nodes.
      outfeed_devices = []
      device_assignment = py_utils.GetTpuDeviceAssignment()
      assert device_assignment
      for replica in range(device_assignment.num_replicas):
        num_cores_per_replica = 1 if self.spmd else (
            device_assignment.num_cores_per_replica)
        for core in range(num_cores_per_replica):
          with tf.device(device_assignment.host_device(replica, core)):
            outfeed_devices.append(
                tpu_ops.outfeed_dequeue_tuple(
                    tensor_types,
                    tensor_shapes,
                    device_ordinal=device_assignment.tpu_ordinal(replica,
                                                                 core)))
      offset = i * num_devices
      output_arrays = list(input_arrays)
      # Each output_array holds a different per-example tensor. We get results
      # for each tensor from each TPU for each TpuTrainStep call.
      for j in range(len(output_arrays)):
        for k in range(len(outfeed_devices)):
          output_arrays[j] = output_arrays[j].write(offset + k,
                                                    outfeed_devices[k][j])

      return tuple([i + 1] + output_arrays)

    def LoopCond(i, *output_arrays):
      del output_arrays
      return i < num_loops

    output_arrays = []
    for i in range(len(tensor_shapes)):
      output_arrays.append(
          tf.TensorArray(
              tensor_types[i],
              size=num_loops * num_devices,
              element_shape=tensor_shapes[i]))
    # Loop once for each time that TpuTrainStep runs.
    output_arrays = tf.while_loop(
        LoopCond, LoopBody, [0] + output_arrays, parallel_iterations=1)[1:]
    concatenated_arrays = [array.concat() for array in output_arrays]
    return dict(zip(sorted(per_example_tensors), concatenated_arrays))

  def TpuTrainStep(self, *args):
    """Train a shard of a batch on a single TPU core.

    Args:
      *args: metrics values from previous steps.

    Returns:
      New summed metrics values and a train_op.
    """
    with tf.name_scope('tpu_train'):
      with py_utils.OpportunisticVariableReuseScope(True):
        with contextlib.ExitStack() as stack:
          if py_utils.IsEagerMode():
            stack.enter_context(py_utils.GradientTape())
          self._model.ConstructFPropBPropGraph()
      per_step_eval_metrics = self._eval_metrics.SetMetrics(
          self._task.eval_metrics, args)
      outfeed_op = self._OutfeedEnqueue(self._task.per_example_tensors)
      summed_metrics = []
      assert len(per_step_eval_metrics) == len(args)
      with tf.control_dependencies([outfeed_op]):
        for x, y in zip(per_step_eval_metrics, args):
          summed_metrics.append(x + y)
      return summed_metrics + [self._task.train_op]

  def BuildTpuSubgraph(self):
    tf.logging.info('TrainProgram BuildTpuSubGraph')
    p = self.params
    self.spmd = (
        self.params.spmd or
        self._task_params.input.use_partitioned_infeed_queue)

    self._eval_metrics = metrics.TpuEvalMetrics(max_metrics=p.max_metrics)

    with py_utils.OpportunisticVariableReuseScope(True):
      self._model = self._InstantiateTaskModel(self._task_params)
    self._task = self._model.GetTask()
    self._task.input.TpuSetup()

    @tpu_function.on_device_training_loop
    def TpuTrainLoop():
      loop_result = tpu_training_loop.repeat(
          self._steps_per_loop,
          self.TpuTrainStep,
          inputs=self._eval_metrics.initial_values,
          name='train_loop')
      # Final metrics are the avg across self._steps_per_loop steps.
      return self._eval_metrics.FinalizeMetrics(loop_result)

    def TrainFunc():
      if py_utils.IsEagerMode():
        # Run the infeed loop in the same function that runs the training loop,
        # so that infeed enqueue/dequeue ops are created by the same
        # InfeedQueue.
        def InfeedBody(i):
          self._task.input.CreateTpuEnqueueOps()
          # Auto control dependency may not support TPU infeed ops, so add the
          # dependency manually.
          with tf.control_dependencies(self._task.input.tpu_infeed_op):
            return i + 1

        tf.while_loop(
            cond=lambda i: i < self._steps_per_loop,
            body=InfeedBody,
            loop_vars=[tf.constant(0)])

      # TODO(laigd): investigate how to run compilation only to catch errors
      # earlier.
      self._compile_op, batch_parallel_res = tpu.split_compile_and_shard(
          TpuTrainLoop,
          num_shards=self.data_parallelism,
          device_assignment=py_utils.GetTpuDeviceAssignment())
      outfeed = self._OutfeedDequeueLoop(self._task.per_example_tensors,
                                         self._steps_per_loop,
                                         self.data_parallelism)

      def _ConstructPostTrainingLoop(metric_values, outfeed):
        """Returns the op for tpu training with tail cpu computation."""
        # Adds a tail computation that is run after the tpu_training loop
        # step finishes. This allows us to run certain computation that
        # acts on the variable between tpu_train_loop iterations and
        # amortizing the cost of the operations. Alternative of running
        # tpu.outside_compilation & using tf.cond is expenseive.
        with tf.control_dependencies(metric_values):
          self._model.ConstructPostTrainingLoop(outfeed)
          with tf.control_dependencies([self._task.post_training_loop_op]):
            return [[tf.identity(o) for o in metric_values], outfeed]

      # Get metric result from a single replica; they are all same here
      # because TpuEvalMetrics.FinalizeMetrics runs a cross_replica_sum.
      metric_values = [t[0] for t in batch_parallel_res]
      return _ConstructPostTrainingLoop(metric_values, outfeed)

    if py_utils.IsEagerMode():
      self.tpu_outs = (
          tf.function(autograph=False)(TrainFunc).get_concrete_function())
    else:
      self.tpu_outs = TrainFunc()

    # Write model analysis.
    self._model_analysis, self._total_num_params = summary_utils.ModelAnalysis(
        self._model)
    tf.logging.info('Total params=%d', self._total_num_params)
    try:
      with tf.io.gfile.GFile(
          os.path.join(self._program_dir, 'model_analysis.txt'), 'w') as f:
        f.write(self._model_analysis)
    except tf.errors.NotFoundError as e:
      tf.logging.info('Failed to write model analysis %s', e)

  def Run(self, sess=None):
    # Prevent overtraining.
    if py_utils.IsEagerMode():
      task_global_step = self._task.global_step.numpy()
    else:
      task_global_step = sess.run(self._task.global_step)
    if self._ShouldStop(task_global_step):
      return True

    if self._ml_perf:
      mlp_log.mlperf_print(
          'block_start',
          None,
          metadata={
              'epoch_count': 1,
              'first_epoch_num': 1
          })

    if py_utils.IsEagerMode():
      values, outfeeds = self.tpu_outs()
      values = py_utils.Transform(lambda x: x.numpy(), values)
      outfeeds = py_utils.Transform(lambda x: x.numpy(), outfeeds)
    else:
      infeed_future = self._infeed_pool.apply_async(
          self._InfeedLoop, args=(sess,))
      values, outfeeds = sess.run(self.tpu_outs)
      infeed_future.wait()

    self._eval_metrics.PackMetricsValues(values)
    eval_metrics = self._eval_metrics.metrics

    if py_utils.IsEagerMode():
      global_step = self._model.global_step.numpy()
    else:
      global_step = sess.run(self._model.global_step)
    step_rate, example_rate, total_examples = (
        self._step_rate_tracker.ComputeStepRate(
            global_step,
            eval_metrics['num_samples_in_batch'][0] * self._steps_per_loop))
    self._SummarizeValue(global_step, 'global_step/sec', step_rate)
    self._SummarizeValue(global_step, 'examples/sec', example_rate)
    self._SummarizeValue(global_step, 'total_samples', total_examples)
    self._SummarizeValue(global_step, 'total_num_params',
                         self._total_num_params)
    status_strs = []
    for key, (val, _) in sorted(eval_metrics.items()):
      self._SummarizeValue(global_step, key, val)
      tf.logging.info((global_step, key, val))
      status_strs.append('%s=%s' % (key, val))
    self.SetStatusMessage('Executing train program at step %d %s' %
                          (global_step, ','.join(status_strs)))

    if py_utils.IsEagerMode():
      task_global_step = self._task.global_step.numpy()
      # TODO(laigd): ProcessFPropResults doesn't work yet.
    else:
      task_global_step = sess.run(self._task.global_step)
      summaries = self._task.ProcessFPropResults(sess, task_global_step,
                                                 eval_metrics, outfeeds)
      self._WriteSummaries(
          os.path.basename(self._program_dir), global_step, summaries)

    if self._ml_perf:
      mlp_log.mlperf_print(
          'block_stop', None, metadata={
              'epoch_num': 1,
              'first_epoch_num': 1
          })

    vizier_early_stop = self._ReportVizierMetrics(
        global_step, self._eval_metrics.ToAverageMetrics())
    return self._ShouldStop(task_global_step) or vizier_early_stop

  def _ShouldStop(self, task_global_step):
    """Simpler version of _ShouldStop without early stopping."""
    if task_global_step >= self._task_params.train.max_steps:
      tf.logging.info('ShouldStop: step:%6d params.train.max_steps:%6d',
                      task_global_step, self._task_params.train.max_steps)
      return True

    return False


class EvalProgram(BaseProgram):
  """Evaluation program."""

  def __init__(self, params, shared_model=None, **kwargs):
    super().__init__(params, shared_model=shared_model, **kwargs)
    self._program_name = 'EvalProgram'
    p = self.params
    if (p.ml_perf is not None and p.ml_perf.benchmark_name is not None and
        p.ml_perf.steps_per_epoch is not None):
      self._ml_perf = p.ml_perf
      self._run_stop = None
    else:
      self._ml_perf = None

  def TpuEvalStep(self, *args):
    """Eval a shard of a batch on a single TPU core.

    Args:
      *args: metrics values from previous steps.

    Returns:
      Summed eval metrics.
    """
    with tf.name_scope('tpu_eval'):
      self._model.ConstructFPropGraph()
      per_step_eval_metrics = self._eval_metrics.SetMetrics(
          self._task.eval_metrics, args)
      summed_metrics = []
      for x, y in zip(per_step_eval_metrics, args):
        summed_metrics.append(x + y)
      return summed_metrics

  def EvalFunc(self):
    """Eval function."""

    @tpu_function.on_device_training_loop
    def TpuEvalLoop():
      loop_result = tpu_training_loop.repeat(
          self._steps_per_loop,
          self.TpuEvalStep,
          inputs=self._eval_metrics.initial_values,
          name='eval_loop')
      # Final metrics are the avg across self._steps_per_loop steps.
      return self._eval_metrics.FinalizeMetrics(loop_result)

    if py_utils.IsEagerMode():
      if self._task.input.params.resettable:
        tf.logging.info('Resetting input_generator.')
        # Reset the iterator within `EvalFunc` to ensure it gets run everytime
        # the `tf.function` is executed in Eager mode.
        self._task.input.Reset()

      # Run the infeed loop in the same function that runs the training loop
      # so that infeed enqueue/dequeue ops are created by the same
      # InfeedQueue.
      def InfeedBody(i):
        self._task.input.CreateTpuEnqueueOps()
        # Auto control dependency may not support TPU infeed ops, so add the
        # dependency manually.
        with tf.control_dependencies(self._task.input.tpu_infeed_op):
          return i + 1

      tf.while_loop(
          cond=lambda i: i < self._steps_per_loop,
          body=InfeedBody,
          loop_vars=[tf.constant(0)])

    # TODO(laigd): investigate how to run compilation only to catch errors
    # earlier.
    self._compile_op, batch_parallel_res = tpu.split_compile_and_shard(
        TpuEvalLoop,
        num_shards=self.data_parallelism,
        device_assignment=py_utils.GetTpuDeviceAssignment())

    # Get metric result from a single replica; they are all same here
    # because TpuEvalMetrics.FinalizeMetrics runs a cross_replica_sum.
    return [t[0] for t in batch_parallel_res]

  def BuildTpuSubgraph(self):
    tf.logging.info(f'EvalProgram {self.params.dataset_name} BuildTpuSubGraph')
    p = self.params
    with cluster_factory.SetEval(True):
      self._eval_metrics = metrics.TpuEvalMetrics(max_metrics=p.max_metrics)
      with py_utils.OpportunisticVariableReuseScope(True):
        self._model = self._InstantiateTaskModel(self._task_params)
      self._task = self._model.GetTask()
      self._task.input.TpuSetup()

      if py_utils.IsEagerMode():
        self.tpu_outs = (
            tf.function(autograph=False)(self.EvalFunc).get_concrete_function())
      else:
        self.tpu_outs = self.EvalFunc()

  def Run(self, sess=None):
    if py_utils.IsEagerMode():
      global_step = self._model.global_step.numpy()
    else:
      global_step = sess.run(self._model.global_step)

    mlperf_epoch_num = None
    if self._ml_perf:
      mlperf_epoch_num = int(global_step / self._ml_perf.steps_per_epoch)
      mlp_log.mlperf_print(
          'eval_start', None, metadata={'epoch_num': mlperf_epoch_num})

    if self._task.input.params.resettable and not py_utils.IsEagerMode():
      tf.logging.info('Resetting input_generator.')
      self._task.input.Reset(sess)

    if py_utils.IsEagerMode():
      values = self.tpu_outs()
      values = py_utils.Transform(lambda x: x.numpy(), values)
    else:
      infeed_future = self._infeed_pool.apply_async(
          self._InfeedLoop, args=(sess,))
      values = sess.run(self.tpu_outs)
      infeed_future.wait()

    status_strs = []
    self._eval_metrics.PackMetricsValues(values)
    eval_metrics = self._eval_metrics.metrics
    for key, (val, _) in sorted(eval_metrics.items()):
      self._SummarizeValue(global_step, key, val)
      tf.logging.info((global_step, key, val))
      status_strs.append('%s=%s' % (key, val))

    mlperf_done = False
    if self._ml_perf:
      mlperf_metric = self._ml_perf.decoder_metric_name
      if (mlperf_metric
          in eval_metrics) and (self._ml_perf.decoder_metric_success_threshold
                                is not None):
        mlperf_metric_value = eval_metrics[mlperf_metric][0]
        mlp_log.mlperf_print(
            'eval_accuracy',
            mlperf_metric_value,
            metadata={'epoch_num': mlperf_epoch_num})

        mlp_log.mlperf_print(
            'eval_stop', None, metadata={'epoch_num': mlperf_epoch_num})
        # Successful ML Perf run if we exceed target accuracy
        if mlperf_metric_value > self._ml_perf.decoder_metric_success_threshold:
          tf.logging.info('ml_perf_final_threshold: %f exceeded',
                          self._ml_perf.decoder_metric_success_threshold)
          if not self._run_stop:
            self._run_stop = mlp_log.mlperf_print(
                'run_stop', None, metadata={'status': 'success'})
            mlperf_done = True

        # Failed ML Perf run if we fail to reach target accuracy after
        # predefined number of steps.
        elif global_step >= self._ml_perf.max_steps_to_train:
          if not self._run_stop:
            self._run_stop = mlp_log.mlperf_print(
                'run_stop', None, metadata={'status': 'abort'})
            mlperf_done = True

    self.SetStatusMessage(
        f'Executing eval program on dataset {self.params.dataset_name} '
        f"at step {global_step}\n{','.join(status_strs)}")

    self._summary_writer.flush()

    if self._ml_perf:
      return mlperf_done
    else:
      return self._ReportVizierMetrics(global_step,
                                       self._eval_metrics.ToAverageMetrics())


def _FetchDecodeOut(tpu_outs, sess=None):
  """Fetch decoder outputs, combining with CPU passthrough tensors if needed.

  Args:
    tpu_outs: A list of decoded tensors and list of cpu passthrough tensors in
      graph mode, or a callable returning such in eager mode.
    sess: A session to use in graph mode.

  Returns:
    A dict containing merged decoded outputs.
  """
  if py_utils.IsEagerMode():
    decode_out_dict, cpu_pt = tpu_outs()
    decode_out_dict = py_utils.Transform(lambda x: x.numpy(), decode_out_dict)
    if cpu_pt is None:
      cpu_pt = {}
    else:
      cpu_pt = py_utils.Transform(lambda x: x.numpy(), cpu_pt)
  else:
    decode_tensors, cpu_passthrough_tensors = tpu_outs
    if cpu_passthrough_tensors is not None:
      decode_out_dict, cpu_pt = sess.run(
          [decode_tensors, cpu_passthrough_tensors])
    else:
      decode_out_dict = sess.run(decode_tensors)
      cpu_pt = {}
  # Combine cpu_pt into decode_out_dict
  common_keys = decode_out_dict.keys() & cpu_pt.keys()
  if common_keys:
    raise ValueError('CPU passthrough keys already present in '
                     f'decode_out_dict keys: {common_keys}')
  decode_out_dict.update(cpu_pt)
  return decode_out_dict


class DecodeProgram(BaseProgram):
  """DecodeProgram."""

  @classmethod
  def Params(cls):
    p = super().Params()
    p.Define('decode_until_out_of_range', False,
             ('If set, ignores steps_per_loop and Decode proceeds until an '
              'OutOfRangeError is triggered by hitting the end of dataset.'))
    p.Define(
        'postprocess_all_at_once', False,
        'If set, decode_out_dict of all steps are accumulated into a list '
        'and passed to PostProcess to run only once at the end. Note that'
        ' the PostProcess of the Task should define logic for aggregating'
        'data from the list of decode_out_dict.')
    p.Define('emails', [],
             'The list of email addresses to send result summaries to.')
    return p

  def __init__(self, params, shared_model=None, **kwargs):
    super().__init__(params, shared_model=shared_model, **kwargs)
    self._program_name = 'DecodeProgram'
    self._decode_out_dict_lst = []

  def DecodeFunc(self):
    """Wrap the DecodeFn with split_compile_and_shard."""

    def _DecodeFn():
      """Decode call to be compiled for TPU."""
      with py_utils.TaskCallScope(self._task):
        input_batch = self._task.input.TpuDequeueBatch()
        decode_dict = self._task.Decode(input_batch)
      self.decode_nm = py_utils.NestedMap(decode_dict)
      return self.decode_nm.Flatten()

    if py_utils.IsEagerMode():
      # Run the infeed loop in the same function that runs the training loop
      # so that infeed enqueue/dequeue ops are created by the same
      # InfeedQueue.
      self._task.input.CreateTpuEnqueueOps()
      self._task.input.CreateCpuPassthroughEnqueueOps()

    self._compile_op, batch_parallel_res = tpu.split_compile_and_shard(
        _DecodeFn,
        num_shards=self.data_parallelism,
        device_assignment=py_utils.GetTpuDeviceAssignment())

    if self.decode_nm:
      decode_tensors = self.decode_nm.Pack(batch_parallel_res)
    else:
      decode_tensors = py_utils.NestedMap()
    cpu_pt = self._task.input.DequeueCpuPassthrough()
    return decode_tensors, cpu_pt

  def _DecodeUntilOutOfRangeInfeedLoop(self, sess=None, infeed_step_queue=None):
    """Infeed loop that stops when it runs out of data (OutOfRange error)."""
    tf.logging.info(f'_InfeedLoop start {self._program_name} '
                    f'on dataset {self.params.dataset_name}')

    def _HandleEndOfData():
      tf.logging.info(f'End of dataset {self.params.dataset_name}.')
      infeed_step_queue.put(-1)  # -1 signals reaching end of dataset.
      self._WriteInputDataStats(sess)
      tf.logging.info('_InfeedLoop done')
    try:
      loop_index = 0
      while True:
        tf.logging.vlog(1, '_InfeedLoop %d', loop_index)
        sess.run(self._task.input.tpu_infeed_op)
        infeed_step_queue.put(loop_index)
        loop_index += 1
    except tf.errors.OutOfRangeError:
      _HandleEndOfData()
    except tf.errors.InvalidArgumentError as e:
      if 'REPEAT_SENTINEL_' in e.message:
        # Sentinel in repeating dataset signaling end of one epoch.
        tf.logging.info('Detected end-of-data sentinel.')
        _HandleEndOfData()
      else:
        tf.logging.info('_InfeedLoop InvalidArgumentError %r', e)
        raise
    except Exception as e:
      tf.logging.info('_InfeedLoop exception %r', e)
      raise

  def BuildTpuSubgraph(self):
    tf.logging.info(
        f'DecodeProgram {self.params.dataset_name} BuildTpuSubGraph')
    with cluster_factory.SetEval(True):
      py_utils.ResetStepSeed()
      with py_utils.OpportunisticVariableReuseScope(True):
        self._model = self._InstantiateTaskModel(self._task_params)
      self._task = self._model.GetTask()
      # We likely still need to initialize them, otherwise there is no way to
      # know the tensor_spec of the iterators for capturing
      self._task.input.TpuSetup(cpu_passthrough=True)

      if py_utils.IsEagerMode():
        with py_utils.ExperimentalIteratorCapture():
          self.tpu_outs = (
              tf.function(autograph=False)(
                  self.DecodeFunc).get_concrete_function())
      else:
        self.tpu_outs = self.DecodeFunc()

  def _DecodeStep(self,
                  sess,
                  step,
                  dec_metrics,
                  global_step,
                  buffered_decode_out,
                  postprocess_futures,
                  threadpool=None):
    """Run one iteration of decode."""
    tf.logging.info(f'Decoding step {step}')
    fetch_start = time.time()
    decode_out_dict = _FetchDecodeOut(self.tpu_outs, sess)
    tf.logging.info(f'Finished TPU decoding on step {step}')
    dec_metrics['decode_secs'].Update(time.time() - fetch_start)
    if self.params.postprocess_all_at_once:
      # Accumulate decode_out_dicts and skip postprocess until the end.
      self._decode_out_dict_lst.append(decode_out_dict)
    else:
      self._RunPostProcess(threadpool, step, decode_out_dict, dec_metrics,
                           global_step, buffered_decode_out,
                           postprocess_futures)

  def _RunPostProcess(self, threadpool, step, decode_out_obj, dec_metrics,
                      global_step, buffered_decode_out, postprocess_futures):
    """Run postprocess in sync or async if a threadpool is provided."""
    if threadpool:
      # Run postprocess on separate CPU thread.
      postprocess_futures.append(
          threadpool.apply_async(
              self._PostProcessStep,
              args=(step, decode_out_obj, dec_metrics, global_step,
                    buffered_decode_out)))
    else:
      self._PostProcessStep(step, decode_out_obj, dec_metrics, global_step,
                            buffered_decode_out)

  def _PostProcessStep(self, idx, decode_out_obj, dec_metrics, global_step,
                       buffered_decode_out):
    """Run postprocess for a single decode step."""
    tf.logging.info(f'PostProcessStep {idx}')
    post_process_start = time.time()
    decode_out = self._task.PostProcessDecodeOut(decode_out_obj, dec_metrics)
    dec_metrics['postprocess_secs'].Update(time.time() - post_process_start)
    tf.logging.info('PostProcessed step: %d %f' %
                    (idx, dec_metrics['num_samples_in_batch'].total_value))
    if decode_out:
      if isinstance(decode_out, dict):
        decode_out = decode_out.items()

      if idx == 0:
        # Add summaries only for the first batch of data.
        for key, value in decode_out:
          if isinstance(value, tf.Summary):
            tf.logging.info(f'Adding summary {key} with tags '
                            f'{[x.tag for x in value.value]}.')
            self._summary_writer.add_summary(value, global_step)
        self._summary_writer.flush()

      buffered_decode_out.extend(
          kv for kv in decode_out if not isinstance(kv[1], tf.Summary))

  def _FinalizeDecode(self,
                      dec_metrics,
                      start_time,
                      global_step,
                      buffered_decode_out,
                      futures=None):
    """Finalize and summarize the results of this Decode program run."""
    if futures:
      # Wait for all async postprocessing jobs to finish.
      for future in futures:
        future.wait()
    num_examples_metric = dec_metrics['num_samples_in_batch']
    summaries = {k: v.Summary(k) for k, v in dec_metrics.items()}
    summaries['cumulative_num_examples'] = tf.Summary(value=[
        tf.Summary.Value(
            tag='cumulative_num_examples',
            simple_value=num_examples_metric.total_value)
    ])
    elapsed_secs = time.time() - start_time
    example_rate = num_examples_metric.total_value / elapsed_secs
    summaries['examples/sec'] = tf.Summary(
        value=[tf.Summary.Value(tag='examples/sec', simple_value=example_rate)])

    self._WriteSummaries(
        os.path.basename(self._program_dir), global_step, summaries)
    decode_out_path = os.path.join(self._program_dir,
                                   'decoder_out_%09d' % global_step)
    decode_finalize_args = base_model.DecodeFinalizeArgs(
        decode_out_path=decode_out_path, decode_out=buffered_decode_out)
    self._task.DecodeFinalize(decode_finalize_args)

    # Result is not returned as a signal for "done", unlike for training.
    self._ReportVizierMetrics(global_step, dec_metrics)

    # Provide train_executions_per_eval as a possible option for email.
    options = base_model.DecodeEmailOptions(
        job_name=os.path.basename(self._program_dir),
        train_executions_per_eval=self.train_executions_per_eval,
        global_step=global_step)
    if self.params.emails:
      try:
        self._task.EmailDecodeSummary(summaries, self.params.emails, options)
      except NotImplementedError:
        tf.logging.error('EmailDecodeSummary is not implemented yet.')
      except Exception as e:  # pylint: disable=broad-except
        tf.logging.error('Exception sending email %r', e)

  def Run(self, sess=None, threadpool=None):
    """Setup and execute Decode program."""
    if py_utils.IsEagerMode():
      global_step = self._model.global_step.numpy()
    else:
      global_step = sess.run(self._model.global_step)
    self.SetStatusMessage(
        f'Executing decode program on dataset {self.params.dataset_name} '
        f'at step {global_step}')

    if self._task.input.params.resettable:
      tf.logging.info('Resetting input_generator.')
      self._task.input.Reset(sess)

    # The infeed_step_queue synchronizes the _InfeedLoop with the Decoding loop
    # (that runs _DecodeStep). As an input batch is successfully fed through
    # the _InfeedLoop, a non-negative counter value is added to the queue.
    # _DecodeStep waits and only runs if it can successfully remove an item
    # from the queue (i.e. there is available data). If End of Dataset is
    # reached (OutOfRangeError), _InfeedLoop inserts a special value of "-1",
    # which will terminate the Decode loop once it's consumed from the queue.
    if self.params.decode_until_out_of_range:
      if py_utils.IsEagerMode():
        raise NotImplementedError(
            'p.decode_until_out_of_range is not supported in eager mode.')
      infeed_step_queue = queue.Queue()
      infeed_future = self._infeed_pool.apply_async(
          self._DecodeUntilOutOfRangeInfeedLoop,
          args=(
              sess,
              infeed_step_queue,
          ))
    else:
      if not py_utils.IsEagerMode():
        infeed_future = self._infeed_pool.apply_async(
            self._InfeedLoop, args=(sess,))

    dec_metrics = self._task.CreateDecoderMetrics()
    if not dec_metrics:
      tf.logging.info('Empty decoder metrics')
      return

    dec_metrics.update({
        'decode_secs': metrics.AverageMetric(),
        'postprocess_secs': metrics.AverageMetric(),
    })

    buffered_decode_out = []
    postprocess_futures = []

    start_time = time.time()
    if self.params.decode_until_out_of_range:
      while True:
        step = infeed_step_queue.get()  # Blocks until an item is returned.
        if step == -1:
          tf.logging.info('Reached end of dataset. Stop decoding.')
          break
        infeed_step_queue.task_done()
        self._DecodeStep(sess, step, dec_metrics, global_step,
                         buffered_decode_out, postprocess_futures, threadpool)
    else:
      for step in range(self._steps_per_loop):
        tf.logging.info('Starting step %d of %d', step, self._steps_per_loop)
        self._DecodeStep(sess, step, dec_metrics, global_step,
                         buffered_decode_out, postprocess_futures, threadpool)
    # Run postprocess after the last step if postprocess_all_at_once.
    if self.params.postprocess_all_at_once and self._decode_out_dict_lst:
      self._RunPostProcess(threadpool, step, self._decode_out_dict_lst,
                           dec_metrics, global_step, buffered_decode_out,
                           postprocess_futures)
    if not py_utils.IsEagerMode():
      infeed_future.wait()

    if threadpool:
      # Async. TPU+host processing is done and can move on to Train.
      threadpool.apply_async(
          self._FinalizeDecode,
          args=(
              dec_metrics,
              start_time,
              global_step,
              buffered_decode_out,
              postprocess_futures,
          ))
    else:
      self._FinalizeDecode(dec_metrics, start_time, global_step,
                           buffered_decode_out)


class ExperimentalDecodeProgram(DecodeProgram):
  """DecodeProgram in a tpu loop.

  Note that decoder outputs across cores are concatenated along the first
  dimension. The first dimension usually corresponds to batch size and as long
  as post process decode outputs have the same expectations, this will work.

  TODO(huangyp) test this for beam search decoders and replace the
  default DecodeProgram.
  """

  @classmethod
  def Params(cls):
    p = super().Params()
    p.num_threads = 2
    return p

  def DecodeFunc(self):
    """Wrap the DecodeLoop with split_compile_and_shard."""

    def _DecodeStep():
      """Decode call to be compiled for TPU."""
      with py_utils.TaskCallScope(self._task):
        input_batch = self._task.input.TpuDequeueBatch()
        decode_dict = self._task.Decode(input_batch)
      self.decode_nm = py_utils.NestedMap(decode_dict)
      return [self._OutfeedEnqueue(decode_dict)]

    @tpu_function.on_device_training_loop
    def DecodeLoopFn():
      return tpu_training_loop.repeat(
          self._steps_per_loop, _DecodeStep, inputs=[])

    self._compile_op, self.decode_loop = tpu.split_compile_and_shard(
        DecodeLoopFn,
        num_shards=self.data_parallelism,
        device_assignment=py_utils.GetTpuDeviceAssignment())

    # Pack the list of outfeed ops with structure in decode_nm.
    decode_tensors = self.decode_nm.Pack(self._OutfeedDequeue(self.decode_nm))
    cpu_pt = self._task.input.DequeueCpuPassthrough()
    return decode_tensors, cpu_pt

  def BuildTpuSubgraph(self):
    p = self.params
    tf.logging.info(
        f'ExperimentalDecodeProgram {p.dataset_name} BuildTpuSubgraph')
    if py_utils.IsEagerMode():
      raise NotImplementedError(
          'ExperimentalDecodeProgram is not supported in eager mode.')
    self.spmd = (p.spmd or self._task_params.input.use_partitioned_infeed_queue)
    with cluster_factory.SetEval(True):
      py_utils.ResetStepSeed()
      with py_utils.OpportunisticVariableReuseScope(True):
        self._model = self._InstantiateTaskModel(self._task_params)
      self._task = self._model.GetTask()
      self._task.input.TpuSetup(cpu_passthrough=True)

      self.tpu_outs = self.DecodeFunc()

  def _OutfeedDequeue(self, decode_nm):
    """Collect outfeed dequeue from all devices.

    Args:
      decode_nm: A NestedMap containing decoded tensors.

    Returns:
      A list of tensors corresponding to stacked decoded outputs. The decoder
      outputs are stacked on the first dimension (usually corresponds to
      batch size).
    """
    num_decode_tensors = len(decode_nm.Flatten())
    outfeed_ops = [[]] * num_decode_tensors
    device_assignment = py_utils.GetTpuDeviceAssignment()
    assert device_assignment
    num_cores_per_replica = (1 if self.spmd else
                             (device_assignment.num_cores_per_replica))
    for replica in range(device_assignment.num_replicas):
      for core in range(num_cores_per_replica):
        with tf.device(device_assignment.host_device(replica, core)):
          outfeeds_per_core = tpu_ops.outfeed_dequeue_tuple(
              dtypes=[x.dtype for x in decode_nm.Flatten()],
              shapes=[x.shape for x in decode_nm.Flatten()],
              device_ordinal=device_assignment.tpu_ordinal(replica, core))
          for idx_outfeed, out_feed in enumerate(outfeeds_per_core):
            outfeed_ops[idx_outfeed] = outfeed_ops[idx_outfeed] + [out_feed]
    return [tf.concat(per_outfeed, axis=0) for per_outfeed in outfeed_ops]

  def _DecodeLoop(self, sess=None):
    sess.run(self.decode_loop)

  def Run(self, sess=None, threadpool=None):
    global_step = sess.run(self._model.global_step)
    self.SetStatusMessage(
        f'Executing decode program on dataset {self.params.dataset_name} '
        f'at step {global_step}')

    if self._task.input.params.resettable:
      tf.logging.info('Resetting input_generator.')
      self._task.input.Reset(sess)

    infeed_future = self._infeed_pool.apply_async(
        self._InfeedLoop, args=(sess,))
    decode_future = self._infeed_pool.apply_async(
        self._DecodeLoop, args=(sess,))

    dec_metrics = self._task.CreateDecoderMetrics()
    start_time = time.time()
    for _ in range(self._steps_per_loop):
      decode_out_dict = _FetchDecodeOut(self.tpu_outs, sess)
      self._task.PostProcessDecodeOut(decode_out_dict, dec_metrics)
    decode_future.wait()
    infeed_future.wait()
    summaries = {k: v.Summary(k) for k, v in dec_metrics.items()}
    elapsed_secs = time.time() - start_time
    num_examples_metric = dec_metrics['num_samples_in_batch']
    example_rate = num_examples_metric.total_value / elapsed_secs
    summaries['examples/sec'] = tf.Summary(
        value=[tf.Summary.Value(tag='examples/sec', simple_value=example_rate)])
    self._WriteSummaries(
        os.path.basename(self._program_dir), global_step, summaries)

    return self._ReportVizierMetrics(global_step, dec_metrics)


class MLPerfTrainDecodeProgram(BaseProgram):
  """Run train/decode in a single session run."""

  @classmethod
  def Params(cls):
    """"Defaults parameters for Programs."""
    p = super().Params()
    p.Define('train_task', None, 'Underlying task')
    p.Define('decode_task', None, 'Underlying task')
    p.Define('train_dataset_name', None, '')
    p.Define('decode_dataset_name', None, '')
    p.Define('train_steps_per_loop', 0, '')
    p.Define('decode_steps_per_loop', 0, '')
    return p

  def __init__(self, params, shared_model=None, **kwargs):
    super().__init__(params, shared_model=shared_model, **kwargs)
    if py_utils.IsEagerMode():
      raise NotImplementedError(
          'MLPerfTrainDecodeProgram is not supported in eager mode.')
    p = self.params
    if p.ml_perf is not None and p.ml_perf.benchmark_name is not None:
      self._ml_perf_log = True
      self._ml_perf = p.ml_perf
      self._ml_perf_epoch = -1
    else:
      self._ml_perf_log = False
    self._program_name = 'TrainAndDecodeProgram'
    self._train_steps_per_loop = params.train_steps_per_loop
    self._decode_steps_per_loop = params.decode_steps_per_loop
    assert self._decode_steps_per_loop == 1, ('Only supports a single decode '
                                              'step right now.')
    self._train_task_params = params.train_task
    self._decode_task_params = params.decode_task
    self._run_start = None
    self._run_stop = None
    self._train_pool = multiprocessing.dummy.Pool(1)
    self._warmup_seconds = 60

  def _InitializeVizier(self):
    """We never use vizier with MLPerfPrograms."""
    self._should_report_metrics = False

  def BuildTpuSubgraph(self):
    p = self.params
    if self._ml_perf_log:
      mlp_log.mlperf_print('global_batch_size', self._ml_perf.global_batch_size)
      mlp_log.mlperf_print('max_sequence_length',
                           self._ml_perf.max_sequence_length)
      mlp_log.mlperf_print('opt_name', self._ml_perf.optimizer_name)
      mlp_log.mlperf_print('opt_base_learning_rate',
                           self._ml_perf.base_learning_rate)
      mlp_log.mlperf_print('opt_learning_rate_warmup_steps',
                           self._ml_perf.warmup_steps)

    self._eval_metrics = metrics.TpuEvalMetrics(max_metrics=p.max_metrics)
    with py_utils.OpportunisticVariableReuseScope(True):
      self._train_model = self._train_task_params.Instantiate()
    self._train_task = self._train_model.GetTask()
    self._train_task.input.TpuSetup()
    self._model = self._train_model

    def TpuTrainStep():
      """Train a shard of a batch on a single TPU core.

      Do not calculate loss metrics.

      Returns:
       [train_op].
      """
      with py_utils.OpportunisticVariableReuseScope(True):
        self._train_model.ConstructFPropBPropGraph()
      return [self._train_task.train_op]

    def TpuTrain():
      loop_result = tpu_training_loop.repeat(
          self._train_steps_per_loop,
          TpuTrainStep,
          inputs=[],
          name='train_loop')
      return loop_result

    py_utils.ResetStepSeed()

    with py_utils.OpportunisticVariableReuseScope(True):
      self._decode_model = self._InstantiateTaskModel(self._decode_task_params)
    self._decode_task = self._decode_model.GetTask()
    self._decode_task.input.TpuSetup(cpu_passthrough=True)

    def _DecodeFn():
      """Decode call to be compiled for TPU."""
      with cluster_factory.SetEval(True):
        input_batch = self._decode_task.input.TpuDequeueBatch()
        decode_dict = self._decode_task.Decode(input_batch)
      self.decode_nm = py_utils.NestedMap(decode_dict)
      return self.decode_nm.Flatten()

    @tpu_function.on_device_training_loop
    def TrainAndDecode():
      with tf.control_dependencies([TpuTrain()]):
        return _DecodeFn()

    self._compile_op, batch_parallel_res = tpu.split_compile_and_shard(
        TrainAndDecode,
        num_shards=self.data_parallelism,
        device_assignment=py_utils.GetTpuDeviceAssignment())

    decode_tensors = self.decode_nm.Pack(batch_parallel_res)
    cpu_pt = self._decode_task.input.DequeueCpuPassthrough()
    self.tpu_outs = (decode_tensors, cpu_pt)

  def _InfeedLoop(self, sess=None):
    if py_utils.IsEagerMode():
      # Eager mode infeed is run as part of the device loop.
      return
    tf.logging.info('_InfeedLoop start')
    try:
      for i in range(self._train_steps_per_loop):
        tf.logging.vlog(1, '_InfeedLoop %d', i)
        sess.run(self._train_task.input.tpu_infeed_op)
      if self._ml_perf_log:
        mlp_log.mlperf_print(
            'eval_start',
            None,
            metadata={
                'first_epoch_num': self._ml_perf_epoch + 1,
                'epoch_count': 1
            })
      for i in range(self._decode_steps_per_loop):
        tf.logging.vlog(1, '_InfeedLoop %d', i)
        sess.run(self._decode_task.input.tpu_infeed_op)
      tf.logging.info('_InfeedLoop done')
    except Exception as e:
      tf.logging.info('_InfeedLoop exception %r %s', e, e)
      raise

  def _TrainAndDecode(self, sess=None):
    decode_out_dict = _FetchDecodeOut(self.tpu_outs, sess)
    self._decode_task.PostProcessDecodeOut(decode_out_dict, self.dec_metrics)

  def Run(self, sess=None):
    global_step = sess.run(self._model.global_step)
    self.dec_metrics = self._decode_task.CreateDecoderMetrics()
    # Start TPU program thread.
    train_future = self._train_pool.apply_async(
        self._TrainAndDecode, args=(sess,))

    if self._warmup_seconds > 0:
      # The first execution of the TPU program has a warm-up
      # so we delay feeding data yet as that's when the MLPerf timing
      # starts. This way, when we actually infeed, the TPU program
      # is immediately ready to execute/dequeue data.
      tf.logging.info('Waiting before first infeed.')
      time.sleep(self._warmup_seconds)
      self._warmup_seconds = 0

    if self._ml_perf_log:
      if not self._run_start:
        mlp_log.mlperf_print(key='init_stop', value=None)
        self._run_start = mlp_log.mlperf_print(key='run_start', value=None)
      steps_per_epoch = self._ml_perf.steps_per_epoch
      epoch = int(global_step) // steps_per_epoch
      if epoch > self._ml_perf_epoch:
        self._ml_perf_epoch = epoch
        mlp_log.mlperf_print(
            'block_start',
            None,
            metadata={
                'first_epoch_num': epoch + 1,
                'epoch_count': 1
            })
      self.SetStatusMessage('MLPerf epoch: %d' % self._ml_perf_epoch)
    # Start infeed thread.
    infeed_future = self._infeed_pool.apply_async(
        self._InfeedLoop, args=(sess,))

    infeed_future.wait()
    train_future.wait()

    if self._ml_perf_log:
      mlp_log.mlperf_print(
          'eval_stop', None, metadata={'epoch_num': (epoch + 1)})
      mlperf_metric = self._ml_perf.decoder_metric_name
      mlperf_metric_value = float(self.dec_metrics[mlperf_metric].value)
      mlp_log.mlperf_print(
          'eval_accuracy', mlperf_metric_value, metadata={'epoch_num': epoch})

      # Successful ML Perf run if we exceed target accuracy
      if mlperf_metric_value > self._ml_perf.decoder_metric_success_threshold:
        tf.logging.info('ml_perf_final_threshold: %f exceeded',
                        self._ml_perf.decoder_metric_success_threshold)
        if not self._run_stop:
          self._run_stop = mlp_log.mlperf_print(
              'run_stop', None, metadata={'status': 'success'})
          self.SetStatusMessage('MLPerf run_time: %.2f' %
                                (self._run_stop - self._run_start))
          return True

      # Failed ML Perf run if we fail to reach target accuracy after
      # predefined number of steps.
      elif global_step >= self._ml_perf.max_steps_to_train:
        if not self._run_stop:
          self._run_stop = mlp_log.mlperf_print(
              'run_stop', None, metadata={'status': 'abort'})
          self.SetStatusMessage('MLPerf run_time: %.2f' %
                                (self._run_stop - self._run_start))
          return True

    return False


class MultiTaskProgramSchedule:
  """Container for ProgramSchedules for a MultiTask model."""

  @classmethod
  def Params(cls):
    p = hyperparams.InstantiableParams(cls)
    p.Define('program_schedule_dict', None,
             'task_name -> ProgramScheduleParams')
    return p


class SimpleProgramSchedule:
  """A schedule of programs associated with a single task.

  Simple sequence is:
  Run train_executions_per_eval * train_program
  Run all the eval_programs
  """

  @classmethod
  def Params(cls):
    """Params for a SimpleProgramSchedule."""
    p = hyperparams.InstantiableParams(cls)
    p.Define('task_dict', None, 'dataset_name -> task params')
    p.Define('task_name', None, 'High level task name')
    p.Define('logdir', None, 'Log directory')
    p.Define('train_program', None, 'Train program params')
    p.Define('train_executions_per_eval', 1, '')
    p.Define('eval_programs', [], 'List of eval program params.')
    p.Define('num_splits_per_client', None, '')
    p.Define('dataset_names', [], 'List of all dataset names.')
    p.Define('async_postprocess', True,
             'whether to CPU postprocess asynchronously with TPU train')

    # TODO(blee): Clean these up.
    p.Define('ml_perf', hyperparams.Params(), 'MlPerf configuration.')
    mlp = p.ml_perf
    mlp.Define('submission_metadata', None,
               'A dictionary of static submission metadata')
    mlp.Define('benchmark_name', None, 'Benchmark name for compliance log.')
    mlp.Define('steps_per_epoch', None, 'Number of training steps per epoch.')
    mlp.Define('decoder_metric_name', None,
               'Name of the decoder metric to report for compliance log.')
    mlp.Define('decoder_metric_success_threshold', None,
               'Benchmark run must exceed this value to succeed.')
    mlp.Define('max_steps_to_train', None,
               'Maximum number of steps to reach target accuracy')
    return p

  def __init__(self,
               params,
               shared_model=None,
               trial=base_trial.NoOpTrial(),
               **kwargs):
    self.params = params.Copy()
    p = self.params
    self._shared_model = shared_model
    self._programs = []
    self.train_program = None

    # Propagate run-time parameters to programs:
    if p.train_executions_per_eval > 0:
      p.train_program.logdir = p.logdir
      if p.train_program.dataset_name not in p.task_dict:
        raise ValueError('could not find train dataset %s in %s' %
                         (p.train_program.dataset_name, p.task_dict))
      p.train_program.task = p.task_dict[p.train_program.dataset_name]
      p.train_program.num_splits_per_client = p.num_splits_per_client
      p.train_program.task_name = p.task_name
      p.train_program.ml_perf = p.ml_perf.Copy()
      self.train_program = p.train_program.Instantiate(
          shared_model=shared_model, trial=trial, **kwargs)
      self._programs.append(self.train_program)
    elif py_utils.ExponentialMovingAverage():
      # When EMA is used, the train program must be added to self._programs
      # before any eval programs.
      raise ValueError('When EMA is used, there must be a train program to '
                       'apply the EMA before eval programs can use it.')

    for eval_program_params in p.eval_programs:
      eval_program_params.logdir = p.logdir
      if eval_program_params.dataset_name not in p.task_dict:
        raise ValueError('could not find eval dataset %s in %s' %
                         (eval_program_params.dataset_name, p.task_dict))
      eval_program_params.task = p.task_dict[eval_program_params.dataset_name]
      eval_program_params.task_name = p.task_name
      eval_program_params.num_splits_per_client = p.num_splits_per_client
      eval_program_params.ml_perf = p.ml_perf.Copy()

    self.eval_programs = []
    for eval_program in p.eval_programs:
      self.eval_programs.append(
          eval_program.Instantiate(
              shared_model=shared_model, trial=trial, **kwargs))
    self._programs += self.eval_programs

    if p.ml_perf is not None:
      self._ml_perf = p.ml_perf.Copy()
      if self._ml_perf.submission_metadata is not None:
        for key, value in self._ml_perf.submission_metadata.items():
          mlp_log.mlperf_print(key, value)
      mlp_log.mlperf_print('init_start', None)
      self._ml_perf_run_start = None
    else:
      self._ml_perf = None

  def Programs(self):
    return self._programs

  def Run(self, sess=None, threadpool=None):
    """Execute the program schedule."""
    if self._ml_perf:
      if not self._ml_perf_run_start:
        mlp_log.mlperf_print(key='init_stop', value=None)
        self._ml_perf_run_start = mlp_log.mlperf_print(
            key='run_start', value=None)
    p = self.params
    start_time = time.time()
    for _ in range(p.train_executions_per_eval):
      done = self.train_program.Run(sess)
      if done:
        break
    train_finish_time = time.time()
    train_time_in_secs = train_finish_time - start_time
    tf.logging.info('Train took %f seconds.', train_time_in_secs)

    # Return when no more evals are needed so we can have an exit
    # for ML Perf
    evals_done = False
    for eval_program in self.eval_programs:
      eval_program.train_executions_per_eval = p.train_executions_per_eval
      tf.logging.info(p.ml_perf)
      tf.logging.info(self._ml_perf)
      if self._ml_perf:
        one_eval_done = None
        if p.async_postprocess and isinstance(eval_program, DecodeProgram):
          # For now, Post-process is only in Decode, other Eval programs do not
          # take or use threadpool.
          one_eval_done = eval_program.Run(sess, threadpool)
        else:
          one_eval_done = eval_program.Run(sess)
        if one_eval_done is not None:
          evals_done |= one_eval_done
      else:
        if p.async_postprocess and isinstance(eval_program, DecodeProgram):
          eval_program.Run(sess, threadpool)
        else:
          eval_program.Run(sess)
    eval_time_in_secs = time.time() - train_finish_time
    tf.logging.info('Eval took %f seconds.', eval_time_in_secs)
    should_exit = (p.train_executions_per_eval == 0) or evals_done
    return should_exit, train_time_in_secs, eval_time_in_secs

  def Shutdown(self):
    if self.train_program:
      self.train_program.Shutdown()
    for eval_program in self.eval_programs:
      eval_program.Shutdown()


def _CreateProgramParams(cls, program_name, dataset_name, steps_per_loop):
  p = cls.Params()
  p.name = program_name
  p.dataset_name = dataset_name
  if program_name == 'decode_tpu':
    _SetDecodeStepsPerLoop(p, steps_per_loop)
  else:
    p.steps_per_loop = steps_per_loop
  return p


def SimpleProgramScheduleForTask(train_dataset_name,
                                 train_steps_per_loop,
                                 eval_dataset_names,
                                 eval_steps_per_loop,
                                 decode_steps_per_loop=None,
                                 experimental_decoder=False,
                                 train_program_cls=TrainProgram,
                                 eval_program_cls=EvalProgram,
                                 async_postprocess=True,
                                 decode_until_out_of_range=False,
                                 postprocess_all_at_once=False,
                                 emails=None):
  """Convenient helper method for common case.

  Args:
    train_dataset_name: Name of the training dataset, eg: 'Train'
    train_steps_per_loop: Number of steps to execute the training program.
    eval_dataset_names: List of eval dataset_name strings, eg: ['Train'].
    eval_steps_per_loop: Number of steps to execute the eval program. Can be a
      single value or a list of values corresponding to the entries in
      eval_dataset_names.
    decode_steps_per_loop: Number of steps to execute the decode program. Can be
      a single value or a list of values corresponding to the entries in
      eval_dataset_names. If it is None, then decode_until_out_of_range must be
      True.
    experimental_decoder: bool. Whether to use experimental deocder which is
      placed in a tpu loop.
    train_program_cls: The class to use for training programs.  Defaults to
      TrainProgram.
    eval_program_cls: The class to use for eval programs.  Defaults to
      EvalProgram.
    async_postprocess: bool. Whether to run CPU postprocessing for Decode in a
      separate thread to save time (i.e. concurrent with train). This avoids
      blocking training. But if the CPU postprocessing takes more time compared
      to Train, then multiple Train loops could complete before Decode finishes
      for an older global step. Then the latest Decode results do not correspond
      to the latest trained model.
    decode_until_out_of_range: bool. Whether to run Decode (and its Infeed loop)
      until there is no more data (OutOfRange error is thrown). If this is True,
      decode_steps_per_loop is ignored (and not required). Currently do not
      support ExperimentalDecodeProgram, which uses loop on TPU. So keep
      experimental_decoder=False
    postprocess_all_at_once: bool/List. Whether to postprocess the (combined)
      batches at once at the end of Decode program, instead of once per step.
      This is needed if one needs to reference/combine data across different
      batches/steps during postprocess. The PostProcess(DecodeOut) function
      should define the logic of aggregating across steps/batches. Can be a
      single value or a list of values corresponding to the entries in
      eval_dataset_names.
    emails: list. List of emails to email decode/scoring summaries.

  Returns:
    A populated SimpleProgramSchedule.Params()
  """

  program_schedule_params = SimpleProgramSchedule.Params()
  program_schedule_params.train_program = _CreateProgramParams(
      train_program_cls, 'train', train_dataset_name, train_steps_per_loop)

  program_schedule_params.dataset_names = []

  program_schedule_params.async_postprocess = async_postprocess

  if isinstance(eval_steps_per_loop, list):
    if len(eval_steps_per_loop) != len(eval_dataset_names):
      raise ValueError('eval_step_per_loop doesn\'t match the size of '
                       f'eval_dataset_names: {len(eval_steps_per_loop)} vs '
                       f'{len(eval_dataset_names)}.')
  else:
    eval_steps_per_loop = [eval_steps_per_loop] * len(eval_dataset_names)
  if isinstance(decode_steps_per_loop, list):
    if len(decode_steps_per_loop) != len(eval_dataset_names):
      raise ValueError('decode_steps_per_loop doesn\'t match the size of '
                       f'eval_dataset_names: {len(decode_steps_per_loop)} vs '
                       f'{len(eval_dataset_names)}.')
  elif decode_steps_per_loop is None:
    if not decode_until_out_of_range:
      raise ValueError('decode_until_out_of_range must be set to True if '
                       'decode_steps_per_loop is not specified (None).')
  else:
    decode_steps_per_loop = [decode_steps_per_loop] * len(eval_dataset_names)
  if isinstance(postprocess_all_at_once, list):
    if len(postprocess_all_at_once) != len(eval_dataset_names):
      raise ValueError('postprocess_all_at_once doesn\'t match the size of '
                       f'eval_dataset_names: {len(postprocess_all_at_once)} vs '
                       f'{len(eval_dataset_names)}.')
  else:
    postprocess_all_at_once = [postprocess_all_at_once
                              ] * len(eval_dataset_names)

  for idx, dataset_name in enumerate(eval_dataset_names):
    program_schedule_params.dataset_names.append(dataset_name)
    if eval_steps_per_loop[idx] > 0:
      program_schedule_params.eval_programs.append(
          _CreateProgramParams(eval_program_cls, 'eval_tpu', dataset_name,
                               eval_steps_per_loop[idx]))

    decoder_param = None
    if decode_until_out_of_range:
      if decode_steps_per_loop is not None:
        tf.logging.warning('decode_until_out_of_range set to True, ignoring '
                           'decode_steps_per_loop setting.')
      if experimental_decoder:
        raise ValueError(
            'experimental_decoder must be False for decode_until_out_of_range')
      decoder_param = _CreateProgramParams(DecodeProgram, 'decode_tpu',
                                           dataset_name, -1)
      decoder_param.postprocess_all_at_once = postprocess_all_at_once[idx]
    elif decode_steps_per_loop[idx] > 0:
      decoder = (
          ExperimentalDecodeProgram if experimental_decoder else DecodeProgram)
      decoder_param = _CreateProgramParams(decoder, 'decode_tpu', dataset_name,
                                           decode_steps_per_loop[idx])
      decoder_param.postprocess_all_at_once = postprocess_all_at_once[idx]
    if decoder_param is not None:
      if emails:
        decoder_param.emails = emails
      program_schedule_params.eval_programs.append(decoder_param)
  return program_schedule_params


def _GetDecodeStepsPerLoop(decode_program):
  if decode_program.decode_until_out_of_range:
    return -1
  else:
    return decode_program.steps_per_loop


def _SetDecodeStepsPerLoop(decode_program, steps_per_loop):
  if steps_per_loop == -1:
    decode_program.decode_until_out_of_range = True
  else:
    decode_program.decode_until_out_of_range = False
    decode_program.steps_per_loop = steps_per_loop


def _ClearSpecifiedProgram(program_list, program_cls_to_clear):
  ret_programs = []
  for program in program_list:
    if not issubclass(program.cls, program_cls_to_clear):
      ret_programs.append(program)
  return ret_programs


def UpdateProgramSchedule(ps_params,
                          dataset_list,
                          train_executions_per_eval,
                          eval_steps_per_loop,
                          decode_steps_per_loop,
                          decode_summary_emails=None):
  """Update ProgramSchedule params with the given new configs.

  Currently this override only support EvalProgram and DecodeProgram.

  Args:
    ps_params: SimpleProgramSchedule.Params(), to be overriden.
    dataset_list: Optional[List[str]], if not None, it will override eval
      datasets in ps_params.
    train_executions_per_eval: Optional[int], if not None, it will override
      train_executions_per_eval in ps_params.
    eval_steps_per_loop: Optional[int], if not None, it will override all the
      eval programs steps_per_loop. Currently list not supported.
    decode_steps_per_loop: Optional[int], if not None, it will override all the
      decode programs steps_per_loop. If set to -1, it will set
      decode_until_out_of_range=True. Currently list not supported.
    decode_summary_emails: List of emails to send Decode summary to.

  Returns:
    ps_params after overriden.
  """
  assert ps_params
  if dataset_list is not None:
    ps_params.dataset_names = dataset_list
    # Dict for all the override datasets:
    # - key: each dataset name
    # - value: dict with keys ('eval_exist', 'decode_exist') and bool values,
    #          indicate whether the dataset already exist in current
    #          EvalProgram, DecodeProgram. If not, we will create them.
    ds_dict = {}
    for dataset in dataset_list:
      ds_dict[dataset] = {'eval_exist': False, 'decode_exist': False}
    eval_programs = []
    default_eval_steps_per_loop = 0
    default_decode_steps_per_loop = 0
    for eval_program in ps_params.eval_programs:
      if issubclass(eval_program.cls, EvalProgram):
        default_eval_steps_per_loop = eval_program.steps_per_loop
      elif issubclass(eval_program.cls, DecodeProgram):
        default_decode_steps_per_loop = _GetDecodeStepsPerLoop(eval_program)
      if eval_program.dataset_name in ds_dict:
        eval_programs.append(eval_program)
        if issubclass(eval_program.cls, EvalProgram):
          ds_dict[eval_program.dataset_name]['eval_exist'] = True
        elif issubclass(eval_program.cls, DecodeProgram):
          ds_dict[eval_program.dataset_name]['decode_exist'] = True

    for dataset_name, exists in ds_dict.items():
      if not exists['eval_exist']:
        eval_programs.append(
            _CreateProgramParams(EvalProgram, 'eval_tpu', dataset_name,
                                 default_eval_steps_per_loop))
      if not exists['decode_exist']:
        eval_programs.append(
            _CreateProgramParams(DecodeProgram, 'decode_tpu', dataset_name,
                                 default_decode_steps_per_loop))
    ps_params.eval_programs = eval_programs

  if train_executions_per_eval is not None:
    ps_params.train_executions_per_eval = train_executions_per_eval

  if eval_steps_per_loop is not None:
    if eval_steps_per_loop == 0:
      ps_params.eval_programs = _ClearSpecifiedProgram(ps_params.eval_programs,
                                                       EvalProgram)
    else:
      for eval_program in ps_params.eval_programs:
        if issubclass(eval_program.cls, EvalProgram):
          eval_program.steps_per_loop = eval_steps_per_loop

  if decode_steps_per_loop is not None:
    if decode_steps_per_loop == 0:
      ps_params.eval_programs = _ClearSpecifiedProgram(ps_params.eval_programs,
                                                       DecodeProgram)
    else:
      for eval_program in ps_params.eval_programs:
        if issubclass(eval_program.cls, DecodeProgram):
          _SetDecodeStepsPerLoop(eval_program, decode_steps_per_loop)

  if decode_summary_emails:
    for eval_program in ps_params.eval_programs:
      if issubclass(eval_program.cls, DecodeProgram):
        eval_program.emails = decode_summary_emails

  return ps_params


class MLPerfProgramSchedule:
  """Program schedule for ML Perf benchmark."""

  @classmethod
  def Params(cls):
    """Params for a MLPerfProgramSchedule."""
    p = hyperparams.InstantiableParams(cls)

    p.Define('task_dict', None, 'dataset_name -> task params')
    p.Define('task_name', None, 'High level task name')
    p.Define('logdir', None, 'Log directory')
    p.Define('train_program', None, 'Train program params')
    p.Define('train_executions_per_eval', 1, '')
    p.Define('dataset_names', [], 'List of all dataset names.')
    p.Define('num_splits_per_client', None, '')

    p.Define('ml_perf', hyperparams.Params(), 'MlPerf configuration.')

    mlp = p.ml_perf
    mlp.Define('benchmark_name', None, 'Benchmark name for compliance log.')
    mlp.Define('decoder_metric_name', None,
               'Name of the decoder metric to report for compliance log.')
    mlp.Define('decoder_metric_success_threshold', None,
               'Benchmark run must exceed this value to succeed.')
    mlp.Define('max_steps_to_train', None,
               'Maximum number of steps to reach target accuracy')
    mlp.Define('steps_per_epoch', None, 'Number of training steps per epoch.')
    mlp.Define('global_batch_size', None, 'Global batch size.')
    mlp.Define('max_sequence_length', None, 'Maximum sequence length.')
    mlp.Define('optimizer_name', None, 'Optimizer used.')
    mlp.Define('base_learning_rate', None, 'Base learning rate.')
    mlp.Define('warmup_steps', None, 'Number of warm-up steps.')

    return p

  def __init__(self, params, shared_model=None, **kwargs):
    self.params = params.Copy()
    p = self.params
    self._shared_model = shared_model

    # Propagate run-time parameters to programs:
    p.train_program.logdir = p.logdir
    if p.train_program.train_dataset_name not in p.task_dict:
      tf.logging.error('could not find %s in %s' %
                       (p.train_program.train_dataset_name, p.task_dict))

    if p.train_program.decode_dataset_name not in p.task_dict:
      tf.logging.error('could not find %s in %s' %
                       (p.train_program.decode_dataset_name, p.task_dict))

    p.train_program.train_task = p.task_dict[p.train_program.train_dataset_name]
    p.train_program.decode_task = p.task_dict[
        p.train_program.decode_dataset_name]

    p.train_program.num_splits_per_client = p.num_splits_per_client
    p.train_program.task_name = p.task_name
    p.train_program.ml_perf = p.ml_perf.Copy()

    self.train_program = p.train_program.Instantiate(
        shared_model=shared_model, **kwargs)
    self._programs = []
    self._programs.append(self.train_program)

  def Programs(self):
    return self._programs

  def Run(self, sess=None, threadpool=None):
    """Execute the program schedule."""
    del threadpool  # Unused.
    p = self.params
    start_time = time.time()
    ret = False
    for _ in range(p.train_executions_per_eval):
      program_done = self.train_program.Run(sess)
      if program_done:
        ret = True
        break
    train_time_in_secs = time.time() - start_time
    eval_time_in_secs = 0
    return ret, train_time_in_secs, eval_time_in_secs

  def Shutdown(self):
    self.train_program.Shutdown()


def MLPerfProgramScheduleForTask(train_dataset_name, train_steps_per_loop,
                                 decode_dataset_name, decode_steps_per_loop):
  """Populate MLPerfProgramSchedule params.

  Args:
    train_dataset_name: Name of the training dataset, eg: 'Train'.
    train_steps_per_loop: Number of steps to execute the training program.
    decode_dataset_name:  Eg: 'Test'.
    decode_steps_per_loop: Number of steps to execute the decode program.

  Returns:
    A populated MLPerfProgramSchedule.Params()
  """

  program_schedule_params = MLPerfProgramSchedule.Params()
  train_program_params = MLPerfTrainDecodeProgram.Params()
  train_program_params.name = 'train_and_decode'
  train_program_params.train_steps_per_loop = train_steps_per_loop
  train_program_params.decode_steps_per_loop = decode_steps_per_loop

  train_program_params.dataset_name = train_dataset_name
  train_program_params.train_dataset_name = train_dataset_name
  train_program_params.decode_dataset_name = decode_dataset_name

  program_schedule_params.train_program = train_program_params

  program_schedule_params.dataset_names = [
      train_dataset_name, decode_dataset_name
  ]

  return program_schedule_params
