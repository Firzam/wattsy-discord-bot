import os
import logging
from dotenv import load_dotenv

import discord

load_dotenv()
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

wattsyClient = discord.Bot()

@wattsyClient.event
async def on_ready():
    logging.info('Logged in as ' + wattsyClient.user.name)

wattsyClient.run(os.getenv("OUI_DISCORD_TOKEN"))