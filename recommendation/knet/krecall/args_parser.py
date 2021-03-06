#! /usr/bin/env python
# -*- coding=utf8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from options import Options

import os
import json
import model_keys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--train_data_path', default='', type=str, help='')
parser.add_argument('--eval_data_path', default='', type=str, help='')
parser.add_argument('--lr', default=0.25, type=float, help='learning rate')
parser.add_argument(
    '--embedding_dim', default=100, type=int, help='embedding embedding_dim')
parser.add_argument('--train_ws', default=5, type=int, help='window size')
parser.add_argument(
    '--train_lower_ws', default=1, type=int, help='lower window size')
parser.add_argument('--min_count', default=50, type=int, help='')
parser.add_argument('--t', default=0.0001, type=float, help='')
parser.add_argument('--verbose', default=1, type=int, help='')
parser.add_argument('--min_count_label', default=1, type=int, help='')
parser.add_argument('--label', default="__label__", type=str, help='')
parser.add_argument('--batch_size', default=64, type=int, help='batch size')
parser.add_argument('--eval_batch_size', default=64, type=int, help='')
parser.add_argument('--num_sampled', default=5, type=int, help='')
parser.add_argument('--max_train_steps', default=None, type=int, help='')
parser.add_argument('--max_eval_steps', default=None, type=int, help='')
parser.add_argument('--max_eval_steps_in_train',
                    default=None, type=int, help='')
parser.add_argument('--epoch', default=1, type=int, help='')
parser.add_argument('--hidden_units', default="64,64", type=str, help='')
parser.add_argument('--model_dir', default="model_dir", type=str, help='')
parser.add_argument('--export_model_dir', default="export_model_dir",
                    type=str, help='')
parser.add_argument('--export_mode', default="recall", type=str, help='')
parser.add_argument('--rank_len', default=100, type=int, help='')
parser.add_argument('--prefetch_size', default=10000, type=int, help='')
parser.add_argument('--shuffle_size', default=10000, type=int, help='')
parser.add_argument('--save_summary_steps', default=100, type=int, help='')
parser.add_argument('--save_checkpoints_secs', default=600, type=int, help='')
parser.add_argument('--keep_checkpoint_max', default=3, type=int, help='')
parser.add_argument('--log_step_count_steps', default=100, type=int, help='')
parser.add_argument('--recall_k', default=1, type=int, help='')
parser.add_argument('--dict_dir', default="dict_dir", type=str, help='')
parser.add_argument('--use_saved_dict', default=0, type=int, help='')
parser.add_argument('--use_profile_hook', default=0, type=int, help='')
parser.add_argument('--profile_steps', default=100, type=int, help='')
parser.add_argument('--root_ops_path', default='', type=str, help='')
parser.add_argument('--remove_model_dir', default=1, type=int, help='')
parser.add_argument('--optimize_level', default=1, type=int, help='')
parser.add_argument('--receive_ws', default=5, type=int, help='')
parser.add_argument('--use_subset', default=0, type=int, help='')
parser.add_argument('--dropout', default=0.1, type=float, help='')
parser.add_argument('--ntargets', default=1, type=int, help='')
parser.add_argument('--chief_lock', default='chief.lock', type=str, help='')
parser.add_argument(
    '--max_distribute_train_steps', default=None, type=int, help='')
parser.add_argument('--train_nce_biases', default=0, type=int, help='')
parser.add_argument('--shuffle_batch', default=0, type=int, help='')
parser.add_argument('--predict_ws', default=5, type=int, help='')
parser.add_argument('--sample_dropout', default=0.5, type=float, help='')
parser.add_argument('--optimizer_type', default='ada', type=str, help='')
parser.add_argument('--tfrecord_file', default='', type=str, help='')
parser.add_argument('--num_tfrecord_file', default=1, type=int, help='')
parser.add_argument(
    '--train_data_format', default='fasttext', type=str, help='')
parser.add_argument(
    '--map_num_parallel_calls', default=1, type=int, help='')
parser.add_argument(
    '--train_parallel_mode', default='default', type=str, help='')
parser.add_argument('--train_num_parallel', default=1, type=int, help='')
parser.add_argument('--use_batch_normalization', default=0, type=int, help='')
parser.add_argument(
    '--sgd_lr_decay_type', default='exponential_decay', type=str, help='')
parser.add_argument('--use_clip_gradients', default=0, type=int, help='')
parser.add_argument('--clip_norm', default=5.0, type=float, help='')
parser.add_argument('--filter_with_rowkey_info', default=0, type=int, help='')
parser.add_argument(
    '--filter_with_rowkey_info_exposure_thr', default=0, type=int, help='')
