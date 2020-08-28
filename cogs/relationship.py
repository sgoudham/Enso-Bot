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

import asyncpg
from discord import Member, Embed
from discord.ext.commands import command, bot_has_permissions, Cog


# Sets up the embed for the marriage info
def marriageInfo(self, target, marriedUser, marriedDate, currentDate, married):
    # Make sure that non-users can still use the marriage
    if not married:
        # Set up the fields for the embed
        fields = [("Married To", "No One", False),
                  ("Marriage Date", "N/A", False),
                  ("Days Married", "N/A", False)]
    else:
        # Calculate the days married
        marriedTime = datetime.datetime.strptime(marriedDate, "%a, %b %d, %Y")
        currentTime = datetime.datetime.strptime(currentDate, "%a, %b %d, %Y")
        delta = currentTime - marriedTime

        # Set up the fields for the embed
        fields = [("Married To", marriedUser.mention, False),
                  ("Marriage Date", marriedDate, False),
                  ("Days Married", delta.days, False)]

    # Set the title, colour, timestamp and thumbnail
    embed = Embed(title=f"{target.name}'s Marriage Information",
                  colour=self.bot.random_colour(),
                  timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=target.avatar_url)

    # Add fields to the embed
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    return embed


# Set up the Cog
class Relationship(Cog):
    """Marry/Divorce etc!"""

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        """Printing out that Cog is ready on startup"""
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @command(name="marry")
    async def marry(self, ctx, member: Member):
        """Wed your Lover!"""

        # Getting the guild of the user
        guild = ctx.guild

        # Make sure that the user cannot marry themselves
        if member.id == ctx.author.id:
            await self.bot.generate_embed(ctx, desc="**Senpaii! ˭̡̞(◞⁎˃ᆺ˂)◞*✰ You can't possibly marry yourself!**")
            return

        # Get the author from the cache
        db_author = await self.bot.check_cache(ctx.author.id, ctx.guild.id)
        married_user = db_author["married"]

        # Make sure that the person is not already married to someone else within the server
        if married_user:
            member = guild.get_member(married_user)
            await self.bot.generate_embed(ctx, desc=f"**((╬◣﹏◢)) You're already married to {member.mention}!**")
            return

        # Get the member mentioned from the cache
        db_member = await self.bot.check_cache(member.id, ctx.guild.id)
        target_user = db_member["married"]

        if target_user:
            member = guild.get_member(target_user)
            await self.bot.generate_embed(ctx, desc=f"**Sorry! That user is already married to {member.mention}**")
            return

        # Send a message to the channel mentioning the author and the person they want to wed.
        await self.bot.generate_embed(ctx, desc=f"{ctx.author.mention} **Proposes To** {member.mention}"
                                                f"\n**Do you accept??**"
                                                f"\nRespond with [**Y**es/**N**o]")

        # A check that makes sure that the reply is not from the author
        # and that the reply is in the same channel as the proposal
        def check(m):
            return m.author == member and m.channel == ctx.channel

        try:
            # Wait for the message from the mentioned user
            msg = await self.bot.wait_for('message', check=check, timeout=90.0)

            # if the person says yes
            if msg.content.lower() in ['y', 'yes', 'yea']:

                # Setup pool connection
                pool = self.bot.db
                async with pool.acquire() as conn:

                    # Get the time of marriage
                    message_time = msg.created_at.strftime("%a, %b %d, %Y")

                    # Update the existing records in the database with the user that they are marrying along with the time of the accepted proposal
                    try:
                        update_query = """UPDATE members SET married = $1, married_date = $2 WHERE member_id = $3 AND guild_id = $4"""
                        await conn.execute(update_query, member.id, message_time, ctx.author.id, guild.id)
                        await conn.execute(update_query, ctx.author.id, message_time, member.id, guild.id)

                    # Catch errors
                    except asyncpg.PostgresError as e:
                        print(f"PostGres Error: {member.id} and {ctx.author.id} Could Not Be Married", e)

                    # Update cache new details
                    else:
                        db_author["married"] = member.id
                        db_author["married_date"] = message_time

                        db_member["married"] = ctx.author.id
                        db_member["married_date"] = message_time

                    # Release connection back to pool
                    finally:
                        await pool.release(conn)

                # Congratulate them!
                desc = f"**Congratulations! ｡ﾟ( ﾟ^∀^ﾟ)ﾟ｡ {ctx.author.mention} and {member.mention} are now married to each other!**"
                await self.bot.generate_embed(ctx, desc=desc)

            # if the person says no
            elif msg.content.lower() in ['n', 'no', 'nah']:

                # Try to console the person and wish them the best in their life
                desc = f"**{ctx.author.mention} It's okay king. Pick up your crown and move on (◕‿◕✿)**"
                await self.bot.generate_embed(ctx, desc=desc)
            else:
                # Abort the process as the message sent did not make sense
                await self.bot.generate_embed(ctx, desc="**Senpaiiii! (｡╯︵╰｡) Speak English Please**")

        except asyncio.TimeoutError as ex:
            print(ex)

            # Send out an error message if the user waited too long
            await self.bot.generate_embed(ctx, desc=f"**(｡T ω T｡) {member.mention} waited too long**")

    @command(name="divorce")
    async def divorce(self, ctx, member: Member):
        """Divorce your Partner!"""

        # Getting the guild of the user
        guild = ctx.guild

        # Make sure that the user cannot divorce themselves
        if member.id == ctx.author.id:
            await self.bot.generate_embed(ctx, desc="**Senpaii! ˭̡̞(◞⁎˃ᆺ˂)◞*✰ You can't possibly divorce yourself!**")
            return

        # Get the author from the cache
        db_author = await self.bot.check_cache(ctx.author.id, ctx.guild.id)
        married_user = db_author["married"]

        # Make sure that the person trying to divorce is actually married to the user
        if married_user is None:
            desc = "**((╬◣﹏◢)) You must be married in order to divorce someone! Baka!**"
            await self.bot.generate_embed(ctx, desc=desc)
            return

        # Make sure the person is married to the person that they're trying to divorce
        elif married_user != member.id:
            member = guild.get_member(married_user)

            desc = f"**(ノ ゜口゜)ノ You can only divorce the person that you're married!" \
                   f"\n That person is {member.mention}**"
            await self.bot.generate_embed(ctx, desc=desc)
            return

        # Send a message to the channel mentioning the author and the person they want to wed.
        await self.bot.generate_embed(ctx, desc=f"{ctx.author.mention} **Wishes to Divorce** {member.mention}"
                                                f"\n**Are you willing to break this sacred bond?**"
                                                f"\nRespond with [**Y**es/**N**o]")

        # A check that makes sure that the reply is not from the author
        # and that the reply is in the same channel as the proposal
        def check(m):
            return m.author == member and m.channel == ctx.channel

        # Surround with try/except to catch any exceptions that may occur
        try:
            # Wait for the message from the mentioned user
            msg = await self.bot.wait_for('message', check=check, timeout=90.0)

            # if the person says yes
            if msg.content.lower() in ['y', 'yes', 'yea']:

                # Setup pool connection
                pool = self.bot.db
                async with pool.acquire() as conn:

                    # Update the existing records in the database that the author and member are divorced
                    try:
                        update_query = """UPDATE members SET married = NULL, married_date = NULL WHERE member_id = $1 and guild_id = $2"""
                        await conn.execute(update_query, ctx.author.id, guild.id)
                        await conn.execute(update_query, member.id, guild.id)

                    # Catch errors
                    except asyncpg.PostgresError as e:
                        print(f"PostGres Error: {member.id} and {ctx.author.id} Could Not Be Divorced", e)

                    # Update cache with new details
                    else:
                        db_author["married"] = None
                        db_author["married_date"] = None

                        db_member = await self.bot.check_cache(member.id, ctx.guild.id)
                        db_member["married"] = None
                        db_member["married_date"] = None

                    # Release connection back to pool
                    finally:
                        await pool.release(conn)

                # Congratulate them!
                desc = f"**૮( ´⁰▱๋⁰ )ა {ctx.author.mention} and {member.mention} are now divorced." \
                       f"\nI hope you two can find happiness in life with other people**"
                await self.bot.generate_embed(ctx, desc=desc)

            # if the person says no
            elif msg.content.lower() in ['n', 'no', 'nah']:

                # Try to console the person and wish them the best in their life
                desc = f"**Sorry {ctx.author.mention} but you're gonna need {member.mention}'s consent to move forward with this!**"
                await self.bot.generate_embed(ctx, desc=desc)

            else:
                # Abort the process as the message sent did not make sense
                await self.bot.generate_embed(ctx, desc="**Senpaiiii! (｡╯︵╰｡) Speak English Please**")

        except asyncio.TimeoutError as ex:
            print(ex)

            # Send out an error message if the user waited too long
            await self.bot.generate_embed(ctx, desc=f"**(｡T ω T｡) {member.mention} waited too long**")

    @command(name="marriageinfo", aliases=["minfo"])
    @bot_has_permissions(embed_links=True)
    async def m_info(self, ctx, member: Member = None):
        """Marriage Information!"""

        # Choose author if no other user has been mentioned
        member = ctx.author if not member else member

        # Getting the guild of the user
        guild = member.guild

        # Get the author from the cache
        result = await self.bot.check_cache(member.id, ctx.guild.id)

        user = result["married"]
        marriage_date = result["married_date"]

        # Set empty values for non-married users
        if not user:
            married = False
            marriedUser = ""
            marriedDate = ""
        # Set the member, date married and setting married status
        else:
            married = True
            marriedUser = guild.get_member(user)
            marriedDate = marriage_date

        # Get the current date of the message sent by the user
        currentDate = ctx.message.created_at.strftime("%a, %b %d, %Y")

        # Get the marriage info embed and then send it to the display
        embed = marriageInfo(self, member, marriedUser, marriedDate, currentDate, married)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Relationship(bot))
