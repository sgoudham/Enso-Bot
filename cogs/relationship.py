import asyncio
import datetime
import random
from contextlib import closing

from discord import Member, Embed, Colour
from discord.ext import commands
from discord.ext.commands import BucketType, command, cooldown, bot_has_permissions

import db
from db import connection2
from settings import colour_list


# Sets up the embed for the marriage info
def marriageInfo(target, marriedUser, marriedDate, currentDate, married):
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
                  colour=Colour(int(random.choice(colour_list))),
                  timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=target.avatar_url)

    # Add fields to the embed
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    return embed


# Set up the Cog
class Relationship(commands.Cog):
    """Marry/Divorce etc!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Printing out that Cog is ready on startup"""
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @command(name="marry", aliases=["Marry"])
    @cooldown(1, 1, BucketType.user)
    async def marry(self, ctx, member: Member):
        """Wed your Lover!"""

        # Getting the guild of the user
        guild = ctx.author.guild
        pool = await connection2(db.loop)

        async with pool.acquire() as conn:
            async with conn.cursor() as author_cursor:
                # Get the author's/members row from the Members Table
                select_query = """SELECT * FROM members WHERE discordID = %s and guildID = %s"""
                author_val = ctx.author.id, guild.id,
                member_val = member.id, guild.id,

                # Execute the Author SQL Query
                await author_cursor.execute(select_query, author_val)
                author_result = await author_cursor.fetchone()
                married_user = author_result[1]

            # Make sure that the user cannot marry themselves
            if member.id == ctx.author.id:
                await ctx.send("**Senpaii! ˭̡̞(◞⁎˃ᆺ˂)◞*✰ You can't possibly marry yourself!**")
                return
            # Make sure that the person is not already married to someone else within the server
            elif married_user is not None:
                member = guild.get_member(int(married_user))
                await ctx.send(f"**((╬◣﹏◢)) You're already married to {member.mention}!**")
                return

            # Set up new cursor for member row
            async with conn.cursor() as member_cursor:
                # Execute the Member SQL Query
                await member_cursor.execute(select_query, member_val)
                member_result = await member_cursor.fetchone()
                target_user = member_result[1]

            if target_user is not None:
                member = guild.get_member(int(target_user))
                await ctx.send(f"**Sorry! That user is already married to {member.mention}**")
                return

        # Send a message to the channel mentioning the author and the person they want to wed.
        await ctx.send(f"{ctx.author.mention} **Proposes To** {member.mention}"
                       f"\n**Do you accept??**"
                       f"\nRespond with [**Y**es/**N**o]")

        # A check that makes sure that the reply is not from the author
        # and that the reply is in the same channel as the proposal
        def check(m):
            return m.author == member and m.channel == ctx.channel

        # Surround with try/except to catch any exceptions that may occur
        try:
            # Wait for the message from the mentioned user
            msg = await self.bot.wait_for('message', check=check, timeout=90)

            # if the person says yes
            if msg.content.lower() in ['y', 'yes', 'yea']:
                # Using connection to the database
                with db.connection() as conn:
                    message_time = msg.created_at.strftime("%a, %b %d, %Y")

                    # Update the existing records in the database with the user that they are marrying along with the time of the accepted proposal
                    update_query = """UPDATE members SET married = (?), marriedDate = (?) WHERE discordID = (?) AND guildID = (?)"""
                    proposer = member.id, message_time, ctx.author.id, guild.id,
                    proposee = ctx.author.id, message_time, member.id, guild.id,

                    with closing(conn.cursor()) as cursor:
                        # Execute the SQL Query's
                        cursor.execute(update_query, proposer)
                        cursor.execute(update_query, proposee)
                        conn.commit()
                        print(cursor.rowcount, "2 people have been married!")

                # Congratulate them!
                await ctx.send(
                    f"**Congratulations! ｡ﾟ( ﾟ^∀^ﾟ)ﾟ｡ {ctx.author.mention} and {member.mention} are now married to each other!**")

            # if the person says no
            elif msg.content.lower() in ['n', 'no', 'nah']:

                # Try to console the person and wish them the best in their life
                await ctx.send(f"**{ctx.author.mention} It's okay king. Pick up your crown and move on (◕‿◕✿)**")
            else:
                # Abort the process as the message sent did not make sense
                await ctx.send("**Senpaiiii! (｡╯︵╰｡) Speak English Please**")

        except asyncio.TimeoutError as ex:
            print(ex)

            # Delete the "proposal"
            await msg.delete()
            # Send out an error message if the user waited too long
            await ctx.send("**(｡T ω T｡) They waited too long**")

    @command(name="divorce", aliases=["Divorce"])
    @cooldown(1, 1, BucketType.user)
    async def divorce(self, ctx, member: Member):
        """Divorce your Partner!"""

        # Getting the guild of the user
        guild = ctx.author.guild

        # Use database connection
        with db.connection() as conn:

            # Get the author's row from the Members Table
            select_query = """SELECT * FROM members WHERE discordID = (?) and guildID = (?)"""
            val = ctx.author.id, guild.id,
            with closing(conn.cursor()) as cursor:

                # Execute the SQL Query
                cursor.execute(select_query, val)
                result = cursor.fetchone()
                married_user = result[1]

            # Make sure that the user cannot divorce themselves
            if member.id == ctx.author.id:
                await ctx.send("**Senpaii! ˭̡̞(◞⁎˃ᆺ˂)◞*✰ You can't possibly divorce yourself!**")
                return
            # Make sure that the person trying to divorce is actually married to the user
            elif married_user is None:
                await ctx.send(f"**((╬◣﹏◢)) You must be married in order to divorce someone! Baka!**")
                return
            # Make sure the person is married to the person that they're trying to divorce
            elif married_user != str(member.id):
                member = guild.get_member(int(married_user))
                await ctx.send(f"**(ノ ゜口゜)ノ You can only divorce the person that you're married!"
                               f"\n That person is {member.mention}**")
                return

        # Send a message to the channel mentioning the author and the person they want to wed.
        await ctx.send(
            f"{ctx.author.mention} **Wishes to Divorce** {member.mention}"
            f"\n**Are you willing to break this sacred bond?**"
            f"\nRespond with [**Y**es/**N**o]")

        # A check that makes sure that the reply is not from the author
        # and that the reply is in the same channel as the proposal
        def check(m):
            return m.author == member and m.channel == ctx.channel

        # Surround with try/except to catch any exceptions that may occur
        try:
            # Wait for the message from the mentioned user
            msg = await self.bot.wait_for('message', check=check, timeout=90)

            # if the person says yes
            if msg.content.lower() in ['y', 'yes', 'yea']:
                # Using connection to the database
                with db.connection() as conn:

                    # Update the existing records in the database with the user that they are marrying along with the time of the accepted proposal
                    update_query = """UPDATE members SET married = null, marriedDate = null WHERE discordID = (?) and guildID = (?)"""
                    divorcer = ctx.author.id, guild.id,
                    divorcee = member.id, guild.id,
                    with closing(conn.cursor()) as cursor:
                        # Execute the SQL Query's
                        cursor.execute(update_query, divorcer)
                        cursor.execute(update_query, divorcee)
                        conn.commit()
                        print(cursor.rowcount, "2 Members have been divorced :(!")

                # Congratulate them!
                await ctx.send(
                    f"**૮( ´⁰▱๋⁰ )ა {ctx.author.mention} and {member.mention} are now divorced."
                    f"\nI hope you two can find happiness in life with other people**")

            # if the person says no
            elif msg.content.lower() in ['n', 'no', 'nah']:

                # Try to console the person and wish them the best in their life
                await ctx.send(
                    f"**{ctx.author.mention} Sorry but you're gonna need {member.mention}'s consent to move forward with this!**")

            else:
                # Abort the process as the message sent did not make sense
                await ctx.send("**Senpaiiii! (｡╯︵╰｡) Speak English Please**")

        except asyncio.TimeoutError as ex:
            print(ex)

            await msg.delete()
            # Send out an error message if the user waited too long
            await ctx.send("**(｡T ω T｡) They waited too long**")

    @command(name="marriageinfo", aliases=["minfo", "Minfo"])
    @cooldown(1, 1, BucketType.user)
    @bot_has_permissions(embed_links=True)
    async def m_info(self, ctx, member: Member = None):
        """Marriage Information!"""

        # If a target has been specified, set them as the user
        if member:
            member = member
        # If no target has been specified, choose the author
        else:
            member = ctx.author

        # Getting the guild of the user
        guild = member.guild

        # Use database connection
        with db.connection() as conn:

            # Get the author's row from the Members Table
            select_query = """SELECT * FROM members WHERE discordID = (?) and guildID = (?)"""
            val = member.id, guild.id,
            with closing(conn.cursor()) as cursor:

                # Execute the SQL Query
                cursor.execute(select_query, val)
                result = cursor.fetchone()
                user = result[1]
                marriage_date = result[2]

            # Set empty values for non-married users
            if user is None:
                married = False
                marriedUser = ""
                marriedDate = ""
            # Set the member, date married and setting married status
            else:
                marriedUser = guild.get_member(int(user))
                marriedDate = marriage_date
                married = True

            # Get the current date of the message sent by the user
            currentDate = ctx.message.created_at.strftime("%a, %b %d, %Y")

            # Get the marriage info embed and then send it to the display
            embed = marriageInfo(member, marriedUser, marriedDate, currentDate, married)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Relationship(bot))
