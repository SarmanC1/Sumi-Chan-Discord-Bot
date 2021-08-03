import discord
from discord.ext import commands
from pretty_help import PrettyHelp, DefaultMenu
import os
from keep_alive import keep_alive

"""
from routes.util import app
from quart import Quart, redirect, url_for, render_template, request

app = Quart(__name__)
async def homePG():
    return "Active Senpai!"
"""

# --Load intents--
intents = discord.Intents.default()
intents.members = True

class SumiChan(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="sc!", description="Nice handy bot that will help around", intents=intents, help_command=None)

bot = SumiChan()

@bot.event
async def on_ready():
    print("Online") # Lets the bot owner know when the bot is ready
    await bot.change_presence(activity = discord.Activity(type=discord.ActivityType.listening, name='Matane!'))
# --Load cogs--
cogs = [
    "moderation",
    "general",
    "help"
]

for cog in cogs:
    bot.load_extension("cogs." + cog)
    print("Loaded: " + cog)

# --Start bot--
bot_token = os.environ.get("TOKEN")
bot.run(bot_token)
