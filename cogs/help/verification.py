import datetime

import discord
from discord import Colour, Embed
from discord.ext import commands
from discord.ext.commands import command, is_owner


# Set up Cog


class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = None

    # Listens to every message sent
    @commands.Cog.listener()
    async def on_message(self, message):
        # Making sure that the bot doesn't reply to itself
        if message.author == message.author.bot:
            return

        # Defining the message content in a variable
        msg = message.content

        # If the message sent is within #verification
        if message.channel.id == 728034083678060594:

            # if the user has typed ~verify
            if "~verify" in msg.lower():
                await message.delete()

                # Get the 'Lucid' role and then give it to the user
                role = discord.utils.get(message.guild.roles, name='Lucid')
                await message.author.add_roles(role)

                # if the person has the "lucid" role
                if role in message.author.roles:
                    # Set hamothyID equal to my id in discord
                    hamothyID = '<@&715412394968350756>'

                    # Set the channel id to "general"
                    general = self.bot.get_channel(663651584399507481)

                    # String for welcoming people in the #general channel
                    general_welcome = f"Welcome to the server! {message.author.mention} I hope you enjoy your stay here <a:huh:676195228872474643> <a:huh:676195228872474643> " \
                                      f"\nPlease go into <#722347423913213992> to choose some ping-able roles for events! " \
                                      f"\nPlease ping {hamothyID} for any questions about the server and of course, the other staff members!"

                    # Send welcome message to #general
                    await general.send(general_welcome)

            # Delete the message no matter what message they send
            else:
                await message.delete()

    # Allowing people to get ping-able self roles
    @command(name="verification")
    @is_owner()
    async def verification(self, ctx):
        # Set up embed to let the user know that they have to type ~verify
        embed = Embed(title="**Verification**",
                      colour=Colour(0xFF69B4),
                      timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url="https://media.discordapp.net/attachments/683490529862090814/715010931620446269"
                                "/image1.jpg?width=658&height=658")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="Type `~verify` to gain access to the rest of the server!",
            value="\u200b",
            inline=False)

        # Send embed to the channel it was called in
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Verification(bot))
