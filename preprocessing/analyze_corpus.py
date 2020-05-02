

def main():

    base_path = '/home/maa343/projects/word-embedding-bootstrap/out'

    for data_path in [base_path + '/reddit_ask_science/whole/1.0/data/fixed/reddit_ask_science.0.txt',
                      base_path + '/reddit_ask_historians/whole/1.0/data/fixed/reddit_ask_historians.0.txt',
                      base_path + '/nyt_2000_sports/whole/1.0/data/fixed/nyt_2000_sports.0.txt',
                      base_path + '/nyt_2000_music/whole/1.0/data/fixed/nyt_2000_music.0.txt',
                      base_path + '/court_4/whole/1.0/data/fixed/court_4.0.txt',
                      base_path + '/court_9/whole/1.0/data/fixed/court_9.0.txt']:

        print '----------------------------------------'
        print 'Data path: ' + data_path

        documents = [line.strip() for line in open(data_path, 'r') if line.strip()]

        vocabulary = {}
        num_words = 0

        for document in documents:
            for word in document.split():
                vocabulary[word] = 1
                num_words += 1

        average_number_words = num_words / len(documents)

        print 'Number of documents: ' + str(len(documents))

        print 'Total number of words: ' + str(num_words)

        print 'Number of unique words: ' + str(len(vocabulary.keys()))

        print 'Ratio of unique words to total words: ' + str(len(vocabulary.keys()) / float(num_words))

        print 'Average number of words per document: ' + str(average_number_words)


if __name__ == '__main__':
    main()
