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

import asyncpg
from discord import Member
from discord.ext.commands import Cog, command, is_owner


class Owner(Cog):
    """Commands for Ensō server"""

    def __init__(self, bot):
        self.bot = bot

    @command(name="dm", hidden=True)
    @is_owner()
    async def dm(self, ctx, member: Member, *, text):
        """DM users"""

        # Delete the message sent instantly
        await ctx.message.delete()
        # Send the message typed the mentioned user
        await member.send(text)

    @command(name="leave", hidden=True)
    @is_owner()
    async def leave(self, ctx):
        """Leaves the guild"""

        await self.bot.generate_embed(ctx, desc="**Leaving the guild... Bye Bye uvu**")
        await ctx.guild.leave()

    @command(name="restart", hidden=True)
    @is_owner()
    async def restart(self, ctx):
        """Restart the bot"""

        await self.bot.generate_embed(ctx, desc="**Success Senpai!"
                                                "\nMy Reboot Had No Problems** <a:ThumbsUp:737832825469796382>")

        self.bot.db.terminate()
        await self.bot.db.wait_closed()
        await self.bot.logout()

    @command(name="reloadusers", hidden=True)
    @is_owner()
    async def reload_db(self, ctx):
        """Reloads the database by inserting/updating all the records"""

        # Setup pool
        pool = self.bot.db

        # Store every single record into an array
        records = [(ctx.guild.id, member.id) for member in ctx.guild.members]

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:

            # Define the insert statement that will insert the user's information
            try:
                insert_query = """INSERT INTO members (guild_id, member_id) VALUES ($1, $2)
                            ON CONFLICT (guild_id, member_id) DO NOTHING"""
                await conn.executemany(insert_query, records)

            # Catch errors
            except asyncpg.PostgresError as e:
                print(f"PostGres Error: Member(s) were not be able to be added to Guild", e)

            # Print success
            else:
                print(f"Record(s) Inserted Into Members")

            # Release connection back to pool
            finally:
                await pool.release(conn)

    @command(name="cache", hidden=True)
    @is_owner()
    async def set_cache(self, ctx, size: Optional[int]):
        """Allow me to dynamically set the cache max size"""

        if size:
            try:
                self.bot.member_cache.change_array_size(size)

            # Catch errors
            except Exception as e:
                print(e)

            # Let me that it's successful
            else:
                await self.bot.generate_embed(ctx, desc=f"Cache Now Storing To **{size}** Records")

        else:
            max_cache_len, cache_len, queue_len = self.bot.member_cache.get_size()
            await self.bot.generate_embed(ctx, desc=f"Current Records Stored Within Cache: **{cache_len}**"
                                                    f"\nCurrent Queue Length: **{queue_len}**"
                                                    f"\nMax Size Of Cache: **{max_cache_len}**")


def setup(bot):
    bot.add_cog(Owner(bot))
