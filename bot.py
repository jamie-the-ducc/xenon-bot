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
import sys
from asyncio import sleep
from datetime import timedelta, datetime, timezone
from io import StringIO
from pathlib import Path
from base64 import b64encode, b64decode

import aiohttp
import discord
import discord.errors
from colorama import Back, Fore, Style
from discord.ext import commands
from discord.ext.tasks import loop

from app.__version__ import __version__
from app.func import (display_bot_info, get_time, read_config, reply_dict, reply_dict_noprefix, strip_codeblock, title)

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
    owner_id=owner,
)


# ON READY
@client.event
async def on_ready():
    print(display_bot_info(client, prefix, activities))


@client.event
async def on_message(message:discord.Message):
    await client.process_commands(message)
    name = message.content
    msg = name.removeprefix(prefix)
    # clean up later
    if name.startswith(prefix) and msg in reply_dict and message.author is not client.user:
        await message.reply(reply_dict[msg])
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{name}{w} in {Fore.YELLOW}#{message.channel}{w} from {Fore.YELLOW}{message.author} {w}({Style.DIM}{message.author.id}{Style.RESET_ALL}{w})")
    elif msg in reply_dict_noprefix and message.author is not client.user:
        await message.reply(reply_dict_noprefix[msg])
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{name}{w} in {Fore.YELLOW}#{message.channel}{w} from {Fore.YELLOW}{message.author} {w}({Style.DIM}{message.author.id}{Style.RESET_ALL}{w})")

# ON MEMBER JOIN
@client.event
async def on_member_join(member:discord.Member):
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Welcome! {Fore.YELLOW}{member}{w} ({Style.DIM}{member.id}{Style.RESET_ALL}{w}) has {Fore.GREEN}joined{w} the server.")
    with open(GUILDS_JSON, "r", encoding="utf-8") as f:
        guilds_dict = json.load(f)

    channel_id = guilds_dict[str(member.guild.id)]
    await client.get_channel(int(channel_id)).send(f"{member.mention} welcome to the server! Enjoy your stay! 💜")


# ON MEMBER REMOVE
@client.event
async def on_member_remove(member:discord.Member):
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Goodbye! {Fore.YELLOW}{member}{w} ({Style.DIM}{member.id}{Style.RESET_ALL}{w}) has {Fore.RED}left{w} the server.")


# ON GULD JOIN
@client.event
async def on_guild_join(guild:discord.Guild):
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Bot {Fore.GREEN}added{w} to server {Fore.YELLOW}{guild}{w} ({Style.DIM}{guild.id}{Style.RESET_ALL}{w}).")


# ON GUILD REMOVE
@client.event
async def on_guild_remove(guild:discord.Guild):
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Bot {Fore.RED}removed{w} from server {Fore.YELLOW}{guild}{w} ({Style.DIM}{guild.id}{Style.RESET_ALL}{w}).")
    with open(GUILDS_JSON, "r", encoding="utf-8") as f:
        guilds_dict = json.load(f)

    guilds_dict.pop(guild.id)
    with open(GUILDS_JSON, "w", encoding="utf-8") as f:
        json.dump(guilds_dict, f, indent=4, ensure_ascii=False)


# CLIENT COMMANDS

@client.event
async def on_command_error(ctx, error):
    #if isinstance(error, commands.MissingRequiredArgument):
    #    await ctx.reply('> Please psas in the required arguments')
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("> You don't have sufficient permissions to use this command")


