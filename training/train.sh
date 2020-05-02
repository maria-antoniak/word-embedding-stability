#!/usr/bin/env bash

#############################################################
# Command line arguments.                                   #
#############################################################
corpus=$1
corpus_size=$2
document_size=$3
model=$4
setting=$5
i=$6
word_frequency_threshold=$7
word_frequency_threshold=0  # reset to zero, so that bootstrap won't get messed up

#############################################################
# Relative paths on the cluster                             #
#############################################################
python_path=~/anaconda2/bin/python
glove_path=/home/maa343/downloads/GloVe/build
ppmi_path=/home/maa343/downloads/omerlevy-hyperwords-688addd64ca2
base_path=/home/maa343/projects/word-embedding-bootstrap

processed_documents_path=${base_path}/out/${corpus}/${document_size}/${corpus_size}/data/${setting}/${corpus}.${i}.txt
model_output_directory=${base_path}/out/${corpus}/${document_size}/${corpus_size}/models/${model}/${setting}

#############################################################
# settings for all models                                   #
#############################################################
embedding_size=100
window_size=5

#############################################################
# word2vec settings                                         #
#############################################################
word2vec_model_path=${model_output_directory}/model.${i}
word2vec_window_size=${window_size}
embedding_dimensions=${embedding_size}

#############################################################
# GloVe settings                                            #
#############################################################
glove_vocab_path=${model_output_directory}/vocab.${i}.txt
glove_cooccurrence_path=${model_output_directory}/cooccurrence.${i}.bin
glove_vectors_path=${model_output_directory}/vectors.${i}
glove_overflow_path=${model_output_directory}/overflow.${i}
glove_verbose=2
glove_memory=4.0
glove_vector_size=${embedding_size}
#glove_vector_size=50
glove_max_iter=15
glove_window_size=${window_size}
#glove_window_size=15
glove_binary=2
glove_num_threads=8
glove_x_max=10

#############################################################
# PPMI settings                                             #
#############################################################
ppmi_output_path=${model_output_directory}
ppmi_dimensions=${embedding_size}
ppmi_smoothing=0.75
ppmi_window_size=${window_size}
ppmi_subsampling_threshold=1e-5
#ppmi_subsampling_threshold=0
ppmi_eig=0.5
ppmi_neg=5

#############################################################
# LSA settings                                              #
#############################################################
lsa_vectors_path=${model_output_directory}/vectors.${i}.pickle
lsa_word_index_dict_path=${model_output_directory}/word_index_dict.${i}.pickle

#############################################################
# Start running.                                            #
#############################################################
echo "------------------------------------------------------"
echo "Corpus: ${corpus}"
echo "Corpus size: ${corpus_size}"
echo "Document size: ${document_size}"
echo "Model: ${model}"
echo "Setting: ${setting}"
echo "Documents path: ${processed_documents_path}"
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
# Train LSA.                                           #
#############################################################
if [ ${model} == lsa ]; then

    echo "Training lsa..."
    ${python_path} training/train_lsa.py --processed_documents_path ${processed_documents_path} \
                                         --vectors_path ${lsa_vectors_path} \
                                         --word_index_dict_path ${lsa_word_index_dict_path} \
                                         --dimensions ${embedding_dimensions}
fi

#############################################################
# Train word2vec.                                           #
#############################################################
if [ ${model} == word2vec ]; then

    echo "Training word2vec..."
    ${python_path} training/train_word2vec.py --processed_documents_path ${processed_documents_path} \
                                              --word_frequency_threshold ${word_frequency_threshold} \
                                              --model_path ${word2vec_model_path} \
                                              --dimensions ${embedding_dimensions} \
                                              --window_size ${word2vec_window_size}
fi

#############################################################
# Train gLoVe.                                              #
#############################################################
if [ ${model} == glove ]; then

    echo "Getting GloVe vocab..."
    ${glove_path}/vocab_count -min-count ${word_frequency_threshold} \
                              -verbose ${glove_verbose} \
                              < ${processed_documents_path} \
                              > ${glove_vocab_path}

    echo "Getting GloVe cooccurrence..."
    ${glove_path}/cooccur -memory ${glove_memory} \
                          -vocab-file ${glove_vocab_path} \
                          -verbose ${glove_verbose} \
                          -window-size ${glove_window_size} \
                          -overflow-file ${glove_overflow_path} \
                          < ${processed_documents_path} \
                          > ${glove_cooccurrence_path}

    #shuffle -memory $MEMORY -verbose $VERBOSE < $COOCCURRENCE_FILE > $COOCCURRENCE_SHUF_FILE

    echo "Training GloVe..."
    ${glove_path}/glove -save-file ${glove_vectors_path} \
                        -threads ${glove_num_threads} \
                        -input-file ${glove_cooccurrence_path} \
                        -x-max ${glove_x_max} \
                        -iter ${glove_max_iter} \
                        -vector-size ${glove_vector_size} \
                        -binary ${glove_binary} \
                        -vocab-file ${glove_vocab_path} \
                        -verbose ${glove_verbose}
fi

#############################################################
# Train PPMI.                                               #
#############################################################
if [ ${model} == ppmi ]; then

#    ${python_path} check_number_unique.py ${processed_documents_path}

    echo "Creating collection of word-context pairs..."
    ${python_path} ${ppmi_path}/hyperwords/corpus2pairs.py --thr ${word_frequency_threshold} \
                                                           --win ${ppmi_window_size} \
                                                           --sub ${ppmi_subsampling_threshold} \
                                                           ${processed_documents_path} \
                                                           > ${ppmi_output_path}/pairs.${i}.txt

    ${ppmi_path}/scripts/pairs2counts.sh ${ppmi_output_path}/pairs.${i}.txt \
                                         > ${ppmi_output_path}/counts.${i}.txt

    ${python_path} ${ppmi_path}/hyperwords/counts2vocab.py ${ppmi_output_path}/counts.${i}.txt

    echo "Calculating PMI matrices for each collection of pairs..."
    ${python_path} ${ppmi_path}/hyperwords/counts2pmi.py --cds ${ppmi_smoothing} \
                                                         ${ppmi_output_path}/counts.${i}.txt \
                                                         ${ppmi_output_path}/pmi.${i}.txt

    echo "Creating embeddings with SVD..."
    ${python_path} ${ppmi_path}/hyperwords/pmi2svd.py  --dim ${ppmi_dimensions} \
                                                       --neg ${ppmi_neg} ${ppmi_output_path}/pmi.${i}.txt \
                                                       ${ppmi_output_path}/svd.${i}.txt

    echo "Saving the embeddings in the textual format..."
    ${python_path} ${ppmi_path}/hyperwords/svd2text.py --eig ${ppmi_eig} \
                                                       ${ppmi_output_path}/svd.${i}.txt \
                                                       ${ppmi_output_path}/vectors.${i}.txt

    echo "Removing unnecessary files..."
    rm ${ppmi_output_path}/pairs.${i}.txt*
    rm ${ppmi_output_path}/counts.${i}.txt*
    rm ${ppmi_output_path}/pmi.${i}.txt*
    rm ${ppmi_output_path}/svd.${i}.txt*
fi

echo "Complete"
