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
         "maki": "Maki Oze",
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


class Waifus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Bot ~ensoPerson command for the server members
    @commands.command(aliases=['enso'])
    @cooldown(1, 1, BucketType.user)
    async def ensoperson(self, ctx, name=None):

        # Defining array of all the people that have images stored in the bot
        array = ['hammy', 'hussein', 'inna', 'kaiju', 'kate',
                 'lukas', 'marshall', 'stitch', 'zara', 'josh',
                 'gria', 'lilu', 'marcus', 'eric', 'ifrah',
                 'janet', 'connor', 'taz', 'ryder', 'ange',
                 'izzy', 'david', 'clarity', 'angel', 'chloe',
                 'corona', 'skye', 'rin']

        # If the channel that the command has been sent is in the list of accepted channels
        if str(ctx.channel) in settings.channels:

            # if a name is specified
            if name:
                # Get the lowercase
                proper_name = name.lower()

                # Surround with try/except to catch any exceptions that may occur
                try:

                    # if the user does ~enso list
                    if proper_name == "list":
                        # Tell the user to try the names in the array
                        await ctx.send(f"Try the names listed below!")

                        # Send the list of members in the bot to the channel
                        server_members = string.capwords(', '.join(map(str, array)))
                        await ctx.send(server_members)

                    else:

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

    @commands.command(aliases=['W'])
    @cooldown(1, 1, BucketType.user)
    async def w(self, ctx, waifu=None):

        # Defining array for the list of waifus available
        waifu_array = ["toga", "yumeko", "maki"]

        # If the channel that the command has been sent is in the list of accepted channels
        if str(ctx.channel) in settings.channels:

            # if a name is specified
            if waifu:
                # Get the lowercase
                proper_waifu = waifu.lower()

                # if the user does ~w list
                if proper_waifu == "list":
                    # Tell the user to try the waifus in the array
                    await ctx.send(f"Try the waifu's listed below!")

                    # Send the list of waifus in the bot to the channel
                    waifu_list = string.capwords(', '.join(map(str, waifu_array)))
                    await ctx.send(waifu_list)

                else:
                    # Surround with try/except to catch any exceptions that may occur
                    try:

                        # Retrieve image of the waifu specified
                        with open(f'images/AnimeImages/Waifus/{proper_waifu}.txt') as file:
                            w_array = file.readlines()

                        # Get the full name of the waifu
                        full_name = Abbrev(proper_waifu)

                        # Embed the image into a message and send it to the channel
                        embed = displayAnimeImage(w_array, ctx, full_name)
                        await ctx.send(embed=embed)

                    except Exception as e:
                        print(e)

                        # Send error message saying that the person isn't recognised
                        await ctx.send(f"Sorry! That waifu doesn't exist!"
                                       f"\nPlease do **~w list** to see the list of waifu's")
            else:

                # Get embed from randomWaifu() and send it to the channel
                embed = randomWaifu(ctx, waifu_array)
                await ctx.send(embed=embed)

    @commands.command(aliases=['H'])
    @cooldown(1, 1, BucketType.user)
    async def h(self, ctx, husbando=None):

        # Defining array for the list of husbando's available
        husbando_array = ["husk", "kakashi", "tamaki"]

        # If the channel that the command has been sent is in the list of accepted channels
        if str(ctx.channel) in settings.channels:

            # if a name is specified
            if husbando:
                # Get the lowercase
                proper_husbando = husbando.lower()

                # Surround with try/except to catch any exceptions that may occur
                try:

                    # if the user does ~w list
                    if proper_husbando == "list":
                        # Tell the user to try the waifus in the array
                        await ctx.send(f"Try the husbando's listed below!")

                        # Send the list of waifus in the bot to the channel
                        husbando_list = string.capwords(', '.join(map(str, husbando_array)))
                        await ctx.send(husbando_list)

                    else:
                        # Retrieve image of the husbando specified
                        with open(f'images/AnimeImages/Husbandos/{proper_husbando}.txt') as file:
                            h_array = file.readlines()

                        # Get the full name of the husbando
                        full_name = Abbrev(proper_husbando)

                        # Embed the image into a message and send it to the channel
                        embed = displayAnimeImage(h_array, ctx, full_name)
                        await ctx.send(embed=embed)

                except Exception as e:
                    print(e)

                    # Send error message saying that the person isn't recognised
                    await ctx.send(
                        f"Sorry! That husbando doesn't exist!"
                        f"\nPlease do **~h list** to see the list of husbando's")
            else:

                # Get embed from randomHusbando() and send it to the channel
                embed = randomHusbando(ctx, husbando_array)
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Waifus(bot))
