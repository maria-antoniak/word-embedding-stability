import os
import sys

CORPUS_PATH_DICT = {'court_4': '/share/magpie/datasets/courtlistener/ca4.lines.recent',
                    'court_9': '/share/magpie/datasets/courtlistener/ca9.lines.recent',
                    'nyt_2000_music': '/share/magpie/datasets/nyt_full/2000',
                    'nyt_2000_sports': '/share/magpie/datasets/nyt_full/2000',
                    'reddit_ask_science': '/home/maa343/data/reddit/askscience.jsonlist',
                    'reddit_ask_historians': '/home/maa343/data/reddit/AskHistorians.jsonlist'}
# CORPUS_SIZES = [0.2, 0.4, 0.6, 0.8, 1.0]
# CORPUS_SIZES = [0.2, 0.4, 0.6, 0.8]
CORPUS_SIZES = [1.0]
MODELS = ['lsa', 'word2vec', 'glove', 'ppmi']
DOCUMENT_SIZES = ['sentence', 'whole']
SETTINGS = ['fixed', 'shuffled', 'bootstrap']
ITERATION_SETTINGS = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
NUM_ITERATIONS = 50
WORD_FREQUENCY_THRESHOLD = 20
NUM_WORDS_TO_PLOT = 10
OPTIONS = ['process', 'vocab', 'train', 'query', 'plot_queries', 'lda', 'top_lists',
           'plot_violins_document_size', 'plot_violins_corpus_size', 'plot_rank',
           'plot_rank_collapsed', 'plot_sd_collapsed', 'query_iters', 'plot_sd_algorithms',
           'plot_sd_iters', 'plot_jaccard_collapsed', 'plot_jaccard_algorithm', 'plot_rank_sd',
           'plot_mean_algorithms']


#############################################################
# Train LDA and save topics.                                #
#############################################################
def run_lda():
    condor_text = 'Universe = vanilla\n' \
                  'Executable = training/lda.sh\n' \
                  'getenv = true\n'

    num_condor_jobs = 0

    for corpus, corpus_path in CORPUS_PATH_DICT.iteritems():

        arguments = corpus + ' ' \
                    + corpus_path

        condor_text += 'arguments = ' + arguments + '\n'
        condor_text += 'output = tmp/lda.stdout.$(process).txt\n'
        condor_text += 'error = tmp/lda.stderr.$(process).txt\n'
        condor_text += 'log = tmp/lda.log.$(process).txt\n'
        condor_text += 'queue 1\n'

        num_condor_jobs += 1

    print 'Submitting ' + str(num_condor_jobs) + ' condor jobs to run LDA...'

    with open('tmp.lda.condor', 'w') as condor_file:
        condor_file.write(condor_text)

    os.system('condor_submit tmp.lda.condor')


#############################################################
# Create a vocabulary file for each corpus.                 #
#############################################################
def run_vocab():
    condor_text = 'Universe = vanilla\n' \
                  'Executable = preprocessing/run_get_vocabulary.sh\n' \
                  'getenv = true\n'

    num_condor_jobs = 0

    for corpus, corpus_path in CORPUS_PATH_DICT.iteritems():
        for corpus_size in CORPUS_SIZES:
            for document_size in DOCUMENT_SIZES:

                arguments = corpus + ' ' \
                            + str(corpus_size) + ' ' \
                            + document_size + ' '

                condor_text += 'arguments = ' + arguments + '\n'
                condor_text += 'output = tmp/vocab.stdout.$(process).txt\n'
                condor_text += 'error = tmp/vocab.stderr.$(process).txt\n'
                condor_text += 'log = tmp/vocab.log.$(process).txt\n'
                condor_text += 'queue 1\n'

                num_condor_jobs += 1

    print 'Submitting ' + str(num_condor_jobs) + ' condor jobs to process corpus...'

    with open('tmp.vocab.condor', 'w') as condor_file:
        condor_file.write(condor_text)

    os.system('condor_submit tmp.vocab.condor')