parser.add_argument(
    '--filter_with_rowkey_info_play', default=0, type=int, help='')
parser.add_argument(
    '--filter_with_rowkey_info_e_play', default=0, type=int, help='')
parser.add_argument(
    '--filter_with_rowkey_info_e_play_ratio_thr',
    default=0.0, type=float, help='')
parser.add_argument('--rowkey_info_file', default='', type=str, help='')
parser.add_argument('--normalize_nce_weights', default=0, type=int, help='')
parser.add_argument('--normalize_embeddings', default=0, type=int, help='')
parser.add_argument('--nce_loss_type', default='default', type=str, help='')
parser.add_argument(
    '--negative_sampler_type', default='fixed', type=str, help='')
parser.add_argument('--use_user_features', default=0, type=int, help='')
parser.add_argument('--user_features_file', default='', type=str, help='')
parser.add_argument('--use_age_feature', default=0, type=int, help='')
parser.add_argument('--use_gender_feature', default=0, type=int, help='')
parser.add_argument('--age_feature_type', default='', type=str, help='')
parser.add_argument('--add_average_pooling', default=1, type=int, help='')
parser.add_argument('--add_max_pooling', default=0, type=int, help='')
parser.add_argument('--add_min_pooling', default=0, type=int, help='')
parser.add_argument('--add_hierarchical_pooling', default=0, type=int, help='')
parser.add_argument('--add_attention_layer', default=0, type=int, help='')
parser.add_argument('--hierarchical_average_window',
                    default=2, type=int, help='')
parser.add_argument('--attention_size', default=200, type=int, help='')
parser.add_argument('--log_step_count_secs', default=30, type=int, help='')
parser.add_argument('--evaluate_every_secs', default=30, type=int, help='')
parser.add_argument('--max_eval_steps_on_train_dataset',
                    default=1000, type=int, help='')
parser.add_argument('--optimizer_epsilon', default=1e-8, type=float, help='')
parser.add_argument('--optimizer_adadelta_rho',
                    default=0.95, type=float, help='')
parser.add_argument('--optimizer_adam_beta1',
                    default=0.9, type=float, help='')
parser.add_argument('--optimizer_adam_beta2',
                    default=0.999, type=float, help='')
parser.add_argument('--optimizer_rmsprop_decay',
                    default=0.9, type=float, help='')
parser.add_argument('--optimizer_rmsprop_momentum',
                    default=0.0, type=float, help='')
parser.add_argument('--optimizer_rmsprop_centered',
                    default=0, type=int, help='')
parser.add_argument('--optimizer_momentum_momentum',
                    default=0.9, type=float, help='')
parser.add_argument('--optimizer_momentum_use_nesterov',
                    default=0, type=int, help='')
parser.add_argument('--optimizer_exponential_decay_steps',
                    default=10000, type=int, help='')
parser.add_argument('--optimizer_exponential_decay_rate',
                    default=0.96, type=float, help='')
parser.add_argument('--optimizer_exponential_decay_staircase',
                    default=0, type=int, help='')
parser.add_argument('--optimizer_ftrl_lr_power',
                    default=-0.5, type=float, help='')
parser.add_argument('--optimizer_ftrl_initial_accumulator_value',
                    default=0.1, type=float, help='')
parser.add_argument('--optimizer_ftrl_l1_regularization',
                    default=0.0, type=float, help='')
parser.add_argument('--optimizer_ftrl_l2_regularization',
                    default=0.0, type=float, help='')
parser.add_argument('--optimizer_ftrl_l2_shrinkage_regularization',
                    default=0.0, type=float, help='')
parser.add_argument('--log_per_lines', default=20000, type=int, help='')
parser.add_argument('--cpp_log_level', default=1, type=int, help='')
parser.add_argument('--tf_log_level', default='INFO', type=str, help='')

opts = Options()


