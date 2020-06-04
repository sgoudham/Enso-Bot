import asyncio
import random

import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown


class Waifus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Bot ~Kakashi command for Zara
    @commands.command(aliases=['Kakashi'])
    @cooldown(1, 0, BucketType.channel)
    async def kakashi(self, ctx):

        channels = ["bot-commands"]

        # path = pathlib.Path(r'C:\Users\sgoud\PycharmProjects\EnsoBot\txtfiles\kakashiImages.txt')
        with open('kakashiImages.txt') as file:
            kakashi_array = file.readlines()

            if str(ctx.channel) in channels:

                # set member as the author
                member = ctx.message.author
                userAvatar = member.avatar_url

                embed = discord.Embed(title="**Hatake Kakashi**", colour=discord.Colour(0xff0000))
                embed.set_image(url=random.choice(kakashi_array))
                embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url='{}'.format(userAvatar))
                await ctx.send(embed=embed)
            else:
                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

    # Bot ~Toga command for Josh
    @commands.command(aliases=['Toga'])
    @cooldown(1, 0, BucketType.channel)
    async def toga(self, ctx):

        channels = ["bot-commands"]

        # path = pathlib.Path(r'C:\Users\sgoud\PycharmProjects\EnsoBot\txtfiles\togaImages.txt')
        with open('togaImages.txt') as file:
            toga_array = file.readlines()

            if str(ctx.channel) in channels:

                member = ctx.message.author  # set member as the author
                userAvatar = member.avatar_url

                embed = discord.Embed(title="**Himiko Toga**", colour=discord.Colour(0xff0000))
                embed.set_image(url=random.choice(toga_array))
                embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url='{}'.format(userAvatar))
                await ctx.send(embed=embed)
            else:
                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        file.close()


def error_function():
    return "Sorry! I only work in #bot-commands!"


def setup(bot):
    bot.add_cog(Waifus(bot))