#############################################################
# Process the corpus for training.                          #
#############################################################
def run_process():
    condor_text = 'Universe = vanilla\n' \
                  'Executable = preprocessing/process.sh\n' \
                  'getenv = true\n'

    num_condor_jobs = 0

    for corpus, corpus_path in CORPUS_PATH_DICT.iteritems():
        for corpus_size in CORPUS_SIZES:
            for document_size in DOCUMENT_SIZES:
                for setting in SETTINGS:
                    for i in range(0, NUM_ITERATIONS):

                        arguments = corpus + ' ' \
                                    + corpus_path + ' ' \
                                    + str(corpus_size) + ' ' \
                                    + document_size + ' ' \
                                    + setting + ' ' \
                                    + str(i) + ' ' \
                                    + str(WORD_FREQUENCY_THRESHOLD)

                        condor_text += 'arguments = ' + arguments + '\n'
                        condor_text += 'output = tmp/process.stdout.$(process).txt\n'
                        condor_text += 'error = tmp/process.stderr.$(process).txt\n'
                        condor_text += 'log = tmp/process.log.$(process).txt\n'
                        condor_text += 'queue 1\n'

                        num_condor_jobs += 1

    print 'Submitting ' + str(num_condor_jobs) + ' condor jobs to process corpus...'

    with open('tmp.process.condor', 'w') as condor_file:
        condor_file.write(condor_text)

    os.system('condor_submit tmp.process.condor')


#############################################################
# Train the embedding models.                               #
#############################################################
def run_train(model):
    condor_text = 'Universe = vanilla\n' \
                  'Executable = training/train.sh\n' \
                  'getenv = true\n'

    num_condor_jobs = 0

    for corpus, corpus_path in CORPUS_PATH_DICT.iteritems():
        for corpus_size in CORPUS_SIZES:
            for document_size in DOCUMENT_SIZES:
                for setting in SETTINGS:
                    for i in range(0, NUM_ITERATIONS):

                        arguments = corpus + ' ' \
                                    + str(corpus_size) + ' ' \
                                    + document_size + ' ' \
                                    + model + ' ' \
                                    + setting + ' ' \
                                    + str(i) + ' ' \
                                    + str(WORD_FREQUENCY_THRESHOLD)

                        condor_text += 'arguments = ' + arguments + '\n'
                        condor_text += 'output = tmp/train.stdout.$(process).txt\n'
                        if model != 'glove':
                            condor_text += 'error = tmp/train.stderr.$(process).txt\n'
                            condor_text += 'log = tmp/train.log.$(process).txt\n'
                        condor_text += 'queue 1\n'

                        num_condor_jobs += 1

    print 'Submitting ' + str(num_condor_jobs) + ' condor jobs to train models...'

    with open('tmp.train.' + model + '.condor', 'w') as condor_file:
        condor_file.write(condor_text)

    os.system('condor_submit tmp.train.' + model + '.condor')


#############################################################
# Get the cosine similarities.                              #
#############################################################
def run_query(model):
    condor_text = 'Universe = vanilla\n' \
                  'Executable = query/query.sh\n' \
                  'getenv = true\n'

    num_condor_jobs = 0

    for corpus, corpus_path in CORPUS_PATH_DICT.iteritems():
        for corpus_size in CORPUS_SIZES:
            for document_size in DOCUMENT_SIZES:
                for setting in SETTINGS:
                    # for model in MODELS:

                    arguments = corpus + ' ' \
                                + str(corpus_size) + ' ' \
                                + document_size + ' ' \
                                + model + ' ' \
                                + setting + ' ' \
                                + str(NUM_ITERATIONS)

                    condor_text += 'arguments = ' + arguments + '\n'
                    condor_text += 'output = tmp/query.stdout.$(process).txt\n'
                    condor_text += 'error = tmp/query.stderr.$(process).txt\n'
                    condor_text += 'log = tmp/query.log.$(process).txt\n'
                    condor_text += 'queue\n'

                    num_condor_jobs += 1

    print 'Submitting ' + str(num_condor_jobs) + ' condor jobs to query models...'

    with open('tmp.query.condor', 'w') as condor_file:
        condor_file.write(condor_text)

    os.system('condor_submit tmp.query.condor')


