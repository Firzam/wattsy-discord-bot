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
wattsyVersion = os.getenv('WATTSY_VERSION')

async def load_cog():
    logging.info('Loading youtube Cog')
    await wattsyClient.add_cog(Youtube(wattsyClient))

@wattsyClient.command
async def version(ctx):
    await ctx.send(f'This bot is using Wattsy version {wattsyVersion}')

@wattsyClient.event
async def on_ready():
    logging.info('Logged in as ' + wattsyClient.user.name)
    logging.info(f'Start Wattsy version {wattsyVersion}')
    await load_cog()


wattsyClient.run(os.getenv('DISCORD_TOKEN'))