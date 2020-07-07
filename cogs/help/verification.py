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

    # Setting up Listener to listen for reactions within the Verification channel
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Get the guild
        guild = self.bot.get_guild(663651584399507476)
        # Get the member
        member = guild.get_member(payload.user_id)

        # Getting the channel verification by setting it to #verification
        channel = guild.get_channel(728034083678060594)

        # If the channel is #verification
        if payload.channel_id == channel.id:

            # A check that makes sure that the reaction is done by the bot
            def check(m):
                return m == self.bot

            # If the member is not a user, do nothing
            if not check:
                return
            else:

                # Get the 'Lucid' role and then give it to the user
                role = discord.utils.get(guild.roles, name='Lucid')

                # if the emoji that was reacted is the tick mark.
                if payload.emoji.name == "✅":
                    await member.add_roles(role)

                    # Set hamothyID equal to my id in discord
                    hamothyID = '<@&715412394968350756>'

                    # Set the channel id to "general"
                    general = guild.get_channel(663651584399507481)

                    # String for welcoming people in the #general channel
                    general_welcome = f"Welcome to the server! {member.mention} I hope you enjoy your stay here <a:huh:676195228872474643> <a:huh:676195228872474643> " \
                                      f"\nPlease go into <#722347423913213992> to choose some ping-able roles for events! " \
                                      f"\nPlease ping {hamothyID} for any questions about the server and of course, the other staff members!"

                    # Send welcome message to #general
                    await general.send(general_welcome)

    # Allowing people to get ping-able self roles
    @command(name="verification")
    @is_owner()
    async def verification(self, ctx):
        # Set up embed to let the user know that they have to react with ✅
        embed = Embed(title="**Verification**",
                      colour=Colour(0xFF69B4),
                      timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="Remember to read the rules!",
            value="React with ✅ to gain access to the rest of the server!",
            inline=False)

        # Edit the Embed And Update it
        verif = await ctx.fetch_message(728424149692842115)
        await verif.edit(embed=embed)

        # Send embed to the channel it was called in and automatically add the reaction ✅
        # verif = await ctx.send(embed=embed)
        # await verif.add_reaction('✅')


def setup(bot):
    bot.add_cog(Verification(bot))
