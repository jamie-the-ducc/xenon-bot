from base64 import b64decode, b64encode
from datetime import datetime, timezone

import discord
from colorama import Fore, Style
from discord.ext import commands

from app.func import get_time, read_config


w = Style.BRIGHT + Fore.WHITE
prefix = [i[1] for i in read_config()][0]


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(aliases=['greet'])
    async def hello(self, ctx:commands.Context):
        name = "hello"
        await ctx.reply(f"> Hello, {ctx.author.display_name}!")
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")


    @commands.command(name="ping", aliases=['l', 'latency'])
    async def get_latency(self, ctx:commands.Context):
        name = "ping"
        ping = int(round(self.bot.latency, 3) * 1000)
        await ctx.reply(f"> Pong! {ping}ms")
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
        print(" " * 12 + f"{Fore.CYAN}└>{w} Bot latency is {Fore.YELLOW}{ping}ms{w}")


    @commands.command(aliases=['p', 'pfp', 'profile'])
    async def avatar(self, ctx:commands.Context, member:discord.Member=None):
        if member == None:
            member = ctx.author
        name = f"avatar {member}"
        await ctx.reply(f"> {member.mention}'s avatar:\n> {member.avatar.url}")
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")


    @commands.command(name="howold", aliases=['o', 'old', 'age'])
    async def discord_timestamp(self, ctx:commands.Context, member:discord.Member=None):
        if member == None:
            member = ctx.author
        name = f"howold {member}"
        date = member.created_at.replace(tzinfo=timezone.utc)
        utc_time = datetime.now(timezone.utc)
        diff = utc_time - date
        await ctx.reply(f"> Your account is: `{str(diff).split(',')[0]} old`\n> Created on: `{date.strftime('%d-%m-%Y %H:%M:%S UTC')}`")
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")


    @commands.command(name='base64encode', aliases=['b64e', 'b64encode', 'base64e'])
    async def base64_encode(self, ctx:commands.Context, *, base64_string=None):
        if base64_string == None:
            await ctx.reply("> Please include the message you want to encode to base64!")
            return
        name = 'base64encode'
        code = b64encode(f"{base64_string}".encode()).decode("utf8")
        await ctx.reply(f"> Successfully encoded `{base64_string}`:\n```py\n{code}```")
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
        print(" " * 12 + f"{Fore.CYAN}└>{w} Encoded {Fore.YELLOW}{base64_string}{w} to {Fore.YELLOW}{code}{w} using base64")


    @commands.command(name='base64decode', aliases=['b64d', 'b64decode', 'base64d'])
    async def base64_decode(self, ctx:commands.Context, *, base64_string=None):
        if base64_string == None:
            await ctx.reply("> Please include the message you want to decode from base64!")
            return
        name = 'base64decode'
        try:
            code = b64decode(base64_string).decode('utf8')
        except:
            await ctx.reply("> Please send a valid base64 string!")
        await ctx.reply(f"> Successfully decoded `{base64_string}`:\n```py\n{code}```")
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
        print(" " * 12 + f"{Fore.CYAN}└>{w} Decoded {Fore.YELLOW}{base64_string}{w} to {Fore.YELLOW}{code}{w} using base64")


def setup(bot):
    bot.add_cog(General(bot))
