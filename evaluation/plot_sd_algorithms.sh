#!/usr/bin/env bash

#############################################################
# Command line arguments.                                   #
#############################################################
corpus=$1

#############################################################
# Relative paths on the cluster                             #
#############################################################
python_path=~/anaconda2/bin/python
base_path=/home/maa343/projects/word-embedding-bootstrap

targets_path=${base_path}/src/targets/targets.${corpus}.txt
plot_path=${base_path}/out/plots


#############################################################
# Start running.                                            #
#############################################################
echo "------------------------------------------------------"
echo "Corpus: ${corpus}"
echo "------------------------------------------------------"

#############################################################
# Create the output directories.                            #
#############################################################
echo "Organizing output directories..."
#${python_path} organize.py --base_path ${base_path} \
#                           --corpus ${corpus} \
#                           --corpus_size ${corpus_size}

#############################################################
# Create a plot for each target word.                       #
#############################################################
echo "Plotting ${corpus}..."
${python_path} evaluation/plot_sd_algorithms.py --corpus ${corpus} \
                                                --plot_path ${plot_path} \
                                                --targets_path ${targets_path} \
                                                --base_path ${base_path}

echo "Complete"
