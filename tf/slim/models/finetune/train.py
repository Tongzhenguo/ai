#! /usr/bin/env python
# -*- coding=utf8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import tensorflow as tf

import input_data
import hook
import build_model_fn


def build_estimator(opts):
    """Build estimator."""

    save_checkpoints_secs = None
    if opts.save_checkpoints_secs > 0:
        save_checkpoints_secs = opts.save_checkpoints_secs

    save_checkpoints_steps = None
    if opts.save_checkpoints_steps > 0:
        save_checkpoints_steps = opts.save_checkpoints_steps

    config_keys = {}
    config_keys['model_dir'] = opts.model_dir
    config_keys['tf_random_seed'] = None
    config_keys['save_summary_steps'] = opts.save_summary_steps
    config_keys['save_checkpoints_secs'] = save_checkpoints_secs
    config_keys['save_checkpoints_steps'] = save_checkpoints_steps
    config_keys['session_config'] = None
    config_keys['keep_checkpoint_max'] = opts.keep_checkpoint_max
    config_keys['keep_checkpoint_every_n_hours'] = 10000
    config_keys['log_step_count_steps'] = opts.log_step_count_steps

    num_samples_per_epoch = len(input_data.read_txt_file(
        opts.train_data_path, False))

    estimator_keys = {}
    estimator_keys['model_fn'] = build_model_fn.model_fn
    estimator_keys['params'] = {
        'opts': opts,
        'num_samples_per_epoch': num_samples_per_epoch
    }
    config = tf.estimator.RunConfig(**config_keys)
    estimator_keys['config'] = config

    estimator = tf.estimator.Estimator(**estimator_keys)
    return estimator


def create_hooks(opts):
    """Create profile hooks."""

    save_steps = opts.profile_steps
    meta_hook = hook.MetadataHook(save_steps=save_steps,
                                  output_dir=opts.model_dir)
    profile_hook = tf.train.ProfilerHook(save_steps=save_steps,
                                         output_dir=opts.model_dir,
                                         show_dataflow=True,
                                         show_memory=True)
    hooks = [meta_hook, profile_hook] if opts.use_profile_hook else None

    return hooks


def train_and_eval_in_local_mode(opts, estimator, hooks):
    """Train and eval model in lcoal mode."""

    build_train_input_fn = input_data.build_train_input_fn(
        opts, opts.train_data_path)
    build_eval_input_fn = input_data.build_eval_input_fn(
        opts, opts.eval_data_path)

    max_steps = None
    if opts.max_train_steps > 0:
        max_steps = opts.max_train_steps
    train_spec = tf.estimator.TrainSpec(
        input_fn=build_train_input_fn,
        max_steps=max_steps,
        hooks=hooks)
    eval_spec = tf.estimator.EvalSpec(
        input_fn=build_eval_input_fn,
        steps=None,
        name='eval',
        start_delay_secs=3,
        throttle_secs=opts.throttle_secs)
    result = tf.estimator.train_and_evaluate(
        estimator, train_spec, eval_spec)
    return result


def export_model_in_local_mode(opts, estimator):
    """Export model in local mode."""

    # export model
    tf.logging.info("Beginning export model ...")
    estimator.export_savedmodel(
        opts.export_model_dir,
        serving_input_receiver_fn=input_data.build_serving_input_fn(opts))
    tf.logging.info("Export model OK")


def train(opts, export=False):
    """Train model."""

    estimator = build_estimator(opts)
    hooks = create_hooks(opts)
    result = train_and_eval_in_local_mode(opts, estimator, hooks)
    if export:
        export_model_in_local_mode(opts, estimator)
    return result


def predict(opts):
    tf.logging.info("Begin predict ...")
    estimator = build_estimator(opts)
    build_predict_input_fn = input_data.build_predict_input_fn(
        opts, opts.predict_data_path)
    results = estimator.predict(
        input_fn=build_predict_input_fn,
        checkpoint_path=opts.predict_checkpoint_path,
        yield_single_examples=True)

    with open(opts.predict_output, 'w') as fout, \
            open(opts.predict_data_path, 'r') as fin:
        for result in results:
            src = fin.readline().strip()
            fout.write(src + ' ')
            fout.write(str(result['score'][1]) + '\n')
    tf.logging.info("Predict done")
