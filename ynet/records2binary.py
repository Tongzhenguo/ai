#! /usr/bin/env python
# -*-coding:utf-8 -*-


import struct
import argparse
import random
import numpy as np


# Basic model parameters as external flags.
FLAGS = None


def records2binary(recordsfile, dictfile, watchedfile, predictsfile):
    D = dict()
    # load dict
    for index, line in enumerate(open(dictfile, "r")):
        D[line.strip()] = index

    watched_size = FLAGS.watched_size
    with open(watchedfile, "wb") as fwatched:
        with open(predictsfile, "wb") as fpredicts:
            for index, line in enumerate(open(recordsfile, "r")):
                tokens = line.strip().split(' ')
                records = tokens[1:]  # skip __label__

                # generate binary records
                max_start = len(records) - watched_size - 1
                assert max_start >= 0
                num_sampled = min(max_start + 1, FLAGS.max_per_user)
                sampled = random.sample(range(max_start + 1), num_sampled)
                for start in sampled:
                    for r in xrange(start, start + watched_size):
                        index = D[records[r]]
                        fwatched.write(struct.pack('<i', index))
                    predict_index = D[records[start + watched_size]]
                    fpredicts.write(struct.pack('<i', predict_index))


def binary2records(recordsfile, dictfile, watchedfile, predictsfile):
    D = dict()
    # load dict
    for index, line in enumerate(open(dictfile, "r")):
        D[index] = line.strip()

    watched_size = FLAGS.watched_size
    watched = np.fromfile(watchedfile, np.int32)
    predicts = np.fromfile(predictsfile, np.int32)

    assert (watched.shape[0] % watched_size == 0)
    nlines = watched.shape[0] / watched_size
    assert (nlines == predicts.shape[0])

    with open(recordsfile, 'w') as frecords:
        for x in xrange(nlines):
            for y in xrange(watched_size):
                offset = x * watched_size + y
                n = watched[offset]
                frecords.write(D[n])
                frecords.write(' ')
            offset = x
            n = predicts[offset]
            frecords.write(D[n])
            frecords.write('\n')


def main():
    if FLAGS.binary:
        binary2records(FLAGS.output_records,
                       FLAGS.input_dict_file,
                       FLAGS.input_watched,
                       FLAGS.input_predicts)
    else:
        records2binary(FLAGS.input_records,
                       FLAGS.input_dict_file,
                       FLAGS.output_watched,
                       FLAGS.output_predicts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_records',
        type=str,
        default='',
        help='records file generated by transform.py.'
    )

    parser.add_argument(
        '--output_records',
        type=str,
        default='',
        help='Output records file from binary form.'
    )

    parser.add_argument(
        '--output_watched',
        type=str,
        default='',
        help='Binary form of watched records.'
    )

    parser.add_argument(
        '--input_watched',
        type=str,
        default='',
        help='Binary form of watched records.'
    )

    parser.add_argument(
        '--output_predicts',
        type=str,
        default='output.fasttext.predicts',
        help='Binary form of predicts for watched records.'
    )
    parser.add_argument(
        '--input_predicts',
        type=str,
        default='',
        help='Binary form of predicts for watched records.'
    )

    parser.add_argument(
        '--input_dict_file',
        type=str,
        default='input.fasttext.dict',
        help='Input dict file for records, generated by vec2binary.py.'
    )

    parser.add_argument(
        '--binary',
        type=bool,
        default=False,
        help='True: Convert binary form to text form.'
    )

    parser.add_argument(
        '--watched_size',
        type=int,
        default=20,
        help='Watched size.'
    )

    parser.add_argument(
        '--max_per_user',
        type=int,
        default=5,
        help='Max number of watched windows selected per user.'
    )

    FLAGS, unparsed = parser.parse_known_args()
    main()