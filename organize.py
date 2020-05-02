import os
import argparse


# /out/corpus/document_size/corpus_size/{query|models|data|plots}

# /out/corpus/document_size/corpus_size/results/{ppmi|word2vec|glove}/{fixed|shuffled}bootstrap}
# /out/corpus/document_size/corpus_size/models/{ppmi|word2vec|glove}/{fixed|shuffled}bootstrap}
# /out/corpus/document_size/corpus_size/data/{fixed|shuffled}bootstrap}
# /out/corpus/document_size/corpus_size/plots/{ppmi|word2vec|glove}


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--base_path', type=str)
    parser.add_argument('--corpus', type=str)
    parser.add_argument('--corpus_size', type=str)
    args = parser.parse_args()

    models = ['word2vec', 'glove', 'ppmi', 'lsa']
    settings = ['fixed', 'shuffled', 'bootstrap']
    document_sizes = ['sentence', 'whole']

    output_path = args.base_path + '/out'
    corpus_path = output_path + '/' + args.corpus

    try:
        if not os.path.isdir(output_path):
            os.makedirs(output_path)

        if not os.path.isdir(output_path + '/plots'):
            os.makedirs(output_path + '/plots')

        if not os.path.isdir(corpus_path):
            os.makedirs(corpus_path)

        for document_size in document_sizes:

            document_size_path = corpus_path + '/' + document_size
            corpus_size_path = document_size_path + '/' + args.corpus_size
            models_path = corpus_size_path + '/models'
            plots_path = corpus_size_path + '/plots'
            results_path = corpus_size_path + '/results'
            data_path = corpus_size_path + '/data'

            if not os.path.isdir(document_size_path):
                os.makedirs(document_size_path)

            if not os.path.isdir(corpus_size_path):
                os.makedirs(corpus_size_path)

            if not os.path.isdir(data_path):
                os.makedirs(data_path)

            if not os.path.isdir(models_path):
                os.makedirs(models_path)

            if not os.path.isdir(plots_path):
                os.makedirs(plots_path)

            if not os.path.isdir(results_path):
                os.makedirs(results_path)

            for setting in settings:

                if not os.path.isdir(data_path + '/' + setting):
                    os.makedirs(data_path + '/' + setting)

            for model in models:

                if not os.path.isdir(models_path + '/' + model):
                    os.makedirs(models_path + '/' + model)

                if not os.path.isdir(plots_path + '/' + model):
                    os.makedirs(plots_path + '/' + model)

                if not os.path.isdir(results_path + '/' + model):
                    os.makedirs(results_path + '/' + model)

                for setting in settings:

                    if not os.path.isdir(models_path + '/' + model + '/' + setting):
                        os.makedirs(models_path + '/' + model + '/' + setting)

                    if not os.path.isdir(results_path + '/' + model + '/' + setting):
                        os.makedirs(results_path + '/' + model + '/' + setting)

    # Sometimes, when running many jobs with Condor, it tries to create directories that already exist.
    except OSError, e:
        if e.errno != 17:
            raise
        pass


if __name__ == '__main__':
    main()
