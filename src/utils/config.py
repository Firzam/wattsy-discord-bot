import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    def __init__(self):
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        
        self.mongo_host = os.getenv('MONGODB_HOST')
        self.mongo_db = os.getenv('MONGODB_DB')
        self.mongo_username = os.getenv('MONGODB_USER')
        self.mongo_password = os.getenv('MONGODB_PASSWORD')

        self.postgre_host = os.getenv('POSTGRES_HOST')
        self.postgres_database = os.getenv('POSTGRES_DB')
        self.postgre_user = os.getenv('POSTGRES_USER')
        self.postgres_password = os.getenv('POSTGRES_PASSWORD')

        self.twitch_clientId = os.getenv("TWITCH_CLIENT_ID")
        self.twitch_clientSecret = os.getenv("TWITCH_CLIENT_SECRET")
        self.twitch_signature = os.getenv("TWITCH_SIGNATURE")
        
        self.wattsyVersion = os.getenv('WATTSY_VERSION')
        self.wattsyToken = os.getenv('DISCORD_TOKEN')

config = Config()