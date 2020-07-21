import datetime
import random
import string

from discord import Embed, Colour
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, command

from settings import colour_list

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

    # Get the member and the userAvatar
    member, userAvatar = getMember(msg)

    # Set up the embed for a random waifu image
    waifu_embed = Embed(
        title=f"Oh Look! A Wonderful Waifu! <a:huh:676195228872474643> <a:huh:676195228872474643> ",
        colour=Colour(random.choice(colour_list)),
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
        colour=Colour(random.choice(colour_list)),
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
        colour=Colour(random.choice(colour_list)),
        timestamp=datetime.datetime.utcnow())
    anime_embed.set_image(url=random.choice(array))
    anime_embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

    return anime_embed


class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Bot ~w/waifu command for the waifu's stored in the bot
    @command(name="w", aliases=['W'])
    @cooldown(1, 1, BucketType.user)
    async def waifu(self, ctx, waifu=None):

        # Defining array for the list of waifus available
        waifu_array = ["toga", "yumeko", "maki"]

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

    # Bot ~h/husbando command for the husbando's stored in the bot
    @command(name="h", aliases=['H'])
    @cooldown(1, 1, BucketType.user)
    async def husbando(self, ctx, husbando=None):

        # Defining array for the list of husbando's available
        husbando_array = ["husk", "kakashi", "tamaki"]

        # if a name is specified
        if husbando:
            # Get the lowercase
            proper_husbando = husbando.lower()

            # Surround with try/except to catch any exceptions that may occur
            try:

                # if the user does ~h list
                if proper_husbando == "list":
                    # Tell the user to try the husbando's in the array
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
    bot.add_cog(Anime(bot))
