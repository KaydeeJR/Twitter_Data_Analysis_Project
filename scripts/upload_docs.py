import logging

import sys
sys.path.append("./utils")

import logger_setup
from connect_to_mongo import ConnectToMongo
import pandas as pd

class UploadDocs:
    """
    Uploads tweets to the cluster
    """
    def __init__(self):
        # Set up connection to MongoDB
        # Atlas Connection string is specified in .env file in project root
        self.connection = ConnectToMongo(uri)
        self.client = self.connection.get_mongo_client()
        # set up logger to output to terminal
        self.logger = logger_setup.logger_console_config(__name__)
    
    def upload_tweets(self, file_path:str, db_name:str, collection_name:str):
        """
        Upload Tweets as Documents to MongoDB. Tweets are stored in a JSON file in local storage

        An insertedIds array contains _id values for each successfully inserted document 
        
        :param file_path: The path to JSON file containing tweets
        :param db_name: The name of the database
        :param collection_name: The name of the collection
        
        :return: The number of tweets successfuly uploaded
        
        >>> upload_tweets(file_path=".\\data\\global_twitter_data.json",db_name="tweets",collection_name="global")
        21999
        """
        tweets_uploaded = 0
        if self.connection.test_connection():
            # confirm connection to cluster
            database = self.client[db_name]
            collection = database[collection_name]
            # access tweets from JSON file using pandas read_json()
            df = pd.read_json(file_path, lines=True)
            for index, row in df.iterrows():
                # specifying an _id field to avoid MongoDB from assigning unique ids for each document
                tweet_dict = {"_id":row["id"]}
                # removing the id columns to avoid repetition
                del row["id"]
                del row["id_str"]
                # add the current json data to the original dictionary
                tweet_dict.update(row)
                try:
                    # upload the combined dictionary and return a document              
                    tweet_doc = collection.insert_one(tweet_dict)
                    if tweet_doc.inserted_id is not None:
                        tweets_uploaded += 1
                except:
                    #  pymongo.errors.DuplicateKeyError
                    self.logger.setLevel(logging.DEBUG)
                    self.logger.error("Duplicate Document Key Error!!!")
        else:
            # no connection
            self.logger.setLevel(logging.DEBUG)
            self.logger.error("Cannot connect to cluster!!!")
        
        return tweets_uploaded