#############################################################
# Get the cosine similarities for different # iters.        #
#############################################################
def run_query_iters():
    condor_text = 'Universe = vanilla\n' \
                  'Executable = query/query.sh\n' \
                  'getenv = true\n'

    corpus = 'court_4'

    num_condor_jobs = 0

    for corpus_size in CORPUS_SIZES:
        for document_size in DOCUMENT_SIZES:
            for setting in SETTINGS:
                for model in MODELS:
                    for num_iterations in ITERATION_SETTINGS:

                        arguments = corpus + ' ' \
                                    + str(corpus_size) + ' ' \
                                    + document_size + ' ' \
                                    + model + ' ' \
                                    + setting + ' ' \
                                    + str(num_iterations)

                        condor_text += 'arguments = ' + arguments + '\n'
                        condor_text += 'output = tmp/query_iters.stdout.$(process).txt\n'
                        condor_text += 'error = tmp/query_iters.stderr.$(process).txt\n'
                        condor_text += 'log = tmp/query_iters.log.$(process).txt\n'
                        condor_text += 'queue\n'

                        num_condor_jobs += 1

    print 'Submitting ' + str(num_condor_jobs) + ' condor jobs to query models...'

    with open('tmp.query_iters.condor', 'w') as condor_file:
        condor_file.write(condor_text)

    os.system('condor_submit tmp.query_iters.condor')


#############################################################
# Get the top N words for each target and iteration.        #
#############################################################
def run_top_lists():
    condor_text = 'Universe = vanilla\n' \
                  'Executable = evaluation/get_top_lists.sh\n' \
                  'getenv = true\n'

    num_condor_jobs = 0

    for corpus, corpus_path in CORPUS_PATH_DICT.iteritems():
        for corpus_size in CORPUS_SIZES:
            for document_size in DOCUMENT_SIZES:
                for setting in SETTINGS:
                    for model in MODELS:

                        arguments = corpus + ' ' \
                                    + str(corpus_size) + ' ' \
                                    + document_size + ' ' \
                                    + model + ' ' \
                                    + setting + ' ' \
                                    + str(NUM_ITERATIONS)

                        condor_text += 'arguments = ' + arguments + '\n'
                        condor_text += 'output = tmp/top_lists.stdout.$(process).txt\n'
                        condor_text += 'error = tmp/top_lists.stderr.$(process).txt\n'
                        condor_text += 'log = tmp/top_lists.log.$(process).txt\n'
                        condor_text += 'queue\n'

                        num_condor_jobs += 1

    print 'Submitting ' + str(num_condor_jobs) + ' condor jobs to get top lists...'

    with open('tmp.top_lists.condor', 'w') as condor_file:
        condor_file.write(condor_text)

    os.system('condor_submit tmp.top_lists.condor')


#############################################################
# Generate the plots.                                       #
#############################################################
def run_plot_queries():
    condor_text = 'Universe = vanilla\n' \
                  'Executable = evaluation/plot_queries.sh\n' \
                  'getenv = true\n'

    num_condor_jobs = 0

    for corpus, corpus_path in CORPUS_PATH_DICT.iteritems():
        for corpus_size in CORPUS_SIZES:
            for document_size in DOCUMENT_SIZES:
                for model in MODELS:

                    arguments = corpus + ' ' \
                                + str(corpus_size) + ' ' \
                                + document_size + ' ' \
                                + model + ' ' \
                                + str(NUM_WORDS_TO_PLOT)

                    condor_text += 'arguments = ' + arguments + '\n'
                    condor_text += 'output = tmp/plot.stdout.$(process).txt\n'
                    condor_text += 'error = tmp/plot.stderr.$(process).txt\n'
                    condor_text += 'log = tmp/plot.log.$(process).txt\n'
                    condor_text += 'queue\n'

                    num_condor_jobs += 1

    print 'Submitting ' + str(num_condor_jobs) + ' condor jobs to create plots...'

    with open('tmp.plot.condor', 'w') as condor_file:
        condor_file.write(condor_text)

    os.system('condor_submit tmp.plot.condor')


