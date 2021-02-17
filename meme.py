import discord
from discord.ext import commands
from discord.utils import get
import sqlite3

class meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if(not message.channel.id == 808462723334668358):
            return
        if self.bot.get_user(message.author.id).bot:
            return
        if len(message.attachments) == 1 or "https://cdn.discordapp.com/attachments/" in message.content:
            await message.add_reaction(emoji=self.bot.get_emoji(804839171059220480))
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.bot.get_user(payload.user_id).bot:
            return
        if not payload.channel_id == 808462723334668358:
            return
        if not payload.emoji.id == 804839171059220480:
            return
        channel = self.bot.get_channel(808462723334668358)
        message = await channel.fetch_message(payload.message_id)
        reaction = get(message.reactions, emoji=self.bot.get_emoji(804839171059220480))
        if reaction and reaction.count == 10:
            conn = sqlite3.connect('db/memes.db')
            c = conn.cursor()
            t = (payload.message_id, )
            try:
                c.execute('SELECT * FROM msg WHERE msg_id=?', t)
                if payload.message_id == c.fetchone():
                    return
            except:
                pass
            try:
                embed=discord.Embed(description=f"{message.content}\n[Original post]({message.jump_url})", color=0x0080c0)
                embed.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar_url}")
                embed.set_image(url=f"{message.attachments[0].url}")
            except:
                flex = message.strip()
                meme = None
                for i in flex:
                    if "https://cdn.discordapp.com/attachments/" in i:
                        flex.remove(i)
                        meme = i
                embed=discord.Embed(description=f"{' '.join(flex)}\n[Original post]({message.jump_url})", color=0x0080c0)
                embed.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar_url}")
                embed.set_image(url=f"{meme}")
            c.execute("INSERT INTO msg VALUES (?)", t)
            conn.commit()
            conn.close()
            await self.bot.get_channel(809354574695235615).send(f"{message.author.mention}", embed=embed)
    
def setup(bot):
    bot.add_cog(meme(bot))

    # TEST
    # ----------------------
    #     @commands.Cog.listener()
    # async def on_message(self, message):
    #     if(not message.channel.id == 801079424925433898):
    #         return
    #     if self.bot.get_user(message.author.id).bot:
    #         return
    #     if len(message.attachments) == 1 or "https://cdn.discordapp.com/attachments/" in message.content:
    #         await message.add_reaction(emoji=self.bot.get_emoji(798950528113573909))
        
    # @commands.Cog.listener()
    # async def on_raw_reaction_add(self, payload):
    #     if self.bot.get_user(payload.user_id).bot:
    #         return
    #     if not payload.channel_id == 801079424925433898:
    #         return
    #     if not payload.emoji.id == 798950528113573909:
    #         return
    #     channel = self.bot.get_channel(801079424925433898)
    #     message = await channel.fetch_message(payload.message_id)
    #     reaction = get(message.reactions, emoji=self.bot.get_emoji(798950528113573909))
    #     if reaction and reaction.count > 1:
    #         await message.pin()

    # ----------------------
    # TEST