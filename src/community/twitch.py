import os
from dotenv import load_dotenv

from discord.ext import commands

import uvicorn
from fastapi import FastAPI, Header, HTTPException, Request

from ..utils.mongo_dao import mongo_instance

load_dotenv()

class Twitch(commands.Cogs, name="twitch"):
    def __init__(self, wattsyClient):
        self.wattsyClient = wattsyClient
        self.app = FastAPI()

        self.twitch_collection = mongo_instance.get_collection("twitch_subscription")
        self.twitch_signature = os.getenv("TWITCH_SIGNATURE")
    
    def start_webhook():
        uvicorn.run(self.app, host="0.0.0.0", port=80)

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

    @app.post("/twitch")
    async def twitch_webhook(self, request : Request, X_Hub_Signature : str = Header(None)):
        body = await request.body()

        if not self.verify_signature(self.twitch_signature, body, X_Hub_Signature):
            raise HTTPException(status_code=403, detail="Invalid signature")

        data = await request.json()
        broadcaster_id = data["condition"]["broadcaster_id"]
        event_type = data["subscription"]["type"]

        guild_id, channel_id = self.get_guild_and_channel(broadcaster_id)

        # Send a message on Discord depending on the event type
        if event_type == "stream.online":
            await self.send_discord_message("A live stream has started on Twitch!")
        elif event_type == "clip.create":
            await self.send_discord_message(f"A new clip was created! Watch it here: {data['event']['url']}")

        return {"status": "ok"}