import contextlib
import textwrap
from io import StringIO
from traceback import format_exception

import discord
from colorama import Fore, Style
from discord.ext import commands

from app.func import get_time, strip_codeblock


w = Style.BRIGHT + Fore.WHITE


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shutdown", aliases=['sd', 'exit', 'quit', 'close', "logout"])
    @commands.is_owner()
    async def shutdown_bot(self, ctx: commands.Context):
        """Turns off the bot"""
        name = "shutdown"
        await ctx.reply("> Turning off bot...")
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{ctx.prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
        await self.bot.close()
        
    @commands.command(name="eval", aliases=["e", "exec", "evaluate"])
    @commands.is_owner()
    async def _eval(self, ctx: commands.Context, *, code = None):
        """Evaluates given python code block and rerturns results"""
        if code == None:
            await ctx.reply("> Please attach a code block to this command!")
            return
        code = strip_codeblock(code)
        name = 'eval'
        
        local_variables = {
            "discord": discord,
            "commands": commands,
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "token": "not.gonna.leak.my.token",
        }
        
        stdout = StringIO()
        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
                )
                obj = await local_variables["func"]()
                result = f"{stdout.getvalue()}\n-- {obj}\n"
            msg = ":white_check_mark: Code executed successfully"
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))
            msg = "<:no:947393772071825418> Code failed with the following error:"
            
        reply = f"{msg}\n```bash\n{result}\n```"
        await ctx.reply(reply)
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{ctx.prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")


def setup(bot):
    bot.add_cog(Owner(bot))
