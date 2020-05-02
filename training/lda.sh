#!/usr/bin/env bash

#############################################################
# Command line arguments.                                   #
#############################################################
corpus=$1
corpus_path=$2

#############################################################
# Relative paths on the cluster                             #
#############################################################
python_path=~/anaconda2/bin/python
base_path=/home/maa343/projects/word-embedding-bootstrap

processed_documents_path=${base_path}/out/${corpus}/whole/1.0/data/fixed/${corpus}.1.txt
lda_output_path=${base_path}/out/${corpus}/lda_topics.whole.1.0.txt

#############################################################
# Start running.                                            #
#############################################################
echo "------------------------------------------------------"
echo "Corpus: ${corpus}"
echo "Documents path: ${corpus_path}"
echo "------------------------------------------------------"

#############################################################
# Train LDA and save topics.                                #
#############################################################
echo "Training LDA and saving topics..."
${python_path} training/train_lda.py --data_path ${processed_documents_path} \
                                     --num_topics 200 \
                                     --output_path ${lda_output_path}

echo "Complete"
