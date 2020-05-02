from sklearn.metrics import jaccard_similarity_score
import argparse
import pandas

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
    parser.add_argument('--targets_path', type=str)
    parser.add_argument('--base_path', type=str)
    parser.add_argument('--plot_path', type=str)
    parser.add_argument('--evaluation_tag', type=str)
    parser.add_argument('--num_top_words', type=int)
    parser.add_argument('--document_size', type=str)
    parser.add_argument('--corpus_size', type=str)
    parser.add_argument('--corpus', type=str)
    args = parser.parse_args()

    # Read in the targets.
    targets = [line.strip() for line in open(args.targets_path, 'r') if line.strip()]

    plotting_data_dicts = []
    settings = ['fixed', 'shuffled', 'bootstrap']
    algorithms = ['lsa', 'word2vec', 'glove', 'ppmi']

    for algorithm in algorithms:
        for setting in settings:
            for target in targets:

                # Read in the query results.
                top_words_path = args.base_path + '/out/' + args.corpus + '/' + args.document_size + '/' + args.corpus_size \
                                 + '/results/' + algorithm + '/' + setting + '/top_words.' + target + '.txt'
                top_words_lists = [line.split()[:args.num_top_words]
                                   for line in open(top_words_path, 'r') if line[0] != '-' and line.strip()]

                for i in range(0, len(top_words_lists)):
                    for j in range(0, len(top_words_lists)):
                        if i != j:
                            jaccard_similarity = jaccard_similarity_score(top_words_lists[i], top_words_lists[j])
                            plotting_data_dicts.append({'JACCARD SIMILARITY': jaccard_similarity,
                                                        'SETTING': setting,
                                                        'ALGORITHM': ALGORITHM_NAME_DICT[algorithm]})

    # Create the plot.
    sns.set(style='whitegrid', palette=sns.cubehelix_palette(5, start=.5, rot=-.75))
    plotting_data_df = pandas.DataFrame(plotting_data_dicts)
    ax = sns.factorplot(x="ALGORITHM", y="JACCARD SIMILARITY", hue='SETTING', data=plotting_data_df,
                        kind='bar', legend=False)

    # Format the plot.
    plt.ylim(0,0.9)
    plt.tight_layout()
    plt.legend(loc='upper left')
    plt.subplots_adjust(top=0.9)
    ax.fig.suptitle('Variation in Top ' + str(args.num_top_words) + ' Words')

    # Save the plot.
    print 'Saving plot to ' + args.plot_path + '/jaccard_algorithm.' + args.evaluation_tag + '.pdf'
    plt.savefig(args.plot_path + '/jaccard_algorithm.' + args.evaluation_tag + '.pdf')
    plt.clf()


if __name__ == '__main__':
    main()




