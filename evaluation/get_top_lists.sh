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
base_path=/home/maa343/projects/word-embedding-bootstrap

targets_path=${base_path}/src/targets/targets.${corpus}.txt
results_directory_path=${base_path}/out/${corpus}/${document_size}/${corpus_size}/results/${model}/${setting}
num_words_to_print=10


#############################################################
# Start running.                                            #
#############################################################
echo "------------------------------------------------------"
echo "Corpus: ${corpus}"
echo "Corpus size: ${corpus_size}"
echo "Document size: ${document_size}"
echo "Model: ${model}"
echo "------------------------------------------------------"

#############################################################
# Create the output directories.                            #
#############################################################
echo "Organizing output directories..."
${python_path} organize.py --base_path ${base_path} \
                           --corpus ${corpus} \
                           --corpus_size ${corpus_size}

#############################################################
# Create a plot for each target word.                       #
#############################################################
echo "Plotting ${model}..."
${python_path} evaluation/get_top_lists.py --targets_path ${targets_path} \
                                           --results_directory_path ${results_directory_path} \
                                           --num_words_to_print ${num_words_to_print} \
                                           --num_iterations ${num_iterations}

echo "Complete"
