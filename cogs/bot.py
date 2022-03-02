import json
from pathlib import Path
from base64 import b64decode

import discord
from colorama import Fore, Style
from discord.ext import commands

from app.func import get_time, read_config, reply_dict, reply_dict_noprefix


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
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            error = 'Please pass in the required arguments'
        elif isinstance(error, commands.MissingPermissions):
            error = "You don't have sufficient permissions to use this command."
        elif isinstance(error, commands.NotOwner):
            error = "Only the bot owner can use this command."
        elif isinstance(error, commands.CommandNotFound):
            if ctx.invoked_with in reply_dict:
                return
        else:
            print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} {Fore.RED}Error:{w}", error)
        await ctx.reply(f"<:no:947393772071825418> An error occured while executing your command:\n```{error}```")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
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
            
        with open(Path.cwd() / "app" / "word_blacklist.txt", 'r') as f:
            censored_list = b64decode(f.read()).decode('utf8').split(',')
            
            if message.author is not self.bot.user:
                content = message.content.lower().split(' ')
                for word in content:
                    if word in censored_list:
                        await message.delete()
                        await message.channel.send(f"> {message.author.mention}, your message was deleted because it contained an inappropriate word.")
                        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Deleted censored word {Fore.GREEN}{word}{w} in {Fore.YELLOW}#{message.channel}{w} from {Fore.YELLOW}{message.author} {w}({Style.DIM}{message.author.id}{Style.RESET_ALL}{w})")
                        return

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Welcome! {Fore.YELLOW}{member}{w} ({Style.DIM}{member.id}{Style.RESET_ALL}{w}) has {Fore.GREEN}joined{w} the server.")
        with open(GUILDS_JSON, "r", encoding="utf-8") as f:
            guilds_dict = json.load(f)
        channel_id = guilds_dict[str(member.guild.id)]
        await self.bot.get_channel(int(channel_id)).send(f"{member.mention} welcome to the server! Enjoy your stay! 💜")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Goodbye! {Fore.YELLOW}{member}{w} ({Style.DIM}{member.id}{Style.RESET_ALL}{w}) has {Fore.RED}left{w} the server.")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Bot {Fore.GREEN}added{w} to server {Fore.YELLOW}{guild}{w} ({Style.DIM}{guild.id}{Style.RESET_ALL}{w}).")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Bot {Fore.RED}removed{w} from server {Fore.YELLOW}{guild}{w} ({Style.DIM}{guild.id}{Style.RESET_ALL}{w}).")
        with open(GUILDS_JSON, "r", encoding="utf-8") as f:
            guilds_dict = json.load(f)
        guilds_dict.pop(str(guild.id))
        with open(GUILDS_JSON, "w", encoding="utf-8") as f:
            json.dump(guilds_dict, f, indent=4, ensure_ascii=False)


def setup(bot):
    bot.add_cog(Bot(bot))
