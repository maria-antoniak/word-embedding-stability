import argparse
import pandas
from collections import defaultdict
import sys


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--targets_path', type=str)
    parser.add_argument('--results_directory_path', type=str)
    parser.add_argument('--num_words_to_print', type=int)
    parser.add_argument('--num_iterations', type=int)
    args = parser.parse_args()

    targets = [line.strip() for line in open(args.targets_path, 'r') if line.strip()]

    for target in targets:

        word_lists = [[None for j in range(0, args.num_words_to_print)] for i in range(0, args.num_iterations)]

        # Read the records for this target.
        averages_path = args.results_directory_path + '/averages.' + target + '.txt'
        records = pandas.read_csv(averages_path, sep='\t').to_dict('records')

        # Get the top words for this target.
        for record in records:

            word = record['WORD'].strip()

            try:
                ranks = [int(rank)-1 for rank in record['RANKS'].split()]
            except ValueError:
                sys.stderr.write('ERROR\n')
                sys.stderr.write(averages_path + '\n')
                sys.stderr.write(target + '\n')
                sys.stderr.write(word + '\n')
                sys.stderr.write(record['RANKS'])
                sys.stderr.write('\n-------------\n')
                exit(0)

            for iteration, rank in enumerate(ranks):
                if rank < args.num_words_to_print:
                    word_lists[iteration][rank] = word

        # Save the results to the output file for this target.
        output_file = open(args.results_directory_path + '/top_words.' + target + '.txt', 'w')

        for words in word_lists:
            for word in words:
                output_file.write(word + ' ')
            output_file.write('\n---------------------\n')


if __name__ == '__main__':
    main()
