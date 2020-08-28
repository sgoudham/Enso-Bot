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
import asyncio
import datetime

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

    not_found = "https://media.discordapp.net/attachments/741072426984538122/748586578074664980/DzEZ4UsXgAAcFjN.png?width=423&height=658"

    embeds = []
    for key in self._dict.values():

        # Only setting up description if waifu og_name has a value
        desc = f"{key['original_name']}" if key["original_name"] else Embed.Empty
        # Only using image if it can be displayed, else display 404 image
        url = key["display_picture"] if key["display_picture"].endswith((".jpeg", ".png", ".jpg")) else not_found

        embed = Embed(title=key["name"], description=desc,
                      colour=bot.random_colour(),
                      url=key["url"])
        embed.set_image(url=url)

        if key["type"] in ["Waifu", "Husbando"]:
            embed.set_author(name=key["type"])
            embed.set_footer(text=f"❤️ {key['likes']} 🗑️ {key['trash']} | Powered by MyWaifuList")
        elif key["type"] in ["TV", "ONA", "OVA"]:
            embed.set_author(name=key["type"])
            if key['romaji_name']:
                embed.set_footer(text=f"{key['romaji_name']} | Powered by MyWaifuList")
            else:
                embed.set_footer(text="Powered by MyWaifuList")

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


class MWLMenu(menus.Menu):
    """Setup menus for MyWaifuList results"""

    def __init__(self, i, perms, _dict, _type, bot, guild_bot):
        super().__init__(timeout=125.0, clear_reactions_after=True)
        self.i = i
        self.perms = perms
        self._dict = _dict
        self.type = _type
        self.bot = bot
        self.guild_bot = guild_bot
        self.dicts = search(self, bot)

    async def remove_reaction(self, reaction):
        """Remove the reaction given"""
        if self.perms.manage_messages:
            await self.message.remove_reaction(reaction, self.ctx.author)

    @staticmethod
    def check(m, payload):
        """Simple check to make sure that the reaction is performed by the user"""
        return m.author == payload.member and m.channel.id == payload.channel_id

    @staticmethod
    def get_page(self):
        """
        Return the current page index
        """

        cur_page = self.i + 1
        pages = len(self.dicts)

        return cur_page, pages

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

        author = embed.author.name
        tv_type = author.split("|")
        __type = tv_type[0].strip()
        return embed.set_author(name=f"{__type} | Page {cur_page}/{pages}")

    async def send_initial_message(self, ctx, channel):
        """Set the first embed to the first element in the pages[]"""

        initial = self.dicts[self.i]

        cur_page, pages = self.get_page(self)
        initial = self.set_author(initial, self.type, cur_page, pages)

        # Send embed
        return await channel.send(embed=initial)

    @menus.button('\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}')
    async def on_first_page_arrow(self, payload):
        """Reaction to allow the user to return to the first page"""

        # Do nothing if the check does not return true
        if self.check(self.ctx, payload):

            # Send the embed and remove the reaction of the user
            if self.i == 0:
                await self.remove_reaction("\U000023ee")
                return

            self.i = 0 % len(self.dicts)
            first_page = self.dicts[self.i]

            cur_page, pages = self.get_page(self)
            first_page = self.set_author_after(first_page, self.type, cur_page, pages)

            await self.message.edit(embed=first_page)
            await self.remove_reaction("\U000023ee")

    @menus.button('\N{LEFTWARDS BLACK ARROW}')
    async def on_left_arrow(self, payload):
        """Reaction to allow user to go to the previous page in the embed"""

        # Do nothing if the check does not return true
        if self.check(self.ctx, payload):
            # Set self.i to (i - 1) remainder length of the array
            self.i = (self.i - 1) % len(self.dicts)
            prev_page = self.dicts[self.i]

            cur_page, pages = self.get_page(self)
            prev_page = self.set_author_after(prev_page, self.type, cur_page, pages)

            # Send the embed and remove the reaction of the user
            await self.message.edit(embed=prev_page)
            await self.remove_reaction("⬅")

    @menus.button('\N{BLACK RIGHTWARDS ARROW}')
    async def on_right_arrow(self, payload):
        """Reaction to allow user to go to the next page in the embed"""

        # Do nothing if the check does not return true
        if self.check(self.ctx, payload):
            # Set self.i to (i + 1) remainder length of the array
            self.i = (self.i + 1) % len(self.dicts)
            next_page = self.dicts[self.i]

            cur_page, pages = self.get_page(self)
            next_page = self.set_author_after(next_page, self.type, cur_page, pages)

            # Send the embed and remove the reaction of the user
            await self.message.edit(embed=next_page)
            await self.remove_reaction("➡")

    @menus.button('\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}')
    async def on_last_page_arrow(self, payload):
        """Reaction to allow the user to go to the last page in the embed"""

        # Do nothing if the check does not return true
        if self.check(self.ctx, payload):

            # Send the embed and remove the reaction of the user
            if self.i == len(self.dicts) - 1:
                await self.remove_reaction("\U000023ed")
                return

            self.i = len(self.dicts) - 1
            last_page = self.dicts[self.i]

            cur_page, pages = self.get_page(self)
            last_page = self.set_author_after(last_page, self.type, cur_page, pages)

            await self.message.edit(embed=last_page)
            await self.remove_reaction("\U000023ed")

    @menus.button('\N{INPUT SYMBOL FOR NUMBERS}')
    async def on_numbered_page(self, payload):
        """Reaction to allow users to input page numbers"""

        # Do nothing if the check does not return true
        if self.check(self.ctx, payload):

            embed = Embed(description="**What Page Would You Like To Go To?**",
                          colour=self.bot.admin_colour)
            message = await self.ctx.send(embed=embed)

            def check(m):
                """Simple check to make sure that the reaction is performed by the user"""
                return m.author == payload.member and m.channel.id == payload.channel_id

            try:
                # Wait for the message from the mentioned user
                msg = await self.bot.wait_for('message', check=check, timeout=20.0)

            # Catch timeout error
            except asyncio.TimeoutError as ex:
                print(ex)

                await self.remove_reaction("\U0001f522")

                embed = Embed(description="**You Waited Too Long D:**",
                              colour=self.bot.admin_colour)
                await message.edit(embed=embed)

                await asyncio.sleep(2.5)
                await message.delete()

            else:
                # As long as the number entered is within the page numbers, go to that page
                if 0 < int(msg.content) <= len(self.dicts):
                    await message.delete()
                    await msg.delete()

                    self.i = int(msg.content) - 1
                    number_page = self.dicts[self.i]

                    cur_page, pages = self.get_page(self)
                    last_page = self.set_author_after(number_page, self.type, cur_page, pages)

                    await self.message.edit(embed=last_page)
                    await self.remove_reaction("\U0001f522")

                # Delete the message and remove the reaction if out of bounds
                else:
                    await message.delete()
                    await self.remove_reaction("\U0001f522")

    @menus.button('\N{INFORMATION SOURCE}')
    async def on_information(self, payload):
        """Show's information about the pagination session"""

        # Do nothing if the check does not return true
        if self.check(self.ctx, payload):

            messages = ['Welcome to the Waifu/Anime Pagination Session!',
                        'This interactively allows you to see pages of text by navigating with '
                        'reactions. They are as follows:\n']

            reaction_emojis = [
                ('\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}', "Takes You To The First Page"),
                ('\N{BLACK LEFT-POINTING TRIANGLE}', "Takes You To The Previous Page"),
                ('\N{BLACK RIGHT-POINTING TRIANGLE}', "Takes You To The Next Page"),
                ('\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}', "Takes You To The Last Page"),
                ('\N{INPUT SYMBOL FOR NUMBERS}', "Enter Page Number To Go To"),
                ('\N{INFORMATION SOURCE}', "Show's This Message"),
                ('\N{BLACK SQUARE FOR STOP}', "Closes The Pagination Session")
            ]

            for value, func in reaction_emojis:
                messages.append(f"{value}, {func}")

            embed = Embed(description='\n'.join(messages),
                          colour=self.bot.admin_colour,
                          timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f'We Were On Page {self.i + 1} Before This Message')

            await self.message.edit(embed=embed)
            await self.remove_reaction("\U00002139")

    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def on_stop(self, payload):
        """Reaction to allow user to make the embed disappear"""

        # Do nothing if the check does not return true
        if self.check(self.ctx, payload):
            # Edit the embed and tell the member that the session has been closed
            embed = Embed(description="**Waifu/Anime Reaction Session Has Been Closed**",
                          colour=self.bot.admin_colour)
            await self.message.edit(embed=embed)
            self.stop()


