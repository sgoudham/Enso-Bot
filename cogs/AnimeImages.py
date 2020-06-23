import asyncio
import datetime
import random
import string

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import settings
from cogs.Embeds import error_function


class Waifus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Bot ~ensoPerson command for the server members
    @commands.command(aliases=['enso', 'Ensoperson'])
    @cooldown(1, 1, BucketType.user)
    async def ensoperson(self, ctx, name=None):
        array = ['hammy', 'hussein', 'inna', 'kaiju', 'kate',
                 'lukas', 'marshall', 'stitch', 'zara', 'josh',
                 'gria', 'lilu', 'marcus', 'eric', 'ifrah',
                 'janet', 'connor', 'taz', 'ryder', 'ange',
                 'izzy', 'david', 'clarity', 'angel', 'chloe',
                 'corona', 'skye']

        def displayServerImage(array, ctx, name):
            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in settings.channels:
                # Set member as the author
                member = ctx.message.author
                userAvatar = member.avatar_url

                embed = discord.Embed(
                    title=f"**Look At What A Cutie {name.capitalize()} is!! <a:huh:676195228872474643> <a:huh:676195228872474643> **",
                    colour=discord.Colour(random.choice(settings.colour_list)))
                embed.set_image(url=random.choice(array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))
                embed.timestamp = datetime.datetime.utcnow()

                return embed

        if name:
            proper_name = name.lower()
            if proper_name == "list":
                await ctx.send(f"Try the names listed below!")

                nice = string.capwords(', '.join(map(str, array)))
                await ctx.send(nice)
                exit()

            try:
                with open(f'images/ServerMembers/{proper_name}.txt') as file:
                    images_array = file.readlines()

                    embed = displayServerImage(images_array, ctx, proper_name)
                    await ctx.send(embed=embed)

            except Exception as e:
                print(e)

                await ctx.send(f"Sorry! That person doesn't exist!! Try the names listed below!")

                nice = string.capwords(', '.join(map(str, array)))
                await ctx.send(nice)

        else:
            with open(f'images/ServerMembers/{random.choice(array)}.txt') as file:
                array = file.readlines()

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in settings.channels:
                # Set member as the author
                member = ctx.message.author
                userAvatar = member.avatar_url

                embed = discord.Embed(
                    title=f"Oh Look! A Cute Person <a:huh:676195228872474643> <a:huh:676195228872474643> ",
                    colour=discord.Colour(random.choice(settings.colour_list)))
                embed.set_image(url=random.choice(array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):

        # Defining the channel and global variables
        global waifu_split_msg
        global husbando_split_msg
        channel = message.channel

        # Defining the message content in lowercase
        user_msg = message.content.lower()

        # Defining array for the list of waifus/husbando's available
        waifu_array = ["toga", "yumeko"]
        husbando_array = ["husk", "kakashi", "tamaki"]

        def randomWaifu(message, waifu_array):
            with open(f'images/AnimeImages/Waifus/{random.choice(waifu_array)}.txt') as file:
                array = file.readlines()

                # Set member as the author
                member = message.author
                # Get the member's avatar
                userAvatar = member.avatar_url

                embed = discord.Embed(
                    title=f"Oh Look! A Cute Waifu! <a:huh:676195228872474643> <a:huh:676195228872474643> ",
                    colour=discord.Colour(random.choice(settings.colour_list)))
                embed.set_image(url=random.choice(array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))
                embed.timestamp = datetime.datetime.utcnow()

                return embed

        def randomHusbando(message, husbando_array):
            with open(f'images/AnimeImages/Husbandos/{random.choice(husbando_array)}.txt') as file:
                array = file.readlines()

                # Set member as the author
                member = message.author
                # Get the member's avatar
                userAvatar = member.avatar_url

                embed = discord.Embed(
                    title=f"Oh Look! A Handsome Husbando! <a:huh:676195228872474643> <a:huh:676195228872474643> ",
                    colour=discord.Colour(random.choice(settings.colour_list)))
                embed.set_image(url=random.choice(array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))
                embed.timestamp = datetime.datetime.utcnow()

                return embed

        # Function to allow modular code and sets up the embed for the
        def displayAnimeImage(array, message, name):
            # If the channel that the command has been sent is in the list of accepted channels
            if str(message.channel) in settings.channels:
                # Set member as the author
                member = message.author
                # Get the member's avatar
                userAvatar = member.avatar_url

                embed = discord.Embed(
                    title=f"**{name.capitalize()}**",
                    colour=discord.Colour(random.choice(settings.colour_list)))
                embed.set_image(url=random.choice(array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))
                embed.timestamp = datetime.datetime.utcnow()

                return embed

        # If the channel that the command has been sent is in the list of accepted channels
        if str(channel) in settings.channels:

            # Surround with try/except to catch any exceptions that may occur
            try:

                if 'w random' in user_msg:
                    embed = randomWaifu(message, waifu_array)
                    await channel.send(embed=embed)

                elif user_msg.startswith('~w'):
                    waifu_split_msg = user_msg.split("w ", 1)
                    w_array = str(waifu_split_msg[-1]).lower()

                    with open(f'images/AnimeImages/Waifus/{w_array}.txt') as file:
                        images_array = file.readlines()

                    embed = displayAnimeImage(images_array, message, w_array)
                    await channel.send(embed=embed)

            except FileNotFoundError as e:
                print(e)

                await channel.send(f"Sorry! That Waifu doesn't exist!! Try the Waifu's listed below!")

                nice = string.capwords(', '.join(map(str, waifu_array)))
                await channel.send(nice)

            # Surround with try/except to catch any exceptions that may occur
            try:

                if 'h random' in user_msg:
                    embed = randomHusbando(message, husbando_array)
                    await channel.send(embed=embed)

                elif user_msg.startswith('~h'):

                    husbando_split_msg = user_msg.split("h ", 1)
                    h_array = str(husbando_split_msg[-1]).lower()

                    with open(f'images/AnimeImages/Husbandos/{h_array}.txt') as file:
                        images_array = file.readlines()

                        embed = displayAnimeImage(images_array, message, h_array)

                        await channel.send(embed=embed)

            except FileNotFoundError as e:
                print(e)

                await channel.send(f"Sorry! That Husbando doesn't exist!! Try the Husbando's listed below!")

                nice = string.capwords(', '.join(map(str, husbando_array)))
                await channel.send(nice)

        else:
            if user_msg.endswith('~w') or user_msg.endswith('~h'):
                message = await channel.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()


def setup(bot):
    bot.add_cog(Waifus(bot))
