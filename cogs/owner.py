import sys
from io import StringIO

import discord
from colorama import Fore, Style
from discord.ext import commands

from app.func import get_time, read_config, strip_codeblock


w = Style.BRIGHT + Fore.WHITE
prefix = [i[1] for i in read_config()][0]


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   

    @commands.command(name="shutdown", aliases=['sd', 'exit'])
    @commands.is_owner()
    async def shutdown_bot(self, ctx:commands.Context):
        name = "shutdown"
        await ctx.reply("> Turning off bot...")
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
        await self.bot.close()
        
        
    @commands.command(name="eval", aliases=["e"])
    @commands.is_owner()
    async def code_evaluation(self, ctx:commands.Context, *, code=None):
        if code == None:
            await ctx.reply("> Please attach a code block to this command!")
            return
        code = strip_codeblock(code)
        name = 'eval'
        secret = {
            "discord": discord,
            "commands": commands,
            "bot": self.bot,
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


def setup(bot):
    bot.add_cog(Owner(bot))