#############################################################
# Generate the plots.                                       #
#############################################################
def run_plot_rank():
    condor_text = 'Universe = vanilla\n' \
                  'Executable = evaluation/plot_rank.sh\n' \
                  'getenv = true\n'

    num_condor_jobs = 0

    for corpus, corpus_path in CORPUS_PATH_DICT.iteritems():
        for corpus_size in CORPUS_SIZES:
            for document_size in DOCUMENT_SIZES:
                for model in MODELS:
                    for setting in SETTINGS:

                        arguments = corpus + ' ' \
                                    + str(corpus_size) + ' ' \
                                    + document_size + ' ' \
                                    + model + ' ' \
                                    + setting

                        condor_text += 'arguments = ' + arguments + '\n'
                        condor_text += 'output = tmp/plot_rank.stdout.$(process).txt\n'
                        condor_text += 'error = tmp/plot_rank.stderr.$(process).txt\n'
                        condor_text += 'log = tmp/plot_rank.log.$(process).txt\n'
                        condor_text += 'queue\n'

                        num_condor_jobs += 1

    print 'Submitting ' + str(num_condor_jobs) + ' condor jobs to create rank plots...'

    with open('tmp.plot_rank.condor', 'w') as condor_file:
        condor_file.write(condor_text)

    os.system('condor_submit tmp.plot_rank.condor')


#############################################################
# Generate the plots.                                       #
#############################################################
def run_plot_rank_collapsed():
    condor_text = 'Universe = vanilla\n' \
                  'Executable = evaluation/plot_rank_collapsed.sh\n' \
                  'getenv = true\n'

    num_condor_jobs = 0

    for corpus, corpus_path in CORPUS_PATH_DICT.iteritems():
        for corpus_size in CORPUS_SIZES:
            for document_size in DOCUMENT_SIZES:
                for model in MODELS:
                    for setting in SETTINGS:

                        arguments = corpus + ' ' \
                                    + str(corpus_size) + ' ' \
                                    + document_size + ' ' \
                                    + model + ' ' \
                                    + setting

                        condor_text += 'arguments = ' + arguments + '\n'
                        condor_text += 'output = tmp/plot_rank_collapsed.stdout.$(process).txt\n'
                        condor_text += 'error = tmp/plot_rank_collapsed.stderr.$(process).txt\n'
                        condor_text += 'log = tmp/plot_rank_collapsed.log.$(process).txt\n'
                        condor_text += 'queue\n'

                        num_condor_jobs += 1

    print 'Submitting ' + str(num_condor_jobs) + ' condor jobs to create rank plots...'

    with open('tmp.plot_rank_collapsed.condor', 'w') as condor_file:
        condor_file.write(condor_text)

    os.system('condor_submit tmp.plot_rank_collapsed.condor')


#############################################################
# Generate the plots.                                       #
#############################################################
def run_plot_rank_sd():
    condor_text = 'Universe = vanilla\n' \
                  'Executable = evaluation/plot_rank_sd.sh\n' \
                  'getenv = true\n'

    num_condor_jobs = 0

    for corpus, corpus_path in CORPUS_PATH_DICT.iteritems():
        for corpus_size in CORPUS_SIZES:
            for document_size in DOCUMENT_SIZES:
                for model in MODELS:
                    for setting in SETTINGS:

                        arguments = corpus + ' ' \
                                    + str(corpus_size) + ' ' \
                                    + document_size + ' ' \
                                    + model + ' ' \
                                    + setting

                        condor_text += 'arguments = ' + arguments + '\n'
                        condor_text += 'output = tmp/plot_rank_sd.stdout.$(process).txt\n'
                        condor_text += 'error = tmp/plot_rank_sd.stderr.$(process).txt\n'
                        condor_text += 'log = tmp/plot_rank_sd.log.$(process).txt\n'
                        condor_text += 'queue\n'

                        num_condor_jobs += 1

    print 'Submitting ' + str(num_condor_jobs) + ' condor jobs to create rank sd plots...'

    with open('tmp.plot_rank_sd.condor', 'w') as condor_file:
        condor_file.write(condor_text)

    os.system('condor_submit tmp.plot_rank_sd.condor')