@client.command(name="welcome", aliases=['w', 'setwelcome'])
@commands.has_permissions(administrator=True)
async def set_welcome_channel(ctx, channel:discord.TextChannel=None):
    if channel == None:
        channel = ctx.message.channel
    name = "welcome #" + channel.name
    with open(GUILDS_JSON, "r", encoding="utf-8") as f:
        guilds_dict = json.load(f)

    guilds_dict[str(ctx.guild.id)] = str(channel.id)
    with open(GUILDS_JSON, "w", encoding="utf-8") as f:
        json.dump(guilds_dict, f, indent=4, ensure_ascii=False)

    await ctx.reply(f"> Set welcome channel for `{ctx.message.guild.name}` to {channel.mention}")
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
    print(" " * 12 + f"{Fore.CYAN}└>{w} Set welcome channel to {Fore.YELLOW}{channel.name}{w} ({Style.DIM}{channel.id}{Style.RESET_ALL}{w})")


@client.command(aliases=['greet'])
async def hello(ctx:commands.Context):
    name = "hello"
    await ctx.reply(f"> Hello, {ctx.author.display_name}!")
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")


@client.command(name="ping", aliases=['l', 'latency'])
async def bot_latency(ctx:commands.Context):
    name = "ping"
    ping = int(round(client.latency, 3) * 1000)
    await ctx.reply(f"> Pong! {ping}ms")
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
    print(" " * 12 + f"{Fore.CYAN}└>{w} Bot latency is {Fore.YELLOW}{ping}ms{w}")


@client.command(aliases=['p', 'pfp', 'profile'])
async def avatar(ctx:commands.Context, member:discord.Member=None):
    if member == None:
        member = ctx.author
    name = f"avatar {member}"
    await ctx.reply(f"> {member.mention}'s avatar:\n> {member.avatar.url}")
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")


@client.command(name="howold", aliases=['o', 'old', 'age'])
async def discord_timestamp(ctx:commands.Context, member:discord.Member=None):
    if member == None:
        member = ctx.author
    name = f"howold {member}"
    date = member.created_at.replace(tzinfo=timezone.utc)
    utc_time = datetime.now(timezone.utc)
    diff = utc_time - date
    await ctx.reply(f"> Your account is: `{str(diff).split(',')[0]} old`\n> Created on: `{date.strftime('%d-%m-%Y %H:%M:%S UTC')}`")
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")


@client.command(name="shutdown", aliases=['sd', 'exit'])
@commands.is_owner()
async def shutdown_bot(ctx:commands.Context):
    name = "shutdown"
    await ctx.reply("> Turning off bot...")
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
    await client.close()
    
    
@client.command(name="eval", aliases=["e"])
@commands.is_owner()
async def code_evaluation(ctx:commands.Context, *, code=None):
    if code == None:
        await ctx.reply("> Please attach a code block to this command!")
        return
    code = strip_codeblock(code)
    name = 'eval'
    secret = {
        "discord": discord,
        "commands": commands,
        "bot": client,
        "ctx": ctx,
        "channel": ctx.channel,
        "author": ctx.author,
        "guild": ctx.guild,
        "message": ctx.message,
        "builtins": None,
        "token": "not.gonna.leak.my.token",
    }
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    try:
        old_stdout = sys.stdout
        exec(code)
        sys.stdout = old_stdout
        result = mystdout.getvalue()
    except Exception as e:
        result = e
    reply = "```py\n" + result + "\n```"
    await ctx.reply(reply)
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")


@client.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_member(ctx:commands.Context, member:discord.Member=None, *, reason:str="No reason provided"):
    if member == None:
        await ctx.reply(f"Please tag a user to use this command! ({ctx.author.mention})")
        return
    name = f"ban"
    await member.send(f"> Sorry! You have been banned from `{ctx.message.guild}` for the following reason:\n```{reason}```")
    await member.ban(reason=reason)
    await ctx.reply(f"> {member.name} has been successfully banned from `{ctx.message.guild}` for the following reason:\n```{reason}```")
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
    print(" " * 12 + f"{Fore.CYAN}└>{w} Banned user {Fore.YELLOW}{member}{w} ({Style.DIM}{member.id}{Style.RESET_ALL}{w}) for reason: {Fore.YELLOW}{reason}{w}")


