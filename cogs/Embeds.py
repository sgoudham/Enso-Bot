import asyncio
import datetime
import random

import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown

import config
from cogs.FunCommands import error_function

colour_list = [c for c in config.colors.values()]
channels = ["enso-chan-commands", 'general']


class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["Kiss", "kiss"])
    @cooldown(1, 0.5, BucketType.channel)
    async def kissing(self, ctx, target: discord.Member):

        try:
            if str(ctx.channel) in channels:

                with open('images/FunCommands/kissing.txt') as file:
                    kissing_array = file.readlines()

                    # set member as the author
                    member = ctx.message.author
                    userAvatar = member.avatar_url

                    embed = discord.Embed(
                        title=f"<:blushlook1:677310734123663363> <:blushlook2:679524467248201769> | **{member.display_name}** kissed **{target.display_name}**",
                        colour=discord.Colour(int(random.choice(colour_list))))
                    embed.set_image(url=random.choice(kissing_array))
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

    @commands.command(aliases=["Cuddle", "cdle", "cud"])
    @cooldown(1, 0.5, BucketType.channel)
    async def cuddle(self, ctx, target: discord.Member):

        try:
            if str(ctx.channel) in channels:

                with open('images/FunCommands/cuddling.txt') as file:
                    cuddling_array = file.readlines()

                    # set member as the author
                    member = ctx.message.author
                    userAvatar = member.avatar_url

                    embed = discord.Embed(
                        title=f"<a:huh:676195228872474643> <a:huh:676195228872474643> | **{member.display_name}** cuddles **{target.display_name}**",
                        colour=discord.Colour(int(random.choice(colour_list))))
                    embed.set_image(url=random.choice(cuddling_array))
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

    @commands.command(aliases=["lem", "Lemon", "Lem"])
    @cooldown(1, 2, BucketType.channel)
    async def lemon(self, ctx, target: discord.Member):

        lemon_array = ["https://media.discordapp.net/attachments/669812887564320769/720093589056520202/lemon.gif",
                       "https://media.discordapp.net/attachments/669812887564320769/720093575492272208/lemon2.gif",
                       "https://media.discordapp.net/attachments/718484280925224981/719629805263257630/lemon.gif"]
        try:
            if str(ctx.channel) in channels:

                # set member as the author
                member = ctx.message.author
                userAvatar = member.avatar_url

                embed = discord.Embed(
                    title=f"<a:huh:676195228872474643> <a:huh:676195228872474643> | **{member.display_name}** Gives A Lemon To **{target.display_name}**",
                    colour=discord.Colour(int(random.choice(colour_list))))
                embed.set_image(url=random.choice(lemon_array))
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


def setup(bot):
    bot.add_cog(Embeds(bot))
