from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

# regular expressions package
from re import sub
import pandas as pd

class TweetsPreprocessing:
    """
    Preprocessing functions to standardize text one word at a time
    """
    def __init__(self):
        # initialize the NLTK module which performs lemmatization on words.
        self.wnl = WordNetLemmatizer()

    def remove_punctuation(self, text):
        """
        Replaces every occurrence of punctuation marks in a string with an empty string.

        :param text: string input that contains punctuation marks
        :return: text without punctuation marks
        
        >>> remove_punctuation("RT @benedictrogers: We must not let this happen.")
        RT benedictrogers We must not let this happen
        """
        if text is None:
            return text
        else:
            return sub('[.:;()/!&-*@$,?^\d+]','', text)

    def lemmatize_word(self, word, part_of_speech):
        """
        Uses NLTKs WordNetLemmatizer module to lemmatize words
        Lemmatization is the process of reducing a word to its base form i.e. lemma. 

        :param word: word to be lemmatized
        :param part_of_speech: 'n' for nouns, 'v' for verbs, 'a' for adjectives, 'r' for adverbs and “s” for satellite adjectives.
        :return: lemmatized word.
        
        >>> lemmatize_word("running",'v')
        run
        """
        if word is None:
            return word
        else:
            return str(self.wnl.lemmatize(word, part_of_speech))

    def remove_stopwords(self, phrase):
        """
        Removes stop words from the phrase
        Stop words are words in any language or corpus that occur frequently.
        For some NLP tasks, these words do not provide any additional or valuable information to the text containing them.
        a, they, the, is, an, etc. are usually considered stop words

        :param phrase: the phrase to remove stopwords from
        :return: phrase without stopwords
        
        >>> remove_stopwords("I am running")
        run
        """
        if phrase is None:
            return phrase
        if phrase not in str(stopwords.words('english')):
            return phrase
    
    def remove_ascii(self, myWord):
        """Function to remove ascii from string input"""
        if myWord is None:
            return myWord
        else:
            return str(sub(r'[^\x00-\x7F]+','', myWord.strip()))

    def remove_link_mentions(self, word):
        """        
        Removes web addresses and twitter handles from Tweets

        :param word: the phrase to remove stopwords from
        :return: phrase without stopwords
        
        >>> remove_link_mentions("RT @anku5hdilraaj_: I guess #WWIII on its way for #Taiwan https://t.co/oomVltBmKF")
        'RT anku5hdilraaj_: I guess #WWIII on its way for #Taiwan https://t.co/oomVltBmKF'
        """
        if not word.startswith('@') or not word.startswith('https'):
            return word

    def preprocessing_pipeline(self, text, part_of_speech):
        """
        Final text pre-processing function which combines all the above methods.
        There are 5 methods used to preprocess tweets
        
        :param text: text to preprocess
        :param part_of_speech: which part of speech to lemmatize.
        
        :return: processed text

        >>> preprocessing_pipeline('RT @anku5hdilraaj_: I guess #WWIII on its way for #Taiwan https://t.co/oomVltBmKF','n')
        'rt ankuhdilraaj_ i guess #wwiii on its way for #taiwan httpstcooomvltbmkf''
        """
        return self.remove_stopwords(self.lemmatize_word(self.remove_ascii(self.remove_punctuation(self.remove_link_mentions(text.lower()))), part_of_speech))
    
    def preprocess_tweets_df(self, dataframe, tweets_col, part_of_speech):
        """
        Perform preprocessing on all tweets in a dataframe column
        
        :param dataframe: dataframe containing tweets data
        :param part_of_speech: which part of speech to lemmatize.
        :param tweets_col: column containing tweets text

        :return: dataframe with processed tweets 
        >>> preprocess_tweets_df(tweets_df[['full_text']])
        df
        """
        df = pd.DataFrame()
        for index, row in dataframe.iterrows():
            df.loc[index, "processed"] = self.preprocessing_pipeline(row[tweets_col], 'n')
        
        return df
        