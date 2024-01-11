import os
import logging
from dotenv import load_dotenv

import discord
from discord.ext import commands

from youtube import Youtube

load_dotenv()
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

wattsyClient = commands.Bot(command_prefix='>', intents=intents)

async def load_cog():
    logging.info('Loading youtube Cog')
    await wattsyClient.add_cog(Youtube(wattsyClient))

@wattsyClient.event
async def on_ready():
    logging.info('Logged in as ' + wattsyClient.user.name)
    await load_cog()


wattsyClient.run(os.getenv('DISCORD_TOKEN'))