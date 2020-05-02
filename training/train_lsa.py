import argparse
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import pickle


def get_vectors(documents, dimensions):

    # Prepare TF-IDF and SVD pipeline.
    vectorizer = TfidfVectorizer(norm='l2', use_idf=True, min_df=0, sublinear_tf=True)
    svd = TruncatedSVD(n_components=dimensions)

    # Run SVD on the training data, then project the training data.
    tfidf_vectors = vectorizer.fit_transform(documents).transpose()
    truncated_vectors = svd.fit_transform(tfidf_vectors)

    # Create the word index dictionary, in order to retrieve vectors.
    word_index_dict = {}
    for i, feature_name in enumerate(vectorizer.get_feature_names()):
        word_index_dict[feature_name] = i

    return word_index_dict, truncated_vectors


def main():

    start_time = datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument('--processed_documents_path', type=str)
    parser.add_argument('--vectors_path', type=str)
    parser.add_argument('--word_index_dict_path', type=str)
    parser.add_argument('--dimensions', type=int)
    args = parser.parse_args()

    documents = [line for line in open(args.processed_documents_path, 'r')]
    word_index_dict, vectors = get_vectors(documents, args.dimensions)

    pickle.dump(word_index_dict, open(args.word_index_dict_path, 'wb'))
    pickle.dump(vectors, open(args.vectors_path, 'wb'))

    print '-- Run Time = ' + str(datetime.now() - start_time)


if __name__ == '__main__':
    main()
