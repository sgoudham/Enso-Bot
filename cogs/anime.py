# Ensō~Chan - A Multi Purpose Discord Bot That Has Everything Your Server Needs!
# Copyright (C) 2020  Goudham Suresh

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import aiohttp
from decouple import config
from discord import Embed
from discord.ext import menus
from discord.ext.commands import Cog, group, bot_has_permissions, command

my_waifu_list_auth = config('MYWAIFULIST_AUTH')


class WaifuCommandNotFound(Exception):
    """Exception raised for errors when user does not use the right arguments for waifu command

    Attributes:
        waifu -- input command which cause the error
        message -- explanation of the error
    """

    def __init__(self, waifu, ctx):
        self.command = waifu
        self.bot = ctx.bot
        self.message = f"Error! Use **{ctx.prefix}help {self.command}** to see {self.command} commands"
        super().__init__(self.message)

    def __str__(self):
        return f'{self.command} -> {self.message}'


async def get_airing_api(self, ctx, url):
    """Retreiving information about the airing shows/waifus"""

    url = f"https://mywaifulist.moe/api/v1/{url}"
    data = {'content-type': "application/json"}

    # Searching API for the current airing shows
    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=data, headers=self.headers) as resp:
            # Store waifu's in dict when request is successful, else send an error
            if resp.status == 200:
                airing = await resp.json()

            # Send error if something went wrong internally/while grabbing data from API
            else:
                await self.bot.generate_embed(ctx, desc="**Something went wrong with MyWaifuList!**")

        # Close session
        await session.close()

    return airing


def store_dict(dict_, key, value):
    """Method to store waifu's in the new dict"""

    dict_[key["name"]][value] = key[value]


def search(self, bot):
    """Method to generate embed of multiple waifu's"""

    embeds = []
    for key in self._dict.values():

        # Only setting up description if waifu og_name has a value
        desc = f"{key['original_name']}" if key["original_name"] else Embed.Empty

        embed = Embed(title=key["name"], description=desc,
                      colour=bot.random_colour(),
                      url=key["url"])
        embed.set_image(url=key["display_picture"])

        if key["type"] in ["Waifu", "Husbando"]:
            embed.set_author(name=key["type"])
            embed.set_footer(text=f"❤️ {key['likes']} 🗑️ {key['trash']} | Powered by MyWaifuList")
        elif key["type"] in ["TV", "ONA", "OVA"]:
            embed.set_author(name=key["type"])
            if key['romaji_name']:
                embed.set_footer(text=f"{key['romaji_name']} | Powered by MyWaifuList")
            else:
                embed.set_footer(text="- | Powered by MyWaifuList")

        embeds.append(embed)

    return embeds


def waifu_embedder(self, waifu, _type):
    """Method to generate embed of single waifu's"""

    # Get all the data to be displayed in the embed
    name = waifu["name"]
    og_name = waifu["original_name"]
    picture = waifu["display_picture"]
    url = waifu["url"]
    likes = waifu["likes"]
    trash = waifu["trash"]
    waifu_type = waifu["type"]

    # Set different values for description based on the command
    if _type == "random":
        desc = f"{og_name} | Random {waifu_type}" if waifu["original_name"] else f"Random {waifu_type}"
    elif _type == "daily":
        desc = f"{og_name} | Daily {waifu_type}" if waifu["original_name"] else f"Daily {waifu_type}"

    embed = Embed(title=name, description=desc,
                  colour=self.bot.random_colour(),
                  url=url)
    embed.set_image(url=picture)
    embed.set_footer(text=f"❤️ {likes} 🗑️ {trash} | Powered by MyWaifuList")

    return embed


