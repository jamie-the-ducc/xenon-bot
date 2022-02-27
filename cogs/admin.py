import json
from datetime import timedelta
from pathlib import Path

import discord
from colorama import Fore, Style
from discord.ext import commands

from app.func import get_time, read_config


w = Style.BRIGHT + Fore.WHITE
prefix = [i[1] for i in read_config()][0]
GUILDS_JSON = Path.cwd() / "app" / "guilds.json"


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # source: https://stackoverflow.com/a/64772835
    @commands.command(name="welcome", aliases=['w', 'setwelcome'])
    @commands.has_permissions(administrator=True)
    async def set_welcome_channel(self, ctx:commands.Context, channel:discord.TextChannel=None):
        if channel == None:
            channel = ctx.message.channel
        name = "welcome #" + channel.name
        with open(GUILDS_JSON, "r", encoding="utf8") as f:
            guilds_dict = json.load(f)

        guilds_dict[str(ctx.guild.id)] = str(channel.id)
        with open(GUILDS_JSON, "w", encoding="utf8") as f:
            json.dump(guilds_dict, f, indent=4, ensure_ascii=False)

        await ctx.reply(f"> Set welcome channel for `{ctx.message.guild.name}` to {channel.mention}")
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
        print(" " * 12 + f"{Fore.CYAN}└>{w} Set welcome channel to {Fore.YELLOW}{channel.name}{w} ({Style.DIM}{channel.id}{Style.RESET_ALL}{w})")
      
        
    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_member(self, ctx:commands.Context, member:discord.Member=None, *, reason:str="No reason provided"):
        if member == None:
            await ctx.reply(f"Please tag a user to use this command! ({ctx.author.mention})")
            return
        name = f"ban"
        await member.send(f"> Sorry! You have been banned from `{ctx.message.guild}` for the following reason:\n```{reason}```")
        await member.ban(reason=reason)
        await ctx.reply(f"> {member.name} has been successfully banned from `{ctx.message.guild}` for the following reason:\n```{reason}```")
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
        print(" " * 12 + f"{Fore.CYAN}└>{w} Banned user {Fore.YELLOW}{member}{w} ({Style.DIM}{member.id}{Style.RESET_ALL}{w}) for reason: {Fore.YELLOW}{reason}{w}")


    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick_member(self, ctx:commands.Context, member:discord.Member=None, *, reason:str="No reason provided"):
        if member == None:
            await ctx.reply(f"Please tag a user to use this command! ({ctx.author.mention})")
            return
        name = "kick"
        await member.send(f"> Sorry! You have been kicked from `{ctx.message.guild}` for the following reason:\n```{reason}```")
        await member.kick(reason=reason)
        await ctx.reply(f"> {member.name} has been successfully kicked from `{ctx.message.guild}` for the following reason:\n```{reason}```")
        print(f" {Style.DIM}({get_time()}){Style.RESET_ALL}{w} Recieved command {Fore.GREEN}{prefix}{name}{w} in {Fore.YELLOW}#{ctx.channel}{w} from {Fore.YELLOW}{ctx.author} {w}({Style.DIM}{ctx.author.id}{Style.RESET_ALL}{w})")
        print(" " * 12 + f"{Fore.CYAN}└>{w} Kicked user {Fore.YELLOW}{member}{w} ({Style.DIM}{member.id}{Style.RESET_ALL}{w}) for reason: {Fore.YELLOW}{reason}{w}")


    @commands.command(name="timeout", aliases=['to', 'tmout'])
    @commands.has_permissions(moderate_members=True)
    async def timeout_member(self, ctx:commands.Context, member:discord.Member=None, minutes:int=None, *, reason:str="No reason provided"):
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


    # doesn't work :/
    @commands.command(name="unban")
    @commands.has_permissions(administrator=True)
    async def unban_member(self, ctx:commands.Context, *, member:discord.Member=None):
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


def setup(bot):
    bot.add_cog(Admin(bot))
