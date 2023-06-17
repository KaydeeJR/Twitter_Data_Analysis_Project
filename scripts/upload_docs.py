from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from dotenv import load_dotenv

import os
import logging

import sys
sys.path.append("./utils")

import logger_setup
import pandas as pd

class UploadDocs:
    """
    Connects to MongoDB server using client
    Uploads tweets to the cluster
    
    Visit https://www.mongodb.com/docs/atlas/tutorial/connect-to-your-cluster/
    for more details on how to connect to a cluster.
    """
    def __init__(self, uri):
        # Create a client to connect to the Mongo DB server
        # Atlas Connection string is specified in .env file in project root
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        # set up logger to output to terminal
        self.logger = logger_setup.logger_console_config(__name__)
    
    def test_connection(self):
        """
        Send a ping to confirm a successful connection to Mongo cluster                
        
        :return: True if connection is successful and False otherwise
        
        >>> test_connection()
        True
        """
        try:
            self.client.admin.command('ping')
            return True
        except Exception as exception:
            self.logger.exception(exception)
        return False
    
    def list_collections(self, db_name: str):
        """
        Retrieve a list of collections available in a specific database

        :param db_name: The name of the database
        
        :return: a list of collection names
        
        >>> list_collections('sample_airbnb')
        ['listingsAndReviews']
        """
        collections_list = []
        if self.test_connection():
            # confirm cluster connection
            databases = self.list_databases()
            if db_name in databases:
                # confirm database exists
                db_object = self.client[db_name]
                collections_list = db_object.list_collection_names()
            else:
                # database does not exist
                self.logger.setLevel(logging.DEBUG)
                self.logger.error("Database does not exist")
        else:
            # no connection
            self.logger.setLevel(logging.DEBUG)
            self.logger.error("Cannot connect to cluster!!!")
        
        return collections_list

    def list_databases(self):
        """
        Retrieve a list of databases available in the MongoDB cluster
        
        :return: a list of database names
        
        >>> list_databases()
        ['sample_airbnb', 'sample_analytics', 'admin', 'local'] 
        """
        db_list = []
        if self.test_connection():
            db_list = self.client.list_database_names()
        return db_list

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
        if self.test_connection():
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
