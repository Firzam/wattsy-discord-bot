from discord.ext import commands

from utils.logger import logger
from utils.sqlite_dao import sqlite_instance

class Casino(commands.Cog, name='Casino'):
    def __init__(self, wattsyClient):
        self.wattsyClient = wattsyClient
        self.con = sqlite_instance.get_connection()
        logger.info("Casino Cog loaded")

    async def on_voice_state_update(self, member, before, afte):
        user = member.id

        self.con.

async def setup(wattsyClient):
    await wattsyClient.add_cog(Mods(wattsyClient))