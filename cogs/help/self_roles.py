import datetime

import discord
from discord import Colour, Embed
from discord.ext import commands
# Set up the Cog
from discord.ext.commands import command, is_owner


class SelfRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Cog listener for enabling roles to be added to users when they react to the embedded message
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        # If the message id equals the self roles message
        if payload.message_id == 722514840559812649:

            # Print out the emoji name
            print(payload.emoji.name)

            # Find a role corresponding to the Emoji name.
            guild_id = payload.guild_id

            # Find the guild Enso and find the role of the emoji that has been reacted to
            guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
            role = discord.utils.find(lambda r: r.name == payload.emoji.name, guild.roles)

            # if the role does exist
            if role is not None:
                # Print to me that the role was found and display the id of the role
                print(role.name + " was found!")
                print(role.id)

                # Find the member who had reacted to the emoji
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                # Add the role to the member
                await member.add_roles(role)

                # Print to me that the role has been added
                print("done")

    # Cog listener for enabling roles to be removed from users when they unreact to the embedded messaged
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        # If the message id equals the self roles message
        if payload.message_id == 722514840559812649:

            # Print out the emoji name
            print(payload.emoji.name)

            # Get the server id
            guild_id = payload.guild_id

            # Find the guild Enso and find the role of the emoji that has been unreacted to
            guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
            role = discord.utils.find(lambda r: r.name == payload.emoji.name, guild.roles)

            # if the role does exist
            if role is not None:
                # Find the member that has the role which the emoji is connected to
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)

                # Remove the role from the member
                await member.remove_roles(role)

    # Allowing people to get ping-able self roles
    @command(name="rolemenu")
    @is_owner()
    async def role_menu(self, ctx):
        # Get the channel id of #self-roles
        channel = self.bot.get_channel(722347423913213992)

        # Set up embed to let people know what ping-able roles can be chosen
        embed = Embed(title="**Role Menu: Ping-Able Roles**",
                      colour=Colour.orange(),
                      timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url="https://media.discordapp.net/attachments/683490529862090814/715010931620446269"
                                "/image1.jpg?width=658&height=658")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.message.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="\u200b",
            value="React to give yourself roles to be pinged for these events!",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="<:MovieNight:722293598938333190> : `Movie Nights`",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="<:Karaoke:722358251932483605> : `Karaoke Nights`",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="<:EnsoBros:722360289345011743> : `Enso Bros Podcasts`",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="<:GameNights:722502073769525268> : `Game Nights`",
            inline=False)

        # Send embed to #self-roles
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(SelfRoles(bot))
