#! /usr/bin/env bash

TF_CFLAGS=( $(python -c 'import tensorflow as tf; print(" ".join(tf.sysconfig.get_compile_flags()))') )
TF_LFLAGS=( $(python -c 'import tensorflow as tf; print(" ".join(tf.sysconfig.get_link_flags()))') )
echo "compile fasttext_example_generate_ops ..."
g++ -std=c++11 -shared \
    fasttext_example_generate_ops.cc \
    fasttext_example_generate_kernels.cc \
    dictionary.cc \
    -o fasttext_example_generate_ops.so \
    -fPIC ${TF_CFLAGS[@]} ${TF_LFLAGS[@]} \
    -O2 -D_GLIBCXX_USE_CXX11_ABI=0


echo "compile fasttext_dict_id_lookup_ops ..."
g++ -std=c++11 -shared \
    fasttext_dict_id_lookup_ops.cc \
    fasttext_dict_id_lookup_kernels.cc \
    -o fasttext_dict_id_lookup_ops.so \
    -fPIC ${TF_CFLAGS[@]} ${TF_LFLAGS[@]} \
    -O2 -D_GLIBCXX_USE_CXX11_ABI=0
