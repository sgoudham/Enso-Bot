import asyncio
import datetime
import random

import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown

import config


# Set up the Cog
class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ~kiss command which allows users to kiss a person in the server
    @commands.command(aliases=["Kiss", "kiss"])
    # Added a cooldown, only 1 instance of the command can be sent every second per user
    @cooldown(1, 1, BucketType.user)
    async def kissing(self, ctx, target: discord.Member):

        # Surround with try/except to catch any exceptions that may occur
        try:

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in config.channels:

                # Open the file containing the kissing gifs
                with open('images/FunCommands/kissing.txt') as file:
                    # Store content of the file in kissing_array
                    kissing_array = file.readlines()

                    # Set member as the author
                    member = ctx.message.author
                    # Get the member avatar
                    userAvatar = member.avatar_url

                    # Set up the embed to display a random kissing gif
                    embed = discord.Embed(
                        title=f"<a:huh:676195228872474643> <a:huh:676195228872474643> | **{member.display_name}** kissed **{target.display_name}**",
                        colour=discord.Colour(int(random.choice(config.colour_list))))
                    embed.set_image(url=random.choice(kissing_array))
                    embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url='{}'.format(userAvatar))
                    embed.timestamp = datetime.datetime.utcnow()

                    # Send the embedded message to the user
                    await ctx.send(embed=embed)

            # else the command is sent in an invalid channel
            else:
                # Call error_function() and display it to the user
                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except FileNotFoundError as e:
            print(e)

    # ~kill command which allows users to kill a person in the server
    @commands.command(aliases=["Kill", "k"])
    # Added a cooldown, only 1 instance of the command can be sent every second per user
    @cooldown(1, 1, BucketType.user)
    async def kill(self, ctx, target: discord.Member):

        # Surround with try/except to catch any exceptions that may occur
        try:

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in config.channels:

                # Open the file containing the killing gifs
                with open('images/FunCommands/killing.txt') as file:
                    # Store content of the file in killing_array
                    killing_array = file.readlines()

                    # Set member as the author
                    member = ctx.message.author
                    # Get the member avatar
                    userAvatar = member.avatar_url

                    # Set up the embed to display a random killing gif
                    embed = discord.Embed(
                        title=f"<:monkaW:718960264896184380> <:monkaW:718960264896184380> | **{member.display_name}** killed **{target.display_name}**",
                        colour=discord.Colour(int(random.choice(config.colour_list))))
                    embed.set_image(url=random.choice(killing_array))
                    embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url='{}'.format(userAvatar))
                    embed.timestamp = datetime.datetime.utcnow()

                    # Send the embedded message to the user
                    await ctx.send(embed=embed)

            # else the command is sent in an invalid channel
            else:
                # Call error_function() and display it to the user
                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except FileNotFoundError as e:
            print(e)

    # ~cuddle command which allows users to cuddle a person in the server
    @commands.command(aliases=["Cuddle"])
    # Added a cooldown, only 1 instance of the command can be sent every second per user
    @cooldown(1, 1, BucketType.user)
    async def cuddle(self, ctx, target: discord.Member):

        # Surround with try/except to catch any exceptions that may occur
        try:

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in config.channels:

                # Open the file containing the cuddling gifs
                with open('images/FunCommands/cuddling.txt') as file:
                    # Store content of the file in cuddling_array
                    cuddling_array = file.readlines()

                    # Set member as the author
                    member = ctx.message.author
                    # Get the member avatar
                    userAvatar = member.avatar_url

                    # Set up the embed to display a random cuddling gif
                    embed = discord.Embed(
                        title=f"<:blushlook1:677310734123663363> <:blushlook2:679524467248201769> | **{member.display_name}** cuddled **{target.display_name}**",
                        colour=discord.Colour(int(random.choice(config.colour_list))))
                    embed.set_image(url=random.choice(cuddling_array))
                    embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url='{}'.format(userAvatar))
                    embed.timestamp = datetime.datetime.utcnow()

                    # Send the embedded message to the user
                    await ctx.send(embed=embed)

            # else the command is sent in an invalid channel
            else:
                # Call error_function() and display it to the user
                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except FileNotFoundError as e:
            print(e)

    # ~slap command which allows users to cuddle a person in the server
    @commands.command(aliases=["Slap"])
    # Added a cooldown, only 1 instance of the command can be sent every second per user
    @cooldown(1, 1, BucketType.user)
    async def slap(self, ctx, target: discord.Member):

        # Surround with try/except to catch any exceptions that may occur
        try:

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in config.channels:

                # Open the file containing the cuddling gifs
                with open('images/FunCommands/slapping.txt') as file:
                    # Store content of the file in cuddling_array
                    slapping_array = file.readlines()

                    # Set member as the author
                    member = ctx.message.author
                    # Get the member avatar
                    userAvatar = member.avatar_url

                    # Set up the embed to display a random slapping gif
                    embed = discord.Embed(
                        title=f"<:baka:718942872061083678> <:baka:718942872061083678> | **{member.display_name}** slapped **{target.display_name}**",
                        colour=discord.Colour(int(random.choice(config.colour_list))))
                    embed.set_image(url=random.choice(slapping_array))
                    embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url='{}'.format(userAvatar))
                    embed.timestamp = datetime.datetime.utcnow()

                    # Send the embedded message to the user
                    await ctx.send(embed=embed)

            # else the command is sent in an invalid channel
            else:
                # Call error_function() and display it to the user
                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except FileNotFoundError as e:
            print(e)

    # ~slap command which allows users to cuddle a person in the server
    @commands.command(aliases=["Pat"])
    # Added a cooldown, only 1 instance of the command can be sent every second per user
    @cooldown(1, 1, BucketType.user)
    async def pat(self, ctx, target: discord.Member):

        # Surround with try/except to catch any exceptions that may occur
        try:

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in config.channels:

                # Open the file containing the patting gifs
                with open('images/FunCommands/patting.txt') as file:
                    # Store content of the file in patting_array
                    patting_array = file.readlines()

                    # Set member as the author
                    member = ctx.message.author
                    # Get the member avatar
                    userAvatar = member.avatar_url

                    # Set up the embed to display a random patting gif
                    embed = discord.Embed(
                        title=f"<:baka:718942872061083678> <:baka:718942872061083678> | **{member.display_name}** patted **{target.display_name}**",
                        colour=discord.Colour(int(random.choice(config.colour_list))))
                    embed.set_image(url=random.choice(patting_array))
                    embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url='{}'.format(userAvatar))
                    embed.timestamp = datetime.datetime.utcnow()

                    # Send the embedded message to the user
                    await ctx.send(embed=embed)

            # else the command is sent in an invalid channel
            else:
                # Call error_function() and display it to the user
                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except FileNotFoundError as e:
            print(e)

    # ~lemon command which allows users to hand people lemons to members in the user
    @commands.command(aliases=["lem", "Lemon", "Lem"])
    # Added a cooldown, only 1 instance of the command can be sent every second per user
    @cooldown(1, 1, BucketType.user)
    async def lemon(self, ctx, target: discord.Member):

        lemon_array = ["https://media.discordapp.net/attachments/669812887564320769/720093589056520202/lemon.gif",
                       "https://media.discordapp.net/attachments/669812887564320769/720093575492272208/lemon2.gif",
                       "https://media.discordapp.net/attachments/718484280925224981/719629805263257630/lemon.gif"]

        # Surround with try/except to catch any exceptions that may occur
        try:

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in config.channels:

                # Set member as the author
                member = ctx.message.author
                # Get the member avatar
                userAvatar = member.avatar_url

                # Set up the embed to display a random lemon gif
                embed = discord.Embed(
                    title=f"<a:huh:676195228872474643> <a:huh:676195228872474643> | **{member.display_name}** Gives A Lemon To **{target.display_name}**",
                    colour=discord.Colour(int(random.choice(config.colour_list))))
                embed.set_image(url=random.choice(lemon_array))
                embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url='{}'.format(userAvatar))
                embed.timestamp = datetime.datetime.utcnow()

                # Send the embedded message to the user
                await ctx.send(embed=embed)

                # else the command is sent in an invalid channel
            else:
                # Call error_function() and display it to the user
                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except FileNotFoundError as e:
            print(e)


# Error handling function to make sure that the commands only work in "enso-chan-commands"
def error_function():
    return "Sorry! I only work in #enso-chan-commands!"


def setup(bot):
    bot.add_cog(Embeds(bot))
