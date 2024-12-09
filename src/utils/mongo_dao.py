from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from utils.config import config
from utils.logger import logger

class MongoDAO():
    def __init__(self):
        try:
            self.client = MongoClient(
                host = config.mongo_host,
                username = config.mongo_username,
                password = config.mongo_password
            )
            
            self.client.admin.command('ping')
            logger.info('Successfully connected to MongoDB')

            # Access the specific database
            self.database = self.client[config.mongo_db]
        except ConnectionFailure as e:
            logger.error(f'Error connecting to MongoDB: {e}')
            self.client = None
            self.database = None

    def get_collection(self, collection_name):
        if self.database is not None:
            return self.database[collection_name]
        else:
            raise ConnectionError("No available MongoDB connection.")

    def close_connection(self):
        if self.client:
            self.client.close()
            logger.info('MongoDB connection closed')

# Create a singleton instance of Database for use in other modules
mongo_instance = MongoDAO()