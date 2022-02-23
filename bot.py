# [Xe]non.py Discord Bot
# Written with 💜 by [Jam!3]#4466
# Initial start: 15/02/2022

# ----------------------------------------------- #
#  ____  __   __
# | _\ \/ /__|_ |_ __   ___  _ __    _ __  _   _
# | | \  // _ \ | '_ \ / _ \| '_ \  | '_ \| | | |
# | | /  \  __/ | | | | (_) | | | |_| |_) | |_| |
# | |/_/\_\___| |_| |_|\___/|_| |_(_) .__/ \__, |
# |__|       |__|    version 1.1    |_|    |___/
# ----------------------------------------------- #

import json
from asyncio import sleep
from pathlib import Path
from string import Template

import discord
import discord.errors
from colorama import Back, Fore, Style
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
GUILDS_JSON = Path.cwd() / "app" / "guilds.json"


LOG_TEMPLATE = Template(f" {Style.DIM}$time{Style.RESET_ALL}{w}\t{Fore.BLACK}{Back.WHITE}$type{Style.RESET_ALL}{w}\t$action\t{Fore.GREEN}$command\t{Fore.YELLOW}$channel\t{Fore.CYAN}$user{w}:{Fore.BLUE}$id{w}")
logger = lambda type,action,command,channel,user,uid:print(LOG_TEMPLATE.substitute(time=get_time(), type=type, action=action, command=command, channel=channel, user=user, id=uid))
print(LOG_TEMPLATE.substitute(time=get_time(), type="INFO", action="CommandRecieved", command="x.ping", channel="#bot-commands", user="Jamie#0000", id=604855154365300753))
input(LOG_TEMPLATE.substitute(time=get_time(), type="INFO", action="ResponseSent", command="178ms", channel="#bot-commands", user="Jamie#0000", id=604855154365300753))

title()

prefix, token, webhook, owner, status_delay = [i[1] for i in read_config()]

activities = ["the birds sing 💛", "the trees sway 💚", "the fire crackle ❤️", "the wind whisper 💜", "the rain fall 💙"]

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
    ready_time = get_time()
    title()
    length_a = len(f"║ [+] Connected to Discord.com as {client.user} ({client.user.id})") - 1
    length_b = len(f"║ [>] Status set to Listening to {activities[-1]}")
    length = length_a + 1 if length_a > length_b else length_b + 1
        
    header = " ╔" + " Bot Information ".center(length, "═") + "╗"
    connect_len = length - length_b
    status_len = length - length_a
    guild_len = length - len(f"║ [>] Watching {len(client.guilds)} server(s) ⭐")
    prefix_len = length - len(f"║ [>] Prefix set to {prefix}")
    ready_len = length - len(f"║ [>] Bot ready at {ready_time}")
    
    print(header)
    print(f" ║{GOOD} Connected to Discord.com as {Fore.GREEN}{client.user}{w} ({Style.DIM}{client.user.id}{Style.RESET_ALL}{w})" + " " * status_len + "║")
    print(f" ║{INFO} Watching {Fore.YELLOW}{len(client.guilds)} server(s){w} ⭐" + " " * guild_len + "║")
    print(f" ║{INFO} Prefix set to {Fore.YELLOW}{prefix}{w} " + " " * prefix_len + "║")
    print(f" ║{INFO} Status set to {Fore.YELLOW}Listening to {activities[-1]}{w}" + " " * connect_len + "║")
    print(f" ║{INFO} Bot ready at {Fore.YELLOW}{ready_time}{w} " + " " * ready_len + "║")
    print(" ╚" + "═" * length + "╝")


# ON MEMBER JOIN
@client.event
async def on_member_join(member):
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Welcome! {Fore.YELLOW}{member}{w} has {Fore.GREEN}joined{w} the server.")  
    with open(GUILDS_JSON, 'r', encoding='utf-8') as f:
        guilds_dict = json.load(f)

    channel_id = guilds_dict[str(member.guild.id)]
    await client.get_channel(int(channel_id)).send(f'{member.mention} welcome to the server! Enjoy your stay! 💜')


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
    with open(GUILDS_JSON, 'r', encoding='utf-8') as f:
        guilds_dict = json.load(f)

    guilds_dict.pop(guild.id)
    with open(GUILDS_JSON, 'w', encoding='utf-8') as f:
        json.dump(guilds_dict, f, indent=4, ensure_ascii=False)


# SET WELCOME CHANNEL
@client.command(name='welcome')
async def set_welcome_channel(ctx, channel: discord.TextChannel):
    with open(GUILDS_JSON, 'r', encoding='utf-8') as f:
        guilds_dict = json.load(f)

    guilds_dict[str(ctx.guild.id)] = str(channel.id)
    with open(GUILDS_JSON, 'w', encoding='utf-8') as f:
        json.dump(guilds_dict, f, indent=4, ensure_ascii=False)
    
    await ctx.send(f'> Set welcome channel for `{ctx.message.guild.name}` to <#{channel.id}>')


# CLIENT COMMANDS
@client.command(name="hello") # x.hello
async def hello(ctx: commands.Context):
    name = "hello"
    await ctx.reply(f"Hello, {ctx.author.display_name}!")
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")


@client.command(name="ping") # x.ping
async def ping(ctx: commands.Context):
    name = "ping"
    ping = int(round(client.latency,3)*1000)
    await ctx.reply(f"Pong! {ping}ms")
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
    print(" " * 12 + f"{Fore.CYAN}└>{w} Bot latency is {Fore.YELLOW}{ping}ms{w}")
    
    
@client.command(name="avatar") # x.avatar
async def avatar(ctx: commands.Context, user):
    name = "avatar"    
    if not user:
        user = ctx.author
    await ctx.reply(f"<@!{user.id}>'s avatar: {user.avatar_url}")
    print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
    
    
@client.command(name="set") # x.set <arg>
async def set_(ctx: commands.Context, arg):
    name = "set" + arg
    if arg == "welcome":
        await set_welcome_channel(ctx, ctx.channel)
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
        print(" " * 12 + f"{Fore.CYAN}└>{w} Set welcome channel to {Fore.YELLOW}{ctx.channel}{w}")
    
    
# END OF CLIENT COMMANDS


# STATUS CHANGE LOOP
@loop(seconds=status_delay)
async def status_change():
    for id, _ in enumerate(activities):
        await sleep(status_delay)
        activity = activities[id]
        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening, name=activity
            ),
            status=discord.Status.idle,
        )
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Status changed to {Fore.YELLOW}Listening to {activity}{w}")


status_change.start()

try:
    client.run(token, reconnect=True)
except discord.errors.LoginFailure:
    print(f"{BAD} Improper token passed ({Fore.YELLOW}config.ini{w})")