#############################################################
# Generate the plots.                                       #
#############################################################
def run_plot_jaccard_collapsed():
    condor_text = 'Universe = vanilla\n' \
                  'Executable = evaluation/plot_jaccard_collapsed.sh\n' \
                  'getenv = true\n'

    num_condor_jobs = 0

    for corpus, corpus_path in CORPUS_PATH_DICT.iteritems():
        for corpus_size in CORPUS_SIZES:
            for document_size in DOCUMENT_SIZES:
                for model in MODELS:

                    arguments = corpus + ' ' \
                                + str(corpus_size) + ' ' \
                                + document_size + ' ' \
                                + model

                    condor_text += 'arguments = ' + arguments + '\n'
                    condor_text += 'output = tmp/plot_jaccard_collapsed.stdout.$(process).txt\n'
                    condor_text += 'error = tmp/plot_jaccard_collapsed.stderr.$(process).txt\n'
                    condor_text += 'log = tmp/plot_jaccard_collapsed.log.$(process).txt\n'
                    condor_text += 'queue\n'

                    num_condor_jobs += 1

    print 'Submitting ' + str(num_condor_jobs) + ' condor jobs to create rank plots...'

    with open('tmp.plot_jaccard_collapsed.condor', 'w') as condor_file:
        condor_file.write(condor_text)

    os.system('condor_submit tmp.plot_jaccard_collapsed.condor')


#############################################################
# Generate the plots.                                       #
#############################################################
def run_plot_jaccard_algorithm():
    condor_text = 'Universe = vanilla\n' \
                  'Executable = evaluation/plot_jaccard_algorithm.sh\n' \
                  'getenv = true\n'

    num_condor_jobs = 0

    top_words_settings = [2, 10]

    for corpus, corpus_path in CORPUS_PATH_DICT.iteritems():
        for corpus_size in CORPUS_SIZES:
            for document_size in DOCUMENT_SIZES:
                for num_top_words in top_words_settings:

                    arguments = corpus + ' ' \
                                + str(corpus_size) + ' ' \
                                + document_size + ' ' \
                                + str(num_top_words)

                    condor_text += 'arguments = ' + arguments + '\n'
                    condor_text += 'output = tmp/plot_jaccard_algorithm.stdout.$(process).txt\n'
                    condor_text += 'error = tmp/plot_jaccard_algorithm.stderr.$(process).txt\n'
                    condor_text += 'log = tmp/plot_jaccard_algorithm.log.$(process).txt\n'
                    condor_text += 'queue\n'

                    num_condor_jobs += 1

    print 'Submitting ' + str(num_condor_jobs) + ' condor jobs to create rank plots...'

    with open('tmp.plot_jaccard_algorithm.condor', 'w') as condor_file:
        condor_file.write(condor_text)

    os.system('condor_submit tmp.plot_jaccard_algorithm.condor')


#############################################################
# Generate the plots.                                       #
#############################################################
def run_plot_sd_collapsed():
    condor_text = 'Universe = vanilla\n' \
                  'Executable = evaluation/plot_sd_collapsed.sh\n' \
                  'getenv = true\n'

    num_condor_jobs = 0

    for corpus, corpus_path in CORPUS_PATH_DICT.iteritems():
        for corpus_size in CORPUS_SIZES:
            for document_size in DOCUMENT_SIZES:
                for model in MODELS:
                    for setting in SETTINGS:

                        arguments = corpus + ' ' \
                                    + str(corpus_size) + ' ' \
                                    + document_size + ' ' \
                                    + model + ' ' \
                                    + setting

                        condor_text += 'arguments = ' + arguments + '\n'
                        condor_text += 'output = tmp/plot_sd_collapsed.stdout.$(process).txt\n'
                        condor_text += 'error = tmp/plot_sd_collapsed.stderr.$(process).txt\n'
                        condor_text += 'log = tmp/plot_sd_collapsed.log.$(process).txt\n'
                        condor_text += 'queue\n'

                        num_condor_jobs += 1

    print 'Submitting ' + str(num_condor_jobs) + ' condor jobs to create rank plots...'

    with open('tmp.plot_sd_collapsed.condor', 'w') as condor_file:
        condor_file.write(condor_text)

    os.system('condor_submit tmp.plot_sd_collapsed.condor')


