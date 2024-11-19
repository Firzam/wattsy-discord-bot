import hmac
import hashlib
import uvicorn
from fastapi import FastAPI, Header, HTTPException, Request

from cogs.twitch import Twitch

from utils.config import config
from utils.logger import Logger

class TwitchController():
    def __init__(self, twitch_cog : Twitch):
        self.twitch_cog = twitch_cog
        self.logger = Logger(__name__).getLogger()

        self.app = FastAPI()
        self.twitch_signature = config.twitch_signature
        self.start_webhook()
    
    def start_webhook(self):
        uvicorn.run(self.app, host="0.0.0.0", port=80)

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

        self.twitch_cog.on_trigger()

        return {"status": "ok"}