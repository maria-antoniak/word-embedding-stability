from gensim.models import Word2Vec
from collections import defaultdict
import argparse
from datetime import datetime


def main():

    start_time = datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument('--processed_documents_path', type=str)
    parser.add_argument('--word_frequency_threshold', type=int)
    parser.add_argument('--model_path', type=str)
    parser.add_argument('--dimensions', type=int)
    parser.add_argument('--window_size', type=int)
    args = parser.parse_args()

    documents = [line.split() for line in open(args.processed_documents_path, 'r')]

    model = Word2Vec(documents,
                     size=args.dimensions,
                     window=args.window_size,
                     min_count=args.word_frequency_threshold)
    model.save(args.model_path)

    print '-- Run Time = ' + str(datetime.now() - start_time)


if __name__ == '__main__':
    main()
