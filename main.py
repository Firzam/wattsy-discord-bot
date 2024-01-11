import os
import logging
from dotenv import load_dotenv

import discord

load_dotenv()
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

wattsyClient = discord.Bot()

@tasks.loop(hours=1)
async def capture_pokemon():
    channel_to_capture_pokemon = wattsyClient.get_channel("995709716598624367")
    wattsyClient.send("$p")

@wattsyClient.event
async def on_ready():
    logging.info('Logged in as ' + wattsyClient.user.name)

capture_pokemon.start()
wattsyClient.run(os.getenv("OUI_DISCORD_TOKEN"))