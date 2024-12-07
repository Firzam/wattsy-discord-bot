import os
from dotenv import load_dotenv

import discord
from enum import Enum

from utils.logger import logger

import requests

load_dotenv()

class DiscordIntents(Enum):
    MESSAGE_CONTENT = "message_content"
    MODERATION = "moderation"
    VOICE_STATE = "voice_states"

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
        
        self.wattsyVersion = os.getenv('WATTSY_VERSION')
        self.wattsyToken = os.getenv('DISCORD_TOKEN')
    
    def setIntents(self):
        intents = discord.Intents.default()
        for intent in DiscordIntents:
            if hasattr(intents, intent.value):
                setattr(intents, intent.value, True)
            else:
                print(f'Warning: Intent "{intent.value}" is not a valid attribute of discord.Intents')
        return intents

config = Config()

from utils.mongo_dao import mongo_instance

class TwichConfig():
    def __init__(self):
        self.twitch_clientId = os.getenv("TWITCH_CLIENT_ID")
        self.twitch_clientSecret = os.getenv("TWITCH_CLIENT_SECRET")
        self.twitch_signature = os.getenv("TWITCH_SIGNATURE")
        
        self.config_collection = mongo_instance.get_collection('config')

    def getNewToken(self):
        refresh_url = 'https://id.twitch.tv/oauth2/token'
        refresh_headers = {
            'client_id': self.twitch_clientId,
            'client_secret': self.twitch_clientSecret,
            'grant_type': 'client_credentials'
        }

        refresh_token = requests.post(refresh_url, headers=refresh_headers)
        refresh_token_response = refresh_token.json()

        new_token = refresh_token_response['access_token']

        config_builder = {
            '_id': 'twitch_token',
            'access_token': new_token
        }

        self.config_collection.replace_one({'_id': 'twitch_token'}, config_builder)

        logger.info('Twitch API Token has been refresh')

        return new_token

    def getTwitchToken(self):
        if self.twitch_access_token  is not None:
            validate_url = 'https://id.twitch.tv/oauth2/token'
            validate_headers = {'Authorization': f'Bearer {self.twitch_access_token }'}
            response = requests.get(validate_url, headers=validate_headers)

            status_code = response.status_code
            client_id = response.json()['client_id']

            if status_code == 200 & client_id == self.twitch_clientId:
                return self.twitch_access_token 
            elif status_code == 401:
                logger.warning('Twitch API Token is no longer valid.')
                return self.getNewToken()
        else:
            self.twitch_access_token  = self.config_collection.find_one({'_id': 'twitch_token'})['access_token']
            return self.getTwitchToken()

twitchConfig = TwichConfig()