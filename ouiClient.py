import os
import logging
from dotenv import load_dotenv

import discord

load_dotenv()
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

ouiClient = discord.Bot()

@ouiClient.event
async def on_ready():
    logging.info('Logged in as ' + ouiClient.user.name)

ouiClient.run(os.getenv("OUI_DISCORD_TOKEN"))