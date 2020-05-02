import argparse
import pandas
from collections import defaultdict
import numpy as np

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--targets_path', type=str)
    parser.add_argument('--evaluation_path', type=str)
    parser.add_argument('--plot_path', type=str)
    parser.add_argument('--evaluation_tag', type=str)
    args = parser.parse_args()

    sns.set(style='whitegrid', font_scale=1.5, palette='Set2')

    # Read in the targets.
    targets = [line.strip() for line in open(args.targets_path, 'r') if line.strip()]

    plotting_data_dicts = []
    for target in targets:

        # Read in the query results.
        averages_path = args.evaluation_path + '/averages.' + target + '.txt'
        input_records = pandas.read_csv(averages_path, sep='\t').to_dict('records')

        # Add each of the top 10 words as a dictionary to the data list.
        for i, record in enumerate(input_records[:10]):
            sd = record['STANDARD DEVIATION']
            average_rank = i + 1
            plotting_data_dicts.append({'AVERAGE RANK': average_rank,
                                        'STANDARD DEVIATION': sd})

    # Create the plot.
    plotting_data_df = pandas.DataFrame(plotting_data_dicts)
    ax = sns.boxplot(x="STANDARD DEVIATION", y="AVERAGE RANK",
                     data=plotting_data_df, color="c", orient="h", showfliers=False)

    # Format the plot.
    ax.set_title('Variation in Similarity by Rank')
    plt.tight_layout()

    # Save the plot.
    print 'Saving plot to ' + args.plot_path + '/rank_sd.' + args.evaluation_tag + '.pdf'
    plt.savefig(args.plot_path + '/rank_sd.' + args.evaluation_tag + '.pdf')
    plt.clf()



if __name__ == '__main__':
    main()




