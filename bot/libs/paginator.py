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

from discord.ext import menus


class AllPermissions(menus.Menu):
    def __init__(self, i, item, perms, embeds, bot, guild_bot):
        super().__init__(timeout=125.0, clear_reactions_after=True)
        self.i = i
        self.perms = perms
        self.dicts = embeds
        self.type = item
        self.bot = bot
        self.guild_bot = guild_bot

    async def send_initial_message(self, ctx, channel):
        """Set the first embed to the first element in the pages[]"""

        initial = self.dicts[self.i]

        cur_page = self.i + 1
        pages = len(self.dicts)
        initial.set_author(name=f"{self.type} Permissions | Page {cur_page}/{pages}")

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
            prev_page.set_author(name=f"{self.type} Permissions | Page {cur_page}/{pages}")

            # Send the embed and remove the reaction of the user
            await self.message.edit(embed=prev_page)
            if self.perms.manage_messages:
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
            next_page.set_author(name=f"{self.type} Permissions | Page {cur_page}/{pages}")

            # Send the embed and remove the reaction of the user
            await self.message.edit(embed=next_page)
            if self.perms.manage_messages:
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
