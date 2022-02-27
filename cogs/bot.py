import json
from pathlib import Path
from datetime import timedelta
from time import time

import discord
from colorama import Fore, Style
from discord.ext import commands

from app.func import (display_bot_info, get_time, read_config, reply_dict,
                      reply_dict_noprefix)


config = [i[1] for i in read_config()]
prefix = config[0]
activities = config[4].split(',')

w = Style.BRIGHT + Fore.WHITE
GUILDS_JSON = Path.cwd() / "app" / "guilds.json"


class Bot(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
       
    # Error handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx:commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('> Please psas in the required arguments')
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("> You don't have sufficient permissions to use this command")
        if isinstance(error, commands.NotOwner):
            await ctx.reply("> Sorry, only the owner can use this command.")
        else:
            print(f"{Fore.RED}Error:{w}", error)
 
 
    # works
    @commands.Cog.listener()
    async def on_ready(self):
        print(display_bot_info(self.bot, prefix, activities))
        global startTime
        startTime = time()


    # works
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        #await self.bot.process_commands(message)
        name = message.content
        msg = name.removeprefix(prefix)
        # clean up later
        if name.startswith(prefix) and msg in reply_dict and message.author is not self.bot.user:
            await message.reply(reply_dict[msg])
            print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{name}{w} in {Fore.YELLOW}#{message.channel}{w} from {Fore.YELLOW}{message.author} {w}({Style.DIM}{message.author.id}{Style.RESET_ALL}{w})")
        elif msg in reply_dict_noprefix and message.author is not self.bot.user:
            await message.reply(reply_dict_noprefix[msg])
            print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{name}{w} in {Fore.YELLOW}#{message.channel}{w} from {Fore.YELLOW}{message.author} {w}({Style.DIM}{message.author.id}{Style.RESET_ALL}{w})")


    # works
    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Welcome! {Fore.YELLOW}{member}{w} ({Style.DIM}{member.id}{Style.RESET_ALL}{w}) has {Fore.GREEN}joined{w} the server.")
        with open(GUILDS_JSON, "r", encoding="utf-8") as f:
            guilds_dict = json.load(f)

        channel_id = guilds_dict[str(member.guild.id)]
        await self.bot.get_channel(int(channel_id)).send(f"{member.mention} welcome to the server! Enjoy your stay! 💜")


    # probably works as well
    @commands.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Goodbye! {Fore.YELLOW}{member}{w} ({Style.DIM}{member.id}{Style.RESET_ALL}{w}) has {Fore.RED}left{w} the server.")


    # works
    @commands.Cog.listener()
    async def on_guild_join(self, guild:discord.Guild):
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Bot {Fore.GREEN}added{w} to server {Fore.YELLOW}{guild}{w} ({Style.DIM}{guild.id}{Style.RESET_ALL}{w}).")


    # works
    @commands.Cog.listener()
    async def on_guild_remove(self, guild:discord.Guild):
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Bot {Fore.RED}removed{w} from server {Fore.YELLOW}{guild}{w} ({Style.DIM}{guild.id}{Style.RESET_ALL}{w}).")
        with open(GUILDS_JSON, "r", encoding="utf-8") as f:
            guilds_dict = json.load(f)

        guilds_dict.pop(str(guild.id))
        with open(GUILDS_JSON, "w", encoding="utf-8") as f:
            json.dump(guilds_dict, f, indent=4, ensure_ascii=False)


    @commands.command(name="ping", aliases=['l', 'latency'])
    async def get_latency(self, ctx:commands.Context):
        name = "ping"
        ping = int(round(self.bot.latency, 3) * 1000)
        uptime = str(timedelta(seconds=int(round(time()-startTime))))
        await ctx.reply(f"Pong!\n> Latency: `{ping}ms`\n> Uptime: `{uptime}`")
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
        print(" " * 12 + f"{Fore.CYAN}└>{w} Bot latency is {Fore.YELLOW}{ping}ms{w}")


def setup(bot):
    bot.add_cog(Bot(bot))
