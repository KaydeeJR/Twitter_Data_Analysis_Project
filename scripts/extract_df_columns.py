import pandas as pd
from re import sub

class ExtractDFColumns:
    """
    Extracts relevant columns from a Pandas DataFrame and cleans up columns.

    This class can be used to extract a subset of columns from a Pandas DataFrame. 
    It is useful for reducing the size of a DataFrame or for selecting only the columns
    that are relevant to a particular analysis.

    :param file_path: A path  DataFrame
    """

    def __init__(self,data_file_path):
        self.tweets_df = pd.read_json(data_file_path, lines=True)


    def fetch_hashtags(self):
        """
        Extracts hashtags from a Pandas DataFrame containing Twitter data.

        :param tweets_df: A Pandas DataFrame containing Twitter data.

        :return: A list of unique hashtags.
        """
        hashtags=[]
        try:
            entities_data = pd.DataFrame(self.tweets_df.entities)
            hashtags.clear()
            for i in entities_data.iterrows():
                row_item = i[1]['entities']['hashtags']
                if len(row_item)>0:
                    hs = row_item[0]['text']
                    if hs not in hashtags:
                        hashtags.append(hs)
        except AttributeError:
            pass
        return hashtags

    def fetch_mentions(self):
        """
        Extracts mentions from a Pandas DataFrame containing Twitter data.

        :param tweets_df: A Pandas DataFrame containing Twitter data.

        :return: A list of unique user names mentioned in the Tweets.
        """
        mentions=[]
        try:
            entities_data = pd.DataFrame(self.tweets_df.entities)
            mentions.clear()
            for i in entities_data.iterrows():
                row_item = i[1]['entities']['user_mentions']
                if len(row_item)>0:
                    ment = row_item[0]['name']
                    if ment not in mentions:
                        mentions.append(ment)
        except AttributeError:
            pass
        
        return mentions
    
    def fetch_tweet_sources(self, row):
        """
        Extracts tweet sources from a Pandas DataFrame containing Twitter data.

        :param row: A DataFrame row containing link sources for Tweets.

        :return: Cleaned sources of Tweets.
        """
        source_link = row['source']
        link_start = source_link.index('\">')
        link_end = source_link.index('</a')
        tweet_source = source_link[link_start:link_end]
        return self.clean_up_sources(tweet_source)       
    
    def clean_up_sources(self, link_sources):
        """
        Cleans text links.

        :param link_sources: Text detailing Twitter data source.

        :return: cleaned text without any punctuation marks
        """
        clean_source = sub('[.:;()/!&-*@$,?^\d+>"]', '', link_sources)        
        return clean_source
    
    def extract_user_names(self, row):
        """
        Extracts user names as a dataframe column
        
        :param row: A DataFrame row that has user name information
        
        :return: User name value to add to the new column called user name
        """
        new_item = row['entities']['user_mentions']
        user_name = ''
        if len(new_item)>0:
            user_name = new_item[0]["name"]
        return user_name