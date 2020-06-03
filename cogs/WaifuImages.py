import random
import asyncio
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

        if str(ctx.channel) not in channels:
            message = await ctx.send(error_function())

            # Let the user read the message for 2.5 seconds
            await asyncio.sleep(2.5)
            # Delete the message
            await message.delete()

        with open('kakashiImages.txt') as file:
            kakashi_array = file.readlines()

        if str(ctx.channel) in channels:

            embed = discord.Embed(title="```Random Kakashi Image```", colour=discord.Colour(0xff0000), )
            embed.set_image(url=random.choice(kakashi_array))
            await ctx.send(embed=embed)

        file.close()


def error_function():
    return "Sorry! I only work in #bot-commands!"


def setup(bot):
    bot.add_cog(Waifus(bot))
