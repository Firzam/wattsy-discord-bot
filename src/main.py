import os
from dotenv import load_dotenv

from utils.logger import logger

import discord
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.moderation = True

wattsyClient = commands.Bot(command_prefix='>', intents=intents)
wattsyVersion = os.getenv('WATTSY_VERSION')

async def load_cog():
    logger.info('Loading Cogs')
    await wattsyClient.load_extension('mods')
    await wattsyClient.load_extension('musicplayer')
    await wattsyClient.load_extension('community.twitch')

@wattsyClient.command
async def version(ctx : commands.Context):
    await ctx.send(f'This bot is using Wattsy version {wattsyVersion}')

@wattsyClient.event
async def on_ready():
    logger.info('Logged in as ' + wattsyClient.user.name)
    logger.info(f'Start Wattsy version {wattsyVersion}')
    await load_cog()


wattsyClient.run(os.getenv('DISCORD_TOKEN'))