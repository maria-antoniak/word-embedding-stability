#!/usr/bin/env bash

#############################################################
# Command line arguments.                                   #
#############################################################
corpus=$1
corpus_path=$2
corpus_size=$3
document_size=$4
setting=$5
i=$6
word_frequency_threshold=$7

#############################################################
# Relative paths on the cluster                             #
#############################################################
python_path=~/anaconda2/bin/python
glove_path=/home/maa343/downloads/GloVe/build
base_path=/home/maa343/projects/word-embedding-bootstrap

processed_documents_path=${base_path}/out/${corpus}/${document_size}/${corpus_size}/data/${setting}/${corpus}.${i}.txt

#############################################################
# Start running.                                            #
#############################################################
echo "------------------------------------------------------"
echo "Corpus: ${corpus}"
echo "Corpus size: ${corpus_size}"
echo "Document size: ${document_size}"
echo "Setting: ${setting}"
echo "Iteration: ${i}"
echo "------------------------------------------------------"

#############################################################
# Create the output directories.                            #
#############################################################
echo "Organizing output directories..."
${python_path} organize.py --base_path ${base_path} \
                           --corpus ${corpus} \
                           --corpus_size ${corpus_size}

#############################################################
# Process the input corpus.                                 #
#############################################################
echo "Processing corpus ${corpus}..."
${python_path} preprocessing/process_corpus.py --documents_path ${corpus_path} \
                                               --processed_documents_path ${processed_documents_path} \
                                               --word_frequency_threshold ${word_frequency_threshold} \
                                               --setting ${setting} \
                                               --corpus ${corpus} \
                                               --corpus_size ${corpus_size} \
                                               --document_size ${document_size}

echo "Complete"
