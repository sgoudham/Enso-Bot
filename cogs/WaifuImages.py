import asyncio
import datetime
import random

import discord
from discord.ext import commands

channels = ["bot-commands"]

colours = [0xff0000, 0x5825ff, 0xff80ed, 0xa0f684, 0x7700cc, 0x0b04d9, 0x3d04ae, 0x000033,
           0x00FFFF,
           0x120A8F, 0x7FFF0, 0xcc3300,
           0x5E260, 0xcc0000, 0x0066cc, 0x7632cd, 0x76a7cd, 0xffa7cd, 0xff24cd, 0xff2443,
           0xff7d43,
           0xb52243, 0xb522ce, 0xb5f43d]


class Waifus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Bot ~Kakashi command for Zara
    @commands.command(aliases=['Kakashi'])
    async def kakashi(self, ctx):

        try:

            with open('images/kakashiImages.txt') as file:
                kakashi_array = file.readlines()

            if str(ctx.channel) in channels:

                # set member as the author
                member = ctx.message.author
                userAvatar = member.avatar_url

                embed = discord.Embed(title="**Hatake Kakashi**", colour=discord.Colour(random.choice(colours)))
                embed.set_image(url=random.choice(kakashi_array))
                embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url='{}'.format(userAvatar))
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

            else:

                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except FileNotFoundError as e:
            print(e)

    # Bot ~Toga command for Josh
    @commands.command(aliases=['Toga'])
    async def toga(self, ctx):

        try:

            with open('images/togaImages.txt') as file:
                toga_array = file.readlines()

                if str(ctx.channel) in channels:

                    member = ctx.message.author  # set member as the author
                    userAvatar = member.avatar_url

                    embed = discord.Embed(title="**Himiko Toga**", colour=discord.Colour(int(random.choice(colours))))
                    embed.set_image(url=random.choice(toga_array))
                    embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url='{}'.format(userAvatar))
                    embed.timestamp = datetime.datetime.utcnow()
                    await ctx.send(embed=embed)

                else:

                    message = await ctx.send(error_function())

                    # Let the user read the message for 2.5 seconds
                    await asyncio.sleep(2.5)
                    # Delete the message
                    await message.delete()

        except FileNotFoundError as e:
            print(e)

    # Bot ~Tamaki command for Kate
    @commands.command(aliases=['Tamaki'])
    async def tamaki(self, ctx):

        try:
            with open('images/tamakiImages.txt') as file:
                tamaki_array = file.readlines()

            if str(ctx.channel) in channels:

                # set member as the author
                member = ctx.message.author
                userAvatar = member.avatar_url

                embed = discord.Embed(title="**Tamaki Suoh**", colour=discord.Colour(random.choice(colours)))
                embed.set_image(url=random.choice(tamaki_array))
                embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url='{}'.format(userAvatar))
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

            else:

                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()
        except FileNotFoundError as e:
            print(e)


# Error handling function to make sure that the commands only work in bot-commands
def error_function():
    return "Sorry! I only work in #bot-commands!"


def setup(bot):
    bot.add_cog(Waifus(bot))
