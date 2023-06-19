from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import logging

import sys
sys.path.append("./utils")

import logger_setup

class ConnectToMongo:
    """
    Connects to MongoDB server using Mongo client
    Test connection, list collections and list databases
    
    Visit https://www.mongodb.com/docs/atlas/tutorial/connect-to-your-cluster/
    for more details on how to connect to a cluster.
    """
    def __init__(self, uri):
        # Create a client to connect to the Mongo DB server
        # Atlas Connection string is specified in .env file in project root
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        # set up logger to output to terminal
        self.logger = logger_setup.logger_console_config(__name__)
    
    def get_mongo_client(self):
        """
        Fetch mongoDB client object        
        
        :return: mongo client object
        
        >>> get_mongo_client()
        client
        """
        return self.client
    

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
