#!/usr/bin/env bash

#############################################################
# Command line arguments.                                   #
#############################################################
corpus=$1
corpus_size=$2
model=$3
setting=$4

#############################################################
# Relative paths on the cluster                             #
#############################################################
python_path=~/anaconda2/bin/python
base_path=/home/maa343/projects/word-embedding-bootstrap
targets_path=${base_path}/src/targets/targets.${corpus}.txt

#############################################################
# Start running.                                            #
#############################################################
echo "------------------------------------------------------"
echo "Corpus: ${corpus}"
echo "Corpus size: ${corpus_size}"
echo "Model: ${model}"
echo "------------------------------------------------------"

#############################################################
# Create the output directories.                            #
#############################################################
echo "Organizing output directories..."
${python_path} organize.py --base_path ${base_path} \
                           --corpus ${corpus} \
                           --corpus_size ${corpus_size} \


#############################################################
# Create a plot for each target word.                       #
#############################################################
echo "Plotting ${model}..."
${python_path} evaluation/plot_violins_document_size.py --targets_path ${targets_path} \
                                                        --base_path ${base_path} \
                                                        --model ${model} \
                                                        --corpus ${corpus} \
                                                        --setting ${setting}

echo "Complete"
