import gensim
import pickle
import argparse


STOPS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
         'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
         'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
         'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
         'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
         'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
         'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
         'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
         'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
         'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
         'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
         'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now',
         'a', 'd', 'v', 'f']


def display_topics(model, dictionary, num_topics, output_path):
    """
    Gets the top N words for each topic and saves the results to an output file.
    """

    # topics = model.show_topics(num_topics=num_topics)

    output_file = open(output_path, 'w')

    for i in range(0, num_topics):

        word_probability_tuples = model.get_topic_terms(i, topn=20)

        for word_id, probability in word_probability_tuples:
            word = dictionary[word_id]
            output_file.write(word + ' ')

        output_file.write('\n')


def remove_stopwords(document):
    return [word for word in document if word not in STOPS]


def remove_short_words(document, min_length=3):
    return [word for word in document if not len(word) < min_length]


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str)
    parser.add_argument('--num_topics', type=int)
    parser.add_argument('--output_path', type=str)
    args = parser.parse_args()

    print '-- Loading documents...'
    documents = [line.strip().split() for line in open(args.data_path, 'r') if line.strip()]

    print '-- Removing stopwords and short words...'
    documents = [remove_stopwords(document)for document in documents]
    documents = [remove_short_words(document)for document in documents]

    print '-- Building dictionary...'
    dictionary = gensim.corpora.Dictionary(documents)
    dictionary.compactify()

    print '-- Building corpus...'
    corpus = [dictionary.doc2bow(document) for document in documents]

    print '-- Training...'
    model = gensim.models.LdaModel(corpus, id2word=dictionary, num_topics=args.num_topics)
    topics = model.show_topics(args.num_topics)

    print '-- Getting topics...'
    # output_file = open(args.output_path, 'w')
    # for topic in topics:
    #     output_file.write(topic + '\n')
    display_topics(model, dictionary, args.num_topics, args.output_path)


if __name__ == '__main__':
    main()
