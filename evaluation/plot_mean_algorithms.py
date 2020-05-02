import argparse
import pandas
from collections import defaultdict
import numpy as np

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

CORPUS_NAME_DICT = {'court_4': '4th Circuit',
                    'court_9': '9th Circuit',
                    'nyt_2000_music': 'NYT Music',
                    'nyt_2000_sports': 'NYT Sports',
                    'reddit_ask_science': 'Reddit Ask Science',
                    'reddit_ask_historians': 'Reddit Ask Historians'}

ALGORITHM_NAME_DICT = {'word2vec': 'SGNS',
                       'ppmi': 'PPMI',
                       'glove': 'GloVe',
                       'lsa': 'LSA'}


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus', type=str)
    parser.add_argument('--plot_path', type=str)
    parser.add_argument('--targets_path', type=str)
    parser.add_argument('--base_path', type=str)
    args = parser.parse_args()

    sns.set(style='whitegrid', palette='colorblind')

    # Read in the targets.
    targets = [line.strip() for line in open(args.targets_path, 'r') if line.strip()]

    settings = ['fixed', 'shuffled', 'bootstrap']
    algorithms = ['lsa', 'word2vec', 'glove', 'ppmi']

    plotting_data_dicts = []

    for algorithm in algorithms:
        for setting in settings:
            for target in targets:

                # Read in the query results.
                averages_path = args.base_path + '/out/' + args.corpus + '/whole/1.0/results/' + algorithm + '/' + setting \
                                + '/averages.' + target + '.txt'
                input_records = pandas.read_csv(averages_path, sep='\t').to_dict('records')

                # Add each of the top 20 words as a dictionary to the data list.
                for i, record in enumerate(input_records[:20]):
                    plotting_data_dicts.append({'ALGORITHM': ALGORITHM_NAME_DICT[algorithm],
                                                'SETTING': setting,
                                                'MEAN': record['MEAN']})

    # Create the plot.
    plotting_data_df = pandas.DataFrame(plotting_data_dicts)
    ax = sns.factorplot(x="ALGORITHM",
                        y="MEAN",
                        hue="SETTING",
                        data=plotting_data_df,
                        kind="bar",
                        legend=False)

    # Format the plot.
    # ax.set_title('Standard Deviation by Algorithm and Setting')
    plt.tight_layout()
    plt.legend(loc='upper left')
    plt.subplots_adjust(top=0.9)
    ax.fig.suptitle('Mean Cosine Similarities in the ' + CORPUS_NAME_DICT[args.corpus] + ' Corpus')

    # Save the plot.
    plot_path = args.plot_path + '/mean_algorithms.' + args.corpus + '.whole.1.0.top_20.pdf'
    print 'Saving plot to ' + plot_path
    plt.savefig(plot_path)
    plt.clf()


if __name__ == '__main__':
    main()




