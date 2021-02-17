import discord
from discord.ext import commands
from discord.utils import get
import sqlite3

class cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.content[:2] == "v!":
            return
        
        conn = sqlite3.connect('db/cmd.db')
        c = conn.cursor()
        t = (message.content.replace("v!", ""),)
        try:
            c.execute('SELECT * FROM command WHERE cmd=?', t)
            drip = c.fetchall()
            await message.channel.send(drip[0][1])
        except:
            pass
        conn.close()

    @commands.command()
    async def del_cmd(self, ctx, cmd):
        if not ctx.author.id == 180938450986467328:
            return

        conn = sqlite3.connect('db/cmd.db')
        c = conn.cursor()
        try:
            t = (cmd, )
            c.execute("DELETE FROM command WHERE cmd=?", t)
            await ctx.send("removed custom cmomand")
        except Exception as error:
            await ctx.send(error)
            pass
        conn.commit()
        conn.close()
        

    @commands.command()
    async def add_cmd(self, ctx, cmd, *, msg):
        if not ctx.author.id == 180938450986467328:
            return

        conn = sqlite3.connect('db/cmd.db')
        c = conn.cursor()
        try:
            t = (cmd, msg)
            c.execute("INSERT INTO command VALUES (?, ?)", t)
            await ctx.send("added custom cmomand")
        except Exception as error:
            await ctx.send(error)
        conn.commit()
        conn.close()
        

def setup(bot):
    bot.add_cog(cmd(bot))