import pyLDAvis.gensim

from gensim import corpora, models
from gensim.similarities import MatrixSimilarity
from gensim.utils import SaveLoad
from gensim.matutils import corpus2csc, sparse2full, corpus2dense

from collections import Counter
from wordcloud import WordCloud
from sklearn.utils import resample


class TopicModelling:
    """
    TODO:
    """

    def __init__(self):
        pass

    def make_dictionary(self, processed_df):
        """
        Create dictionary(structured data).
        Representing words as unique identifiers helps NLP applications to easily compare and manipulate words.

        :param processed_df : the tweets dataframe to use to create a mapping.
        
        :return mapping: mapping of words in tweets dataframe to integer IDs
        """
        return corpora.Dictionary(processed_df)

    def save_dictionary(self, mapping_dict, mapping_name):
        """
        Saves the dictionary as a file in the current directory.

        :param mapping_dict: the tweets dataframe to use to create a mapping
        :param mapping_name: the tweets dataframe to use to create a mapping

        :return boolean: True if saved succeeded
        """
        mapping_dict.save(mapping_name+'.dict')

        return True

    def create_bow(self, processed_df, mapping_dict):
        """
        Converts a document into a bag-of-words(bow).
        bow is a sparse vector that contains the number of times each word in the vocabulary
        appears in the document.
        word ID is the integer ID of the word in the vocabulary
        word count is the number of times the word appears in the document.

        :param mapping_dict: mapping dictionary created by Corpora library
        :param processed_df: the tweets dataframe to use to create a mapping

        :return: list of tuples (word ID, word count)
        """
        return [mapping_dict.doc2bow(row) for index, row in processed_df.iterrows()]

    def serialize_bow(self, bow_name, bow):
        """
        :param:
        """
        corpora.MmCorpus.serialize(bow_name+'.mm', bow)
        return True

    def create_lda_model(self, tweet_corpus, mapping_dict, no_of_topics=50, no_of_passes=10, no_of_iterations=50, alpha_level=0.001):
        """
        LDA model learns shared topics across the tweet corpus.
        """
        return models.LdaMulticore(tweet_corpus, id2word=mapping_dict, num_topics=no_of_topics, passes=no_of_passes,
                                   iterations=no_of_iterations, alpha=alpha_level)

    def visualize_lda_results(self, lda_model, tweet_corpus, mapping_dict):
        """
        Produce an interactive visualization allows users to easily scan the data for topics of interest
        These topics can be subsequently sorted.

        Each circle is a topic and the size represents the abundance of that topic in the corpus. 
        Along with each topic are the associated words that go with it.
        """
        ldaViz = pyLDAvis.gensim.prepare(lda_model, tweet_corpus, mapping_dict)
        return ldaViz

    def save_lda_objects(self, lda_object, lda_name):
        """
        Save model objects
        """
        SaveLoad.save(lda_object, lda_name)
        return True

    def load_lda_objects(self, ):
        kagLda = SaveLoad.load('kaggleLDAmodel0201')
        kagDict = corpora.Dictionary.load('kaggleDictionary0201.dict')
        kagCorpus = corpora.MmCorpus('kaggleCorpus0201.mm')

    def create_word_cloud(cleanedTweetList, mySortedDf, myTopic, myTopicThresh=0.1):
        """
        Create word cloud of tweets passing a given threshold for a given topic
        """
        sortedIdx = sortByTopicToIdx(
            cleanedTweetList, mySortedDf, myTopic, myTopicThresh=0.1)
        mySortedTweets = sortTweetsByIdx(cleanedTweetList, sortedIdx)
        filteredWords = ' '.join([' '.join(string)
                                 for string in mySortedTweets])
        myTopicCloud = WordCloud(
            max_font_size=100, scale=8).generate(filteredWords)
        fig = plt.figure(figsize=(10, 10), dpi=1600)
        plt.imshow(myTopicCloud)
        plt.axis("off")
        plt.show()
