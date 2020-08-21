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

            finally:
                # Release connection back to pool
                await pool.release(conn)


def setup(bot):
    bot.add_cog(Owner(bot))