#############################################################
# Generate the plots.                                       #
#############################################################
def run_plot_sd_iters():
    condor_text = 'Universe = vanilla\n' \
                  'Executable = evaluation/plot_sd_iters.sh\n' \
                  'getenv = true\n'

    num_condor_jobs = 0

    corpus = 'court_4'

    for corpus_size in CORPUS_SIZES:
        for document_size in DOCUMENT_SIZES:
            for model in MODELS:
                for setting in SETTINGS:

                    arguments = corpus + ' ' \
                                + str(corpus_size) + ' ' \
                                + document_size + ' ' \
                                + model + ' ' \
                                + setting

                    condor_text += 'arguments = ' + arguments + '\n'
                    condor_text += 'output = tmp/plot_sd_iters.stdout.$(process).txt\n'
                    condor_text += 'error = tmp/plot_sd_iters.stderr.$(process).txt\n'
                    condor_text += 'log = tmp/plot_sd_iters.log.$(process).txt\n'
                    condor_text += 'queue\n'

                    num_condor_jobs += 1

    print 'Submitting ' + str(num_condor_jobs) + ' condor jobs to create sd iters plots...'

    with open('tmp.plot_sd_iters.condor', 'w') as condor_file:
        condor_file.write(condor_text)

    os.system('condor_submit tmp.plot_sd_iters.condor')


#############################################################
# Generate the plots.                                       #
#############################################################
def run_plot_sd_algorithms():
    condor_text = 'Universe = vanilla\n' \
                  'Executable = evaluation/plot_sd_algorithms.sh\n' \
                  'getenv = true\n'

    num_condor_jobs = 0

    for corpus, corpus_path in CORPUS_PATH_DICT.iteritems():

        arguments = corpus

        condor_text += 'arguments = ' + arguments + '\n'
        condor_text += 'output = tmp/plot_sd_algorithms.stdout.$(process).txt\n'
        condor_text += 'error = tmp/plot_sd_algorithms.stderr.$(process).txt\n'
        condor_text += 'log = tmp/plot_sd_algorithms.log.$(process).txt\n'
        condor_text += 'queue\n'

        num_condor_jobs += 1

    print 'Submitting ' + str(num_condor_jobs) + ' condor jobs to create sd plots...'

    with open('tmp.plot_sd_algorithms.condor', 'w') as condor_file:
        condor_file.write(condor_text)

    os.system('condor_submit tmp.plot_sd_algorithms.condor')


#############################################################
# Generate the mean plots.                                       #
#############################################################
def run_plot_mean_algorithms():
    condor_text = 'Universe = vanilla\n' \
                  'Executable = evaluation/plot_mean_algorithms.sh\n' \
                  'getenv = true\n'

    num_condor_jobs = 0

    for corpus, corpus_path in CORPUS_PATH_DICT.iteritems():

        arguments = corpus

        condor_text += 'arguments = ' + arguments + '\n'
        condor_text += 'output = tmp/plot_mean_algorithms.stdout.$(process).txt\n'
        condor_text += 'error = tmp/plot_mean_algorithms.stderr.$(process).txt\n'
        condor_text += 'log = tmp/plot_mean_algorithms.log.$(process).txt\n'
        condor_text += 'queue\n'

        num_condor_jobs += 1

    print 'Submitting ' + str(num_condor_jobs) + ' condor jobs to create mean plots...'

    with open('tmp.plot_mean_algorithms.condor', 'w') as condor_file:
        condor_file.write(condor_text)

    os.system('condor_submit tmp.plot_mean_algorithms.condor')


