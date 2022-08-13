import json
import pandas as pd
# from textblob import TextBlob

class TweetDfExtractor:
    """
    class with functions that parse tweets json into a pandas dataframe

    Return
    ------
    dataframe
    """

    def __init__(self, tweets_list):
        # class constructor
        self.tweets_list = tweets_list

    def get_columns(self):
        iterable = iter(self.tweets_list)
        tweet_dict = dict(self.tweets_list)
        print(tweet_dict.keys())

    def get_tweet_df(self, save=False) -> pd.DataFrame:
        """generate columns list"""

        columns = ['created_at', 'source', 'original_text', 'polarity', 'subjectivity', 'lang', 'favorite_count', 'retweet_count',
                   'original_author', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags', 'user_mentions', 'place']

        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(text)
        lang = self.find_lang()
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        follower_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        data = zip(created_at, source, text, polarity, subjectivity, lang, fav_count, retweet_count,
                   screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            # if parameter save = true then save dataframe to CSV file
            # where to save?
            fileName = input("Please Enter the Filename: ")
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')

        return df

    # example functions
    """ 
    def find_statuses_count(self) -> list:
        statuses_count

    def find_full_text(self) -> list:
        text =

    def find_sentiments(self, text) -> list:

        return polarity, self.subjectivity

    def find_created_time(self) -> list:

        return created_at

    def find_source(self) -> list:
       source =

       return source

    def find_screen_name(self) -> list:
       screen_name

    def find_followers_count(self) -> list:
        followers_count

    def find_friends_count(self) -> list:
        friends_count

    def is_sensitive(self) -> list:
        try:
            is_sensitive = [x['possibly_sensitive'] for x in self.tweets_list]
        except KeyError:
            is_sensitive = None

        return is_sensitive

    def find_favourite_count(self) -> list:

    def find_retweet_count(self) -> list:
        retweet_count

    def find_hashtags(self) -> list:
        hashtags

    def find_mentions(self) -> list:
        mentions

    def find_location(self) -> list:
        try:
            location = self.tweets_list['user']['location']
        except TypeError:
            location = ''

        return location """


if __name__ == "__main__":
    # main function
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text', 'clean_text', 'sentiment', 'polarity', 'subjectivity', 'lang', 'favorite_count', 'retweet_count',
               'original_author', 'screen_count', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    tweet_df = pd.read_json(
        "D:/10XAcademy/Twitter Data/AfricaTwitterData.json", lines=True)
    print(tweet_df)
    #tweet = TweetDfExtractor(tweet_list)
    # constructor is called
    # tweet.get_columns()
    # tweet_df = tweet.get_tweet_df()

    # use all defined functions to generate a dataframe with the specified columns above
