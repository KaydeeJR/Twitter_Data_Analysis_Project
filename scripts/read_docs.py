import logging

import sys
sys.path.append("./utils")

import logger_setup
import pandas as pd
from connect_to_mongo import ConnectToMongo


class ReadDocs:
    """
    Access docs stored in MongoDB, list collections and list databases
    """
    def __init__(self, uri):
        # Connect to MongoDB
        # Atlas Connection string is specified in .env file in project root
        self.connection = ConnectToMongo(uri)
        self.client = self.connection.get_mongo_client()
        # set up logger to output to terminal
        self.logger = logger_setup.logger_console_config(__name__)
    
    def list_databases(self):
        """
        Retrieve a list of databases available in the MongoDB cluster
        
        :return: a list of database names
        
        >>> list_databases()
        ['sample_airbnb', 'sample_analytics', 'admin', 'local'] 
        """
        db_list = []
        if self.connection.test_connection():
            db_list = self.client.list_database_names()
        return db_list
    
    def list_collections(self, db_name: str):
        """
        Retrieve a list of collections available in a specific database

        :param db_name: The name of the database
        
        :return: a list of collection names
        
        >>> list_collections('sample_airbnb')
        ['listingsAndReviews']
        """
        collections_list = []
        if self.connection.test_connection():
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
    
    def read_tweets_in_collection(self, database_name:str, collection_name:str):
        """
        Pull Tweets as Documents from MongoDB and store them in a dataframe
        
        :param database_name: The name of the database to read from
        :param collection_name: The name of the collection to read from
        
        :return: dataframe containing tweets
        
        >>> read_tweets_in_collection(database_name="tweets", collection_name="global")
        df
        """
        database = self.client[database_name]
        collection = database[collection_name]
        collection_docs = collection.find()
        results_as_dataframe = pd.DataFrame(collection_docs)
        return results_as_dataframe