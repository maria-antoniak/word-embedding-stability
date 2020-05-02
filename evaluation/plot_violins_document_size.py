import argparse
import pandas
from collections import defaultdict

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
    parser.add_argument('--base_path', type=str)
    parser.add_argument('--model', type=str)
    parser.add_argument('--corpus', type=str)
    parser.add_argument('--setting', type=str)
    args = parser.parse_args()

    # Read in the targets.
    document_sizes = ['sentence', 'whole']
    targets = [line.strip() for line in open(args.targets_path, 'r') if line.strip()]

    data_dicts = []

    for document_size in document_sizes:
        for target in targets:

            # Read in the query results.
            averages_path = args.base_path + '/out/' + args.corpus \
                            + '/' + document_size + '/1.0/results/' + args.model + '/' + args.setting + '/averages.' + target + '.txt'
            records = pandas.read_csv(averages_path, sep='\t').to_dict('records')

            # Add each of the top 10 words as a dictionary to the data list.
            for i, record in enumerate(records[:10]):
                data_dicts.append({'DOCUMENT SIZE': document_size,
                                   'RANK': i+1,
                                   'STANDARD DEVIATION': record['STANDARD DEVIATION']})

    # Violin chart.
    sns.set(style='whitegrid', font_scale=1.5, palette=sns.cubehelix_palette(5, start=.5, rot=-.75))
    data_df = pandas.DataFrame(data_dicts)
    ax = sns.violinplot(x='RANK', y='STANDARD DEVIATION', hue='DOCUMENT SIZE',
                        data=data_df, palette=sns.cubehelix_palette(5, start=.5, rot=-.75), split=True)

    # Format chart.
    ax.set_title('Document Size Comparison')
    plt.tight_layout()

    # Save chart.
    plt.savefig(args.base_path + '/out/plots/violin_plot.document_size_comparison.'
                + args.corpus + '.' + args.model + '.' + args.setting + '.pdf')
    plt.clf()

    # Bar chart
    # these need to be averaged for the bar plot to work... I think
    # data_df = pandas.DataFrame(data_dicts)
    # ax = sns.barplot(x="RANK", y="STANDARD DEVIATION", hue="DOCUMENT SIZE", data=data_df, palette='Set2')
    # ax.set_title('comparison of sentence and whole document sizes')
    # plt.savefig(args.base_path + '/out/plots/bar_plot.document_size_comparison.'
    #             + args.corpus + '.' + args.model + '.' + args.setting + '.png')
    # plt.clf()


if __name__ == '__main__':
    main()




