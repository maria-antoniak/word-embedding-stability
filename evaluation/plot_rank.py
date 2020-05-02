import argparse
import pandas
from collections import defaultdict
import numpy as np

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns


# sentence vs whole document size
# big vs small corpus size
# comparison of algorithms
# --> could show just the bootstrap for some of these?


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--targets_path', type=str)
    parser.add_argument('--evaluation_path', type=str)
    parser.add_argument('--plot_path', type=str)
    parser.add_argument('--evaluation_tag', type=str)
    args = parser.parse_args()

    # Read in the targets.
    targets = [line.strip() for line in open(args.targets_path, 'r') if line.strip()]

    for target in targets:

        # Read in the query results.
        averages_path = args.evaluation_path + '/averages.' + target + '.txt'
        input_records = pandas.read_csv(averages_path, sep='\t').to_dict('records')

        # Add each of the top 10 words as a dictionary to the data list.
        plotting_data_dicts = []
        for i, record in enumerate(input_records[:10]):
            word = record['WORD']
            ranks = [int(rank) for rank in record['RANKS'].split()]
            for rank in ranks:
                plotting_data_dicts.append({'WORD': word,
                                            'RANK': rank})

        # DEBUGGING
        words = defaultdict(int)
        for plotting_data in plotting_data_dicts:
            words[plotting_data['WORD']] += 1
        for word, count in words.iteritems():
            print word, count

        # Create the plot.
        sns.set(style='whitegrid', font_scale=1.5, palette='Set2')
        plotting_data_df = pandas.DataFrame(plotting_data_dicts)
        ax = sns.boxplot(x="RANK", y="WORD", data=plotting_data_df, color="c", orient="h", showfliers=False)

        # Format the plot to make things pretty and readable.
        ax.set_title('Change in Rank: "' + target + '"')
        plt.tight_layout()

        # Save the plot.
        print 'Saving plot to ' + args.plot_path + '/rankings.' + target + '.' + args.evaluation_tag + '.pdf'
        plt.savefig(args.plot_path + '/rankings.' + target + '.' + args.evaluation_tag + '.pdf')
        plt.clf()



if __name__ == '__main__':
    main()