class Anime(Cog):
    """
    Search MyWaifuList for Waifu's, Anime's and more!
    Please keep in mind that this API is in ALPHA.
    Searches might not return the proper results and images may be missing
    """

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
        Display's airing anime and waifu's within those anime's
        """

        error = WaifuCommandNotFound(ctx.command, ctx)
        await self.bot.generate_embed(ctx, desc=error.message)

    @airing.command(name="trash", aliases=["worst", "garbage"])
    @bot_has_permissions(embed_links=True, add_reactions=True)
    async def airing_trash(self, ctx):
        """Get the most popular waifu’s from the airing anime"""

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
        # Get the permissions of the channel
        perms = bot.permissions_in(ctx.message.channel)

        # Send the menu to the display
        menu = MWLMenu(i, perms, airing_trash, "waifu", self.bot, bot)
        await menu.start(ctx)

    @airing.command(name="popular", aliases=["pop"])
    @bot_has_permissions(embed_links=True, add_reactions=True)
    async def airing_popular(self, ctx):
        """Get the most popular waifu’s from the airing anime"""

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
        # Get the permissions of the channel
        perms = bot.permissions_in(ctx.message.channel)

        # Send the menu to the display
        menu = MWLMenu(i, perms, airing_popular, "waifu", self.bot, bot)
        await menu.start(ctx)

    @airing.command(name="best")
    @bot_has_permissions(embed_links=True, add_reactions=True)
    async def airing_best(self, ctx):
        """Get the best waifu’s from the airing anime"""

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
        # Get the permissions of the channel
        perms = bot.permissions_in(ctx.message.channel)

        # Send the menu to the display
        menu = MWLMenu(i, perms, airing_best, "waifu", self.bot, bot)
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
        # Get the permissions of the channel
        perms = bot.permissions_in(ctx.message.channel)

        # Send the menu to the display
        menu = MWLMenu(i, perms, anime_dict, "anime", self.bot, bot)
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
        # Get the permissions of the channel
        perms = bot.permissions_in(ctx.message.channel)

        # Send the menu to the display
        menu = MWLMenu(i, perms, anime_or_waifu, "waifu", self.bot, bot)
        await menu.start(ctx)

    @group(name="waifu", invoke_without_command=True, case_insensitive=True)
    @bot_has_permissions(embed_links=True)
    async def waifu(self, ctx):
        """
        Waifu's that are retrieved from MyWaifuList
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
