import platform
from base64 import b64decode, b64encode
from datetime import datetime, timezone

import discord
from colorama import Fore, Style
from discord.ext import commands

from app.__version__ import __version__
from app.func import get_time, read_config


w = Style.BRIGHT + Fore.WHITE
prefix = [i[1] for i in read_config()][0]
footer = "✅ Developed by [Jam!3]#4466"
colour = 0x00C09A


command_dict = {
    "general":{
        "hello":{"alias":["greet"], "usage":f"{prefix}hello", "description":"Replies to the sender"},
        "avatar":{"alias":["p", "pfp", "profile"], "usage":f"{prefix}avatar <@member>", "description":"Sends the profile picture of the mentioned member"},
        "howold":{"alias":["o", "old", "age"], "usage":f"{prefix}howold <@user_tag>", "description":"Sends the account creation date of the mentioned member"},
        "b64encode":{"alias":["b64e", "base64e", "base64encode"], "usage":f"{prefix}b64encode [code block]", "description":"Encodes provided message to base64"},
        "b64decode":{"alias":["b64d", "base64d", "base64decode"], "usage":f"{prefix}b64decode [code block]", "description":"Decodes provided base64 to message"},
        "rickroll":{"alias":["rick"], "usage":f"{prefix}rickroll", "description":"Sends rickroll gif 😏"},
        "info":{"alias":[""], "usage":f"{prefix}info", "description":"Replies with bot name and developer nfo"},
        "invite":{"alias":[""], "usage":f"{prefix}invite", "description":"Sends invite URL for the bot"},
    },
    "admin":{
        "setwelcome":{"alias":["w", "welcome"], "usage":f"{prefix}setwelcome <#channel_tag>", "description":"Sets mentioned channel for member join/leave messages"},
        "kick":{"alias":[""], "usage":f"{prefix}kick [@member] <reason>", "description":"Kicks mentioned member from the server"},
        "ban":{"alias":[""], "usage":f"{prefix}ban [@member] <reason>", "description":"Bans mentioned member from the server"},
        "unban":{"alias":[""], "usage":f"{prefix}unban [@member]", "description":"Unans mentioned member in the server"},
        "timeout":{"alias":["t", "tmout"], "usage":f"{prefix}timeout [@member] [time (minutes)] <reason>", "description":"Timesout mentioned member in the server for a specified amount of time"},
    },
    "owner":{
        "shutdown":{"alias":["sd", "exit", "quit", "close"], "usage":f"{prefix}shutdown", "description":"Turns off the bot"},
        "eval":{"alias":["e", "exec", "evaluate"], "usage":f"{prefix}eval [code block]", "description":"Evaluates the given python code block and rerturns results"},
    },
    "prefixless":{
        "rick roll":{"alias":["rick"], "usage":"rick roll", "description":"Sends rickroll gif 😏"},
        "hello":{"alias":["hi", "reply"], "usage":"hello", "description":"Replies to the sender"},
        "flush":{"alias":[""], "usage":"flush", "description":"Sends the flush emote <:flush_v2:946581195737665577>"},
    },
    "demo":{
        "":{"alias":[""], "usage":f"{prefix}", "description":""},
    }
}
    


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def logs(self, ctx, name):
        return f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})"

    @commands.command()
    async def botstats(self, ctx):
        # Katt#8347
        name = "botstats"
        
        embed = discord.Embed(title='<:stats:947404175761891358> Bot Statistics <:stats_flip:948381659387015298>', description=f'{self.bot.user} (`{self.bot.user.id}`)', colour=ctx.author.colour, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        
        embed.add_field(name='<:dev:948397415612944414> Developer', value="<@604855154365300753>")
        embed.add_field(name='<:admin:947403881602760715> Contributor', value="<@942917416768376942>")
        embed.add_field(name='<:github:948482698744328223> GitHub', value="[xenon-bot.io](https://cutt.ly/xenon-bot)")
        
        embed.add_field(name='<:bot1:948474603687276544><:bot2:948474630400794634> Version', value=__version__)
        embed.add_field(name='<:python:948474655977644032> Python Version', value=platform.python_version())
        embed.add_field(name='<:pycord:948474678190698526> Pycord', value=discord.__version__)

        embed.add_field(name='<:members:948476307455488071> Guild Count', value=len(self.bot.guilds))
        embed.add_field(name='<:members:948476307455488071> User Count', value=len(set(self.bot.get_all_members())))
        embed.add_field(name='<:cmd:948483223032332298> Commands', value=len(self.bot.commands))
        
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)
        
        print(self.logs(ctx, name))

    @commands.command()
    async def hello(self, ctx: commands.Context):
        """Replies to the sender"""
        name = "hello"
        embed = discord.Embed(description=f"Hello, {ctx.author.mention}!", color=colour, timestamp=ctx.message.created_at)
        await ctx.reply(embed=embed)
        print(self.logs(ctx, name))

    @commands.command(aliases=['p', 'pfp', 'profile'])
    async def avatar(self, ctx: commands.Context, member: discord.Member = None):
        """Sends avatar of mentioned member"""
        if member == None:
            member = ctx.author
        name = f"avatar {member}"
        url = member.avatar.url
        embed = discord.Embed(title=f"{member.name}'s Avatar", description="", url=url, color=colour, timestamp=ctx.message.created_at)
        embed.set_image(url=url)
        embed.set_footer(text=footer)
        await ctx.reply(embed=embed)
        print(self.logs(ctx, name))

    @commands.command(name="howold", aliases=['o', 'old', 'age'])
    async def discord_timestamp(self, ctx: commands.Context, member: discord.Member = None):
        """Sends the account creation date of the mentioned member"""
        if member == None:
            member = ctx.author
        name = f"howold {member}"
        date = member.created_at.replace(tzinfo=timezone.utc)
        utc_time = datetime.now(timezone.utc)
        diff = utc_time - date
        await ctx.reply(f"> Your account is: `{str(diff).split(',')[0]} old`\n> Created on: `{date.strftime('%d-%m-%Y %H:%M:%S UTC')}`")
        print(self.logs(ctx, name))

    @commands.command(name='base64encode', aliases=['b64e', 'b64encode', 'base64e'])
    async def base64_encode(self, ctx: commands.Context, *, base64_string: str = None):
        """Encodes provided message to base64"""
        if base64_string == None:
            await ctx.reply("> Please include the message you want to encode to base64!")
            return
        name = 'base64encode'
        code = b64encode(f"{base64_string}".encode()).decode("utf8")
        await ctx.reply(f"> Successfully encoded `{base64_string}`:\n```py\n{code}```")
        print(self.logs(ctx, name))
        print(f"{' ' * 12}{Fore.CYAN}└>{w} Encoded {Fore.YELLOW}{base64_string}{w} to {Fore.YELLOW}{code}{w} using base64")

    @commands.command(name='base64decode', aliases=['b64d', 'b64decode', 'base64d'])
    async def base64_decode(self, ctx: commands.Context, *, base64_string: str = None):
        """Decodes provided base64 to message"""
        if base64_string == None:
            await ctx.reply("> Please include the message you want to decode from base64!")
            return
        name = 'base64decode'
        try:
            code = b64decode(base64_string).decode('utf8')
        except:
            await ctx.reply("> Please send a valid base64 string!")
        await ctx.reply(f"> Successfully decoded `{base64_string}`:\n```py\n{code}```")
        print(self.logs(ctx, name))
        print(f"{' ' * 12}{Fore.CYAN}└>{w} Decoded {Fore.YELLOW}{base64_string}{w} to {Fore.YELLOW}{code}{w} using base64")

    @commands.command(name="echo", aliases=["ec"])
    async def repeat_message(self, ctx: commands.Context, *, message: str):
        """Echoes message back to the sender"""
        await ctx.message.delete()
        await ctx.send(message)
        
    @commands.command(name="serverstats", aliases=["stats", "s"])
    async def server_statistics(self, ctx: commands.Context):
        name="serverstats"

        member_list = [member for member in ctx.guild.members if not member.bot]
        mem_count = len(member_list)
        
        online_list = []
        for x, member in enumerate(member_list):
            if member.status != discord.Status.offline:
                online_list.append(member)
            if mem_count == x:
                break

        bot_count = len([member for member in ctx.guild.members if member.bot])
        online_count = len(online_list)
        
        date = ctx.guild.created_at.replace(tzinfo=timezone.utc)
        utc_time = datetime.now(timezone.utc)
        diff = utc_time - date
        days_old = str(diff).split(',')[0]
        creation_date = date.strftime('%d-%m-%Y %H:%M:%S UTC')

        embed = discord.Embed(title="<:stats:947404175761891358> Server Statistics <:stats_flip:948381659387015298>", description=f"💜 Server: {ctx.guild.name} (`{ctx.guild.id}`)", color=colour, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=ctx.guild.icon)
        
        #embed.add_field(name = chr(173), value = chr(173))
        embed.add_field(name="<:owner:947403810828083210> Server Owner", value=ctx.guild.owner.mention, inline=True)
        embed.add_field(name="🌹 Role Count", value=len(ctx.guild.roles), inline=True)
        embed.add_field(name="🌷 Channel Count", value=len(ctx.guild.channels), inline=True)
        
        embed.add_field(name="📊 Total Members", value=len(ctx.guild.members), inline=True)
        embed.add_field(name="🔢 Member Count", value=mem_count, inline=True)
        embed.add_field(name="🤖 Bot Count", value=bot_count, inline=True)
        
        embed.add_field(name="<:online:947403969779609620> Online Members", value=online_count, inline=True)
        embed.add_field(name="🕒 Server Age", value=f"{days_old} old", inline=True)
        embed.add_field(name="📅 Creation Date", value=creation_date, inline=True)
        
        embed.set_footer(text=footer)
        await ctx.reply(embed=embed)
        
        print(self.logs(ctx, name))
    

def setup(bot):
    bot.add_cog(General(bot))
