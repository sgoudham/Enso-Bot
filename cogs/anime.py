import datetime
import random
import string
from typing import Optional

from discord import Embed
from discord.ext.commands import bot_has_permissions, Cog, group

from settings import rndColour

# Defining the full names of the waifu's/husbando's
anime = {"yumeko": "Jabami Yumeko",
         "toga": "Himiko Toga",
         "maki": "Maki Oze",
         "kakashi": "Hatake Kakashi",
         "tamaki": "Tamaki Suoh",
         "husk": "Husk"
         }


# Gets the member and user avatar
def getMember(msg):
    # Set member as the author
    member = msg.author
    # Get the member avatar
    userAvatar = member.avatar_url

    return member, userAvatar


# Function to turn the user inputted name into the full name
def Abbrev(anime_msg):
    # Get the lowercase
    split_anime = anime_msg.split()
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

    # Get the member and the userAvatar
    member, userAvatar = getMember(msg)

    # Set up the embed for a random waifu image
    waifu_embed = Embed(
        title=f"Oh Look! A Wonderful Waifu! <a:huh:676195228872474643> <a:huh:676195228872474643> ",
        colour=rndColour(),
        timestamp=datetime.datetime.utcnow())
    waifu_embed.set_image(url=random.choice(array))
    waifu_embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

    return waifu_embed


# Function to return a random image of a husbando
def randomHusbando(msg, husbando):
    # Retrieve a random image of a husbando within the bot
    with open(f'images/AnimeImages/Husbandos/{random.choice(husbando)}.txt') as file:
        array = file.readlines()

    # Get the member and the userAvatar
    member, userAvatar = getMember(msg)

    # Set up the embed for a random husbando image
    husbando_embed = Embed(
        title=f"Oh Look! A Handsome Husbando! <a:huh:676195228872474643> <a:huh:676195228872474643> ",
        colour=rndColour(),
        timestamp=datetime.datetime.utcnow())
    husbando_embed.set_image(url=random.choice(array))
    husbando_embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

    return husbando_embed


# Function to allow modular code and sets up the embed for the anime images
def displayAnimeImage(array, msg, name):
    # Get the member and the userAvatar
    member, userAvatar = getMember(msg)

    # Set up embed for an image relating to a husbando or waifu
    anime_embed = Embed(
        title=f"**{name}**",
        colour=rndColour(),
        timestamp=datetime.datetime.utcnow())
    anime_embed.set_image(url=random.choice(array))
    anime_embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

    return anime_embed


# List of Waifu's
def waifus():
    return ["toga", "yumeko", "maki"]


# List of Husbando's
def husbandos():
    return ["kakashi", "tamaki"]


class Anime(Cog):
    """Waifus and Husbandos!"""

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        """Printing out that Cog is ready on startup"""
        print(f"{self.__class__.__name__} Cog has been loaded!\n-----")

    @group(invoke_without_command=True)
    @bot_has_permissions(embed_links=True)
    async def waifu(self, ctx, waifu: Optional[str] = None):
        """Shows a Waifu"""

        if waifu:
            lcase_waifu = waifu.lower()

            try:

                # Retrieve image of the waifu specified
                with open(f'images/AnimeImages/Waifus/{lcase_waifu}.txt') as file:
                    w_array = file.readlines()

                # Get the full name of the waifu
                full_name = Abbrev(lcase_waifu)

                # Embed the image into a message and send it to the channel
                embed = displayAnimeImage(w_array, ctx, full_name)
                await ctx.send(embed=embed)

            except FileNotFoundError as e:
                print(e)

                # Send error message saying that the person isn't recognised
                await ctx.send(f"Sorry! That waifu doesn't exist!"
                               f"\nPlease do **{ctx.prefix}waifu list** to see the list of Waifu's")
        else:

            # Get embed from randomWaifu() and send it to the channel
            embed = randomWaifu(ctx, waifus())
            await ctx.send(embed=embed)

    @group(invoke_without_command=True)
    @bot_has_permissions(embed_links=True)
    async def husbando(self, ctx, husbando: Optional[str] = None):
        """Shows a Husbando"""

        if husbando:
            # Get the lowercase
            lcase_husbando = husbando.lower()

            try:
                # Retrieve image of the husbando specified
                with open(f'images/AnimeImages/Husbandos/{lcase_husbando}.txt') as file:
                    h_array = file.readlines()

                # Get the full name of the husbando
                full_name = Abbrev(lcase_husbando)

                # Embed the image into a message and send it to the channel
                embed = displayAnimeImage(h_array, ctx, full_name)
                await ctx.send(embed=embed)

            except FileNotFoundError as e:
                print(e)

                # Send error message saying that the person isn't recognised
                await ctx.send(
                    f"Sorry! That husbando doesn't exist!"
                    f"\nPlease do **{ctx.prefix}h list** to see the list of husbando's")

        else:

            # Get embed from randomHusbando() and send it to the channel
            embed = randomHusbando(ctx, husbandos())
            await ctx.send(embed=embed)

    @waifu.command(name="list")
    async def wlist(self, ctx):
        """Returns a list of Waifu's Available"""

        # Send the list of waifus in the bot to the channel
        waifu_list = string.capwords(', '.join(map(str, waifus())))

        # Tell the user to try the waifus in the array
        await ctx.send(f"Try the waifu's listed below!"
                       f"\n{waifu_list}")

    @husbando.command(name="list")
    async def hlist(self, ctx):
        """Returns a list of Husbando's Available"""

        # Send the list of waifus in the bot to the channel
        husbando_list = string.capwords(', '.join(map(str, husbandos())))

        # Tell the user to try the husbando's in the array
        await ctx.send(f"Try the husbando's listed below!"
                       f"\n{husbando_list}")


def setup(bot):
    bot.add_cog(Anime(bot))
