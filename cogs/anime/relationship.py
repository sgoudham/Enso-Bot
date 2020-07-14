import asyncio

from discord import Member
from discord.ext import commands
from discord.ext.commands import BucketType, command, cooldown

# Set up the Cog
import db


class Relationship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="marry", aliases=["Marry"])
    @cooldown(1, 1, BucketType.user)
    async def marry(self, ctx, member: Member):
        """Allows the bot to wed two young lovers together"""

        # Getting the guild of the user
        guild = ctx.author.guild

        # Use database connection
        with db.connection() as conn:

            # Get the author's row from the Members Table
            select_query = """SELECT * FROM members WHERE discordID = (?) and guildID = (?)"""
            val = ctx.author.id, guild.id,
            cursor = conn.cursor()

            # Execute the SQL Query
            cursor.execute(select_query, val)
            result = cursor.fetchone()

            # Make sure that the user cannot marry themselves
            if member.id == ctx.author.id:
                await ctx.send("Senpaii! ˭̡̞(◞⁎˃ᆺ˂)◞*✰ You can't possibly marry yourself!")
                return
            # Make sure that the person is not already married to someone else within the server
            elif result[2] is not None:
                member = guild.get_member(int(result[2]))
                await ctx.send(f"((╬◣﹏◢)) You're already married to {member.mention}!")
                return

        # Send a message to the channel mentioning the author and the person they want to wed.
        await ctx.send(f"{ctx.author.mention} **Proposes To** {member.mention} **Do you accept??** "
                       f"\nRespond with [**Y**es/**N**o]")

        # A check that makes sure that the reply is not from the author
        # and that the reply is in the same channel as the proposal
        def check(m):
            return m.author == member and m.channel == ctx.channel

        # Surround with try/except to catch any exceptions that may occur
        try:
            # Wait for the message from the mentioned user
            msg = await self.bot.wait_for('message', check=check, timeout=30)

            # if the person says yes
            if msg.content.lower() in ['y', 'yes', 'yea']:
                # Using connection to the database
                with db.connection() as conn:
                    message_time = msg.created_at.strftime("%a, %b %d, %Y")

                    # Update the existing records in the database with the user that they are marrying along with the time of the accepted proposal
                    update_query = """UPDATE members SET married = (?), marriedDate = (?) WHERE discordID = (?) AND guildID = (?)"""
                    proposer = member.id, message_time, ctx.author.id, guild.id,
                    proposee = ctx.author.id, message_time, member.id, guild.id,
                    cursor = conn.cursor()

                    # Execute the SQL Query's
                    cursor.execute(update_query, proposer)
                    cursor.execute(update_query, proposee)
                    conn.commit()
                    print(cursor.rowcount, "2 people have been marred!")

                # Congratulate them!
                await ctx.send(
                    f"Congratulations! ｡ﾟ( ﾟ^∀^ﾟ)ﾟ｡ {ctx.author.mention} and {member.mention} are now married to each other!")

            # if the person says no
            elif msg.content.lower() in ['n', 'no', 'nah']:

                # Try to console the person and wish them the best in their life
                await ctx.send(f"{ctx.author.mention} It's okay King. Pick up your crown and move on (◕‿◕✿)")
            else:
                # Abort the process as the message sent did not make sense
                await ctx.send("Senpaiiii! (｡╯︵╰｡) Speak English Please")

        except asyncio.TimeoutError as ex:
            print(ex)

            # Send out an error message if the user waited too long
            await ctx.send("(｡T ω T｡) They waited too long")

    @command(name="divorce", aliases=["Divorce"])
    @cooldown(1, 1, BucketType.user)
    async def divorce(self, ctx, member: Member):
        """Allows the bot to divorce users"""

        # Getting the guild of the user
        guild = ctx.author.guild

        # Use database connection
        with db.connection() as conn:

            # Get the author's row from the Members Table
            select_query = """SELECT * FROM members WHERE discordID = (?) and guildID = (?)"""
            val = ctx.author.id, guild.id,
            cursor = conn.cursor()

            # Execute the SQL Query
            cursor.execute(select_query, val)
            result = cursor.fetchone()

            # Make sure that the user cannot divorce themselves
            if member.id == ctx.author.id:
                await ctx.send("Senpaii! ˭̡̞(◞⁎˃ᆺ˂)◞*✰ You can't possibly divorce yourself!")
                return
            # Make sure that the person trying to divorce is actually married to the user
            elif result[2] is None:
                await ctx.send(f"((╬◣﹏◢)) You must be married in order to divorce someone! Baka!")
                return
            # Make sure the person is married to the person that they're trying to divorce
            elif result[2] != str(member.id):
                member = guild.get_member(int(result[2]))
                await ctx.send(f"(ノ ゜口゜)ノ You can only divorce the person that you're married!"
                               f"\n That person is {member.mention}")
                return

        # Send a message to the channel mentioning the author and the person they want to wed.
        await ctx.send(
            f"{ctx.author.mention} **Wishes to Divorce** {member.mention} **Are you willing to break this sacred bond??**"
            f"\nRespond with [**Y**es/**N**o]")

        # A check that makes sure that the reply is not from the author
        # and that the reply is in the same channel as the proposal
        def check(m):
            return m.author == member and m.channel == ctx.channel

        # Surround with try/except to catch any exceptions that may occur
        try:
            # Wait for the message from the mentioned user
            msg = await self.bot.wait_for('message', check=check, timeout=30)

            # if the person says yes
            if msg.content.lower() in ['y', 'yes', 'yea']:
                # Using connection to the database
                with db.connection() as conn:

                    # Update the existing records in the database with the user that they are marrying along with the time of the accepted proposal
                    update_query = """UPDATE members SET married = null, marriedDate = null WHERE discordID = (?) and guildID = (?)"""
                    divorcer = ctx.author.id, guild.id,
                    divorcee = member.id, guild.id,
                    cursor = conn.cursor()

                    # Execute the SQL Query's
                    cursor.execute(update_query, divorcer)
                    cursor.execute(update_query, divorcee)
                    conn.commit()
                    print(cursor.rowcount, "2 Members have been divorced :(!")

                # Congratulate them!
                await ctx.send(
                    f" ૮( ´⁰▱๋⁰ )ა {ctx.author.mention} and {member.mention} are now divorced. I hope you two can find happiness in life with other people")

            # if the person says no
            elif msg.content.lower() in ['n', 'no', 'nah']:

                # Try to console the person and wish them the best in their life
                await ctx.send(f"Sorry but you're gonna need {ctx.author.mention}'s consent to move forward with this!")

            else:
                # Abort the process as the message sent did not make sense
                await ctx.send("Senpaiiii! (｡╯︵╰｡) Speak English Please")

        except asyncio.TimeoutError as ex:
            print(ex)

            # Send out an error message if the user waited too long
            await ctx.send("(｡T ω T｡) They waited too long")


def setup(bot):
    bot.add_cog(Relationship(bot))
