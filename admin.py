import discord
from discord.ext import commands
from discord.utils import get
import os
import datetime
import sqlite3
from discord.ext.commands import CommandNotFound

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create_memedb(self, ctx):
        if not ctx.author.id == 180938450986467328:
            return
        conn = sqlite3.connect('db/memes.db')
        c = conn.cursor()
        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS msg (msg_id int PRIMARY KEY)''')
        conn.commit()
        conn.close()
        await ctx.send("Done!")

    @commands.command()
    async def create_statusdb(self, ctx):
        if not ctx.author.id == 180938450986467328:
            return
        conn = sqlite3.connect('db/status.db')
        c = conn.cursor()
        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS status (user_id int PRIMARY KEY, status text)''')
        conn.commit()
        conn.close()
        await ctx.send("Done!")

    @commands.command()
    async def create_cmddb(self, ctx):
        if not ctx.author.id == 180938450986467328:
            return
        conn = sqlite3.connect('db/cmd.db')
        c = conn.cursor()
        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS command (cmd text PRIMARY KEY, msg text)''')
        conn.commit()
        conn.close()
        await ctx.send("Done!")

    @commands.command()
    async def botstatus(self, ctx, type, *, txt):
        if not ctx.author.id == 180938450986467328:
            return
        if type.lower() == "playing":
            activity = discord.Game(name=f"{txt}")
        elif type.lower() == "watching":
            activity = discord.Activity(type=discord.ActivityType.watching, name=f"{txt}")
        elif type.lower() == "listening":
            activity = discord.Activity(type=discord.ActivityType.listening, name=f"{txt}")
        else:
            await ctx.send("Only use: playing, watching, listening")
            return
        await self.bot.change_presence(activity=activity)

    @commands.command()
    async def cogs(self, ctx):
        if not ctx.author.id == 180938450986467328:
            return
        return_list = []
        for filename in os.listdir("."):
            if filename.endswith(".py"):
                if filename != "bot.py":
                    return_list.append(filename.replace(".py", ""))
        await ctx.send(", ".join(return_list))

    @commands.command()
    async def reloadall(self, ctx):
        if not ctx.author.id == 180938450986467328:
            return
        return_list = []
        for filename in os.listdir("."):
            if filename.endswith(".py"):
                if filename != "bot.py":
                    return_list.append(filename.replace(".py", ""))
        for extension in return_list:
            try:
                self.bot.reload_extension(extension)
                await ctx.send(f"Reloaded {extension}")
            except Exception as error:
                await ctx.send(f"{extension} cannot be reloadded. [{error}]

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            return
            
        raise error


def setup(bot):
    bot.add_cog(admin(bot))

