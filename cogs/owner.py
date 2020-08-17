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
        """Restart the Bot"""

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

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Define the insert statement that will insert the user's information
                insert = """INSERT INTO members (guildID, discordID) VALUES """ + ", ".join(
                    map(lambda m: f"({ctx.guild.id}, {m.id})",
                        ctx.guild.members)) + """ ON DUPLICATE KEY UPDATE guildID = VALUES(guildID), discordID = VALUES(discordID)"""

                # Execute the insert statement
                await cur.execute(insert)
                await conn.commit()
                print(cur.rowcount, f"Record(s) inserted successfully into Members from {ctx.guild.name}")

                # Sending confirmation message
                await ctx.send(f"Database Reloaded Successfully for **{ctx.guild.name}**")


def setup(bot):
    bot.add_cog(Owner(bot))
