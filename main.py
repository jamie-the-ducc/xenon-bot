# [Xe]non Bot for Discord
# Written with 💜 by [Jam!3]#4466
# Began: 15/02/2022
# Last updated: 26/02/2022

# ----------------------------------------------- #
#  ____  __   __                                  #
# | _\ \/ /__|_ |_ __   ___  _ __    _ __  _   _  #
# | | \  // _ \ | '_ \ / _ \| '_ \  | '_ \| | | | #
# | | /  \  __/ | | | | (_) | | | |_| |_) | |_| | #
# | |/_/\_\___| |_| |_|\___/|_| |_(_) .__/ \__, | #
# |__|       |__|    version 0.2    |_|    |___/  #
# ----------------------------------------------- #

import os
from asyncio import sleep

import aiohttp
import discord
import discord.errors
from colorama import Fore, Style
from discord.ext import commands
from discord.ext.tasks import loop

from app.__version__ import __version__

from app.func import get_time, read_config, title

w = Style.BRIGHT + Fore.WHITE
GOOD = f" {w}[{Fore.GREEN}+{w}]"
BAD = f" {w}[{Fore.RED}x{w}]"
INFO = f" {w}[{Fore.BLUE}>{w}]"
INPUT = f" {w}[{Fore.YELLOW}-{w}]"
BOT_OWNER = "[Jam!3]#4466"

title()

activities = [ # unused
    "the birds sing 💛",
    "the trees sway 💚",
    "the fire crackle ❤️",
    "the wind whisper 💜",
    "the rain fall 💙",
]

prefix, token, webhook, owner, activities, status_delay = [i[1] for i in read_config(init=True)]
activities = activities.split(',')

# source: https://discordpy.readthedocs.io/en/stable/intents.html
intents = discord.Intents.default()
intents.reactions = True
intents.presences = True
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix=prefix,
    intents=intents,
    activity=discord.Activity(type=discord.ActivityType.listening, name=activities[-1]),
    status=discord.Status.idle,
    owner_id=owner,
)


# Cogs
@bot.command()
async def unload(ctx:commands.Context, extension):
    bot.unload_extension(f'cogs.{extension}')


@bot.command()
async def load(ctx:commands.Context, extension):
    bot.load_extension(f'cogs.{extension}')


# Status changer loop
@loop(seconds=status_delay)
async def status_change():
    for id, _ in enumerate(activities):
        await sleep(status_delay)
        activity = activities[id]
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name=activity), 
            status=discord.Status.idle
        )
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Status changed to {Fore.YELLOW}Listening to {activity}{w}")


status_change.start()


# Cog loader
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# Run the bot
try:
    bot.run(token, reconnect=True)
except discord.errors.LoginFailure:
    print(f"{BAD} Improper token passed ({Fore.YELLOW}config.ini{w})")
except aiohttp.bot_exceptions.botConnectorError:
    print(f"{BAD} Failed to connect to {Fore.YELLOW}discord.com{w} (try again later)")
