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

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Get the guild
        guild = self.bot.get_guild(payload.guild_id)
        # Get the member
        member = guild.get_member(payload.user_id)
        # Get the 'Lucid' role and then give it to the user
        role = discord.utils.get(guild.roles, name='Lucid')

        if payload.channel_id == 728034083678060594:
            if payload.emoji.name == "✅":
                await member.add_roles(role)

                # Set hamothyID equal to my id in discord
                hamothyID = '<@&715412394968350756>'

                # Set the channel id to "general"
                general = self.bot.get_channel(663651584399507481)

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
        # Set up embed to let the user know that they have to type ~verify
        embed = Embed(title="**Verification**",
                      colour=Colour(0xFF69B4),
                      timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url="https://media.discordapp.net/attachments/683490529862090814/715010931620446269"
                                "/image1.jpg?width=658&height=658")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="\u200b",
            value="React with ✅ to gain access to the rest of the server!",
            inline=False)

        # Send embed to the channel it was called in
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Verification(bot))