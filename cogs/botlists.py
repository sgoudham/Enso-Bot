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

import aiohttp
import dbl
from decouple import config
from discord.ext import commands, tasks

disforge_auth = config('DISFORGE_AUTH')
disc_bots_gg_auth = config('DISCORD_BOTS_BOTS_AUTH')
top_gg_auth = config('TOP_GG_AUTH')


async def post_bot_stats(self):
    """Update guild count on bot lists"""

    async with aiohttp.ClientSession() as session:
        await session.post(f"https://discord.bots.gg/api/v1/bots/{self.user.id}/stats",
                           data={"guildCount": {len(self.guilds)},
                                 "Content-Type": "application/json"},
                           headers={'Authorization': disc_bots_gg_auth})

        await session.post(f"https://disforge.com/api/botstats/{self.user.id}",
                           data={"servers": {len(self.guilds)}},
                           headers={'Authorization': disforge_auth})

        await session.close()


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = top_gg_auth
        self.dblpy = dbl.DBLClient(self.bot, self.token)

        @tasks.loop(minutes=30, reconnect=True)
        async def post_updates():
            """Post updates to botlists"""

            await self.bot.wait_until_ready()

            try:
                await post_bot_stats(self.bot)
                await self.dblpy.post_guild_count()
            except Exception as e:
                print(e)
            else:
                print("Server count posted successfully")

        # Start the background task(s)
        post_updates.start()


def setup(bot):
    bot.add_cog(TopGG(bot))
