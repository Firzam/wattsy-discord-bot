import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

from yt_dlp import YoutubeDL
from googleapiclient.discovery import build

import re

load_dotenv()

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],

}

ffmepg_opts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
}

soundcloud_regex = (
    r'(https?://)?(www\.)?(soundcloud\.com|snd\.sc)/'
    r'([a-zA-Z0-9._%+-]+/([a-zA-Z0-9._%+-]+))'
)

youtube_regex = (
    r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
    r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

class MusicPlayer(commands.Cog, name='MusicPlayer'):
    def __init__(self, wattsyClient):
        self.wattsyClient = wattsyClient
        self.queue = {}
        self.api_key = os.getenv('YOUTUBE_API_KEY')

        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.youtubeDownloader = YoutubeDL(ydl_opts)
    
    def search(self, query):
        request = self.youtube.search().list(
            part='id,snippet',
            q=query,
            maxResults=1,
            type='video'
        )
        
        response = request.execute()
        song = {
            'url': 'https://www.youtube.com/watch?v=' + response['items'][0]['id']['videoId'],
            'title': response['items'][0]['snippet']['title'],
            'thumbnail': response['items'][0]['snippet']['thumbnails']['default']
        }

        return song
    
    def getSongInfo(self, query):
        
        soundcloud_match = re.search(soundcloud_regex, query)
        youtube_match = re.search(youtube_regex, query)

        if soundcloud_match or youtube_match:
            songRawInfo = self.youtubeDownloader.extract_info(query, download=False)
        else:
            songRawInfo = self.youtubeDownloader.extract_info(self.search(query), download=False)
        
        
        songInfo ={
            'url': songRawInfo['webpage_url'],
            'title': songRawInfo['title'],
            'thumbnail': songRawInfo['thumbnail'],
            'stream': songRawInfo['url']
        }
        
        songEmbed = discord.Embed(title = songInfo['title'])

        songEmbed.set_author(name='Wattsy')
        songEmbed.set_thumbnail(url=songInfo['thumbnail'])

        songEmbed.add_field(name = 'URL',
                            value = songInfo['url'])

        song = songInfo
        song['embed'] = songEmbed
        return song
        

    @commands.command(name='play')
    async def play(self, ctx, *, arg):
        guild_id = ctx.guild.id

        if(ctx.author.voice is None):
            await ctx.send('You are not in a voice channel')
            return
        else:
            voiceChannel = ctx.author.voice.channel
        
        serverQueue = self.queue.get(guild_id)
        if (serverQueue is not None) and (voiceChannel is not serverQueue['voiceChannel']):
            await ctx.send('Wattsy is already playing music in another channel')
            return
        
        if serverQueue is None:
            queue_construct = {
                'messageChannel': None,
                'messageNotification': None,
                'voiceChannel': None,
                'connection': None,
                'songs': [],
                'volume': 1 
            }

            queue_construct['messageChannel'] = ctx.channel
            queue_construct['voiceChannel'] = voiceChannel

            serverQueue = queue_construct
            self.queue[guild_id] = serverQueue
        
        song = self.getSongInfo(arg)
        serverQueue['songs'].append(song)

        if serverQueue.get('connection') is None:
            serverQueue['connection'] = await serverQueue['voiceChannel'].connect()
            await self.playMusic(ctx)

    async def nextMusic(self, ctx : commands.Context):
        guild_id = ctx.guild.id
        serverQueue = self.queue[guild_id]
        serverQueue['songs'].pop(0)

        await self.playMusic(ctx)

    async def playMusic(self, ctx : commands.Context):
        guild_id = ctx.guild.id
        serverQueue = self.queue.get(guild_id)
        connection = serverQueue.get('connection')

        if len(serverQueue['songs']) == 0:
            del self.queue[guild_id]
            await ctx.send('Disconnecting')
            await connection.disconnect()
            return
        
        player = discord.FFmpegPCMAudio(serverQueue['songs'][0]['stream'], **ffmepg_opts)

        try:
            if serverQueue['messageNotificaiton'] is not None:
                serverQueue['messageNotificaiton'].edit(embed = serverQueue['songs'][0]['embed'])
            else:
                serverQueue['messageNotificaiton'] = await ctx.send(embed = serverQueue['songs'][0]['embed'])
            connection.play(player
                            , after=lambda: self.wattsyClient.loop.create_task(self.nextMusic(ctx))
                            , signal_type='music')
        except Exception as e:
            print(e)
            del self.queue[guild_id]
            await ctx.send('An error happen while trying to listen to: ' + serverQueue['songs'][0]['title'])
            await connection.disconnect()
    
async def setup(wattsyClient):
    await wattsyClient.add_cog(MusicPlayer(wattsyClient))