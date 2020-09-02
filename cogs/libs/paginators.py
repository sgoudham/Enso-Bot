# Ensō~Chan - A Multi Purpose Discord Bot That Has Everything Your Server Needs!
# Copyright (C) 2020  Hamothy

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

import datetime

from discord import Embed
from discord.ext import menus


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
        embed.set_author(name=f"{key['type']} | ID: {key['id']}")

        if key["type"] in ["Waifu", "Husbando"]:
            embed.set_footer(text=f"❤️ {key['likes']} 🗑️ {key['trash']} | Powered by MyWaifuList")
        elif key["type"] in ["TV", "ONA", "OVA"]:
            if key['romaji_name']:
                embed.set_footer(text=f"{key['romaji_name']} | Powered by MyWaifuList")
            else:
                embed.set_footer(text="Powered by MyWaifuList")

        embeds.append(embed)

    return embeds


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


class MWLMenu(menus.Menu):
    """Setup menus for MyWaifuList results"""

    def __init__(self, i, perms, _dict, bot):
        super().__init__(timeout=125.0, clear_reactions_after=True)
        self.i = i
        self.perms = perms
        self._dict = _dict
        self.bot = bot
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
    def set_author(embed, cur_page, pages):
        """
        Returns the author for the first initial embed

        The reason why it's different is because I need to retrieve the previous author that I set for the
        embed (to get the type from the API)

        """

        __type = embed.author.name
        embed.remove_author()
        return embed.set_author(name=f"{__type} | Page {cur_page}/{pages}")

    @staticmethod
    def set_author_after(embed, cur_page, pages):
        """
        Returns the author for all the pages when the user reacts to go back and forwards

        This needs to be another method because the previous author is gonna be different to the one
        specified at the start "multiple_dict_generators()"
        """

        author = embed.author.name
        tv_type = author.split("|")
        __type = f"{tv_type[0].strip()} | {tv_type[1].strip()}"
        return embed.set_author(name=f"{__type} | Page {cur_page}/{pages}")

    async def send_initial_message(self, ctx, channel):
        """Set the first embed to the first element in the pages[]"""

        initial = self.dicts[self.i]

        cur_page, pages = self.get_page(self)
        initial = self.set_author(initial, cur_page, pages)

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
            first_page = self.set_author_after(first_page, cur_page, pages)

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
            prev_page = self.set_author_after(prev_page, cur_page, pages)

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
            next_page = self.set_author_after(next_page, cur_page, pages)

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
            last_page = self.set_author_after(last_page, cur_page, pages)

            await self.message.edit(embed=last_page)
            await self.remove_reaction("\U000023ed")

    @menus.button('\N{INPUT SYMBOL FOR NUMBERS}')
    async def on_numbered_page(self, payload):
        """Reaction to allow users to input page numbers"""

        # Do nothing if the check does not return true
        if self.check(self.ctx, payload):

            embed = Embed(description="**What Page Would You Like To Go To? (Only Numbers!)**",
                          colour=self.bot.random_colour())
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
                              colour=self.bot.random_colour())
                await message.edit(embed=embed)

                await asyncio.sleep(2.5)
                await message.delete()

            else:
                # As long as the number entered is within the page numbers, go to that page
                try:
                    if 0 < int(msg.content) <= len(self.dicts):
                        await message.delete()
                        await msg.delete()

                        self.i = int(msg.content) - 1
                        number_page = self.dicts[self.i]

                        cur_page, pages = self.get_page(self)
                        last_page = self.set_author_after(number_page, cur_page, pages)

                        await self.message.edit(embed=last_page)
                        await self.remove_reaction("\U0001f522")

                    # Delete the message and remove the reaction if out of bounds
                    else:
                        await message.delete()
                        await msg.delete()
                        await self.remove_reaction("\U0001f522")
                except Exception as e:
                    print(e)
                    await message.delete()
                    await msg.delete()
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
                ('\N{INFORMATION SOURCE}', "Shows This Message"),
                ('\N{BLACK SQUARE FOR STOP}', "Closes The Pagination Session")
            ]

            for value, func in reaction_emojis:
                messages.append(f"{value}, {func}")

            embed = Embed(description='\n'.join(messages),
                          colour=self.bot.random_colour(),
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
                          colour=self.bot.random_colour())
            await self.message.edit(embed=embed)
            self.stop()
