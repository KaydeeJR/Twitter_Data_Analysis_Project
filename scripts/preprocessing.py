from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.tag import pos_tag

from re import sub  # regular expressions package
import pandas as pd

class TweetsPreprocessing:
    """
    Preprocessing functions to standardize text one word at a time
    """

    def __init__(self):
        # initialize the NLTK module which performs lemmatization on words.
        self.wnl = WordNetLemmatizer()
        self.tokenizer = TweetTokenizer()

    def remove_punctuation(self, text):
        """
        Replaces every occurrence of punctuation marks in a string with an empty string.

        :param text: string input that contains punctuation marks
        :return: text without punctuation marks

        >>> remove_punctuation("RT : I guess #WWIII on its way for #Taiwan https://t.co/oomVltBmKF")
        'RT ankuhdilraaj_ I guess #WWIII on its way for #Taiwan httpstcooomVltBmKF'
        """
        if text is None:
            return text
        else:
            return sub('[.:;()/!&-*@$,?^\d+]', '', text)

    def lemmatize_phrase(self, phrase):
        """
        Uses NLTKs WordNetLemmatizer module to lemmatize words.
        Lemmatization is the process of reducing a word to its base form i.e. lemma. 

        'n' for nouns, 'v' for verbs, 'a' for adjectives, 'r' for adverbs and “s” for satellite adjectives.

        :param phrase: the phrase to be lemmatized
        :return: string containing lemmatized words.

        >>> lemmatize_phrase("The beautiful, green leaves fell from the tree.")
        'The beautiful , green leaf fell from the tree .'
        >>> lemmatize_word("The quickly-moving train sped past the station")
        'The quickly-moving train speed past the station'
        """
        if phrase is None:
            return phrase
        else:
            # phrase is not empty
            parts_of_speech = {'NOUN': 'n', 'VERB': 'v',
                               'ADJ': 'a', 'ADV': 'r', 'ADJ': 's', 'PRON': 'n'}

            text_tokens = self.tokenizer.tokenize(phrase)
            lemmatized_tokens = []

            tags = pos_tag(tokens=text_tokens, tagset='universal', lang="eng")
            for i in range(len(tags)):
                pos = tags[i][1]
                if pos in parts_of_speech:
                    lemma = self.wnl.lemmatize(
                        tags[i][0], parts_of_speech[pos])
                    # add the lemma to the list
                    lemmatized_tokens.append(lemma)
                else:
                    lemmatized_tokens.append(tags[i][0])

            lemmatized_text = ' '.join((lemmatized_tokens))
            return lemmatized_text

    def remove_stopwords(self, phrase):
        """
        Removes stop words from the phrase
        Stop words are words in any language or corpus that occur frequently.
        For some NLP tasks, these words do not provide any additional or valuable information to the text containing them.
        a, they, the, is, an, etc. are usually considered stop words

        :param phrase: the phrase to remove stopwords from
        :return: phrase without stopwords

        >>> remove_stopwords('RT @anku5hdilraaj_: I guess #WWIII on its way for #Taiwan https://t.co/oomVltBmKF')
        'RT @anku5hdilraaj_ : I guess #WWIII way #Taiwan https://t.co/oomVltBmKF'
        """
        if phrase is None:
            return phrase
        else:
            # phrase is not empty
            stopwords_list = stopwords.words('english')
            tokens = self.tokenizer.tokenize(phrase)
            filtered_tokens = [
                token for token in tokens if token not in stopwords_list]
            filtered_text = ' '.join(filtered_tokens)
            return filtered_text

    def remove_non_ascii(self, text):
        """
        Function to remove non-ASCII characters from string input and replace them with an empty string
        Remove extra whitespace at the end of text
        Non-ASCII characters include: ellipses, Symbols, Emojis

        :param text: the phrase to remove ASCII characters from
        :return: string without ASCII characters
        >>> remove_non_ascii('RT @CGMeifangZhang: Unlike what happened after the #Ukraine crisis when…')
        'RT @CGMeifangZhang: Unlike what happened after the #Ukraine crisis when'
        """
        if text is None:
            return text
        else:
            return str(sub(r'[^\x00-\x7F]', '', text.strip()))

    def remove_link_mentions(self, text):
        """        
        Removes web addresses and twitter handles from Tweets

        :param text: the phrase to remove stopwords from
        :return: phrase without links and @mentions

        >>> remove_link_mentions("RT @anku5hdilraaj_: I guess #WWIII on its way for #Taiwan https://t.co/oomVltBmKF")
        'RT I guess #WWIII on its way for #Taiwan'
        """
        words_list = [word for word in text.split(
        ) if word is not None and not word.startswith('@') and not word.startswith('https') and not word.startswith('http')]
        phrase = " ".join(words_list)
        return phrase

    def preprocessing_pipeline(self, text):
        """
        Final text pre-processing function which combines all the above methods.
        There are 5 methods used to preprocess tweets:
        1. remove links and mentions
        2. remove punctuation - this does not include ellipses for long texts
        3. remove non-ascii characters - includes ellipses for long texts
        4. lemmatize words
        5. remove stopwords

        :param text: text to preprocess
        :return: processed text

        >>> preprocessing_pipeline('RT @CGMeifangZhang: #Latest When the PLA conducted massive drills around #Taiwan in response to the serious provocations made by the US on…')
        'rt #latest pla conduct massive drill around #taiwan response serious provocation make u'
        """
        return self.remove_stopwords(self.lemmatize_phrase(self.remove_non_ascii(self.remove_punctuation(self.remove_link_mentions(text.lower())))))

    def preprocess_tweets_df(self, dataframe, tweets_col):
        """
        Performs preprocessing on all tweets in a dataframe column

        :param dataframe: dataframe containing tweets data
        :param part_of_speech: which part of speech to lemmatize.
        :param tweets_col: column containing tweets text

        :return: list of words
        >>> preprocess_tweets_df(tweets_df, "full_text", 'n')
        []
        """
        return [[self.preprocessing_pipeline(word) for word in row[tweets_col].split() if word is not None]
                for index, row in dataframe.iterrows()]
        # for index, row in :
        #     words_list.append(self.preprocessing_pipeline(row[tweets_col], 'n'))
        # return words_list