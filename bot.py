# [Xe]non Bot for Discord
# Written with 💜 by [Jam!3]#4466
# Began: 15/02/2022

# ----------------------------------------------- #
#  ____  __   __                                  #
# | _\ \/ /__|_ |_ __   ___  _ __    _ __  _   _  #
# | | \  // _ \ | '_ \ / _ \| '_ \  | '_ \| | | | #
# | | /  \  __/ | | | | (_) | | | |_| |_) | |_| | #
# | |/_/\_\___| |_| |_|\___/|_| |_(_) .__/ \__, | #
# |__|       |__|    version 0.1    |_|    |___/  #
# ----------------------------------------------- #

import json
from asyncio import sleep
from pathlib import Path

import aiohttp
import discord
import discord.errors
from colorama import Back, Fore, Style
from discord.ext import commands
from discord.ext.tasks import loop

from app.__version__ import __version__
from app.func import get_time, read_config, title, display_bot_info, reply_dict

w = Style.BRIGHT + Fore.WHITE
GOOD = f" {w}[{Fore.GREEN}+{w}]"
BAD = f" {w}[{Fore.RED}x{w}]"
INFO = f" {w}[{Fore.BLUE}>{w}]"
INPUT = f" {w}[{Fore.YELLOW}-{w}]"
BOT_OWNER = "[Jam!3]#4466"
GUILDS_JSON = Path.cwd() / "app" / "guilds.json"

title()

activities = [ # unused
    "the birds sing 💛",
    "the trees sway 💚",
    "the fire crackle ❤️",
    "the wind whisper 💜",
    "the rain fall 💙",
]

prefix, token, webhook, owner, activities, status_delay = [i[1] for i in read_config()]
activities = activities.split(',')

intents = discord.Intents.all()

client = commands.Bot(
    command_prefix=prefix,
    intents=intents,
    activity=discord.Activity(type=discord.ActivityType.listening, name=activities[-1]),
    status=discord.Status.idle,
)


# ON READY
@client.event
async def on_ready():
    print(display_bot_info(client, prefix, activities))


@client.event
async def on_message(message):
    await client.process_commands(message)
    name = message.content
    msg = name.removeprefix(prefix)
    if msg in reply_dict and message.author is not client.user:
        await message.reply(reply_dict[msg])
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{name}{w} in {Fore.YELLOW}#{message.channel}{w} from {Fore.YELLOW}{message.author} {w}({Style.DIM}{message.author.id}{Style.RESET_ALL}{w})")


# ON MEMBER JOIN
@client.event
async def on_member_join(member):
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Welcome! {Fore.YELLOW}{member}{w} has {Fore.GREEN}joined{w} the server.")
    with open(GUILDS_JSON, "r", encoding="utf-8") as f:
        guilds_dict = json.load(f)

    channel_id = guilds_dict[str(member.guild.id)]
    await client.get_channel(int(channel_id)).send(f"{member.mention} welcome to the server! Enjoy your stay! 💜")


# ON MEMBER REMOVE
@client.event
async def on_member_remove(member):
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Goodbye! {Fore.YELLOW}{member}{w} has {Fore.RED}left{w} the server.")


# ON GULD JOIN
@client.event
async def on_guild_join(guild):
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Bot {Fore.GREEN}added{w} to server {Fore.YELLOW}{guild}{w}.")


# ON GUILD REMOVE
@client.event
async def on_guild_remove(guild):
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Bot {Fore.RED}removed{w} from server {Fore.YELLOW}{guild}{w}.")
    with open(GUILDS_JSON, "r", encoding="utf-8") as f:
        guilds_dict = json.load(f)

    guilds_dict.pop(guild.id)
    with open(GUILDS_JSON, "w", encoding="utf-8") as f:
        json.dump(guilds_dict, f, indent=4, ensure_ascii=False)


# SET WELCOME CHANNEL
@client.command(name="welcome")
async def set_welcome_channel(ctx, channel:discord.TextChannel=None):
    if channel == None:
        await ctx.reply(f"> Missing argument! Proper usage: `{prefix}welcome <#channel>`")
    else:
        name = "welcome #" + channel.name
        with open(GUILDS_JSON, "r", encoding="utf-8") as f:
            guilds_dict = json.load(f)

        guilds_dict[str(ctx.guild.id)] = str(channel.id)
        with open(GUILDS_JSON, "w", encoding="utf-8") as f:
            json.dump(guilds_dict, f, indent=4, ensure_ascii=False)

        await ctx.reply(f"> Set welcome channel for `{ctx.message.guild.name}` to <#{channel.id}>")
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
        print(" " * 12 + f"{Fore.CYAN}└>{w} Set welcome channel to {Fore.YELLOW}{channel.name}{w} ({Style.DIM}{channel.id}{Style.RESET_ALL}{w})")


# CLIENT COMMANDS
@client.command(name="hello")  # x.hello
async def hello(ctx: commands.Context):
    name = "hello"
    await ctx.reply(f"> Hello, {ctx.author.display_name}!")
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")


@client.command(name="ping")  # x.ping
async def ping(ctx:commands.Context):
    name = "ping"
    ping = int(round(client.latency, 3) * 1000)
    await ctx.reply(f"> Pong! {ping}ms")
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
    print(" " * 12 + f"{Fore.CYAN}└>{w} Bot latency is {Fore.YELLOW}{ping}ms{w}")


@client.command(name="avatar")  # x.avatar
async def avatar(ctx:commands.Context, user:discord.Member=None):
    if user == None:
        user = ctx.author
    name = f"avatar {user}"
    await ctx.reply(f"> <@!{user.id}>'s avatar:\n> {user.avatar.url}")
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
# END OF CLIENT COMMANDS


# STATUS CHANGE LOOP
@loop(seconds=status_delay)
async def status_change():
    for id, _ in enumerate(activities):
        await sleep(status_delay)
        activity = activities[id]
        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name=activity), 
            status=discord.Status.idle
        )
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Status changed to {Fore.YELLOW}Listening to {activity}{w}")


status_change.start()

try:
    client.run(token, reconnect=True)
except discord.errors.LoginFailure:
    print(f"{BAD} Improper token passed ({Fore.YELLOW}config.ini{w})")
except aiohttp.client_exceptions.ClientConnectorError:
    print(f"{BAD} Failed to connect to {Fore.YELLOW}discord.com{w} (try again later)")
