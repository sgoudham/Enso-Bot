import datetime
import random
import string
from typing import Optional

from discord import Embed, Member, Colour
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, command

import settings


class GetInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ~userinfo to allow the users to see information about them relating to the guild
    @command(name="userinfo", aliases=["ui"])
    @cooldown(1, 5, BucketType.user)
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
        # For each role that the user has (Skipping the first element as it's always going to be @everyone
        for role in mentions[1:]:
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
            colour=Colour(int(random.choice(settings.colour_list))),
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

    # ~serverinfo to allow the users to see information the guild itself
    @command(name="serverinfo", aliases=["guildinfo"])
    @cooldown(1, 5, BucketType.user)
    async def server_info(self, ctx):

        # Define guild icon and id
        guild_icon = ctx.guild.icon_url
        guild_id = ctx.guild.id

        # Define the statuses of the members within the discord
        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

        # Set up embed to display all the server information
        embed = Embed(title="**Server Information**",
                      colour=Colour(int(random.choice(settings.colour_list))),
                      timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=guild_icon)
        embed.set_footer(text=f"ID: {guild_id}", icon_url='{}'.format(guild_icon))

        # Define fields to be added into the embed
        fields = [("Owner", ctx.guild.owner, True),
                  ("Created", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), False),
                  ("Region", str(ctx.guild.region).upper(), False),
                  ("Statuses", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", False),
                  ("\u200b", "\u200b", False),
                  ("Members", len(ctx.guild.members), True),
                  ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                  ("Bots", len(list(filter(lambda c: c.bot, ctx.guild.members))), True),
                  ("Banned Members", len(await ctx.guild.bans()), True),
                  ("Text Channels", len(ctx.guild.text_channels), True),
                  ("Voice Channels", len(ctx.guild.voice_channels), True),
                  ("Categories", len(ctx.guild.categories), True),
                  ("Roles", len(ctx.guild.roles), True),
                  ("Invites", len(await ctx.guild.invites()), True)]

        # Add fields to the embed
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        # Send the embed to the channel that the command was triggered in
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(GetInfo(bot))
