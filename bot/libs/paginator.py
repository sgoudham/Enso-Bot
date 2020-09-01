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

from discord import Embed
from discord.ext import menus


class SimpleMenu(menus.Menu):
    def __init__(self, i, item, perms, embeds, bot):
        super().__init__(timeout=125.0, clear_reactions_after=True)
        self.i = i
        self.perms = perms
        self.dicts = embeds
        self.type = item
        self.bot = bot

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

    async def send_initial_message(self, ctx, channel):
        """Set the first embed to the first element in the pages[]"""

        initial = self.dicts[self.i]

        cur_page, pages = self.get_page(self)
        pages = len(self.dicts)
        initial.set_author(name=f"{self.type} | Page {cur_page}/{pages}")

        # Send embed
        return await channel.send(embed=initial)

    @menus.button('\N{LEFTWARDS BLACK ARROW}')
    async def on_left_arrow(self, payload):
        """Reaction to allow user to go to the previous page in the embed"""

        # Do nothing if the check does not return true
        if self.check(self.ctx, payload):
            # Set self.i to (i - 1) remainder length of the array
            self.i = (self.i - 1) % len(self.dicts)
            prev_page = self.dicts[self.i]

            cur_page, pages = self.get_page(self)
            prev_page.set_author(name=f"{self.type} | Page {cur_page}/{pages}")

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
            next_page.set_author(name=f"{self.type} | Page {cur_page}/{pages}")

            # Send the embed and remove the reaction of the user
            await self.message.edit(embed=next_page)
            await self.remove_reaction("➡")

    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def on_stop(self, payload):
        """Reaction to allow user to make the embed disappear"""

        # Do nothing if the check does not return true
        if self.check(self.ctx, payload):
            # Edit the embed and tell the member that the session has been closed
            embed = Embed(description="**Pagination Session Has Been Closed**",
                          colour=self.bot.random_colour())
            await self.message.edit(embed=embed)
            self.stop()
