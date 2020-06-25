import asyncio
import datetime
import random
import string

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import settings
from cogs.Embeds import error_function

# Defining the full names of the waifu's/husbando's
anime = {"yumeko": "Jabami Yumeko",
         "toga": "Himiko Toga",
         "kakashi": "Hatake Kakashi",
         "tamaki": "Tamaki Suoh",
         "husk": "Husk"
         }


# Function to turn the user inputted name into the full name
def Abbrev(anime_msg):
    # Get the lowercase
    lowercase_anime = anime_msg.lower()
    split_anime = lowercase_anime.split()
    new_msg = ""
    # For each word in split_anime
    for word in split_anime:
        # If the word exists in the anime array
        if word in anime:
            # Set a new string equal to the full name of the waifu/husbando
            new_msg = anime[word]

    return new_msg


# Function to return a random image of a waifu
def randomWaifu(msg, waifu):
    # Retrieve a random image of a waifu within the bot
    with open(f'images/AnimeImages/Waifus/{random.choice(waifu)}.txt') as file:
        array = file.readlines()

    # Set member as the author
    member = msg.author
    # Get the member's avatar
    userAvatar = member.avatar_url

    # Set up the embed for a random waifu image
    waifu_embed = discord.Embed(
        title=f"Oh Look! A Wonderful Waifu! <a:huh:676195228872474643> <a:huh:676195228872474643> ",
        colour=discord.Colour(random.choice(settings.colour_list)))
    waifu_embed.set_image(url=random.choice(array))
    waifu_embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))
    waifu_embed.timestamp = datetime.datetime.utcnow()

    return waifu_embed


# Function to return a random image of a husbando
def randomHusbando(msg, husbando):
    # Retrieve a random image of a husbando within the bot
    with open(f'images/AnimeImages/Husbandos/{random.choice(husbando)}.txt') as file:
        array = file.readlines()

    # Set member as the author
    member = msg.author
    # Get the member's avatar
    userAvatar = member.avatar_url

    # Set up the embed for a random husbando image
    husbando_embed = discord.Embed(
        title=f"Oh Look! A Handsome Husbando! <a:huh:676195228872474643> <a:huh:676195228872474643> ",
        colour=discord.Colour(random.choice(settings.colour_list)))
    husbando_embed.set_image(url=random.choice(array))
    husbando_embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))
    husbando_embed.timestamp = datetime.datetime.utcnow()

    return husbando_embed


# Function to allow modular code and sets up the embed for the anime images
def displayAnimeImage(array, msg, name):
    # Set member as the author
    member = msg.author
    # Get the member's avatar
    userAvatar = member.avatar_url

    # Set up embed for an image relating to a husbando or waifu
    anime_embed = discord.Embed(
        title=f"**{name}**",
        colour=discord.Colour(random.choice(settings.colour_list)))
    anime_embed.set_image(url=random.choice(array))
    anime_embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))
    anime_embed.timestamp = datetime.datetime.utcnow()

    return anime_embed


