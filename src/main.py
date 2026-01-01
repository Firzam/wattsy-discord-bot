import discord
from discord.ext import commands

from utils.config import config
from utils.logger import logger

intents = config.setIntents()

wattsyClient = commands.Bot(command_prefix='>', intents=intents)
wattsyVersion = config.wattsyVersion

async def load_cog():
    logger.info('Loading Cogs')
    # await wattsyClient.load_extension('cogs.casino')
    # await wattsyClient.load_extension('cogs.mods')
    await wattsyClient.load_extension('cogs.musicplayer')
    # await wattsyClient.load_extension('cogs.twitch')
    await wattsyClient.load_extension('controllers.twitch_controller')

@wattsyClient.command
async def version(ctx : commands.Context):
    await ctx.send(f'This bot is using Wattsy version {wattsyVersion}')

@wattsyClient.event
async def on_ready():
    logger.info('Logged in as ' + wattsyClient.user.name)
    logger.info(f'Start Wattsy version {wattsyVersion}')
    await load_cog()


wattsyClient.run(config.wattsyToken)