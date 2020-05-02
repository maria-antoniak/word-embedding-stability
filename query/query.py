from gensim.models import Word2Vec
import argparse
import os
from collections import defaultdict
from operator import itemgetter
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import pickle
import sys


def update_word_scores_dict(target, vocabulary, W, word_index_dict, word_scores_dict):

    target_vector = W[word_index_dict[target], :]
    scores = cosine_similarity(W, target_vector.T.reshape(1, -1))
    scores = scores.flatten()

    for word in vocabulary:

        if word in word_index_dict:
            index = word_index_dict[word]
            score = scores[index]
            if word == target:
                score = -np.Inf
            word_scores_dict[word].append(score)

        else:
            # If a word isn't present in this bootstrap iteration, then
            # assign a cosine similarity of zero.
            word_scores_dict[word].append(0)

    return word_scores_dict


def load_glove_model(vocab_path, vectors_path):

    words = [line.rstrip().split(' ')[0] for line in open(vocab_path, 'r')]

    word_vector_dict = {}
    for line in open(vectors_path, 'r'):
            values = line.rstrip().split(' ')
            word, vector = values[0], map(float, values[1:])
            word_vector_dict[word] = vector

    vocab_size = len(words)
    word_index_dict = {word: index for index, word in enumerate(words)}
    index_word_dict = {index: word for index, word in enumerate(words)}

    vector_dim = len(word_vector_dict[index_word_dict[0]])
    W = np.zeros((vocab_size, vector_dim))
    for word, vector in word_vector_dict.iteritems():
        if word == '<unk>':
            continue
        W[word_index_dict[word], :] = vector

    # Normalize each word vector to unit variance.
    d = np.sum(W ** 2, 1) ** 0.5
    W_norm = (W.T / d).T

    return W_norm, word_index_dict, index_word_dict


def get_scores_from_glove(target, vocabulary, models_directory_path, num_iterations):
    word_scores_dict = defaultdict(list)

    num_glove_models = 0

    for i in range(0, num_iterations):

        vocab_path = models_directory_path + '/vocab.' + str(i) + '.txt'
        vectors_path = models_directory_path + '/vectors.' + str(i) + '.txt'

        print 'Vectors path: ' + vectors_path

        if os.path.isfile(vocab_path) and os.path.isfile(vectors_path):

            num_glove_models += 1

            W, word_index_dict, index_word_dict = load_glove_model(vocab_path, vectors_path)

            word_scores_dict = update_word_scores_dict(target,
                                                       vocabulary,
                                                       W,
                                                       word_index_dict,
                                                       word_scores_dict)

    print 'Number of GloVe models: ' + str(num_glove_models)

    return word_scores_dict


def load_ppmi_model(vectors_path):

    word_vector_dict = {}
    vector_length = 0

    for line in open(vectors_path, 'r'):
        if line.strip():
            tokens = line.strip().split()
            word_vector_dict[tokens[0]] = np.asarray([float(x) for x in tokens[1:]])
            vector_length = len(word_vector_dict[tokens[0]])

    index_word_dict = {}
    word_index_dict = {}
    W = np.zeros(shape=(len(word_vector_dict), vector_length), dtype=np.float32)
    index = 0

    for word, vector in word_vector_dict.iteritems():
        word_index_dict[word] = index
        index_word_dict[index] = word
        W[index, :] = vector
        index += 1

    # Normalize each word vector to unit variance.
    d = np.sum(W ** 2, 1) ** 0.5
    W_norm = (W.T / d).T

    return W_norm, word_index_dict, index_word_dict


def get_scores_from_ppmi(target, vocabulary, models_directory_path, num_iterations):
    word_scores_dict = defaultdict(list)

    for i in range(0, num_iterations):
        vectors_path = models_directory_path + '/vectors.' + str(i) + '.txt'

        W, word_index_dict, index_word_dict = load_ppmi_model(vectors_path)

        word_scores_dict = update_word_scores_dict(target,
                                                   vocabulary,
                                                   W,
                                                   word_index_dict,
                                                   word_scores_dict)

    return word_scores_dict


def load_lsa_model(vectors_path, word_index_dict_path):
    word_index_dict = pickle.load(open(word_index_dict_path, 'rb'))
    vectors = pickle.load(open(vectors_path, 'rb'))
    return word_index_dict, vectors


def get_scores_from_lsa(target, vocabulary, models_directory_path, num_iterations):
    word_scores_dict = defaultdict(list)

    for i in range(0, num_iterations):
        vectors_path = models_directory_path + '/vectors.' + str(i) + '.pickle'
        word_index_dict_path = models_directory_path + '/word_index_dict.' + str(i) + '.pickle'

        word_index_dict, vectors = load_lsa_model(vectors_path, word_index_dict_path)

        word_scores_dict = update_word_scores_dict(target,
                                                   vocabulary,
                                                   vectors,
                                                   word_index_dict,
                                                   word_scores_dict)

    return word_scores_dict


