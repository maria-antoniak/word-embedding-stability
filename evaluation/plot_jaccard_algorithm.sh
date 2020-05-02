#!/usr/bin/env bash

#############################################################
# Command line arguments.                                   #
#############################################################
corpus=$1
corpus_size=$2
document_size=$3
num_top_words=$4

#############################################################
# Relative paths on the cluster                             #
#############################################################
python_path=~/anaconda2/bin/python
base_path=/home/maa343/projects/word-embedding-bootstrap

targets_path=/home/maa343/projects/word-embedding-bootstrap/src/targets/targets.${corpus}.txt
plot_path=${base_path}/out/plots
evaluation_tag=${corpus}.${document_size}.${corpus_size}.${num_top_words}

#############################################################
# Start running.                                            #
#############################################################
echo "------------------------------------------------------"
echo "Corpus: ${corpus}"
echo "Corpus size: ${corpus_size}"
echo "Document size: ${document_size}"
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
echo "Plotting jaccard by algorithm..."
${python_path} evaluation/plot_jaccard_algorithm.py --targets_path ${targets_path} \
                                                    --plot_path ${plot_path} \
                                                    --base_path ${base_path} \
                                                    --evaluation_tag ${evaluation_tag} \
                                                    --document_size ${document_size} \
                                                    --corpus_size ${corpus_size} \
                                                    --num_top_words ${num_top_words} \
                                                    --corpus ${corpus}

echo "Complete"
