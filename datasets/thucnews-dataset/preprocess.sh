#! /usr/bin/env bash

set -e

MYDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${MYDIR}

mkdir -p data
mkdir -p data/bert
mkdir -p data/fasttext

python concat.py ./thucnews data/thucnews.txt data/bert/label.txt
shuf data/thucnews.txt -o data/thucnews_shuf.txt

total_lines=$(wc -l data/thucnews_shuf.txt | awk '{print $1}')
train_lines=`echo "scale=2;${total_lines}*0.8"|bc|awk '{print int($1)}'`
test_lines=`echo "scale=2;${total_lines}*0.2"|bc|awk '{print int($1)}'`
head data/thucnews_shuf.txt -n ${train_lines} > data/bert/train.tsv
tail data/thucnews_shuf.txt -n ${test_lines} > data/bert/dev.tsv

python jieba_tokenize.py data/bert/train.tsv data/fasttext/train.tsv
python jieba_tokenize.py data/bert/dev.tsv data/fasttext/dev.tsv
