#!/usr/bin/env bash

#############################################################
# Command line arguments.                                   #
#############################################################
corpus=$1
corpus_size=$2
document_size=$3
model=$4
setting=$5

#############################################################
# Relative paths on the cluster                             #
#############################################################
python_path=~/anaconda2/bin/python
base_path=/home/maa343/projects/word-embedding-bootstrap

targets_path=/home/maa343/projects/word-embedding-bootstrap/src/targets/targets.${corpus}.txt
#plot_path=${base_path}/out/${corpus}/${document_size}/${corpus_size}/plots/${model}
plot_path=${base_path}/out/plots
results_path=${base_path}/out/${corpus}/${document_size}/${corpus_size}/results/${model}/${setting}
evaluation_tag=${corpus}.${document_size}.${corpus_size}.${model}.${setting}

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
${python_path} evaluation/plot_sd_iters.py --targets_path ${targets_path} \
                                           --plot_path ${plot_path} \
                                           --evaluation_path ${results_path} \
                                           --evaluation_tag ${evaluation_tag}

echo "Complete"
