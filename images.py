import discord
from discord.ext import commands
from discord.utils import get
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import textwrap
import os
import sqlite3

class img(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        async with ctx.typing():
            upload_file = f"{user.id}_profile.png"

            img = Image.open("imgs/Profile_Template.png").convert('RGBA')

            # PROFIL BILD
            asset = user.avatar_url_as(size = 128)
            data = BytesIO(await asset.read())
            pfp = Image.open(data).convert('RGBA')
            pfp = pfp.resize((421,421))
            img.paste(pfp, (64, 144), pfp)
            # PROFIL BILD
            # TEXT
            draw = ImageDraw.Draw(img)

            font = ImageFont.truetype("fonts/squealer.ttf", 45)
            draw.text((40, 33), f"{user.name}", font=font, fill='rgb(255, 153, 102)')

            conn = sqlite3.connect('db/status.db')
            c = conn.cursor()
            t = (user.id,)
            try:
                c.execute('SELECT status FROM status WHERE user_id=?', t)
                text = ''.join(c.fetchone()) #180 MAX
            except:
                text = "None"
            conn.close()
            font = ImageFont.truetype("fonts/Ubuntu-Light.ttf", 20)
            draw.text((45, 628), "\n".join(textwrap.wrap(text, width=40)), font=font, fill='rgb(36, 36, 36)')
            # TEXT

            # FINFISHING
            img.save(upload_file, optimize=True)
        await ctx.send(file = discord.File(upload_file))
        os.remove(upload_file)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        upload_file = f"{member.id}_welcome.png"

        # PROFIL BILD
        asset = member.avatar_url_as(size = 128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data).convert('RGBA')
        pfp = pfp.resize((200,200))
        # width, height = pfp.size
        # x = (width - height)//2
        # img_cropped = pfp.crop((x, 0, x+height, height))
        # mask = Image.new('L', img_cropped.size)
        # mask_draw = ImageDraw.Draw(mask)
        # width, height = img_cropped.size
        # mask_draw.ellipse((0, 0, width, height), fill=255)
        # img_cropped.putalpha(mask)
        # PROFIL BILD

        #BACKGROUND
        img = Image.new('RGBA', (800, 200), color = (0, 0, 0, 0))
        panel = Image.open("imgs/panel.png").convert('RGBA')
        # TEXT
        text = member.name
        f_size = 60
        if len(text) > 15:
            f_size = 50
        elif len(text) > 18:
            f_size = 40
        elif len(text) > 23:
            f_size = 30
        elif len(text) > 30:
            f_size = 27
        draw = ImageDraw.Draw(panel)
        font = ImageFont.truetype("fonts/AquireLight.ttf", f_size)
        draw.text((10, 3), f"{text}", font=font, fill='rgb(255, 67, 67)')
        # TEXT
        img.paste(panel, (200, 0))
        img.paste(pfp, (0,0), pfp)
        #BACKGROUND

        img.save(upload_file, optimize=True)
        await self.bot.get_channel(803196358935969802).send(file = discord.File(upload_file))
        os.remove(upload_file)

    # @commands.command()
    # async def test(self, ctx):
    #     member = ctx.author
    #     upload_file = f"{member.id}_welcome.png"
    #     # PROFIL BILD
    #     asset = member.avatar_url_as(size = 128)
    #     data = BytesIO(await asset.read())
    #     pfp = Image.open(data).convert('RGBA')
    #     pfp = pfp.resize((200,200))
    #     # width, height = pfp.size
    #     # x = (width - height)//2
    #     # img_cropped = pfp.crop((x, 0, x+height, height))
    #     # mask = Image.new('L', img_cropped.size)
    #     # mask_draw = ImageDraw.Draw(mask)
    #     # width, height = img_cropped.size
    #     # mask_draw.ellipse((0, 0, width, height), fill=255)
    #     # img_cropped.putalpha(mask)
    #     # PROFIL BILD
    #     #BACKGROUND
    #     img = Image.new('RGBA', (800, 200), color = (0, 0, 0, 0))
    #     panel = Image.open("imgs/panel.png").convert('RGBA')
    #     # TEXT
    #     text = member.name
    #     f_size = 60
    #     if len(text) > 15:
    #         f_size = 50
    #     if len(text) > 18:
    #         f_size = 40
    #     if len(text) > 23:
    #         f_size = 30
    #     if len(text) > 30:
    #         f_size = 27
    #     draw = ImageDraw.Draw(panel)
    #     font = ImageFont.truetype("fonts/AquireLight.ttf", f_size)
    #     draw.text((10, 3), f"{text}", font=font, fill='rgb(255, 67, 67)')
    #     # TEXT
    #     img.paste(panel, (200, 0))
    #     img.paste(pfp, (0,0), pfp)
    #     #BACKGROUND
    #     img.save(upload_file, optimize=True)
    #     await ctx.send(file = discord.File(upload_file))
    #     os.remove(upload_file)

    @commands.command()
    async def status(self, ctx, *, status):
        if len(status) > 180:
            await ctx.send("Status is to 180 characters limited")
            return
        conn = sqlite3.connect('db/status.db')
        c = conn.cursor()
        try:
            t = (ctx.author.id, status)
            c.execute("INSERT INTO status VALUES (?, ?)", t)
        except:
            pass
        try:
            t = (status, ctx.author.id)
            c.execute("UPDATE status SET status = ? WHERE user_id = ?;", t)
        except:
            pass
        
        conn.commit()
        conn.close()
        await ctx.send("Updatet your status!")

def setup(bot):
    bot.add_cog(img(bot))