def get_scores_from_word2vec(target, vocabulary, models_directory_path, num_iterations):

        word_scores_dict = defaultdict(list)

        for i in range(0, num_iterations):

            model_path = models_directory_path + '/model.' + str(i)
            model = Word2Vec.load(model_path)

            top_words = model.most_similar(positive=[target],
                                           negative=[],
                                           topn=len(model.vocab),
                                           restrict_vocab=None)

            # Add the score for the current model to its appropriate list in the dictionary.
            # The if-else checks for missing bootstrap words!
            word_score_dict = {word: score for word, score in top_words}
            for word in vocabulary:
                if word in word_score_dict:
                    word_scores_dict[word].append(word_score_dict[word])
                else:
                    word_scores_dict[word].append(0)

        return word_scores_dict


def get_word_ranks_dict(word_scores_dict, num_iterations):

    word_ranks_dict = defaultdict(list)

    # For each model, get the rank of every word.
    for i in range(0, num_iterations):

        # Get the words and scores for this iteration.
        word_score_dict = {}
        for word, scores in word_scores_dict.iteritems():
            word_score_dict[word] = scores[i]

        # Sort the words according to their cosine similarities.
        score_word_tuples = [(score, word) for word, score in word_score_dict.iteritems()]
        score_word_tuples.sort(reverse=True)

        # Transform the scores to ranks.
        for j, (score, word) in enumerate(score_word_tuples):
            rank = j + 1
            word_ranks_dict[word].append(rank)

    for word in word_ranks_dict:
        if len(word_ranks_dict[word]) != num_iterations:
            sys.stderr.write(word + '\n')
            sys.stderr.write('number of ranks != number of iterations\n')
            sys.stderr.write(str(len(word_ranks_dict[word])) + ' != ' + str(num_iterations) + '\n')
            sys.stderr.write('-----------------\n')
            exit(0)

    return word_ranks_dict


def main():

    start_time = datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument('--models_directory_path', type=str)
    parser.add_argument('--vocabulary_path', type=str)
    parser.add_argument('--targets_path', type=str)
    parser.add_argument('--num_iterations', type=int)
    parser.add_argument('--model', type=str)
    parser.add_argument('--query_results_path', type=str)
    args = parser.parse_args()

    np.seterr(invalid='ignore')

    vocabulary = pickle.load(open(args.vocabulary_path, 'rb'))
    targets = [line.strip() for line in open(args.targets_path, 'r') if line.strip()]

    for target in targets:

        # Get a map of words and their cosine similarities to the target word.
        if args.model == 'word2vec':
            word_scores_dict = get_scores_from_word2vec(target, vocabulary, args.models_directory_path, args.num_iterations)
        elif args.model == 'glove':
            word_scores_dict = get_scores_from_glove(target, vocabulary, args.models_directory_path, args.num_iterations)
        elif args.model == 'ppmi':
            word_scores_dict = get_scores_from_ppmi(target, vocabulary, args.models_directory_path, args.num_iterations)
        elif args.model == 'lsa':
            word_scores_dict = get_scores_from_lsa(target, vocabulary, args.models_directory_path, args.num_iterations)

        for word, scores in word_scores_dict.iteritems():
            if len(scores) != args.num_iterations:
                sys.stderr.write(word + '\n')
                sys.stderr.write('number of scores != number of iterations\n')
                sys.stderr.write(str(len(scores)) + ' != ' + str(args.num_iterations) + '\n')
                sys.stderr.write('-----------------\n')
                exit(0)

        # Get the mean and standard deviation for each word.
        word_mean_dict = {word: np.mean(np.array(scores))
                          for word, scores in word_scores_dict.iteritems()}
        word_variance_dict = {word: np.std(np.array(scores))
                              for word, scores in word_scores_dict.iteritems()}
        word_ranks_dict = get_word_ranks_dict(word_scores_dict, args.num_iterations)

        # Print the sorted scores to TSV file.
        output_path = args.query_results_path + '/averages' + '.' + str(args.num_iterations) + '.' + target + '.txt'
        output_file = open(output_path, 'w')
        output_file.write('TARGET\tWORD\tMEAN\tSTANDARD DEVIATION\tNUM SCORES\tSCORES\tRANKS\n')

        for word, mean in sorted(word_mean_dict.items(),
                                 key=itemgetter(1),
                                 reverse=True):
            output_file.write(target + '\t'
                              + word + '\t'
                              + str(mean) + '\t'
                              + str(word_variance_dict[word]) + '\t'
                              + str(len(word_scores_dict[word])) + '\t'
                              + ' '.join([str(score) for score in word_scores_dict[word]]) + '\t'
                              + ' '.join([str(rank) for rank in word_ranks_dict[word]]) + '\n')
        output_file.write('\n')

    print '-- Run Time = ' + str(datetime.now() - start_time)

if __name__ == '__main__':
    main()
