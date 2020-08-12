import datetime
import random
from typing import Optional

import aiohttp
from decouple import config
from discord import Embed
from discord.ext import menus
from discord.ext.commands import bot_has_permissions, Cog, group

from settings import rndColour, enso_embedmod_colours

my_waifu_list_auth = config('MYWAIFULIST_AUTH')

# Defining the full names of the waifu's/husbando's
anime = {"yumeko": "Jabami Yumeko",
         "toga": "Himiko Toga",
         "maki": "Maki Oze",
         "kakashi": "Hatake Kakashi",
         "tamaki": "Tamaki Suoh",
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


def randomWaifu(msg, waifu):
    """Return Embed for Specific Waifu"""

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


def randomHusbando(msg, husbando):
    """Display embed for Specific Husbando"""

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


def displayAnimeImage(array, msg, name):
    """Setup Embed for Specific Waifu/Husbando"""

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


def waifus():
    """List of Waifu's"""
    return ["toga", "yumeko", "maki"]


def husbandos():
    """List of Husbando's"""
    return ["kakashi", "tamaki"]


def store_waifus(waifus_dict, waifu, value):
    """Method to store waifu's in the new dict"""

    waifus_dict[waifu["name"]][value] = waifu[value]


def multiple_waifu_generator(waifus_dict):
    """Method to generate embed of multiple waifu's"""

    embeds = []
    for key in waifus_dict.values():
        embed = Embed(title=key["name"], description=f"{key['original_name']} | {key['type']}",
                      colour=rndColour(),
                      url=key["url"])
        embed.set_image(url=key["display_picture"])
        embed.set_footer(text=f"❤️ {key['likes']} 🗑️ {key['trash']} | Powered by MyWaifuList")

        embeds.append(embed)

    return embeds


def single_waifu_generator(waifu):
    """Method to generate embed of single waifu's"""

    # Get all the data to be displayed in the embed
    name = waifu["name"]
    og_name = waifu["original_name"]
    picture = waifu["display_picture"]
    url = waifu["url"]
    likes = waifu["likes"]
    trash = waifu["trash"]
    waifu_type = waifu["type"]

    # Set up the embed
    embed = Embed(title=name, description=f"{og_name} | {waifu_type}",
                  colour=rndColour(),
                  url=url)
    embed.set_image(url=picture)
    embed.set_footer(text=f"❤️ {likes} 🗑️ {trash} | Powered by MyWaifuList")

    return embed


# Set up the Cog
class HelpMenu(menus.Menu):
    def __init__(self, i, waifu, bot, botter):
        super().__init__(timeout=125.0, clear_reactions_after=True)
        self.waifus_dict = waifu
        self.i = i
        self.waifu = multiple_waifu_generator(self.waifus_dict)
        self.bot = bot
        self.botter = botter

    # Message to be sent on the initial command ~help
    async def send_initial_message(self, ctx, channel):
        # Set the first embed to the first element in the pages[]

        initial = multiple_waifu_generator(self.waifus_dict)[self.i]

        cur_page = self.i + 1
        pages = len(self.waifu)
        initial.set_author(name=f"Page {cur_page}/{pages}")

        # Send embed
        return await channel.send(embed=initial)

    # Reaction to allow user to go to the previous page in the embed
    @menus.button('\N{LEFTWARDS BLACK ARROW}')
    async def on_left_arrow(self, payload):

        # Simple check to make sure that the reaction is performed by the user
        def check(m):
            return m.author == payload.member

        # Do nothing if the check does not return true
        if check(self.ctx):
            # Set self.i to (i - 1) remainder length of the array
            self.i = (self.i - 1) % len(multiple_waifu_generator(self.waifus_dict))
            prev_page = multiple_waifu_generator(self.waifus_dict)[self.i]

            cur_page = self.i + 1
            pages = len(self.waifu)
            prev_page.set_author(name=f"Page {cur_page}/{pages}")

            # Send the embed and remove the reaction of the user
            await self.message.edit(embed=prev_page)
            if self.botter.guild_permissions.manage_messages:
                await self.message.remove_reaction("⬅", self.ctx.author)

    # Reaction to allow user to go to the next page in the embed
    @menus.button('\N{BLACK RIGHTWARDS ARROW}')
    async def on_right_arrow(self, payload):

        # Simple check to make sure that the reaction is performed by the user
        def check(m):
            return m.author == payload.member

        # Do nothing if the check does not return true
        if check(self.ctx):
            # Set self.i to (i + 1) remainder length of the array
            self.i = (self.i + 1) % len(multiple_waifu_generator(self.waifus_dict))
            next_page = multiple_waifu_generator(self.waifus_dict)[self.i]

            cur_page = self.i + 1
            pages = len(self.waifu)
            next_page.set_author(name=f"Page {cur_page}/{pages}")

            # Send the embed and remove the reaction of the user
            await self.message.edit(embed=next_page)
            if self.botter.guild_permissions.manage_messages:
                await self.message.remove_reaction("➡", self.ctx.author)

    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def on_stop(self, payload):

        # Simple check to make sure that the reaction is performed by the user
        def check(m):
            return m.author == payload.member

        # Do nothing if the check does not return true
        if check(self.ctx):
            # Delete the embed and stop the function from running
            await self.message.delete()
            self.stop()


class Anime(Cog):
    """Waifus and Husbandos!"""

    def __init__(self, bot):
        self.bot = bot
        self.headers = {'apikey': my_waifu_list_auth}

    @Cog.listener()
    async def on_ready(self):
        """Printing out that Cog is ready on startup"""
        print(f"{self.__class__.__name__} Cog has been loaded!\n-----")

    @group(name="waifu", invoke_without_command=True, aliases=["Waifu"])
    @bot_has_permissions(embed_links=True, add_reactions=True)
    async def waifu(self, ctx, *, waifu2: Optional[str] = None):
        """
        Shows a Waifu (UNDER CONSTRUCTION)
        Waifu's are grabbed from mywaifulist.com
        """

        # Local Variable i to allow the index of the pages[] to be modified
        i = 0

        # When a waifu has been specified, retrieve waifu(s) matching the user input
        if waifu2:

            waifus_dict = {}
            url = "https://mywaifulist.moe/api/v1/search/"
            data = {"term": waifu2,
                    'content-type': "application/json"}

            # Searching API for waifu(s)
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=data, headers=self.headers) as resp:
                    # Store waifu's in dict when request is successful, else send an error
                    if resp.status == 200:
                        waifu_dict = await resp.json()

                    # Send error if something went wrong internally/while grabbing data from API
                    else:
                        await ctx.send("Something went wrong!")

            # As long waifu's were returned from the GET request
            # Store waifus in a dict
            if len(waifu_dict["data"]) > 0:
                for waifu in waifu_dict["data"]:

                    # Only store "Waifu's" and "Husbando's"
                    if waifu["type"] in ["Waifu", "Husbando"]:
                        waifus_dict[waifu["name"]] = {}
                        for value in waifu:
                            store_waifus(waifus_dict, waifu, value)
                    else:
                        break

            # When no waifu has been retrieved, send error message to the user
            else:
                embed = Embed(description="**Waifu Not Found!**",
                              colour=enso_embedmod_colours)
                await ctx.send(embed=embed)

            # Get the instance of the bot
            bot = ctx.guild.get_member(self.bot.user.id)

            # Send the menu to the display
            menu = HelpMenu(i, waifus_dict, self, bot)
            await menu.start(ctx)

        else:

            # Set variables to retrieve data from the API
            url = "https://mywaifulist.moe/api/v1/meta/random"

            # Retrieve a random waifu from the API
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as resp:
                    # Store waifu's in dict when request is successful, else send an error
                    if resp.status == 200:
                        waifu_dict = await resp.json()
                        waifu = waifu_dict["data"]

                    # Send error if something went wrong internally/while grabbing data from API
                    else:
                        await ctx.send("Something went wrong!")

            await ctx.send(embed=single_waifu_generator(waifu))

    @waifu.command(name="daily", aliases=["Daily"])
    async def daily_waifu(self, ctx):
        """Returns the daily Waifu from MyWaifuList"""

        url = "https://mywaifulist.moe/api/v1/meta/daily"

        # Retrieve a random waifu from the API
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as resp:
                # Store waifu's in dict when request is successful, else send an error
                if resp.status == 200:
                    waifu_dict = await resp.json()
                    waifu = waifu_dict["data"]

                # Send error if something went wrong internally/while grabbing data from API
                else:
                    await ctx.send("Something went wrong!")

        await ctx.send(embed=single_waifu_generator(waifu))


def setup(bot):
    bot.add_cog(Anime(bot))
