import discord
from discord.ext import commands

from DAO.mods_dao import ModsDAO

class Mods(commands.Cog, name='Mods'):
    def __init__(self, wattsyClient):
        self.wattsyClient = wattsyClient
        self.modsDAO = ModsDAO()
        

async def setup(wattsyClient):
    await wattsyClient.add_cog(Mods(wattsyClient))