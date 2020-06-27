import datetime
import random
import string
from typing import Optional

import discord
from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown

import settings


class GetInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ~userinfo to allow the users to see information about them relating to the guild
    @commands.command(name="userinfo", aliases=["ui"])
    @cooldown(1, 1, BucketType.user)
    async def user_info(self, ctx, target: Optional[Member]):
        # If a target has been specified, set them as the user
        if target:
            target = target
        # If no target has been specified, choose the author
        else:
            target = ctx.author

        # Get the member avatar
        userAvatar = target.avatar_url

        # Get all the roles of the user
        mentions = [role.mention for role in target.roles]

        # Store the roles in a string called "roles"
        roles = ""
        # For each role that the user has
        for role in mentions:

            # Make sure that @everyone is not included in the list of roles
            if role == "<@&663651584399507476>":
                # Don't add anything to the string
                roles = ''

            else:
                # Add the role to the string
                roles += role + ' '

        # Store all the permissions that the user has in a string
        permission = ""
        # For each permission that the user has
        for perms in target.guild_permissions:

            # If the permission is set to "True"
            if perms[1]:
                # Make the string look nice by replacing _ with a space
                permission += (perms[0].replace('_', ' ')) + ', '

            # If the permission is set to "False", Don't do anything
            else:
                pass

        # Capitalise every word in the array and get rid of the ", " at the end of the string
        permissions = string.capwords("".join(map(str, permission[0:-2])))

        # Set up the embed to display everything about the user
        embed = Embed(
            title=f"**User Information**",
            colour=discord.Colour(int(random.choice(settings.colour_list))),
            timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=userAvatar)
        embed.set_footer(text=f"ID: {target.id}", icon_url='{}'.format(userAvatar))

        # Define fields to be added into the embed
        embed_fields = [("Name", str(target.mention), True),
                        ("Tag", target.name, True),
                        ("Discrim", "#" + target.discriminator, True),
                        ("Registered", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                        ("Joined", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                        ("Roles", roles, False),
                        ("All Permissions", permissions, False),
                        ("Status", str(target.status).title(), True),
                        ("Boosting Server", bool(target.premium_since), True),
                        ("Bot", target.bot, True)]

        # Add fields to the embed
        for name, value, inline in embed_fields:
            embed.add_field(name=name, value=value, inline=inline)

        # Send the embed to the channel that the command was triggered in
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo", aliases=["guildinfo"])
    @cooldown(1, 1, BucketType.user)
    async def server_info(self, ctx):
        pass


def setup(bot):
    bot.add_cog(GetInfo(bot))
