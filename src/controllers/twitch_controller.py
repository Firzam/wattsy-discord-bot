from discord.ext import commands, tasks

from flask import Flask, abort, request
import hmac
import hashlib

from utils.config import config, twitchConfig
from utils.logger import logger

class TwitchController(commands.Cog, name="twitch_controller"):
    def __init__(self, wattsyClient : commands.Bot):
        self.wattsyClient = wattsyClient
        self.twitch_cog = wattsyClient.get_cog('twitch')

        self.twitch_signature = twitchConfig.twitch_signature

        self.app = Flask(__name__)

        @self.app.route('/version')
        def version():
            return {"version": config.wattsyVersion}

        @self.app.route('/twitch', methods=['POST'])
        async def twitch_webhook():
            headers = request.headers
            body = request.get_json()

            if not self.verify_signature(body, headers):
                logger.warning("\"/twitch\" endpoint was called with the wrong signature from " + request.remote_addr)
                abort(403)

            await self.twitch_cog.on_trigger(body)

            return {"status": "ok"}

        self.wattsyClient.loop.create_task(self.startServer())

    def verify_signature(self, body, headers):
        twitch_signature_header = headers.get("Twitch-Eventsub-Message-Signature")
        message_id = headers.get("Twitch-Eventsub-Message-Id")
        timestamp = headers.get("Twitch-Eventsub-Message-Timestamp")

        if not twitch_signature_header or not message_id or not timestamp:
            return False

        message = message_id + timestamp + body.decode()
        computed_hmac = hmac.new(self.twitch_signature.encode(), message.encode(), hashlib.sha256).hexdigest()
        expected_signature = f"sha256={computed_hmac}"

        return hmac.compare_digest(twitch_signature_header, expected_signature)

    @tasks.loop()
    async def start_server(self):
        from waitress import serve
        self.app.logger
        serve(self.app, host='0.0.0.0', port=80)

    @start_server.before_loop
    async def before_start(self):
        await self.wattsyClient.wait_until_ready()

async def setup(wattsyClient):
    await wattsyClient.add_cog(TwitchController(wattsyClient))