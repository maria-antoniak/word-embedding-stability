#!/usr/bin/env bash

#############################################################
# Command line arguments.                                   #
#############################################################
corpus=$1
corpus_size=$2
document_size=$3

#############################################################
# Relative paths on the cluster                             #
#############################################################
python_path=~/anaconda2/bin/python
base_path=/home/maa343/projects/word-embedding-bootstrap

processed_documents_path=${base_path}/out/${corpus}/${document_size}/${corpus_size}/data/fixed/${corpus}.1.txt
vocabulary_path=${base_path}/out/${corpus}/${document_size}/${corpus_size}/data/fixed/${corpus}.vocab.txt

${python_path} preprocessing/get_vocabulary.py --processed_documents_path ${processed_documents_path} \
                                               --vocabulary_path ${vocabulary_path}
