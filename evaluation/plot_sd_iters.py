import argparse
import pandas

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns


# ITERATION_SETTINGS = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
ITERATION_SETTINGS = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--targets_path', type=str)
    parser.add_argument('--evaluation_path', type=str)
    parser.add_argument('--plot_path', type=str)
    parser.add_argument('--evaluation_tag', type=str)
    args = parser.parse_args()

    # Read in the targets.
    targets = [line.strip() for line in open(args.targets_path, 'r') if line.strip()]

    plotting_data_dicts = []
    for num_iterations in ITERATION_SETTINGS:
        for target in targets:

            # Read in the query results.
            averages_path = args.evaluation_path + '/averages' + '.' + str(num_iterations) + '.' + target + '.txt'
            input_records = pandas.read_csv(averages_path, sep='\t').to_dict('records')

            # Add each of the top 20 words as a dictionary to the data list.
            for i, record in enumerate(input_records[:20]):
                plotting_data_dicts.append({'NUMBER OF ITERATIONS': num_iterations,
                                            'STANDARD DEVIATION': record['STANDARD DEVIATION']})

    # Create the plot.
    sns.set(style='whitegrid', font_scale=1.5, palette='Blues_d')
    plotting_data_df = pandas.DataFrame(plotting_data_dicts)
    ax = sns.pointplot(x="NUMBER OF ITERATIONS", y="STANDARD DEVIATION", data=plotting_data_df)

    # Format the plot.
    ax.set_title('Stability over Iterations')
    plt.tight_layout()

    # Save the plot.
    print 'Saving plot to ' + args.plot_path + '/sd_iters.' + args.evaluation_tag + '.pdf'
    plt.savefig(args.plot_path + '/sd_iters.' + args.evaluation_tag + '.pdf')
    plt.clf()



if __name__ == '__main__':
    main()




