import datetime
import random
import string
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
    waifus_dict[waifu["name"]][value] = waifu[value]


def embed_generator(waifus_dict, i):
    embeds = []
    for key in waifus_dict.values():
        embed = Embed(title=key["name"], description=f"{key['original_name']} | {key['type']}",
                      colour=rndColour(),
                      url=key["url"])
        embed.set_image(url=key["display_picture"])
        embed.set_footer(text=f"❤️ {key['likes']} 🗑️ {key['trash']} | Powered by MyWaifuList")

        embeds.append(embed)

    return embeds


def get_dict(waifus_dict):
    return waifus_dict


# Set up the Cog
class HelpMenu(menus.Menu):
    def __init__(self, i, waifu, bot):
        super().__init__(timeout=125.0, clear_reactions_after=True)
        self.waifus_dict = waifu
        self.i = i
        self.length = embed_generator(self.waifus_dict, self.i)
        self.bot = bot

    # Message to be sent on the initial command ~help
    async def send_initial_message(self, ctx, channel):
        # Set the first embed to the first element in the pages[]

        initial = embed_generator(self.waifus_dict, self.i)[self.i]

        cur_page = self.i + 1
        pages = len(self.length)
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
        if not check(self.ctx):
            return
        # Allow the page number to be decreased
        else:

            # Set self.i to (i - 1) remainder length of the array
            self.i = (self.i - 1) % len(embed_generator(self.waifus_dict, self.i))
            prev_page = embed_generator(self.waifus_dict, self.i)[self.i]

            cur_page = self.i + 1
            pages = len(self.length)
            prev_page.set_author(name=f"Page {cur_page}/{pages}")

            # Send the embed and remove the reaction of the user
            await self.message.edit(embed=prev_page)
            await self.message.remove_reaction("⬅", self.ctx.author)

    # Reaction to allow user to go to the next page in the embed
    @menus.button('\N{BLACK RIGHTWARDS ARROW}')
    async def on_right_arrow(self, payload):

        # Simple check to make sure that the reaction is performed by the user
        def check(m):
            return m.author == payload.member

        # Do nothing if the check does not return true
        if not check(self.ctx):
            return
        # Allow the page number to be increased
        else:

            # Set self.i to (i + 1) remainder length of the array
            self.i = (self.i + 1) % len(embed_generator(self.waifus_dict, self.i))
            next_page = embed_generator(self.waifus_dict, self.i)[self.i]

            cur_page = self.i + 1
            pages = len(self.length)
            next_page.set_author(name=f"Page {cur_page}/{pages}")

            # Send the embed and remove the reaction of the user
            await self.message.edit(embed=next_page)
            await self.message.remove_reaction("➡", self.ctx.author)

    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def on_stop(self, payload):

        # Simple check to make sure that the reaction is performed by the user
        def check(m):
            return m.author == payload.member

        # Do nothing if the check does not return true
        if not check(self.ctx):
            return
        # Allow the embed to be deleted
        else:

            # Delete the embed and stop the function from running
            await self.message.delete()
            self.stop()


class Anime(Cog):
    """Waifus and Husbandos!"""

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        """Printing out that Cog is ready on startup"""
        print(f"{self.__class__.__name__} Cog has been loaded!\n-----")

    @group(invoke_without_command=True, aliases=["Waifu"])
    @bot_has_permissions(embed_links=True)
    async def waifu(self, ctx, waifu2: Optional[str] = None):
        """
        Shows a Waifu (UNDER CONSTRUCTION)
        Waifu's are grabbed from mywaifulist.com
        """

        # Local Variable i to allow the index of the pages[] to be modified
        i = 0

        if waifu2:

            waifus_dict = {}

            async with aiohttp.ClientSession() as session:
                async with session.post(f"https://mywaifulist.moe/api/v1/search/",
                                        data={"term": waifu2,
                                              'content-type': "application/json"},
                                        headers={'apikey': my_waifu_list_auth}) as resp:
                    if resp.status == 200:
                        waifu_dict = await resp.json()
                    else:
                        await ctx.send("Something went wrong!")

            for waifu in waifu_dict["data"]:
                if waifu["type"] in ["Waifu", "Husbando"]:
                    waifus_dict[waifu["name"]] = {}
                    for value in waifu:
                        store_waifus(waifus_dict, waifu, value)
                else:
                    break

            # Send the menu to the display
            menu = HelpMenu(i, waifus_dict, self)
            await menu.start(ctx)

            """
            name = waifu["name"]
            og_name = waifu["original_name"]
            picture = waifu["display_picture"]
            url = waifu["url"]
            likes = waifu["likes"]
            trash = waifu["trash"]

            embed = Embed(title=name, description=og_name,
                          colour=rndColour(),
                          url=url)
            embed.set_image(url=picture)
            embed.set_footer(text=f"❤️ {likes} 🗑️ {trash} | Powered by MyWaifuList")
            """

        else:

            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://mywaifulist.moe/api/v1/meta/random",
                                       headers={'apikey': my_waifu_list_auth}) as resp:
                    if resp.status == 200:
                        waifu_dict = await resp.json()
                    else:
                        await ctx.send("Something went wrong!")

            waifu = waifu_dict["data"]
            name = waifu["name"]
            og_name = waifu["original_name"]
            picture = waifu["display_picture"]
            url = waifu["url"]
            likes = waifu["likes"]
            trash = waifu["trash"]
            type = waifu["type"]

            embed = Embed(title=name, description=f"{og_name} | {type}",
                          colour=rndColour(),
                          url=url)
            embed.set_image(url=picture)
            embed.set_footer(text=f"❤️ {likes} 🗑️ {trash} | Powered by MyWaifuList")

            await ctx.send(embed=embed)

    @group(invoke_without_command=True, aliases=["Husbando"])
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

                # Send error message saying that the Husbando isn't recognised
                embed = Embed(
                    description="Sorry! That Husbando Doesn't Exist!"
                                f"\nPlease Do **{ctx.prefix}husbando list** To View The List Of Husbando's Available",
                    colour=enso_embedmod_colours)
                await ctx.send(embed=embed)

        else:

            # Get embed from randomHusbando() and send it to the channel
            embed = randomHusbando(ctx, husbandos())
            await ctx.send(embed=embed)

    @waifu.command(name="list", aliases=["List"])
    async def wlist(self, ctx):
        """Returns a list of Waifu's Available"""

        # Send the list of waifus in the bot to the channel
        waifu_list = string.capwords(', '.join(map(str, waifus())))

        # Tell the user to try the waifus in the array
        embed = Embed(description="Try The Waifu's Listed Below!"
                                  f"\n**{waifu_list}**",
                      colour=enso_embedmod_colours)
        await ctx.send(embed=embed)

    @husbando.command(name="list", aliases=["List"])
    async def hlist(self, ctx):
        """Returns a list of Husbando's Available"""

        # Send the list of waifus in the bot to the channel
        husbando_list = string.capwords(', '.join(map(str, husbandos())))

        # Tell the user to try the husbando's in the array
        embed = Embed(description="Try The Husbando's Listed Below!"
                                  f"\n**{husbando_list}**",
                      colour=enso_embedmod_colours)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Anime(bot))
