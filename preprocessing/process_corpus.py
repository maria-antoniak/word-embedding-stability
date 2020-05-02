import re
import random
import argparse
import os
from collections import defaultdict
from datetime import datetime
import json


def remove_extra_spaces(text):
    return ' '.join(text.split())


def remove_non_alpha(text):
    return re.sub('[^A-Za-z\s]', ' ', text)


def process_text(text):
    text = text.lower()
    text = remove_non_alpha(text)
    text = remove_extra_spaces(text)
    return text


def remove_duplicates(seq):
    """
    Removes duplicates while maintaining order.
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def get_documents_toy(input_path, word_frequency_threshold, document_size):

    documents = []
    word_frequency_dict = defaultdict(int)

    # Gather a list of the documents in which each document is a sentence.
    for line in open(input_path, 'r'):

        text = process_text(line.strip())
        documents.append(text)

        for word in text.split():
            word_frequency_dict[word] += 1

    # Remove infrequent words from the documents.
    documents = [' '.join([word for word in document.split() if word_frequency_dict[word] > word_frequency_threshold])
                 for document in documents]

    # Remove duplicate documents while maintaining the order of the documents.
    documents = remove_duplicates(documents)

    return documents


def get_documents_cbt(input_path, word_frequency_threshold, document_size):

    documents = []
    word_frequency_dict = defaultdict(int)

    # Gather a list of the documents in which each document is the whole story.
    if document_size == 'whole':
        for i, line in enumerate(open(input_path, 'r')):

            if '_BOOK_TITLE_' in line or i == 0:
                documents.append('')
            else:
                text = process_text(line.strip())
                documents[-1] += ' ' + text

                for word in text.split():
                    word_frequency_dict[word] += 1

    # Gather a list of the documents in which each document is a sentence.
    elif document_size == 'sentence':
        for line in open(input_path, 'r'):

            text = process_text(line.strip())
            documents.append(text)

            for word in text.split():
                word_frequency_dict[word] += 1

    # Remove infrequent words from the documents.
    documents = [' '.join([word for word in document.split() if word_frequency_dict[word] > word_frequency_threshold])
                 for document in documents if document.strip()]

    # Remove duplicate documents while maintaining the order of the documents.
    documents = remove_duplicates(documents)

    return documents


def get_documents_nyt(directory_path, word_frequency_threshold, document_size, genre):
    """
    Data is located here: /share/magpie/datasets/nyt_full/YYYY/MM/DD/*.xml
    Each .xml file contains a single article.
    """

    documents = []
    word_frequency_dict = defaultdict(int)

    # Iterate through the .xml articles in the folder for a particular YYYY/MM/DD/.
    # Gather a list of the documents in which each document is the whole story.

    for subdir, dirs, file_names in os.walk(directory_path):
        for file_name in file_names:
            if '.xml' in file_name:

                input_path = os.path.join(subdir, file_name)
                read_text = False
                text = ''
                genres = ''

                # Parse and gather the text and the genre.
                for line in open(input_path, 'r'):

                    line = ' '.join(line.split())

                    if 'type="taxonomic_classifier"' in line:
                        genres += ' ' + line
                    if line == '</block>':
                        read_text = False
                    if read_text:
                        text += ' ' + line.replace('<p>', '').replace('</p>', '')
                    if line == '<block class="full_text">':
                        read_text = True

                # Process the text and chunk into sentences or whole documents.
                if genre in genres.lower():

                    if document_size == 'whole':
                        text = process_text(text)
                        documents.append(text)

                        for word in text.split():
                            word_frequency_dict[word] += 1

                    elif document_size == 'sentence':
                        sentences = text.split('.')
                        for sentence in sentences:
                            sentence = process_text(sentence)
                            documents.append(sentence)

                            for word in sentence.split():
                                word_frequency_dict[word] += 1

    # Remove infrequent words from the documents.
    documents = [' '.join([word for word in document.split() if word_frequency_dict[word] > word_frequency_threshold])
                 for document in documents if document.strip()]

    # Remove duplicate documents while maintaining the order of the documents.
    documents = remove_duplicates(documents)

    return documents


def get_documents_reddit(input_path, word_frequency_threshold, document_size):

    documents = []
    word_frequency_dict = defaultdict(int)

    for line in open(input_path, 'r'):

        data_dict = json.loads(line)

        if document_size == 'whole':

            text = ''

            if 'title' in data_dict:
                text += ' ' + data_dict['title']
            if 'selftext' in data_dict:
                text += ' ' + data_dict['selftext']
            if 'body' in data_dict and data_dict['body'] != '[deleted]':
                text += ' ' + data_dict['body']

            text = process_text(text)

            for word in text.split():
                word_frequency_dict[word] += 1

            documents.append(text)

        elif document_size == 'sentence':

            sentences = []

            if 'title' in data_dict:
                sentences.append(data_dict['title'])
            if 'selftext' in data_dict:
                sentences += re.split('!|\.|\?', data_dict['selftext'])
            if 'body' in data_dict and data_dict['body'] != '[deleted]':
                sentences += re.split('!|\.|\?', data_dict['body'])

            for sentence in sentences:

                sentence = process_text(sentence)

                for word in sentence.split():
                    word_frequency_dict[word] += 1

                documents.append(sentence)

    # Remove infrequent words from the documents.
    documents = [' '.join([word for word in document.split() if word_frequency_dict[word] > word_frequency_threshold])
                 for document in documents if document.strip()]

    # Remove duplicate documents while maintaining the order of the documents.
    documents = remove_duplicates(documents)

    return documents


def get_documents_court(input_path, word_frequency_threshold, document_size):

    documents = []
    word_frequency_dict = defaultdict(int)

    # Gather a list of the documents in which each document is the whole story.
    if document_size == 'whole':
        for i, line in enumerate(open(input_path, 'r')):

            text = process_text(line.strip())
            documents.append(text)

            for word in text.split():
                word_frequency_dict[word] += 1

    # Gather a list of the documents in which each document is a sentence.
    elif document_size == 'sentence':
        for line in open(input_path, 'r'):

            sentences = re.split('!|\.|\?', line.strip())

            for sentence in sentences:

                sentence = process_text(sentence)

                for word in sentence.split():
                    word_frequency_dict[word] += 1

                documents.append(sentence)

    # Remove infrequent words from the documents.
    documents = [' '.join([word for word in document.split() if word_frequency_dict[word] > word_frequency_threshold])
                 for document in documents if document.strip()]

    # Remove duplicate documents while maintaining the order of the documents.
    documents = remove_duplicates(documents)

    return documents


def main():

    start_time = datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument('--documents_path', type=str)
    parser.add_argument('--processed_documents_path', type=str)
    parser.add_argument('--word_frequency_threshold', type=int)
    parser.add_argument('--setting', type=str)
    parser.add_argument('--corpus', type=str)
    parser.add_argument('--corpus_size', type=float)
    parser.add_argument('--document_size', type=str)
    args = parser.parse_args()

    documents = []

    # Gather and process the documents of the appropriate size.
    if args.corpus == 'toy':
        documents = get_documents_toy(args.documents_path, args.word_frequency_threshold, args.document_size)
    elif args.corpus == 'cbt':
        documents = get_documents_cbt(args.documents_path, args.word_frequency_threshold, args.document_size)
    elif args.corpus == 'nyt_2000_sports':
        documents = get_documents_nyt(args.documents_path, args.word_frequency_threshold, args.document_size, 'sports')
    elif args.corpus == 'nyt_2000_music':
        documents = get_documents_nyt(args.documents_path, args.word_frequency_threshold, args.document_size, 'music')
    elif args.corpus == 'reddit_ask_science' or args.corpus == 'reddit_ask_historians':
        documents = get_documents_reddit(args.documents_path, args.word_frequency_threshold, args.document_size)
    elif args.corpus == 'court_4' or args.corpus == 'court_9':
        documents = get_documents_court(args.documents_path, args.word_frequency_threshold, args.document_size)

    # Resize the corpus.
    # Documents should be selected in blocks, not randomly (otherwise we mess up the shuffling and bootstrap).
    documents = documents[:int(len(documents)*args.corpus_size)]

    # Keep the documents in a fixed order, shuffle them, or take a bootstrap sample.
    if args.setting == 'fixed':
        pass
    elif args.setting == 'shuffled':
        random.shuffle(documents)
    elif args.setting == 'bootstrap':
        documents = [random.choice(documents) for _ in range(len(documents))]

    # Save the corpus to file.
    processed_documents_file = open(args.processed_documents_path, 'w')
    for document in documents:
        processed_documents_file.write(document + '\n')

    print '-- Processed ' + str(len(documents)) + ' documents'
    print '-- Processed ' + str(len(set(documents))) + ' unique documents'
    print '-- Run Time = ' + str(datetime.now() - start_time)


if __name__ == '__main__':
    main()
