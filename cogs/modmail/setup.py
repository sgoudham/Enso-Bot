import datetime

import mariadb
from discord import Embed
from discord.ext import commands
from discord.ext.commands import command, cooldown, BucketType, has_permissions

import db
from settings import enso_embedmod_colours


# Set up the Cog
class SetupModmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="mmsetup")
    @has_permissions(manage_messages=True, manage_roles=True, manage_channels=True)
    @cooldown(1, 1, BucketType.user)
    async def _setup(self, ctx, *args):
        """Allows the bot to setup a channel for users to react to for sending modmail"""

        # Retrieve a list of channel id's in the guild
        channels = [channel.id for channel in ctx.guild.channels]

        # Allows the user to setup modmail for the first time
        if args[0] == "set":
            if args[1] == "modmail":

                # Checking if the guild already exists within the database
                with db.connection() as conn:
                    # Get the author's row from the Members Table
                    select_query = """SELECT * FROM moderatormail WHERE guildID = (?)"""
                    val = ctx.author.guild.id,
                    cursor = conn.cursor()

                    # Execute the SQL Query
                    cursor.execute(select_query, val)
                    result = cursor.fetchone()

                    # Throw error if the guild already exists and then stop the function
                    if result is not None:
                        await ctx.send("**Looks like this guild already has a modmail system set up!" +
                                       f"\nPlease check `{ctx.prefix}help` for information on how to update/delete existing information**")
                        return

                # As long as the channel exists within the guild
                if int(args[2]) in channels:

                    # Ask for the channel ID that the modmail should be logged to
                    await ctx.send("**Please enter the ID of the channel you want your modmail to be sent**")

                    # Check the response is from the author and from the same channel as the previous message
                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel

                    # Wait for the message from the author
                    msg = await self.bot.wait_for('message', check=check)

                    # As long as the channel exists within the guild
                    if int(msg.content) in channels:

                        # Set up embed to let the user how to start sending modmail
                        ModMail = Embed(title="**Welcome to Modmail!**",
                                        colour=enso_embedmod_colours,
                                        timestamp=datetime.datetime.utcnow())

                        ModMail.set_thumbnail(url=self.bot.user.avatar_url)

                        # Define fields to be inserted into the embed
                        fields = [
                            ("**React to this message if you want to send a message to the Staff Team!**",
                             "**React with ✅**", False),
                            ("We encourage all suggestions/thoughts and opinions on the server!" +
                             "As long as it is **valid** criticism.",
                             "Purely negative feedback will not be considered.", False)]

                        # Add the fields to the embed
                        for name, value, inline in fields:
                            ModMail.add_field(name=name, value=value, inline=inline)

                        try:
                            # Get the channel object from the channelID input by the user
                            channel = ctx.author.guild.get_channel(int(args[2]))
                            modmailchannelID = await channel.send(embed=ModMail)
                            # Auto add the ✅ reaction
                            await modmailchannelID.add_reaction('✅')

                            # Store the information within the database
                            with db.connection() as conn:
                                # Define the insert statement that will insert information about the modmail channel
                                insert_query = """INSERT INTO moderatormail (guildID, channelID, messageID, modmailChannelID) VALUES (?, ?, ?, ?)"""
                                vals = ctx.author.guild.id, args[2], modmailchannelID.id, int(msg.content),
                                cursor = conn.cursor()

                                # Execute the SQL Query
                                cursor.execute(insert_query, vals)

                            await ctx.send("**Your Modmail system is now successfully set up!" +
                                           f"\nPlease refer to `{ctx.prefix}help` for any information**")
                            return

                        except mariadb.IntegrityError as err:
                            print(err)
                            await ctx.send("Looks like this guild already has a modmail system set up!" +
                                           f"\nPlease check `{ctx.prefix}help` for information on how to update/delete existing information")
                    else:
                        # Send error message if the channel ID is not recognised
                        await ctx.send("`Invalid Channel ID. Aborting Process...`")
                        return
                else:
                    # Send error message if the channel ID is not recognised
                    await ctx.send("`Invalid Channel ID. Aborting Process...`")
                    return

        # Allows the user to update the channel that the modmail can be sent to
        if args[0] == "update":
            if args[1] == "modmail":

                # Checking if the guild already exists within the database
                with db.connection() as conn:
                    # Get the author's row from the Members Table
                    select_query = """SELECT * FROM moderatormail WHERE guildID = (?)"""
                    vals = ctx.author.guild.id,
                    cursor = conn.cursor()

                    # Execute the SQL Query
                    cursor.execute(select_query, vals)
                    result = cursor.fetchone()

                    # Throw error if the guild already exists and then stop the function
                    if result is None:
                        await ctx.send("**Looks like this guild does not have a modmail system setup!" +
                                       f"\nPlease check `{ctx.prefix}help` for information on how to update/delete existing information**")
                        return

                # As long as the channel exists within the guild
                if int(args[2]) in channels:

                    try:
                        # Store the information within the database
                        with db.connection() as conn:
                            # Define the insert statement that will insert information about the modmail channel
                            update_query = """UPDATE moderatormail SET modmailChannelID = (?) WHERE guildID = (?)"""
                            vals = args[2], ctx.author.guild.id
                            cursor = conn.cursor()

                            # Execute the SQL Query
                            cursor.execute(update_query, vals)
                            conn.commit()

                    except mariadb.Error as err:
                        print(err)
                        await ctx.send("**Looks like something went wrong during the update!"
                                       "\nMake sure that the Channel ID is correct!**")

                    channel = ctx.author.guild.get_channel(int(args[2]))
                    await ctx.send(
                        f"**The channel has been updated! Your new modmail will be sent to** {channel.mention}")

                else:
                    # Send error message if the channel ID is not recognised
                    await ctx.send("`Invalid Channel ID. Aborting Process...`")
                    return

        # Allows the user to completely erase the modmail system currently set up
        if args[0] == "delete":
            if args[1] == "modmail":

                # Checking if the guild already exists within the database
                with db.connection() as conn:
                    # Get the author's row from the Members Table
                    select_query = """SELECT * FROM moderatormail WHERE guildID = (?)"""
                    vals = ctx.author.guild.id,
                    cursor = conn.cursor()

                    # Execute the SQL Query
                    cursor.execute(select_query, vals)
                    result = cursor.fetchone()

                    # Throw error if the guild already exists and then stop the function
                    if result is None:
                        await ctx.send("**Looks like this guild does not have a modmail system setup!" +
                                       f"\nPlease check `{ctx.prefix}help` for information on how to update/delete existing information**")
                        return

                try:
                    # Store the information within the database
                    with db.connection() as conn:
                        # Define the delete statement to remove all information about the guild
                        delete_query = """DELETE FROM moderatormail WHERE guildID = (?)"""
                        vals = ctx.author.guild.id,
                        cursor = conn.cursor()

                        # Execute the SQL Query
                        cursor.execute(delete_query, vals)
                        conn.commit()

                except mariadb.Error as err:
                    print(err)
                    await ctx.send("**Looks like this guild has not set up the modmail system yet!" +
                                   f"\nPlease do `{ctx.prefix}help` to find out how to set it up!**")

                # Sending confirmation message that the modmail system has been deleted
                await ctx.send("**Modmail system successfully deleted!" +
                               f"\nPlease do `{ctx.prefix}help` to find out how to set Modmail again!**")


def setup(bot):
    bot.add_cog(SetupModmail(bot))
