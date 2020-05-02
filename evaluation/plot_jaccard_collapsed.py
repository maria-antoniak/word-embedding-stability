from sklearn.metrics import jaccard_similarity_score
import argparse
import pandas

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--targets_path', type=str)
    parser.add_argument('--algorithm_path', type=str)
    parser.add_argument('--plot_path', type=str)
    parser.add_argument('--evaluation_tag', type=str)
    args = parser.parse_args()

    sns.set(style='whitegrid', palette='Set2')

    # Read in the targets.
    targets = [line.strip() for line in open(args.targets_path, 'r') if line.strip()]

    plotting_data_dicts = []
    num_top_words_settings = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    settings = ['fixed', 'shuffled', 'bootstrap']

    for setting in settings:
        for num_top_words in num_top_words_settings:
            for target in targets:

                # Read in the query results.
                top_words_path = args.algorithm_path + '/' + setting + '/top_words.' + target + '.txt'
                top_words_lists = [line.split()[:num_top_words] for line in open(top_words_path, 'r') if line[0] != '-' and line.strip()]

                for i in range(0, len(top_words_lists)):
                    for j in range(0, len(top_words_lists)):
                        if i != j:
                            jaccard_similarity = jaccard_similarity_score(top_words_lists[i], top_words_lists[j])
                            plotting_data_dicts.append({'JACCARD SIMILARITY': jaccard_similarity,
                                                        'N': num_top_words,
                                                        'SETTING': setting})

    # Create the plot.
    plotting_data_df = pandas.DataFrame(plotting_data_dicts)
    ax = sns.barplot(x="N", y="JACCARD SIMILARITY", hue='SETTING', data=plotting_data_df)

    # Format the plot.
    ax.set_title('Agreement in Top N Membership')
    plt.tight_layout()

    # Save the plot.
    print 'Saving plot to ' + args.plot_path + '/jaccard_collapsed.' + args.evaluation_tag + '.pdf'
    plt.savefig(args.plot_path + '/jaccard_collapsed.' + args.evaluation_tag + '.pdf')
    plt.clf()



if __name__ == '__main__':
    main()