class Waifus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Bot ~ensoPerson command for the server members
    @commands.command(aliases=['enso', 'Ensoperson'])
    @cooldown(1, 1, BucketType.user)
    async def ensoperson(self, ctx, name=None):

        # Defining array of all the people that have images stored in the bot
        array = ['hammy', 'hussein', 'inna', 'kaiju', 'kate',
                 'lukas', 'marshall', 'stitch', 'zara', 'josh',
                 'gria', 'lilu', 'marcus', 'eric', 'ifrah',
                 'janet', 'connor', 'taz', 'ryder', 'ange',
                 'izzy', 'david', 'clarity', 'angel', 'chloe',
                 'corona', 'skye']

        # Function to display all the images requested of the people
        def displayServerImage(array, ctx, name):
            # Set member as the author
            member = ctx.message.author
            # Get the member's avatar
            userAvatar = member.avatar_url

            # Set embed up for the person requested by the user
            embed = discord.Embed(
                title=f"**Look At What A Cutie {name.capitalize()} is!! <a:huh:676195228872474643> <a:huh:676195228872474643> **",
                colour=discord.Colour(random.choice(settings.colour_list)))
            embed.set_image(url=random.choice(array))
            embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))
            embed.timestamp = datetime.datetime.utcnow()

            return embed

        # If the channel that the command has been sent is in the list of accepted channels
        if str(ctx.channel) in settings.channels:

            # if a name is specified
            if name:
                # Get the lowercase
                proper_name = name.lower()

                # if the user does ~enso list
                if proper_name == "list":
                    # Tell the user to try the names in the array
                    await ctx.send(f"Try the names listed below!")

                    # Send the list of members in the bot to the channel
                    nice = string.capwords(', '.join(map(str, array)))
                    await ctx.send(nice)
                    exit()

                # Surround with try/except to catch any exceptions that may occur
                try:

                    # Retrieve image of the member specified
                    with open(f'images/ServerMembers/{proper_name}.txt') as file:
                        images_array = file.readlines()

                    # Embed the image into a message and send it to the channel
                    embed = displayServerImage(images_array, ctx, proper_name)
                    await ctx.send(embed=embed)

                except Exception as e:
                    print(e)

                    # Send error message saying that the person isn't recognised
                    await ctx.send(f"Sorry! That person doesn't exist!! Try the names listed below!")

                    # Send the list of available members to the channel
                    nice = string.capwords(', '.join(map(str, array)))
                    await ctx.send(nice)

            # Else if the name is not specified
            else:

                # Retrieve a random image of a member in the bot
                with open(f'images/ServerMembers/{random.choice(array)}.txt') as file:
                    array = file.readlines()

                # Set member as the author
                member = ctx.message.author
                # Get the member's avatar
                userAvatar = member.avatar_url

                # Embed the image in a message and send it to the channel
                embed = discord.Embed(
                    title=f"Oh Look! A Cute Person <a:huh:676195228872474643> <a:huh:676195228872474643> ",
                    colour=discord.Colour(random.choice(settings.colour_list)))
                embed.set_image(url=random.choice(array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))
                embed.timestamp = datetime.datetime.utcnow()

                await ctx.send(embed=embed)

        else:

            message = await ctx.send(error_function())

            # Let the user read the message for 2.5 seconds
            await asyncio.sleep(2.5)
            # Delete the message
            await message.delete()

    # Cog on_message for waifus and husbandos
    @commands.Cog.listener()
    # Cooldown NOT WORKING
    @cooldown(1, 1, BucketType.user)
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

        # If the channel that the command has been sent is in the list of accepted channels
        if str(channel) in settings.channels:

            # Surround with try/except to catch any exceptions that may occur
            try:

                # Makes sure that the user wants a random image of a waifu
                if 'w random' in user_msg:

                    # Get embed from randomWaifu() and send it to the channel
                    embed = randomWaifu(message, waifu_array)
                    await channel.send(embed=embed)

                # Makes sure that the user wants a specific image of a waifu
                elif user_msg.startswith('~w'):

                    # Define who the waifu is using string splitting
                    waifu_split_msg = user_msg.split("w ", 1)
                    w_array = str(waifu_split_msg[-1]).lower()

                    # Retrieve the image of the waifu that the user has specified
                    with open(f'images/AnimeImages/Waifus/{w_array}.txt') as file:
                        images_array = file.readlines()

                    # Get the full name of the waifu
                    full_name = Abbrev(w_array)

                    # Get the embed from a displayAnimeImage() and send it to the channel
                    embed = displayAnimeImage(images_array, message, full_name)
                    await channel.send(embed=embed)

            except FileNotFoundError as e:
                print(e)

                # Throw error message saying no waifu's could be found
                await channel.send(f"Sorry! That Waifu doesn't exist!! Try the Waifu's listed below!")

                # Send list of suitable waifu's to the channel
                nice = string.capwords(', '.join(map(str, waifu_array)))
                await channel.send(nice)

            # Surround with try/except to catch any exceptions that may occur
            try:

                # Makes sure that the user wants a random image of a husbando
                if 'h random' in user_msg:

                    # Get embed from randomHusbando() and send it to the channel
                    embed = randomHusbando(message, husbando_array)
                    await channel.send(embed=embed)

                # Makes sure that the user wants a specific image of a husbando
                elif user_msg.startswith('~h'):
                    # Making sure that the commands don't conflict with ~help
                    if user_msg.endswith('~help'):
                        return

                    # Define who the husbando is using string splitting
                    husbando_split_msg = user_msg.split("h ", 1)
                    h_array = str(husbando_split_msg[-1]).lower()

                    # Retrieve the image of the Husbando that the user has specified
                    with open(f'images/AnimeImages/Husbandos/{h_array}.txt') as file:
                        images_array = file.readlines()

                    # Get the full name of the husbando
                    full_name = Abbrev(h_array)

                    # Get the embed from a displayAnimeImage() and send it to the channel
                    embed = displayAnimeImage(images_array, message, full_name)
                    await channel.send(embed=embed)

            except FileNotFoundError as e:
                print(e)

                # Throw error message saying no husbando's could be found
                await channel.send(f"Sorry! That Husbando doesn't exist!! Try the Husbando's listed below!")

                # Send list of suitable Husbando's to the channel
                nice = string.capwords(', '.join(map(str, husbando_array)))
                await channel.send(nice)

        # if the message is outwith the enso-chan-commands
        else:
            # Makes sure that the user only typed ~w or ~h
            if user_msg.endswith('~w') or user_msg.endswith('~h'):
                # Send error message
                message = await channel.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()


def setup(bot):
    bot.add_cog(Waifus(bot))
