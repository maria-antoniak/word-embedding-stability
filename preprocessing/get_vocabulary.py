import argparse
from collections import defaultdict
from datetime import datetime
import pickle


def main():

    start_time = datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument('--processed_documents_path', type=str)
    parser.add_argument('--vocabulary_path', type=str)
    args = parser.parse_args()

    documents = [line.split() for line in open(args.processed_documents_path, 'r')]

    word_count_dict = defaultdict(int)
    for document in documents:
        for word in document:
            word_count_dict[word] += 1

    pickle.dump(word_count_dict, open(args.vocabulary_path, 'wb'))

    print '-- Run Time = ' + str(datetime.now() - start_time)


if __name__ == '__main__':
    main()
