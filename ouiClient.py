import os
from dotenv import load_dotenv

import discord

load_dotenv()

ouiClient = discord.Bot()

ouiClient.run(os.getenv("OUI_DISCORD_TOKEN"))