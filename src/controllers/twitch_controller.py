import hmac
import hashlib
import uvicorn
from fastapi import FastAPI, Header, HTTPException, Request

from utils.config import config
from utils.logger import logger



class TwitchController():
    def __init__(self, twitch_cog):
        self.twitch_cog = twitch_cog
        

        self.app = FastAPI()
        self.twitch_signature = config.twitch_signature

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
    
    def setup_route(self):
        @self.app.post("/twitch")
        async def twitch_webhook(self, request : Request, headers : str = Header(None)):
            body = await request.body()

            if not self.verify_signature(body, headers):
                raise HTTPException(status_code=403, detail="Invalid signature")

            await self.twitch_cog.on_trigger(body)

            return {"status": "ok"}