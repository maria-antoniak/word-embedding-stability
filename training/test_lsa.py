from gensim.models import lsimodel
from collections import defaultdict
import argparse
from datetime import datetime
import gensim
import re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from operator import itemgetter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer


def lsa_gensim(documents):
    dimensions = 50
    documents = [line.split() for line in
                 open('/Users/mah343/Documents/data/childrens-book-corpus/data/cbt_test.txt', 'r')]

    dictionary = gensim.corpora.Dictionary(documents)
    dictionary.compactify()
    corpus = [dictionary.doc2bow(document) for document in documents]

    model = lsimodel.LsiModel(corpus=corpus,
                              num_topics=dimensions)
    # num_topics=args.dimensions)
    # model.save(args.model_path)
    print model.show_topics(num_topics=10)
    print '\n'

    vector1 = dictionary.doc2bow([u'cat'])
    vector2 = dictionary.doc2bow([u'dog'])
    # print model[test_doc]

    print cosine_similarity(vector1, vector2)


def remove_extra_spaces(text):
    return ' '.join(text.split())


def remove_non_alpha(text):
    return re.sub('[^A-Za-z\s]', ' ', text)


def process_text(text):
    text = text.lower()
    text = remove_non_alpha(text)
    text = remove_extra_spaces(text)
    return text


def lsa_sklearn(documents, dimensions):

    # Prepare TF-IDF and SVD pipeline.
    vectorizer = TfidfVectorizer(norm='l2', use_idf=True, min_df=0, sublinear_tf=True)
    svd = TruncatedSVD(n_components=dimensions)

    # Run SVD on the training data, then project the training data.
    tfidf_vectors = vectorizer.fit_transform(documents).transpose()
    truncated_vectors = svd.fit_transform(tfidf_vectors)

    # TFIDF seems to be removing some words...
    print 'tfidf vectors shape = ' + str(tfidf_vectors.shape)
    print 'truncated vectors shape = ' + str(truncated_vectors.shape)

    print vectorizer.get_feature_names()
    word_index_dict = {}
    index_word_dict = {}
    for i, feature_name in enumerate(vectorizer.get_feature_names()):
        word_index_dict[feature_name] = i
        index_word_dict[i] = feature_name


    query_word = 'cat'

    # scores = cosine_similarity(truncated_vectors,
    #                            truncated_vectors[word_index_dict[query_word]])
    #
    # word_scores_dict = {}
    # for i, score in enumerate(scores.flatten()):
    #     word = index_word_dict[i]
    #     # if word == 'cat':
    #     #     score = -np.Inf  # Down-weight the similarity of the target with itself.
    #     word_scores_dict[word] = score
    #
    # for word, score in sorted(word_scores_dict.items(), key=itemgetter(1), reverse=True)[:10]:
    #     print word, score

    word_scores_dict = defaultdict(list)
    target_vector = truncated_vectors[word_index_dict[query_word], :]
    scores = cosine_similarity(truncated_vectors, target_vector.T.reshape(1, -1))

    for i, score in enumerate(scores.flatten()):
        word = index_word_dict[i]
        if word == query_word:
            score = -np.Inf     # Down-weight the similarity of the target with itself.
        word_scores_dict[word].append(score)

    for word, score in sorted(word_scores_dict.items(), key=itemgetter(1), reverse=True)[:10]:
        print word, score


def main():

    start_time = datetime.now()

    # parser = argparse.ArgumentParser()
    # parser.add_argument('--processed_documents_path', type=str)
    # parser.add_argument('--word_frequency_threshold', type=int)
    # parser.add_argument('--model_path', type=str)
    # parser.add_argument('--dimensions', type=int)
    # parser.add_argument('--window_size', type=int)
    # args = parser.parse_args()
    #
    # documents = [line.split() for line in open(args.processed_documents_path, 'r')]

    dimensions = 50
    documents = [process_text(line) for line in
                 open('/Users/mah343/Documents/data/childrens-book-corpus/data/cbt_train.txt', 'r')]

    vocab = defaultdict(int)
    for document in documents:
        for word in document.split():
            vocab[word] = 1
    print 'original vocab size = ' + str(len(vocab))
    print 'original number of docs = ' + str(len(documents))

    lsa_sklearn(documents, dimensions)

    print '-- Run Time = ' + str(datetime.now() - start_time)


if __name__ == '__main__':
    main()
