import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

from googleapiclient.discovery import build

load_dotenv()

class Youtube(commands.Cog, name='Youtube'):
    def __init__(self, wattsyClient):
        self.wattsyClient = wattsyClient
        self.queue = {}
        self.api_key = os.getenv('YOUTUBE_API_KEY')
    
    def search(self, query):
        request = self.youtube.search().list(
            part='id,snippet',
            q=query,
            maxResults=5,
            type='video'
        )
        response = request.execute()

    @commands.command()
    async def play(self, ctx):
        voiceChannel = ctx.author.voice.channel

        if(voiceChannel is None):
            await ctx.send('You are not in a voice channel')
            return
        
        serverQueue = self.queue["guild_id"]
        if serverQueue:
            if(voiceChannel != serverQueue['voiceChannel']):
                await ctx.send("Wattsy is already playing music in another channel")
                return
        else:
            queue_construct = {
                "messageChannel": None,
                "voiceChannel": None,
                "connection": None,
                "songs": None,
                "volume": 1 
            }

    async def playMusic(self, guild_id):
        serverQueue = self.queue["guild_id"]
        voiceChannel = serverQueue["voiceChannel"]

        if(voiceChannel):
            return