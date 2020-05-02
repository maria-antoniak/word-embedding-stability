#!/usr/bin/env bash

#############################################################
# Command line arguments.                                   #
#############################################################
corpus=$1
corpus_size=$2
document_size=$3
model=$4
setting=$5
num_iterations=$6

#############################################################
# Relative paths on the cluster                             #
#############################################################
python_path=~/anaconda2/bin/python
glove_path=/home/maa343/downloads/GloVe/build
base_path=/home/maa343/projects/word-embedding-bootstrap

targets_path=/home/maa343/projects/word-embedding-bootstrap/src/targets/targets.${corpus}.txt
models_directory_path=${base_path}/out/${corpus}/${document_size}/${corpus_size}/models/${model}/${setting}
query_results_path=${base_path}/out/${corpus}/${document_size}/${corpus_size}/results/${model}/${setting}/
vocabulary_path=${base_path}/out/${corpus}/${document_size}/${corpus_size}/data/fixed/${corpus}.vocab.txt

#############################################################
# Start running.                                            #
#############################################################
echo "------------------------------------------------------"
echo "Corpus: ${corpus}"
echo "Corpus size: ${corpus_size}"
echo "Document size: ${document_size}"
echo "Model: ${model}"
echo "Setting: ${setting}"
echo "------------------------------------------------------"

#############################################################
# Create the output directories.                            #
#############################################################
echo "Organizing output directories..."
${python_path} organize.py --base_path ${base_path} \
                           --corpus ${corpus} \
                           --corpus_size ${corpus_size}

#############################################################
# Get the cosine similarities for the target words.         #
#############################################################
echo "Evaluating ${model} for ${setting}..."
${python_path} query/query.py --models_directory_path ${models_directory_path} \
                              --vocabulary_path ${vocabulary_path} \
                              --targets_path ${targets_path} \
                              --num_iterations ${num_iterations} \
                              --model ${model} \
                              --query_results_path ${query_results_path}

echo "Complete"