def parse_args(argv):
    args = parser.parse_args(argv[1:])
    opts.train_data_path = args.train_data_path
    opts.eval_data_path = args.eval_data_path
    opts.lr = args.lr
    opts.embedding_dim = args.embedding_dim
    opts.train_ws = args.train_ws
    opts.train_lower_ws = args.train_lower_ws
    opts.min_count = args.min_count
    opts.t = args.t
    opts.verbose = args.verbose
    opts.min_count_label = args.min_count_label
    opts.label = args.label
    opts.batch_size = args.batch_size
    opts.eval_batch_size = args.eval_batch_size
    opts.num_sampled = args.num_sampled
    opts.max_train_steps = args.max_train_steps
    if opts.max_train_steps is not None and opts.max_train_steps < 0:
        opts.max_train_steps = None
    opts.max_eval_steps = args.max_eval_steps
    if opts.max_eval_steps is not None and opts.max_eval_steps < 0:
        opts.max_eval_steps = None
    opts.max_eval_steps_in_train = args.max_eval_steps_in_train
    if (opts.max_eval_steps_in_train is not None
            and opts.max_eval_steps_in_train < 0):
        opts.max_eval_steps_in_train = None
    opts.epoch = args.epoch
    opts.hidden_units = map(int, filter(lambda x: x != '',
                                        args.hidden_units.split(',')))
    opts.model_dir = args.model_dir
    opts.export_model_dir = args.export_model_dir
    opts.export_mode = args.export_mode
    opts.rank_len = args.rank_len
    opts.prefetch_size = args.prefetch_size
    opts.shuffle_size = args.shuffle_size
    opts.save_summary_steps = args.save_summary_steps
    if opts.save_summary_steps < 0:
        opts.save_summary_steps = None
    opts.save_checkpoints_secs = args.save_checkpoints_secs
    opts.keep_checkpoint_max = args.keep_checkpoint_max
    opts.log_step_count_steps = args.log_step_count_steps
    opts.recall_k = args.recall_k
    opts.dict_dir = args.dict_dir
    opts.use_saved_dict = bool(args.use_saved_dict)
    opts.use_profile_hook = bool(args.use_profile_hook)
    opts.profile_steps = args.profile_steps
    opts.root_ops_path = args.root_ops_path
    opts.remove_model_dir = bool(args.remove_model_dir)
    opts.optimize_level = args.optimize_level
    opts.receive_ws = args.receive_ws
    opts.use_subset = bool(args.use_subset)
    opts.dropout = args.dropout
    opts.ntargets = args.ntargets
    opts.chief_lock = args.chief_lock
    opts.max_distribute_train_steps = args.max_distribute_train_steps
    if (opts.max_distribute_train_steps is not None
            and opts.max_distribute_train_steps < 0):
        opts.max_distribute_train_steps = None
    opts.train_nce_biases = bool(args.train_nce_biases)
    opts.shuffle_batch = bool(args.shuffle_batch)
    opts.predict_ws = args.predict_ws
    opts.sample_dropout = args.sample_dropout
    opts.optimizer_type = args.optimizer_type
    opts.tfrecord_file = args.tfrecord_file
    opts.num_tfrecord_file = args.num_tfrecord_file
    opts.train_data_format = args.train_data_format
    opts.map_num_parallel_calls = args.map_num_parallel_calls
    opts.train_parallel_mode = args.train_parallel_mode
    opts.train_num_parallel = args.train_num_parallel
    opts.use_batch_normalization = bool(args.use_batch_normalization)
    opts.sgd_lr_decay_type = args.sgd_lr_decay_type
    opts.use_clip_gradients = bool(args.use_clip_gradients)
    opts.clip_norm = args.clip_norm
    opts.filter_with_rowkey_info = bool(args.filter_with_rowkey_info)
    opts.filter_with_rowkey_info_exposure_thr = \
        args.filter_with_rowkey_info_exposure_thr
    opts.filter_with_rowkey_info_play = args.filter_with_rowkey_info_play
    opts.filter_with_rowkey_info_e_play = args.filter_with_rowkey_info_e_play
    opts.filter_with_rowkey_info_e_play_ratio_thr = \
        args.filter_with_rowkey_info_e_play_ratio_thr
    opts.rowkey_info_file = args.rowkey_info_file
    opts.normalize_nce_weights = bool(args.normalize_nce_weights)
    opts.normalize_embeddings = bool(args.normalize_embeddings)
    opts.nce_loss_type = args.nce_loss_type
    opts.negative_sampler_type = args.negative_sampler_type
    opts.use_user_features = bool(args.use_user_features)
    opts.user_features_file = args.user_features_file
    opts.use_age_feature = bool(args.use_age_feature)
    opts.use_gender_feature = bool(args.use_gender_feature)
    opts.age_feature_type = args.age_feature_type
    opts.add_average_pooling = bool(args.add_average_pooling)
    opts.add_max_pooling = bool(args.add_max_pooling)
    opts.add_min_pooling = bool(args.add_min_pooling)
    opts.add_hierarchical_pooling = bool(args.add_hierarchical_pooling)
    opts.add_attention_layer = bool(args.add_attention_layer)
    opts.hierarchical_average_window = args.hierarchical_average_window
    opts.attention_size = args.attention_size
    opts.log_step_count_secs = args.log_step_count_secs
    opts.evaluate_every_secs = args.evaluate_every_secs
    opts.max_eval_steps_on_train_dataset = args.max_eval_steps_on_train_dataset
    if (opts.max_eval_steps_on_train_dataset is not None
            and opts.max_eval_steps_on_train_dataset <= 0):
        opts.max_eval_steps_on_train_dataset = None
    opts.optimizer_epsilon = args.optimizer_epsilon
    opts.optimizer_adadelta_rho = args.optimizer_adadelta_rho
    opts.optimizer_adam_beta1 = args.optimizer_adam_beta1
    opts.optimizer_adam_beta2 = args.optimizer_adam_beta2
    opts.optimizer_rmsprop_decay = args.optimizer_rmsprop_decay
    opts.optimizer_rmsprop_momentum = args.optimizer_rmsprop_momentum
    opts.optimizer_rmsprop_centered = bool(args.optimizer_rmsprop_centered)
    opts.optimizer_momentum_momentum = args.optimizer_momentum_momentum
    opts.optimizer_momentum_use_nesterov = \
        bool(args.optimizer_momentum_use_nesterov)
    opts.optimizer_exponential_decay_steps = \
        args.optimizer_exponential_decay_steps
    opts.optimizer_exponential_decay_rate = \
        args.optimizer_exponential_decay_rate
    opts.optimizer_exponential_decay_staircase = \
        bool(args.optimizer_exponential_decay_staircase)
    opts.optimizer_ftrl_lr_power = args.optimizer_ftrl_lr_power
    opts.optimizer_ftrl_initial_accumulator_value = \
        args.optimizer_ftrl_initial_accumulator_value
    opts.optimizer_ftrl_l1_regularization = \
        args.optimizer_ftrl_l1_regularization
    opts.optimizer_ftrl_l2_regularization = \
        args.optimizer_ftrl_l2_regularization
    opts.optimizer_ftrl_l2_shrinkage_regularization = \
        args.optimizer_ftrl_l2_shrinkage_regularization
    opts.log_per_lines = args.log_per_lines
    opts.cpp_log_level = args.cpp_log_level
    tf_log_level = args.tf_log_level
    if tf_log_level == 'DEBUG':
        opts.tf_log_level = tf.logging.DEBUG
    elif tf_log_level == 'INFO':
        opts.tf_log_level = tf.logging.INFO
    elif tf_log_level == 'ERROR':
        opts.tf_log_level = tf.logging.ERROR
    elif tf_log_level == 'FATAL':
        opts.tf_log_level = tf.logging.FATAL
    else:
        raise ValueError("Invalid tf_log_level.")


