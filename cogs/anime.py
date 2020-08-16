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
from typing import Optional

import aiohttp
from decouple import config
from discord import Embed
from discord.ext import menus
from discord.ext.commands import Cog, group, bot_has_permissions

my_waifu_list_auth = config('MYWAIFULIST_AUTH')


def store_waifus(waifus_dict, waifu, value):
    """Method to store waifu's in the new dict"""

    waifus_dict[waifu["name"]][value] = waifu[value]


def multiple_waifu_generator(self, bot):
    """Method to generate embed of multiple waifu's"""

    embeds = []
    for key in self.waifus_dict.values():
        embed = Embed(title=key["name"], description=f"{key['original_name']} | {key['type']}",
                      colour=bot.random_colour(),
                      url=key["url"])
        embed.set_image(url=key["display_picture"])
        embed.set_footer(text=f"❤️ {key['likes']} 🗑️ {key['trash']} | Powered by MyWaifuList")

        embeds.append(embed)

    return embeds


def single_waifu_generator(self, waifu):
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
                  colour=self.bot.random_colour(),
                  url=url)
    embed.set_image(url=picture)
    embed.set_footer(text=f"❤️ {likes} 🗑️ {trash} | Powered by MyWaifuList")

    return embed


# Set up the Cog
class HelpMenu(menus.Menu):
    def __init__(self, i, waifu, bot, guild_bot):
        super().__init__(timeout=125.0, clear_reactions_after=True)
        self.waifus_dict = waifu
        self.i = i
        self.bot = bot
        self.waifu = multiple_waifu_generator(self, bot)
        self.guild_bot = guild_bot

    # Message to be sent on the initial command ~help
    async def send_initial_message(self, ctx, channel):
        # Set the first embed to the first element in the pages[]

        initial = self.waifu[self.i]

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
            self.i = (self.i - 1) % len(self.waifu)
            prev_page = self.waifu[self.i]

            cur_page = self.i + 1
            pages = len(self.waifu)
            prev_page.set_author(name=f"Page {cur_page}/{pages}")

            # Send the embed and remove the reaction of the user
            await self.message.edit(embed=prev_page)
            if self.guild_bot.guild_permissions.manage_messages:
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
            self.i = (self.i + 1) % len(self.waifu)
            next_page = self.waifu[self.i]

            cur_page = self.i + 1
            pages = len(self.waifu)
            next_page.set_author(name=f"Page {cur_page}/{pages}")

            # Send the embed and remove the reaction of the user
            await self.message.edit(embed=next_page)
            if self.guild_bot.guild_permissions.manage_messages:
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

    @group(name="waifu", invoke_without_command=True, case_insensitive=True)
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
                              colour=self.bot.admin_colour)
                await ctx.send(embed=embed)

            # Get the instance of the bot
            bot = ctx.guild.get_member(self.bot.user.id)

            # Send the menu to the display
            menu = HelpMenu(i, waifus_dict, self.bot, bot)
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
                        waifu3 = waifu_dict["data"]

                    # Send error if something went wrong internally/while grabbing data from API
                    else:
                        await ctx.send("Something went wrong!")

            await ctx.send(embed=single_waifu_generator(self, waifu3))

    @waifu.command(name="daily")
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

        await ctx.send(embed=single_waifu_generator(self, waifu))


def setup(bot):
    bot.add_cog(Anime(bot))