@client.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_member(ctx:commands.Context, member:discord.Member=None, *, reason:str="No reason provided"):
    if member == None:
        await ctx.reply(f"Please tag a user to use this command! ({ctx.author.mention})")
        return
    name = "kick"
    await member.send(f"> Sorry! You have been kicked from `{ctx.message.guild}` for the following reason:\n```{reason}```")
    await member.kick(reason=reason)
    await ctx.reply(f"> {member.name} has been successfully kicked from `{ctx.message.guild}` for the following reason:\n```{reason}```")
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
    print(" " * 12 + f"{Fore.CYAN}└>{w} Kicked user {Fore.YELLOW}{member}{w} ({Style.DIM}{member.id}{Style.RESET_ALL}{w}) for reason: {Fore.YELLOW}{reason}{w}")


# doesn't work :/
@client.command(name="timeout", aliases=['to', 'tmout'])
@commands.has_permissions(moderate_members=True)
async def timeout_member(ctx:commands.Context, member:discord.Member=None, minutes:int=None, *, reason:str="No reason provided"):
    if member == None:
        await ctx.reply(f"> Please tag a user to use this command! ({ctx.author.mention})")
        return
    if minutes == None:
        await ctx.reply(f"> Please include the amount of minutes you want to time out a member for!")
    name = "timeout"
    duration = timedelta(minutes=minutes)
    print(duration)
    await member.timeout_for(duration, reason=reason)
    await ctx.reply(f"> {member.mention} timed out for `{minutes} minute(s)` for the following reason:\n```{reason}```")
    await member.send(f"> Sorry! You have been timed out for `{minutes} minute(s)` in `{ctx.message.guild}` for the following reason:\n```{reason}```")
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
    print(" " * 12 + f"{Fore.CYAN}└>{w} Timed out member {Fore.YELLOW}{member}{w} ({Style.DIM}{member.id}{Style.RESET_ALL}{w}) for {Fore.YELLOW}{minutes} minute(s){w} for reason: {Fore.YELLOW}{reason}{w}")


# Doesn't work :(
@client.command(name="unban")
@commands.has_permissions(administrator=True)
async def unban_member(ctx:commands.Context, *, member:discord.Member=None):
    if member == None:
        await ctx.reply(f"Please tag a user to use this command! ({ctx.author.mention})")
        return
    name = "unban"
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member.name, member.discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'> Unbanned {user.name} ({user.mention})')
            print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
            print(" " * 12 + f"{Fore.CYAN}└>{w} Unbanned user {Fore.YELLOW}{member}{w} ({Style.DIM}{member.id}{Style.RESET_ALL}{w})")
            return


@client.command(name='base64encode', aliases=['b64e', 'b64encode', 'base64e'])
async def base64_code(ctx:commands.Context, *, base64_string=None):
    if base64_string == None:
        await ctx.reply("> Please include the message you want to encode to base64!")
        return
    name = 'base64encode'
    code = b64encode(f"{base64_string}".encode()).decode("utf8")
    await ctx.reply(f"> Successfully encoded `{base64_string}`:\n```py\n{code}```")
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
    print(" " * 12 + f"{Fore.CYAN}└>{w} Encoded {Fore.YELLOW}{base64_string}{w} to {Fore.YELLOW}{code}{w} using base64")


@client.command(name='base64decode', aliases=['b64d', 'b64decode', 'base64d'])
async def base64_code(ctx:commands.Context, *, base64_string=None):
    if base64_string == None:
        await ctx.reply("> Please include the message you want to decode from base64!")
        return
    name = 'base64decode'
    code = b64decode(base64_string).decode('utf8')
    await ctx.reply(f"> Successfully decoded `{base64_string}`:\n```py\n{code}```")
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
    print(" " * 12 + f"{Fore.CYAN}└>{w} Decoded {Fore.YELLOW}{base64_string}{w} to {Fore.YELLOW}{code}{w} using base64")
    
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
