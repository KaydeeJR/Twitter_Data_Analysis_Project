import pyLDAvis.gensim
import matplotlib.pyplot as plt
import numpy as np

from gensim import corpora, models
from gensim.similarities import MatrixSimilarity
from gensim.utils import SaveLoad
from gensim.matutils import corpus2csc, sparse2full, corpus2dense

from collections import Counter
from wordcloud import WordCloud
from sklearn.utils import resample


class TopicModelling:
    """
    A class for performing topic modeling on a collection of tweets.

    This class provides methods for creating a bag of words, dictionary corpus, training LDA models,
    and visualizing the results. It uses popular libraries such as Gensim and wordcloud
    for topic modeling and visualization.
    """

    def __init__(self):
        pass

    def make_dictionary(self, processed_df):
        """
        Creating and managing a vocabulary of words from a dataframe. 

        :param processed_df : the tweets dataframe to use to create a mapping.
        
        :return mapping: mapping of words in tweets dataframe to integer IDs
        """
        return corpora.Dictionary(processed_df)

    def save_dictionary(self, mapping_dict, mapping_name):
        """
        Saves the dictionary as a file in the current directory.

        :param mapping_dict: the dictionary mapping of ids to words
        :param mapping_name: the file name of the dictionary

        :return boolean: True if saved succeeded, False otherwise
        """
        mapping_dict.save(mapping_name+'.dict')

        return True
    
    def load_dictionary(self, filename):
        """
        Load the dictionary from a local file in the current directory.

        :param filename: the name of file containing the dictionary

        :return dictionary: a mapping of words to integer IDs
        """
        dictionary = corpora.Dictionary.load(filename+r'.dict')
        return dictionary
    
    def create_bow(self, tweet_list, mapping_dict):
        """
        Converts a list of words into a bag-of-words(bow). Essentially representing text data as a numerical vector. 
        
        bow is a sparse vector that contains the number of times each word in the list
        appears in the document.

        word ID is the integer ID of the word in the vocabulary
        word count is the number of times the word appears in the document.

        :param mapping_dict: mapping dictionary created by Corpora library
        :param tweet_list: the tweets list to use to create a mapping

        :return: list of tuples (word ID, word count)
        """
        return [mapping_dict.doc2bow(tweet) for tweet in tweet_list]

    def serialize_bow(self, bow_name, bow):
        """
        :param bow_name: file name of the bag-of-words(bow).
        :param bow: bag-of-words(bow)

        :return: True if file is saved, false otherwise
        """
        corpora.MmCorpus.serialize(bow_name+'.mm', bow)
        return True
    
    def load_bow(self, filename):
        """
        Load the dictionary as a file in the current directory.

        :param filename: the name of the file to load the dictionary object

        :return bag_of_words: the vector of words
        """
        bow_corpus = corpora.MmCorpus(filename+r'.mm')
        return bow_corpus
    
    def create_lda_model(self, bow, mapping_dict, no_of_topics=50, no_of_passes=10, no_of_iterations=50, alpha_level=0.001):
        """
        LDA model learns shared topics across the tweet corpus.
        
        The low number for alpha corresponds to a low number of topics per tweet,
        since tweets are relatively very short

        For the number of topics, 50 seems to be a good compromise between optimizing accuracy and interpretability.
        Increasing the number of topics, decreases the log perplexity (an error metric)
        which makes it more difficult to interpret the data. 
        
        :param bow: the bag-of-words(bow) vector
        :param mapping_dict: a dictionary mapping of ids to word

        :return: Numpy array of the variational bound score calculated for each document.
        """
        return models.LdaMulticore(bow, id2word=mapping_dict, num_topics=no_of_topics, passes=no_of_passes,
                                   iterations=no_of_iterations, alpha=alpha_level)

    def save_lda_model(self, lda_model, lda_name):
        """
        Save LDA model
        
        :param lda_model: the LDA model
        :param lda_name: the name of the file

        :return: True if save succeeded, otherwise False
        """
        SaveLoad.save(lda_model, lda_name)
        return True

    def load_lda_model(self, filename):
        """
        Load LDA model from file
        
        :param filename: the name of the file in the current directory

        :return: the LDA model
        """
        lda_model = SaveLoad.load(filename)
        return lda_model


    def visualize_lda_results(self, lda_model, tweet_corpus, mapping_dict):
        """
        Produce an interactive visualization.

        :param lda_model: the LDA model
        :param tweet_corpus: the bow
        :param mapping_dict: the mapping of words to integer IDs

        :return: an interactive plot of the topics in the tweets data
        """
        ldaViz = pyLDAvis.gensim.prepare(lda_model, tweet_corpus, mapping_dict)
        return ldaViz

    def create_word_cloud(self,tweet_list):
        """
        Create word cloud of tweets

        :param tweet_list: the list of words in tweets

        :return: the word cloud of tweets
        """
        word_strings = ' '.join([' '.join(string) for string in tweet_list])
        topic_cloud = WordCloud(max_font_size=100, scale=8).generate(word_strings)
        fig = plt.figure(figsize=(10, 10), dpi=1600)
        plt.imshow(topic_cloud)
        plt.axis("off")
        plt.show()