def validate_opts():
    if opts.optimize_level not in model_keys.ALL_OPTIMIZE_LEVELS:
        raise ValueError(
            "optimaize_level {} not surpported.".format(opts.optimize_level))
    if opts.predict_ws > opts.receive_ws:
        raise ValueError(
            "predict_ws[{}] should not be larger than receive_ws[{}]".format(
                opts.predict_ws, opts.receive_ws))
    if len([u for u in opts.hidden_units if u <= 0]) > 0:
        raise ValueError("hidden_units contain unit <= 0")
    if opts.dropout < 0.0:
        raise ValueError("dropout should not less than 0")
    if opts.normalize_nce_weights and opts.train_nce_biases:
        raise ValueError(
            "option normalize_nce_weights and train_nce_biases conflicts.")

    if opts.use_user_features:
        if not opts.use_age_feature and not opts.use_gender_feature:
            raise ValueError("None user features can be used.")

    if (opts.tf_config is not None and
            opts.train_parallel_mode != model_keys.TrainParallelMode.DEFAULT):
        raise ValueError(
            "Distribute mode only surpport 'default' train parallel mode.")


def parse_tf_config():
    """Parse environment TF_CONFIG. config put in opts."""

    tf_config = os.environ.get('TF_CONFIG')
    if tf_config is not None:
        tf_config = json.loads(tf_config)

    opts.tf_config = tf_config
    opts.task_type = model_keys.TaskType.LOCAL  # default mode
    if opts.tf_config is not None:
        opts.task_type = opts.tf_config['task']['type']
        opts.task_index = opts.tf_config['task']['index']


def parse(argv):
    parse_args(argv)
    parse_tf_config()
    validate_opts()

    return opts
