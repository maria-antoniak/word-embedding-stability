import argparse
import pandas
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn
from collections import defaultdict


def get_records(evaluation_path, setting, target):
    averages_path = evaluation_path + '/' + setting + '/averages.' + target + '.txt'
    records = pandas.read_csv(averages_path, sep='\t').to_dict('records')
    return records


def sort_records(sorted_words, records_to_sort):

    word_record_map = {record['WORD']: record for record in records_to_sort}
    newly_sorted_records = [word_record_map[word] for word in sorted_words]

    return newly_sorted_records


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--targets_path', type=str)
    parser.add_argument('--num_words_to_plot', type=int)
    parser.add_argument('--plot_path', type=str)
    parser.add_argument('--evaluation_path', type=str)
    parser.add_argument('--evaluation_tag', type=str)
    parser.add_argument('--model', type=str)
    args = parser.parse_args()

    # Seaborn settings to make things pretty and readable.
    # seaborn.set(font_scale=1.75, style='whitegrid', palette=seaborn.cubehelix_palette(3, start=.5, rot=-.75, light=0.75))
    # seaborn.set(font_scale=1.75, style='whitegrid', palette=seaborn.color_palette('cubehelix', 5))
    seaborn.set(font_scale=1.75, style='whitegrid', palette=seaborn.color_palette("colorblind", 3))

    # Read in the targets.
    settings = ['fixed', 'shuffled', 'bootstrap']
    targets = [line.strip() for line in open(args.targets_path, 'r') if line.strip()]

    for target in targets:

        print '-- Plotting ' + target + '...'

        # Construct the dictionary of settings and records.
        setting_records_dict = defaultdict(list)
        for setting in settings:
            records = get_records(args.evaluation_path, setting, target)
            setting_records_dict[setting] = records

        # Sort the records to match the order of the fixed setting.
        # The bootstrap setting could be missing words (because missing documents).
        bootstrap_words = [record['WORD'] for record in setting_records_dict['bootstrap']]
        sorted_words = [record['WORD'] for record in setting_records_dict['fixed'] if record['WORD'] in bootstrap_words]
        setting_records_dict['fixed'] = sort_records(sorted_words, setting_records_dict['fixed'])
        setting_records_dict['shuffled'] = sort_records(sorted_words, setting_records_dict['shuffled'])
        setting_records_dict['bootstrap'] = sort_records(sorted_words, setting_records_dict['bootstrap'])

        # Add subplots for the three settings of the N words most closely related to the target word.
        for setting, records in setting_records_dict.iteritems():

            records = records[:args.num_words_to_plot]
            records.reverse()

            y_labels = [record['WORD'] for record in records]
            y = [i for i in range(len(records))]
            x = [record['MEAN'] for record in records]
            e = [record['STANDARD DEVIATION'] for record in records]

            # Offset the error bars slightly, so that they don't overlap.
            if setting == 'shuffled':
                y = [float(value) - 0.2 for value in y]
            elif setting == 'bootstrap':
                y = [float(value) - 0.4 for value in y]

            # plt.errorbar(x, y, xerr=e, elinewidth=2.5, linestyle='None', markersize=10, marker='^', label=setting)
            plt.errorbar(x, y, xerr=e, linestyle='None', marker='^', label=setting, capsize=5)
            plt.yticks(y, y_labels)
            # plt.xlim(0, 1.0)

        model_formatted = args.model
        if args.model == 'word2vec':
            model_formatted = 'SGNS'
        elif args.model == 'ppmi':
            model_formatted = 'PPMI'
        elif args.model == 'glove':
            model_formatted = 'GloVe'
        elif args.model == 'lsa':
            model_formatted = 'LSA'

        plt.legend(loc='upper left')
        plt.title(model_formatted) # + ': "' + target + '"')
        plt.margins(x=0.1, y=0.1)
        plt.xlabel('Cosine Similarity')
        plt.ylabel('Most Similar Words')
        plt.tight_layout()

        output_path = args.plot_path + '/query.' + target + '.' + args.evaluation_tag + '.pdf'
        plt.savefig(output_path)
        plt.clf()


if __name__ == '__main__':
    main()
