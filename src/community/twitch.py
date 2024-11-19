from discord.ext import commands

from fastapi import FastAPI, Header, HTTPException, Request
import hmac
import hashlib
import uvicorn

from utils.config import config
from utils.mongo_dao import mongo_instance
from utils.logger import Logger

class Twitch(commands.Cog, name="twitch"):
    def __init__(self, wattsyClient):
        self.wattsyClient = wattsyClient
        self.app = FastAPI()
        self.logger = Logger(__name__).getLogger()

        self.twitch_collection = mongo_instance.get_collection("twitch_subscription")
        self.twitch_signature = config.twitch_signature
        self.logger.info("Twich Cog loaded")
    
    def start_webhook(self):
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
    
    def verify_signature(self, body, headers):
        twitch_signature_header = headers.get("Twitch-Eventsub-Message-Signature")
        message_id = headers.get("Twitch-Eventsub-Message-Id")
        timestamp = headers.get("Twitch-Eventsub-Message-Timestamp")

        if not twitch_signature_header or not message_id or not timestamp:
            return False

        # Construct the HMAC message
        message = message_id + timestamp + body.decode()
        computed_hmac = hmac.new(self.twitch_signature.encode(), message.encode(), hashlib.sha256).hexdigest()
        expected_signature = f"sha256={computed_hmac}"

        # Use a timing-safe comparison to verify the signature
        return hmac.compare_digest(twitch_signature_header, expected_signature)

    @app.post("/twitch")
    async def twitch_webhook(self, request : Request, headers : str = Header(None)):
        body = await request.body()

        if not self.verify_signature(body, headers):
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

async def setup(wattsyClient):
    await wattsyClient.add_cog(Twitch(wattsyClient))