from discord.ext import commands

from controllers.twitch_controller import TwitchController

from utils.config import config
from utils.mongo_dao import mongo_instance
from utils.logger import logger

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
    
    async def on_trigger(self, request):
        data = await request.json()
        broadcaster_id = data["condition"]["broadcaster_id"]
        event_type = data["subscription"]["type"]

        guild_id, channel_id = self.get_guild_and_channel(broadcaster_id)

        # Send a message on Discord depending on the event type
        if event_type == "stream.online":
            await self.send_discord_message("A live stream has started on Twitch!")
        elif event_type == "clip.create":
            await self.send_discord_message(f"A new clip was created! Watch it here: {data['event']['url']}")

async def setup(wattsyClient):
    await wattsyClient.add_cog(Twitch(wattsyClient))