#############################################################
# Generate the violin plots.                                #
#############################################################
def run_plot_violins_document_size():
    condor_text = 'Universe = vanilla\n' \
                  'Executable = evaluation/plot_violins_document_size.sh\n' \
                  'getenv = true\n'

    num_condor_jobs = 0

    for corpus, corpus_path in CORPUS_PATH_DICT.iteritems():
        for corpus_size in CORPUS_SIZES:
            for model in MODELS:
                for setting in SETTINGS:

                    arguments = corpus + ' ' \
                                + str(corpus_size) + ' ' \
                                + model + ' ' \
                                + setting

                    condor_text += 'arguments = ' + arguments + '\n'
                    condor_text += 'output = tmp/plot_violins_document_size.stdout.$(process).txt\n'
                    condor_text += 'error = tmp/plot_violins_document_size.stderr.$(process).txt\n'
                    condor_text += 'log = tmp/plot_violins_document_size.log.$(process).txt\n'
                    condor_text += 'queue\n'

                    num_condor_jobs += 1

    print 'Submitting ' + str(num_condor_jobs) + ' condor jobs to create violin plots...'

    with open('tmp.plot_violins_document_size.condor', 'w') as condor_file:
        condor_file.write(condor_text)

    os.system('condor_submit tmp.plot_violins_document_size.condor')


#############################################################
# Generate the violin plots.                                #
#############################################################
def run_plot_violins_corpus_size():
    condor_text = 'Universe = vanilla\n' \
                  'Executable = evaluation/plot_violins_corpus_size.sh\n' \
                  'getenv = true\n'

    num_condor_jobs = 0

    model = 'word2vec'

    MODIFIED_CORPUS_PATH_DICT = {'court_4': '/share/magpie/datasets/courtlistener/ca4.lines.recent',
                                 'reddit_ask_science': '/home/maa343/data/reddit/askscience.jsonlist'}

    for corpus, corpus_path in MODIFIED_CORPUS_PATH_DICT.iteritems():
        for setting in SETTINGS:

            arguments = corpus + ' ' \
                        + model + ' ' \
                        + setting

            condor_text += 'arguments = ' + arguments + '\n'
            condor_text += 'output = tmp/plot_violins_corpus_size.stdout.$(process).txt\n'
            condor_text += 'error = tmp/plot_violins_corpus_size.stderr.$(process).txt\n'
            condor_text += 'log = tmp/plot_violins_corpus_size.log.$(process).txt\n'
            condor_text += 'queue\n'

            num_condor_jobs += 1

    print 'Submitting ' + str(num_condor_jobs) + ' condor jobs to create violin plots...'

    with open('tmp.plot_violins_corpus_size.condor', 'w') as condor_file:
        condor_file.write(condor_text)

    os.system('condor_submit tmp.plot_violins_corpus_size.condor')


#############################################################
# Main.                                                     #
#############################################################
def main():

    # Create an output directory for the log files.
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    # Get command line option.
    option = sys.argv[1]
    if option not in OPTIONS:
        print 'ERROR: ' + option + ' is not a real option!'
        exit(1)

    # Run the selected process.
    if option == 'lda':
        run_lda()

    if option == 'process':
        run_process()

    if option == 'vocab':
        run_vocab()

    if option == 'train':
        model = sys.argv[2]
        if model not in MODELS:
            print 'ERROR: ' + model + ' is not a real model!'
            exit(1)
        run_train(model)

    if option == 'query':
        model = sys.argv[2]
        if model not in MODELS:
            print 'ERROR: ' + model + ' is not a real model!'
            exit(1)
        run_query(model)

    if option == 'query_iters':
        run_query_iters()

    if option == 'plot_queries':
        run_plot_queries()

    if option == 'plot_rank':
        run_plot_rank()

    if option == 'plot_rank_collapsed':
        run_plot_rank_collapsed()

    if option == 'plot_rank_sd':
        run_plot_rank_sd()

    if option == 'plot_sd_collapsed':
        run_plot_sd_collapsed()

    if option == 'plot_jaccard_collapsed':
        run_plot_jaccard_collapsed()

    if option == 'plot_jaccard_algorithm':
        run_plot_jaccard_algorithm()

    if option == 'plot_sd_algorithms':
        run_plot_sd_algorithms()

    if option == 'plot_mean_algorithms':
        run_plot_mean_algorithms()

    if option == 'plot_sd_iters':
        run_plot_sd_iters()

    if option == 'plot_violins_document_size':
        run_plot_violins_document_size()

    if option == 'plot_violins_corpus_size':
        run_plot_violins_corpus_size()

    if option == 'top_lists':
        run_top_lists()


if __name__ == '__main__':
    main()
