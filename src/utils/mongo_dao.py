import os
from dotenv import load_dotenv

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

load_dotenv()

class MongoDAO():
    def __init__(self):
        try:
            self.client = MongoClient(
                host=os.getenv('MONGODB_HOST'),
                username=os.getenv('MONGODB_USER'),
                password=os.getenv('MONGODB_PASSWORD'),
                authSource=os.getenv('MONGODB_AUTH_DB')
            )
            
            self.client.admin.command('ping')
            print("INFO: Successfully connected to MongoDB")

            # Access the specific database
            self.database = self.client[os.getenv('MONGODB_DB')]
        except ConnectionFailure as e:
            print(f"Error connecting to MongoDB: {e}")
            self.client = None
            self.database = None

    def get_collection(self, collection_name):
        if self.database:
            return self.database[collection_name]
        else:
            raise ConnectionError("No available MongoDB connection.")

    def close_connection(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")

# Create a singleton instance of Database for use in other modules
mongo_instance = MongoDAO()