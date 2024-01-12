import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

import youtube_dl
from googleapiclient.discovery import build

load_dotenv()

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

class Youtube(commands.Cog, name='Youtube'):
    def __init__(self, wattsyClient):
        self.wattsyClient = wattsyClient
        self.queue = {}
        self.api_key = os.getenv('YOUTUBE_API_KEY')

        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.youtubeDownloader = youtube_dl.YoutubeDL(ydl_opts)
    
    def search(self, query):
        request = self.youtube.search().list(
            part='id,snippet',
            q=query,
            maxResults=1,
            type='video'
        )
        
        response = request.execute()
        song = {
            'id': response['items'][0]['id']['videoId'],
            'title': response['items'][0]['snippet']['title'],
            'thumbnail': response['items'][0]['snippet']['thumbnails']['default']
        }

        return song
        

    @commands.command()
    async def play(self, ctx, *, arg):
        voiceChannel = ctx.author.voice.channel
        guild_id = ctx.guild.id

        if(voiceChannel is None):
            await ctx.send('You are not in a voice channel')
            return
        
        serverQueue = self.queue.get(guild_id)
        if (serverQueue is not None) and (voiceChannel is not serverQueue['voiceChannel']):
            await ctx.send('Wattsy is already playing music in another channel')
            return
        
        if serverQueue is None:
            queue_construct = {
                'messageChannel': None,
                'voiceChannel': None,
                'connection': None,
                'songs': [],
                'volume': 1 
            }

            queue_construct['messageChannel'] = ctx.channel
            queue_construct['voiceChannel'] = voiceChannel

            serverQueue = queue_construct
            self.queue[guild_id] = serverQueue
        
        song = self.search(arg)
        serverQueue['songs'].append(song)

        if serverQueue.get('connection') is None:
            serverQueue['connection'] = serverQueue['voiceChannel'].connect()
            await self.playMusic(ctx)

    async def nextMusic(self, ctx):
        guild_id = ctx.guild.id
        serverQueue = self.queue['guild_id']
        serverQueue['songs'].pop(0)

        self.playMusic(ctx)

    async def playMusic(self, ctx):
        guild_id = ctx.guild.id
        serverQueue = self.queue.get(guild_id)
        connection = serverQueue.get('connection')

        if len(serverQueue['songs']) == 0:
            await ctx.send('Disconnecting')
            connection.disconnect()
            self.queue.pop(guild_id)
            return

        song = self.youtubeDownloader.download(['https://www.youtube.com/watch?v=' + serverQueue['songs'][0]['id']])
        connection.play(FFmpegAudio(song), 
                        after=self.nextMusic(ctx))