import discord
from discord.ext import commands

from dao.mods_dao import ModsDAO

from utils.logger import logger

class Mods(commands.Cog, name='Mods'):
    def __init__(self, wattsyClient):
        self.wattsyClient = wattsyClient
        self.modsDAO = ModsDAO()

        logger.info("Mods Cog loaded")
        

async def setup(wattsyClient):
    await wattsyClient.add_cog(Mods(wattsyClient))