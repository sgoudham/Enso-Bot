import datetime

from discord import Embed
from discord.ext import commands
from discord.ext.commands import command, cooldown, BucketType

import db
from settings import enso_embedmod_colours, blank_space


# Set up the Cog
class SetupModmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="mmsetup")
    @cooldown(1, 1, BucketType.user)
    async def _setup(self, ctx, *args):
        """Allows the bot to setup a channel for users to react to for sending modmail"""

        # Make sure the first two arguments are set and modmail
        if args[0] == "set":
            if args[1] == "modmail":

                # Retrieve a list of channel id's in the guild
                channels = [channel.id for channel in ctx.guild.channels]

                # Ask for the channel ID that the modmail should be logged to
                await ctx.send("`Please enter the ID of the channel you want your modmail to be sent`")

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
                        (blank_space, "**React to this message if you want to send a message to the Staff Team!**",
                         False),
                        ("**React with ✅**",
                         "We encourage all suggestions/thoughts and opinions on the server! As long as it is **valid** criticism."
                         "Purely negative feedback will not be considered.", False)]

                    # Add the fields to the embed
                    for name, value, inline in fields:
                        ModMail.add_field(name=name, value=value, inline=inline)

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
                else:
                    # Send error message if the channel ID is not recognised
                    await ctx.send("`Invalid Channel ID. Aborting Process...`")
                    return


def setup(bot):
    bot.add_cog(SetupModmail(bot))