# Set up the Cog
class HelpMenu(menus.Menu):
    def __init__(self, i, _dict, _type, bot, guild_bot):
        super().__init__(timeout=125.0, clear_reactions_after=True)
        self._dict = _dict
        self.type = _type
        self.i = i
        self.bot = bot
        self.dicts = search(self, bot)
        self.guild_bot = guild_bot

    @staticmethod
    def set_author(embed, _type, cur_page, pages):
        """
        Returns the author for the first initial embed

        The reason why it's different is because I need to retrieve the previous author that I set for the
        embed (to get the type from the API)

        """

        if _type == "anime":
            __type = embed.author.name
            embed.remove_author()
            return embed.set_author(name=f"{__type} | Page {cur_page}/{pages}")
        elif _type == "waifu":
            __type = embed.author.name
            embed.remove_author()
            return embed.set_author(name=f"{__type} | Page {cur_page}/{pages}")

    @staticmethod
    def set_author_after(embed, _type, cur_page, pages):
        """
        Returns the author for all the pages when the user reacts to go back and forwards

        This needs to be another method because the previous author is gonna be different to the one
        specified at the start "multiple_dict_generators()"
        """

        if _type == "anime":
            author = embed.author.name
            tv_type = author.split("|")
            __type = tv_type[0].strip()
            return embed.set_author(name=f"{__type} | Page {cur_page}/{pages}")

        elif _type == "waifu":
            author = embed.author.name
            tv_type = author.split("|")
            __type = tv_type[0].strip()
            return embed.set_author(name=f"{__type} | Page {cur_page}/{pages}")

    async def send_initial_message(self, ctx, channel):
        """Set the first embed to the first element in the pages[]"""

        initial = self.dicts[self.i]

        cur_page = self.i + 1
        pages = len(self.dicts)
        initial = self.set_author(initial, self.type, cur_page, pages)

        # Send embed
        return await channel.send(embed=initial)

    @menus.button('\N{LEFTWARDS BLACK ARROW}')
    async def on_left_arrow(self, payload):
        """Reaction to allow user to go to the previous page in the embed"""

        # Simple check to make sure that the reaction is performed by the user
        def check(m):
            return m.author == payload.member

        # Do nothing if the check does not return true
        if check(self.ctx):
            # Set self.i to (i - 1) remainder length of the array
            self.i = (self.i - 1) % len(self.dicts)
            prev_page = self.dicts[self.i]

            cur_page = self.i + 1
            pages = len(self.dicts)
            prev_page = self.set_author_after(prev_page, self.type, cur_page, pages)

            # Send the embed and remove the reaction of the user
            await self.message.edit(embed=prev_page)
            if self.guild_bot.guild_permissions.manage_messages:
                await self.message.remove_reaction("⬅", self.ctx.author)

    @menus.button('\N{BLACK RIGHTWARDS ARROW}')
    async def on_right_arrow(self, payload):
        """Reaction to allow user to go to the next page in the embed"""

        # Simple check to make sure that the reaction is performed by the user
        def check(m):
            return m.author == payload.member

        # Do nothing if the check does not return true
        if check(self.ctx):
            # Set self.i to (i + 1) remainder length of the array
            self.i = (self.i + 1) % len(self.dicts)
            next_page = self.dicts[self.i]

            cur_page = self.i + 1
            pages = len(self.dicts)
            next_page = self.set_author_after(next_page, self.type, cur_page, pages)

            # Send the embed and remove the reaction of the user
            await self.message.edit(embed=next_page)
            if self.guild_bot.guild_permissions.manage_messages:
                await self.message.remove_reaction("➡", self.ctx.author)

    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def on_stop(self, payload):
        """Reaction to allow user to make the embed disappear"""

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

    @group(name="airing", invoke_without_command=True, case_insensitive=True)
    @bot_has_permissions(embed_links=True, add_reactions=True)
    async def airing(self, ctx):
        """
        Display airing shows and waifu's in those shows
        (UNDER CONSTRUCTION)
        """
        error = WaifuCommandNotFound(ctx.command, ctx)
        await self.bot.generate_embed(ctx, desc=error.message)

    @airing.command(name="trash", aliases=["worst", "garbage"])
    @bot_has_permissions(embed_links=True, add_reactions=True)
    async def airing_trash(self, ctx):
        """Get the most popular waifu’s from the airing shows"""

        # Variables to set up the reaction menu
        i = 0
        airing_trash = {}
        trash_waifus = await get_airing_api(self, ctx, "airing/trash")

        # Store all the shows with the name as the key
        for waifu in trash_waifus["data"]:
            airing_trash[waifu["name"]] = {}
            for value in waifu:
                store_dict(airing_trash, waifu, value)

        # Get the instance of the bot
        bot = ctx.guild.get_member(self.bot.user.id)

        # Send the menu to the display
        menu = HelpMenu(i, airing_trash, "waifu", self.bot, bot)
        await menu.start(ctx)

    @airing.command(name="popular", aliases=["pop"])
    @bot_has_permissions(embed_links=True, add_reactions=True)
    async def airing_popular(self, ctx):
        """Get the most popular waifu’s from the airing shows"""

        # Variables to setup the reaction menu
        i = 0
        airing_popular = {}
        popular_waifus = await get_airing_api(self, ctx, "airing/popular")

        # Store all the shows with the name as the key
        for waifu in popular_waifus["data"]:
            airing_popular[waifu["name"]] = {}
            for value in waifu:
                store_dict(airing_popular, waifu, value)

        # Get the instance of the bot
        bot = ctx.guild.get_member(self.bot.user.id)

        # Send the menu to the display
        menu = HelpMenu(i, airing_popular, "waifu", self.bot, bot)
        await menu.start(ctx)

    @airing.command(name="best")
    @bot_has_permissions(embed_links=True, add_reactions=True)
    async def airing_best(self, ctx):
        """Get the best waifu’s from the airing shows"""

        # Local Variable i to allow the pages to be modified
        i = 0
        airing_best = {}
        best_waifus = await get_airing_api(self, ctx, "airing/best")

        # Store all the shows with the name as the key
        for waifu in best_waifus["data"]:
            airing_best[waifu["name"]] = {}
            for value in waifu:
                store_dict(airing_best, waifu, value)

        # Get the instance of the bot
        bot = ctx.guild.get_member(self.bot.user.id)

        # Send the menu to the display
        menu = HelpMenu(i, airing_best, "waifu", self.bot, bot)
        await menu.start(ctx)

    @airing.command(name="anime", aliases=["shows", "series"])
    @bot_has_permissions(embed_links=True, add_reactions=True)
    async def anime(self, ctx):
        """Display the current airing anime"""

        # Local Variable i to allow the pages to be modified
        i = 0
        anime_dict = {}
        animes = await get_airing_api(self, ctx, "airing")

        # Store all the shows with the name as the key
        for show in animes["data"]:
            anime_dict[show["name"]] = {}
            for value in show:
                store_dict(anime_dict, show, value)

        # Get the instance of the bot
        bot = ctx.guild.get_member(self.bot.user.id)

        # Send the menu to the display
        menu = HelpMenu(i, anime_dict, "anime", self.bot, bot)
        await menu.start(ctx)

    @command(name="search", aliases=["lookup"], usage="`<waifu|anime>`")
    @bot_has_permissions(embed_links=True, add_reactions=True)
    async def search(self, ctx, *, term: str):
        """Search the entire website! (Anime|Waifus|Husbandos)"""

        # Local Variable i to allow the index of the embeds to be modified
        i = 0

        anime_or_waifu = {}
        url = "https://mywaifulist.moe/api/v1/search/"
        data = {"term": term,
                'content-type': "application/json"}

        # Searching API for waifu(s)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=self.headers) as resp:
                # Store waifu's in dict when request is successful, else send an error
                if resp.status == 200:
                    waifu_dict = await resp.json()

                # Send error if something went wrong internally/while grabbing data from API
                else:
                    await self.bot.generate_embed(ctx, desc="**Something went wrong with MyWaifuList!**")

            # Close session
            await session.close()

        # As long waifu's were returned from the GET request
        # Store waifus in a dict
        if len(waifu_dict["data"]) > 0:
            for waifu in waifu_dict["data"]:
                # Only store "Waifu's" and "Husbando's"
                if waifu["type"] in ["Waifu", "Husbando"]:
                    anime_or_waifu[waifu["name"]] = {}
                    for value in waifu:
                        store_dict(anime_or_waifu, waifu, value)

                elif waifu["type"] in ["TV", "ONA", "OVA"]:
                    anime_or_waifu[waifu["name"]] = {}
                    for value in waifu:
                        store_dict(anime_or_waifu, waifu, value)

        # When no waifu has been retrieved, send error message to the user
        else:
            await self.bot.generate_embed(ctx, desc="**Waifu/Anime Not Found!**")

        # Get the instance of the bot
        bot = ctx.guild.get_member(self.bot.user.id)

        # Send the menu to the display
        menu = HelpMenu(i, anime_or_waifu, "waifu", self.bot, bot)
        await menu.start(ctx)

    @group(name="waifu", invoke_without_command=True, case_insensitive=True)
    @bot_has_permissions(embed_links=True)
    async def waifu(self, ctx):
        """
        Waifu's are grabbed from mywaifulist.com
        (UNDER CONSTRUCTION)
        """
        error = WaifuCommandNotFound(ctx.command, ctx)
        await self.bot.generate_embed(ctx, desc=error.message)

    @waifu.command(name="daily")
    @bot_has_permissions(embed_links=True)
    async def daily_waifu(self, ctx):
        """Returns the Daily Waifu from MyWaifuList"""

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
                    await self.bot.generate_embed(ctx, desc="**Something went wrong with MyWaifuList!**")

            # Close session
            await session.close()

        await ctx.send(embed=waifu_embedder(self, waifu, "daily"))

    @waifu.command(name="random", aliases=["rnd"])
    @bot_has_permissions(embed_links=True)
    async def random_waifu(self, ctx):
        """Returning a Random Waifu from MyWaifuList"""

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
                    await self.bot.generate_embed(ctx, desc="**Something went wrong with MyWaifuList!**")

            await session.close()

        await ctx.send(embed=waifu_embedder(self, waifu, "random"))


def setup(bot):
    bot.add_cog(Anime(bot))
