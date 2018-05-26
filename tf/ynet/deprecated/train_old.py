#! /usr/bin/env python
# -*-coding:utf-8 -*-

from ynet import YNet
from input_data_binary import load_video_embeddings_from_binary
import tensorflow as tf

def nce_loss(
        embeddings,
        biases,
        predicts,
        user_vectors,
        num_classes,
        name="nce_loss",
        partition_strategy="div"):
    """Computes and returns the noise-contrastive estimation training loss.

    Args:
        uv: A Tensor of shape [batch_size, dim]. The forward activations of
        the YNet.
        labels: A Tensor of type int64 and shape [batch_size].
        The target classes.
        embeddings: A Tensor of shape [num_classes, dim]
        biases: A Tensor of shape [num_classes]. The class biases.
        num_classes: An int. The number of target classes
        name:

    Return:
        loss: nce loss
    """
    losses = tf.nn.nce_loss(
        weights=embeddings,
        biases=biases,
        labels=predicts,
        inputs=user_vectors,
        num_sampled=FLAGS.num_sampled,
        num_classes=num_classes,
        name=name
    )
    return tf.reduce_mean(losses, name=name + '_mean')


def training(loss, lr):
    """Sets up the training Ops.
    Creates a summarizer to track the loss over time in TensorBoard.

    Creates an optimizer and applies the gradients to all trainable
    variables.

    The Op returned by this function is what must be passed to the
    `sess.run()` call to cause the model to train.

    Args:
        loss: Loss tensor, from nce_loss()
        lr: The learning rate to use for gradient descent.

    Returns:
        train_op: The Op for training.
    """
    # optimizer = tf.train.GradientDescentOptimizer(lr)
    optimizer = tf.train.AdamOptimizer(lr)
    # Create a variable to track the global step.
    global_step = tf.Variable(0, name='global_step', trainable=False)
    # Use the optimizer to apply the gradients that minimize the loss
    # (and also increment the global step counter) as a single training
    # step.
    train_op = optimizer.minimize(loss, global_step=global_step)
    return train_op


def run_training():
    """Train YNet for a number of epoches."""
    batch_size = FLAGS.batch_size
    keep_prob = FLAGS.keep_prob
    learning_rate = FLAGS.learning_rate
    epoches = FLAGS.epoches
    watched_size = FLAGS.watched_size

    with tf.Graph().as_default():
        # 加载训练好的词向量
        video_embeddings, num_videos, embedding_dim = \
            load_video_embeddings_from_binary(
                FLAGS.video_embeddings_file_binary)

        video_biases = tf.Variable(tf.zeros([num_videos]))

        # 用户浏览历史 placeholder
        watched_pl = tf.placeholder(tf.int32, shape=(batch_size, watched_size))
        # 待预测的视频 placeholder
        predicts_pl = tf.placeholder(tf.int32, shape=(batch_size, 1))

        inputs = generate_average_inputs(video_embeddings, watched_pl)

        # 构造 DNN 网络
        model = YNet(inputs, keep_prob, embedding_dim)
        user_vectors = model.user_vectors

        # 负采样算法
        loss = nce_loss(video_embeddings,
                        video_biases,
                        predicts_pl,
                        user_vectors,
                        num_videos)
        train_op = training(loss, learning_rate)
        init = tf.global_variables_initializer()

        data_sets = read_data_sets_from_binary(FLAGS.train_watched_file,
                                               FLAGS.train_predicts_file,
                                               FLAGS.validation_watched_file,
                                               FLAGS.validation_predicts_file,
                                               FLAGS.test_watched_file,
                                               FLAGS.test_predicts_file,
                                               FLAGS.watched_size)
        num_examples = data_sets.train.num_examples
        max_steps = ((num_examples + batch_size - 1) / batch_size) * epoches
        print("max steps: {}".format(max_steps))

        with tf.Session() as sess:
            sess.run(init)
            for step in xrange(max_steps):
                feed_dict = fill_feed_dict(data_sets.train,
                                           watched_pl,
                                           predicts_pl)
                # Run one step of the model.  The return values are the
                # activations from the `train_op` (which is discarded) and
                # the `loss` Op.  To inspect the values of your Ops or
                # variables, you may include them in the list passed to
                # sess.run() and the value tensors will be returned in the
                # tuple from the call.
                _, loss_value = sess.run([train_op, loss],
                                         feed_dict=feed_dict)
                if step % 100 == 0:
                    print("step {}, loss = {}".format(step, loss_value))


def generate_average_inputs(video_embeddings, watched_pl):
    """Generate average tensor of embedded video watches.

    Args:
        video_embeddings: A shape (num_videos, dim) Tensor. Video embeddings.
        watched_pl: A shape (batch, watched_size) Tensor.
        Placeholder of user watched histories

    Return:
        mean: Average tensor of embedded video watches
    """
    x = tf.gather(video_embeddings, watched_pl)
    mean = tf.reduce_mean(x, 1)
    return mean


def fill_feed_dict(data_set, watched_pl, predicts_pl):
    """Fills the feed_dict for training the given step.

    A feed_dict takes the form of:
    feed_dict = {
      <placeholder>: <tensor of values to be passed for placeholder>,
      ....
    }

    Args:
        data_set:
        watched_pl:
        predicts_pl:

    Returns:
        feed_dict: The feed dictionary mapping from placeholders to values.
    """
    watched_feed, predicts_feed = data_set.next_batch(FLAGS.batch_size)
    feed_dict = {
        watched_pl: watched_feed,
        predicts_pl: predicts_feed,
    }
    return feed_dict