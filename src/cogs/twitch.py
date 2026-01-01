from discord.ext import commands

from utils.config import config, twitchConfig
from utils.mongo_dao import mongo_instance
from utils.logger import logger

import requests

class Twitch(commands.Cog, name="twitch"):
    def __init__(self, wattsyClient):
        self.wattsyClient = wattsyClient
        self.twitch_collection = mongo_instance.get_collection("twitch_subscription")
        logger.info("Twich Cog loaded")

    def get_guild_and_channel(self, broadcaster_id):
        record = self.twitch_collection.find_one({"broadcaster_id": broadcaster_id})
        if record:
            return record['guild_id'], record['channel_id']
        return None, None

    async def send_discord_message(self, guild_id, channel_id, message):
        guild = self.wattsyClient.get_guild(guild_id)
        if guild:
            channel = guild.get_channel(channel_id)
            if channel:
                await channel.send(message)

    async def on_trigger(self, data):
        broadcaster_id = data['condition']['broadcaster_id']
        event_type = data['subscription']['type']

        guild_id, channel_id = self.get_guild_and_channel(broadcaster_id)

        if event_type == "stream.online":
            await self.send_discord_message("A live stream has started on Twitch!")
        elif event_type == "clip.create":
            await self.send_discord_message(f"A new clip was created! Watch it here: {data['event']['url']}")

    def getBroadcasterIdByAccountName(self, name: str):
        headers = {
            'Authorization' : 'Bearer ' + twitchConfig.getTwitchToken(),
            'Client-Id': twitchConfig.twitch_clientId
        }
        params = {
            'login': name
        }
        api_url = "https://api.twitch.tv/helix/users"

        response = requests.get(api_url, params=params, headers=headers).json()

        return response['data']['id']

    def checkExistingConfig(self, broadcaster_id):
        if self.twitch_collection.find_one({'_id': broadcaster_id}) is not None:
            self.twitch_collection.delete_one({'_id': broadcaster_id})

    @commands.command(name='twitch')
    async def twitch_command(self, ctx : commands.Context, subCommand, *, name):
        if subCommand == 'set-account':
            broadcaster_id = self.getBroadcasterIdByAccountName(name)
            self.checkExistingConfig(broadcaster_id)
            config_builder = {
                "_id": broadcaster_id,
                "guild_id": ctx.guild.id,
                "channel_id": ctx.channel.id
            }
            self.twitch_collection.insert_one(config_builder).inserted_id()

            await ctx.send(f'Account {name} has been set as a Twitch account to watch for! Notification will be sent to this channel')
        elif subCommand == 'show':
            pass

async def setup(wattsyClient):
    await wattsyClient.add_cog(Twitch(wattsyClient))