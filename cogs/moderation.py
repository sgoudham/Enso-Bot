# Ensō~Chan - A Multi Purpose Discord Bot That Has Everything Your Server Needs!
# Copyright (C) 2020  Hamothy

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import datetime
import string
from datetime import timedelta
from typing import Optional

import discord
from discord import Member, Embed, DMChannel, NotFound, User
from discord.ext.commands import command, guild_only, has_guild_permissions, bot_has_guild_permissions, Greedy, \
    cooldown, BucketType, Cog

from cogs.libs.functions import string_list, get_region, get_content_filter, get_notifs, detect_perms, perms

# TODO: CREATE A BITARRAY SO THAT THE MODLOG EVENTS ARE TOGGLEABLE
# TODO: MAKE SURE THAT THE BITARRAY IS ONLY IMPLEMENTED AFTER ALL EVENTS ARE CODED

# Defining a dictionary of the statuses to emojis
member_status = {
    "online": "<a:online:753214525272096831>",
    "idle": "<a:idle:753214548756004924>",
    "dnd": "<a:dnd:753214555999567953>",
    "offline": "<a:offline:753214562970501171>"
}


async def send_to_modlogs(self, ctx, target, reason, action):
    """
    Function to send the moderation actions to modlogs channel

    On top of the normal logging, this function sends another embed
    if the user has used the inbuilt mute command which allows for a
    reason to be given

    """

    # Get the channel of the modlog within the guild
    if modlog := self.bot.get_modlog_for_guild(ctx.guild.id):
        channel = ctx.guild.get_channel(modlog)

        if isinstance(target, User):
            desc = f"**User -->** {target}\n**ID -->** {target.id}" \
                   f"\n\n**Auctioned By --> {ctx.author.mention} | {ctx.author}\nID -->** {ctx.author.id}"
            embed = Embed(title=f"User {action}",
                          description=desc,
                          colour=self.bot.admin_colour,
                          timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=target.avatar_url)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_footer(text=f"User {action}")
        else:
            desc = f"**Member --> {target.mention} |** {target}\n**ID -->** {target.id}" \
                   f"\n\n**Auctioned By --> {ctx.author.mention} | {ctx.author}\nID -->** {ctx.author.id}"
            embed = Embed(title=f"Member {action}",
                          description=desc,
                          colour=self.bot.admin_colour,
                          timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=target.avatar_url)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_footer(text=f"Member {action}")

        await channel.send(embed=embed)


async def check(ctx, members):
    """
    Check Function

    - Checks if all arguments are given
    - Checks if user mentions themselves

    Error will be thrown in these two cases
    """

    if not len(members):
        desc = f"Not Correct Syntax!\nUse **{ctx.prefix}help** to find how to use **{ctx.command}**"
        await ctx.bot.generate_embed(ctx, desc=desc)
        return True

    elif ctx.author in members:
        await ctx.bot.generate_embed(ctx, desc=f"**{ctx.bot.cross} Forbidden Action {ctx.bot.cross}**")
        return True


async def ummute_members(self, ctx, targets, reason):
    """

    Method to allow members to be unmuted

    2 embeds will be sent, one to the channel that the user is in
    And if the user has the modlogs channel setup, an embed will be logged there
c3
    """

    for target in targets:
        if (ctx.guild.me.top_role.position > target.top_role.position
                and not target.guild_permissions.administrator):

            # Get the roles of the user
            result = await self.bot.check_cache(target.id, ctx.guild.id)

            # Get muted roles of the user from cache/database and give them back
            role_ids = result["muted_roles"]
            roles = [ctx.guild.get_role(int(id_)) for id_ in role_ids.split(", ") if len(id_)]

            # Clear all the roles of the user
            await self.bot.clear_roles(member=target)

            await target.edit(roles=roles)

            # Send confirmation to the channel that the user is in
            await self.bot.generate_embed(ctx, desc=f"{ctx.bot.tick} **{target}** Was Unmuted! {ctx.bot.tick}")

            await send_to_modlogs(self, ctx, target, reason, action="Unmuted")

        # Send error message if the User could not be muted
        else:
            desc = f"**{target.mention} Could Not Be Unmuted!**"
            await self.bot.generate_embed(ctx, desc=desc)


async def mute_members(self, ctx, targets, reason, muted):
    """

    Method to allow members to be muted

    2 embeds will be sent, one to the channel that the user is in
    And if the user has the modlogs channel setup, an embed will be logged there

    """

    for target in targets:

        # When user is already muted, send error message
        if muted in target.roles:
            await self.bot.generate_embed(ctx, desc=f"**{ctx.bot.cross} User Is Already Muted! {ctx.bot.cross}**")

        else:

            # Store managed roles into the list of roles to be added to the user (including muted)
            roles = [role for role in target.roles if role.managed]
            roles.append(muted)

            if (ctx.guild.me.top_role.position > target.top_role.position
                    and not target.guild_permissions.administrator):

                # Store the current roles of the user within database
                await self.bot.store_roles(target=target, ctx=ctx, member=target)
                # Give the user the muted role (and any integration roles if need be)
                await target.edit(roles=roles, reason=reason)

                # Send confirmation to the channel that the user is in
                embed = Embed(description=f"{ctx.bot.tick} **{target}** Was Muted! {ctx.bot.tick}",
                              colour=self.bot.admin_colour)

                if self.bot.get_roles_persist(ctx.guild.id) == 0:
                    embed.add_field(name="**WARNING: ROLE PERSIST NOT ENABLED**",
                                    value="The bot **will not give** the roles back to the user if they leave the server."
                                          "\nAllowing the user to bypass the Mute by leaving and rejoining."
                                          f"\nPlease enable Role Persist by doing **{ctx.prefix}rolepersist enable**",
                                    inline=True)

                await ctx.send(embed=embed)

                await send_to_modlogs(self, ctx, target, reason, action="Muted")

            # Send error message if the User could not be muted
            else:
                await self.bot.generate_embed(ctx, desc=f"**{target.mention} Could Not Be Muted!**")


async def ban_members(self, ctx, users, reason):
    """

    Method to allow members to be banned

    2 embeds will be sent, one to the channel that the user is in
    And if the user has the modlogs channel setup, an embed will be logged there

    """

    # Get the list of banned users from the server
    bans = await ctx.guild.bans()
    banned_members = list(map(lambda m: m.user, bans))

    for user in users:
        # Make sure that the user not banned already
        if user in banned_members:
            await self.bot.generate_embed(ctx, desc=f"{ctx.bot.cross} **Member Is Already Banned!** {ctx.bot.cross}")
            continue

        # Ban
        if user in ctx.guild.members:
            member = ctx.guild.get_member(user.id)
            if (ctx.guild.me.top_role.position > member.top_role.position
                    and not member.guild_permissions.administrator):

                await member.ban(reason=reason)
                await self.bot.generate_embed(ctx, desc=f"{ctx.bot.tick} **{member}** Was Banned! {ctx.bot.tick}")

                await send_to_modlogs(self, ctx, member, reason, action="Banned")

            # Send error message if the User could not be banned
            else:
                await self.bot.generate_embed(ctx, desc=f"**{member} Could Not Be Banned!**")
        else:
            await ctx.guild.ban(discord.Object(id=user.id), reason=reason)

            # Send confirmation to the channel that the user is in
            await self.bot.generate_embed(ctx,
                                          desc=f"{self.bot.tick} **{user}** Was Power Banned! {self.bot.tick}")

            await send_to_modlogs(self, ctx, user, reason, action="Power Banned")


async def unban_members(self, ctx, users, reason):
    """

    Method to allow members to be unbanned

    2 embeds will be sent, one to the channel that the user is in
    And if the user has the modlogs channel setup, an embed will be logged there

    """

    # Get the list of banned users from the server
    bans = await ctx.guild.bans()
    ban_users = list(map(lambda m: m.user, bans))

    for user in users:
        if user not in ban_users:
            await self.bot.generate_embed(ctx, desc=f"{ctx.bot.cross} **Member Is Not Banned!** {ctx.bot.cross}")

        else:
            await ctx.guild.unban(discord.Object(id=user.id), reason=reason)

            # Send confirmation to the channel that the user is in
            await self.bot.generate_embed(ctx, desc=f"{ctx.bot.tick} **{user}** Was Unbanned! {ctx.bot.tick}")

            await send_to_modlogs(self, ctx, user, reason, action="Unbanned")


async def kick_members(self, ctx, targets, reason):
    """

    Method to allow the kick member log to be sent to the modlog channel

    2 embeds will be sent, one to the channel that the user is in
    And if the user has the modlogs channel setup, an embed will be logged there

    """

    for target in targets:
        if (ctx.guild.me.top_role.position > target.top_role.position
                and not target.guild_permissions.administrator):

            await target.kick(reason=reason)

            await self.bot.generate_embed(ctx, desc=f"{ctx.bot.tick} **{target}** Was Kicked! {ctx.bot.tick}")

            await send_to_modlogs(self, ctx, target, reason, action="Kicked")

        # Send error message if the User could not be kicked
        else:
            await self.bot.generate_embed(ctx, desc=f"**{target.mention} Could Not Be Kicked!**")


class Moderation(Cog):
    """Moderation Commands! (Kick/Ban/Mute etc)"""

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @command(name="kick", usage="`<member>...` `[reason]`")
    @guild_only()
    @has_guild_permissions(kick_members=True)
    @bot_has_guild_permissions(kick_members=True)
    @cooldown(1, 1, BucketType.user)
    async def kick_member(self, ctx, members: Greedy[Member], *, reason: Optional[str] = "No Reason Given"):
        """
        Kick Member(s) from Server
        Multiple Members can be Kicked at Once
        """

        if not await check(ctx, members):
            with ctx.typing():
                # Send embed of the kicked member
                await kick_members(self, ctx, members, reason)

    @command(name="mute", usage="`<member>...` `[reason]`")
    @has_guild_permissions(manage_roles=True)
    @bot_has_guild_permissions(manage_roles=True)
    @cooldown(1, 1, BucketType.user)
    async def mute(self, ctx, members: Greedy[Member], *, reason: Optional[str] = "No Reason Given"):
        """
        Mute Member(s) from Server
        Multiple Members can be Muted At Once
        """

        if not await check(ctx, members):
            with ctx.typing():

                # Get muted role from the server
                role = discord.utils.get(ctx.guild.roles, name="Muted")

                # Create muted role when no muted role exists and mute member(s)
                if not role:
                    muted = await ctx.guild.create_role(name="Muted")
                    for channel in ctx.guild.channels:
                        await channel.set_permissions(muted, send_messages=False)

                    await mute_members(self, ctx, members, reason, muted)

                else:
                    await mute_members(self, ctx, members, reason, role)

    @command(name="unmute", usage="`<member>...` `[reason]`")
    @has_guild_permissions(manage_roles=True)
    @bot_has_guild_permissions(manage_roles=True)
    @cooldown(1, 1, BucketType.user)
    async def unmute(self, ctx, members: Greedy[Member], *, reason: Optional[str] = "No Reason Given"):
        """
        Unmute Member(s) from Server
        Multiple Members can be unmuted at once
        """
        unmute = False

        if not await check(ctx, members):
            with ctx.typing():
                role = discord.utils.get(ctx.guild.roles, name="Muted")
                if not role:
                    desc = f"**{self.bot.cross} No Muted Role Was Found! {self.bot.cross}**"
                    await self.bot.generate_embed(ctx, desc=desc)

                else:
                    for member in members:
                        if role in member.roles:
                            await ummute_members(self, ctx, members, reason)
                            unmute = True
                        if role not in member.roles and unmute is False:
                            desc = f"**{self.bot.cross} {member.mention} Is Not Muted! {self.bot.cross}**"
                            await self.bot.generate_embed(ctx, desc=desc)

    @command(name="ban", usage="`<member>...` `[reason]`")
    @guild_only()
    @has_guild_permissions(ban_members=True)
    @bot_has_guild_permissions(ban_members=True)
    @cooldown(1, 1, BucketType.user)
    async def ban(self, ctx, members: Greedy[User], *, reason: Optional[str] = "No Reason Given"):
        """
        Ban Member(s) from Server
        Multiple Members can be banned at once
        """

        if not await check(ctx, members):
            with ctx.typing():
                await ban_members(self, ctx, members, reason)

    @command(name="unban", usage="`<member>...` `[reason]`")
    @guild_only()
    @has_guild_permissions(ban_members=True)
    @bot_has_guild_permissions(ban_members=True)
    @cooldown(1, 1, BucketType.user)
    async def unban(self, ctx, members: Greedy[User], *, reason: Optional[str] = "No Reason Given"):
        """
        Unban Member(s) from Server
        Multiple Members can be Unbanned At Once
        """

        if not await check(ctx, members):
            with ctx.typing():
                await unban_members(self, ctx, members, reason)

    @command(name="purge")
    @guild_only()
    @has_guild_permissions(manage_messages=True)
    @bot_has_guild_permissions(manage_messages=True, read_message_history=True)
    @cooldown(1, 1, BucketType.user)
    async def purge(self, ctx, amount: int = None):
        """
        Purge Messages from Channel
        (No Amount Will Default to 50 Messages Deleted)
        """

        # When an amount is specified and is between 0 and 100
        if amount:
            if 0 < amount <= 100:

                # Delete the message sent and then the amount specified
                # (Only messages sent within the last 14 days)

                await ctx.message.delete()
                deleted = await ctx.channel.purge(limit=amount,
                                                  after=datetime.datetime.utcnow() - timedelta(days=14))

                await ctx.send(f"Deleted **{len(deleted):,}** messages.", delete_after=5)

            # Send error if amount is not between 0 and 100
            else:
                await self.bot.generate_embed(ctx, desc="The amount provided is not between **0** and **100**")

        # Delete the last 50 messages if no amount is given
        else:

            # Delete the message sent and then the amount specified
            # (Only messages sent within the last 14 days)

            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=50,
                                              after=datetime.datetime.utcnow() - timedelta(days=14))

            await ctx.send(f"Deleted **{len(deleted):,}** messages.", delete_after=5)

    @ban.error
    @unban.error
    async def ban_command_error(self, ctx, exc):
        """Catching error if channel is not recognised"""

        error = getattr(exc, "original", exc)

        if isinstance(error, NotFound):
            text = f"**{self.bot.cross} User Not Detected... Aborting Process** {self.bot.cross}"
            await self.bot.generate_embed(ctx, desc=text)

    @Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        """Logging Bulk Message Deletion from Server"""

        if modlogs := self.bot.get_modlog_for_guild(payload.guild_id):
            modlogs_channel = self.bot.get_channel(modlogs)

            deleted_msgs_channel = self.bot.get_channel(payload.channel_id)
            desc = f"**Bulk Delete in {deleted_msgs_channel.mention} | {len(payload.message_ids)} messages deleted**"

            # Set up embed showing the messages deleted and what channel they were deleted in
            embed = Embed(
                description=desc,
                colour=self.bot.admin_colour,
                timestamp=datetime.datetime.utcnow())
            embed.set_author(name=deleted_msgs_channel.guild.name, icon_url=deleted_msgs_channel.guild.icon_url)
            embed.set_footer(text="Bulk Message Deletion")

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_remove(self, member):
        """Log Member Leaves from Server"""

        if member == self.bot.user: return

        removed_at = datetime.datetime.utcnow()
        if modlogs := self.bot.get_modlog_for_guild(member.guild.id):
            modlogs_channel = self.bot.get_channel(modlogs)

            embed = Embed(title="Member Left",
                          description=f"**Member --> {member.mention} |** {member}"
                                      f"\n**ID -->** {member.id}",
                          colour=self.bot.admin_colour,
                          timestamp=removed_at)
            embed.add_field(name="Account Creation Date",
                            value=member.created_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"), inline=True)
            embed.add_field(name="Member Left Date", value=removed_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"),
                            inline=True)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"Member Left")

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_join(self, member):
        """Log Member Joins to Server"""

        if member == self.bot.user: return

        joined_at = datetime.datetime.utcnow()
        if modlogs := self.bot.get_modlog_for_guild(member.guild.id):
            modlogs_channel = self.bot.get_channel(modlogs)

            embed = Embed(title="Member Joined",
                          description=f"**Member --> {member.mention} |** {member}"
                                      f"\n**ID -->** {member.id}",
                          colour=self.bot.admin_colour,
                          timestamp=joined_at)
            embed.add_field(name="Account Creation Date",
                            value=member.created_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"), inline=True)
            embed.add_field(name="Member Joined Date", value=joined_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"),
                            inline=True)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"Member Joined")

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_ban(self, guild, user):
        """Logs Member Bans to Server"""

        if user == self.bot.user: return

        banned_at = datetime.datetime.utcnow()
        if modlogs := self.bot.get_modlog_for_guild(guild.id):
            modlogs_channel = self.bot.get_channel(modlogs)

            embed = Embed(title="Member Banned",
                          description=f"**Member --> {user.mention} |** {user}"
                                      f"\n**ID -->** {user.id}",
                          colour=self.bot.admin_colour,
                          timestamp=banned_at)
            embed.add_field(name="Account Creation Date",
                            value=user.created_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"), inline=True)
            embed.add_field(name="Member Banned Date", value=banned_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"),
                            inline=True)
            embed.set_footer(text="Member Banned")
            embed.set_thumbnail(url=user.avatar_url)

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_unban(self, guild, user):
        """Logs Member Unbans to Server"""

        unbanned_at = datetime.datetime.utcnow()
        if modlogs := self.bot.get_modlog_for_guild(guild.id):
            modlogs_channel = self.bot.get_channel(modlogs)

            embed = Embed(title="Member Unbanned",
                          description=f"**Member --> {user.mention} |** {user}"
                                      f"\n**ID -->** {user.id}",
                          colour=self.bot.admin_colour,
                          timestamp=unbanned_at)
            embed.add_field(name="Account Creation Date",
                            value=user.created_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"), inline=True)
            embed.add_field(name="Member Unbanned Date", value=unbanned_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"),
                            inline=True)
            embed.set_footer(text="Member Unbanned")
            embed.set_thumbnail(url=user.avatar_url)

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_update(self, before, after):
        """Logging Member Profile Updates"""

        if modlogs := self.bot.get_modlog_for_guild(after.guild.id):
            modlogs_channel = self.bot.get_channel(modlogs)

            # Logging nickname changes or custom activity updates
            if before.nick != after.nick:

                # Get the status of the member
                after_status = member_status[str(after.status)]
                # Getting activity
                after_activity = f"{after.activity.emoji or '' if after.activity.type == discord.ActivityType.custom else ''}" \
                                 f"{after.activity.name}" if after.activity else None

                fields = [("Nickname Before",
                           f"{before.nick or None}", False),
                          ("Nickname After",
                           f"{after.nick or None}", False)]

                embed = Embed(title="Member Nickname Updated",
                              description=f"**Member --> {after.mention} |** {after}"
                                          f"\n**ID -->** {after.id}"
                                          f"\n\n**Activity -->** {after_activity}"
                                          f"\n**Status -->** {after_status}",
                              colour=self.bot.admin_colour,
                              timestamp=datetime.datetime.utcnow())
                embed.set_author(name=after, icon_url=after.avatar_url)
                embed.set_footer(text="Member Nickname Updated")

                # Add fields to the embed
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await modlogs_channel.send(embed=embed)

            # Logging Role additions/removals from Members
            if before.roles != after.roles:

                # Grab total list of roles that the user has after additions/removal
                role = string_list(after.roles, 30, "Role")

                # Retrieve the roles that were added/removed to/from the Member
                new_roles = [roles for roles in after.roles if roles not in before.roles]
                old_roles = [roles for roles in before.roles if roles not in after.roles]

                # As long as roles were added to the Member, log the role(s) that were given
                if len(new_roles) >= 1:
                    new_roles_string = " **|** ".join(r.mention for r in new_roles)

                    # Change the description of the embed depending on how many roles were added
                    if len(new_roles) == 1:
                        field = ("Member Role Added", new_roles_string, False)
                        footer = "Member Role Added"
                    else:
                        field = ("Member Roles Added", new_roles_string, False)
                        footer = "Member Roles Added"

                    embed = Embed(title=footer,
                                  description=f"**Member --> {after.mention} |** {after}"
                                              f"\n**ID -->** {after.id}",
                                  colour=self.bot.admin_colour,
                                  timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=after, icon_url=after.avatar_url)
                    embed.add_field(name=field[0], value=field[1], inline=field[2])
                    embed.add_field(name="All Roles", value=role or "No Roles", inline=False)
                    embed.set_footer(text=footer)

                    await modlogs_channel.send(embed=embed)

                # As long as roles were removed from the member, log the role(s) that were removed
                if len(old_roles) >= 1:
                    old_roles_string = " **|** ".join(r.mention for r in old_roles)

                    # Change the description of the embed depending on how many roles were removed
                    if len(old_roles) == 1:
                        field = ("Member Role Removed", old_roles_string, False)
                        footer = "Member Role Removed"
                    else:
                        field = ("Member Roles Removed", old_roles_string, False)
                        footer = "Member Roles Removed"

                    embed = Embed(title=footer,
                                  description=f"**Member --> {after.mention} |** {after}"
                                              f"\n**ID -->** {after.id}",
                                  colour=self.bot.admin_colour,
                                  timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=after, icon_url=after.avatar_url)
                    embed.add_field(name=field[0], value=field[1], inline=field[2])
                    embed.add_field(name="All Roles", value=role or "No Roles", inline=False)
                    embed.set_footer(text=footer)

                    await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before, after):
        """Logging Message Edits (Within Cache)"""

        msg_channel = self.bot.get_channel(after.channel.id)

        # Get the channel within the cache
        if not isinstance(msg_channel, DMChannel):
            # Get the channel within the cache
            channel = self.bot.get_modlog_for_guild(after.guild.id)
        else:
            return

        # When no modlogs channel is returned, do nothing
        if channel:
            modlogs_channel = self.bot.get_channel(channel)

            # Logging Message Content Edits
            # Not logging any message edits from bots
            if before.content != after.content and not after.author.bot:
                desc = f"**Channel --> {after.channel.mention} |** #{after.channel}" \
                       f"\n**Message ID -->** {after.id}" \
                       f"\n**Edited Message -->** [Jump To Message]({after.jump_url})"

                # Allowing messages of all sizes to be logged
                def message_fields(status):
                    if status == "Before":
                        if len(before.content) <= 1024:
                            fields = [(f"Edited Message Before", before.content, False)]
                        else:
                            fields = [(f"Before Message Content #1", before.content[:1000], False),
                                      (f"Before Message Content #2", before.content[1000:], False)]
                    else:
                        if len(after.content) <= 1024:
                            fields = [(f"Edited Message After", after.content, False)]
                        else:
                            fields = [(f"After Message Content #1", after.content[:1000], False),
                                      (f"After Message Content #2", after.content[1000:], False)]

                    # Add fields to the embed
                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)

                embed = Embed(title="Message Edited",
                              description=desc,
                              colour=self.bot.admin_colour,
                              timestamp=datetime.datetime.utcnow())
                embed.set_author(name=after.author, icon_url=after.author.avatar_url)
                message_fields("Before")
                message_fields("After")
                embed.set_footer(text="Message Edited")

                await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_raw_message_edit(self, payload):
        """Logging Message Edits Not Stored Within Internal Cache"""

        msg_channel = self.bot.get_channel(int(payload.data["channel_id"]))

        # Get the channel within the cache
        if not isinstance(msg_channel, DMChannel):
            channel = self.bot.get_modlog_for_guild(int(payload.data["guild_id"]))
        else:
            return

        # Only log this message edit when the message does not exist within the internal cache
        # and modlogs channel is set up
        if channel and not payload.cached_message:
            modlogs_channel = self.bot.get_channel(channel)

            desc = f"**Channel --> {msg_channel.mention} |** #{msg_channel}" \
                   f"\n**Message ID -->** {payload.message_id}" \
                   f"\n**Message Content -->** N/A"
            embed = Embed(title="Raw Message Edited",
                          description=desc,
                          colour=self.bot.admin_colour,
                          timestamp=datetime.datetime.utcnow())
            embed.set_author(name=modlogs_channel.guild.name, icon_url=modlogs_channel.guild.icon_url)
            embed.set_footer(text="Raw Message Edited")

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message):
        """Logging Message Deletions (Within Cache)"""

        # Get the channel within the cache
        channel = self.bot.get_modlog_for_guild(message.guild.id)

        # When no modlogs channel is returned, do nothing
        if channel and not message.author.bot:
            modlogs_channel = self.bot.get_channel(channel)

            # Allowing messages of all sizes to be logged
            if len(message.content) <= 1024:
                fields = [("Deleted Message Content", message.content or "View Attachment", False)]
            else:
                fields = [("Deleted Message Content #1", message.content[:1000], False),
                          ("Deleted Message Content #2", message.content[1000:], False)]

            if not message.attachments:
                desc = f"**Channel --> {message.channel.mention} |** #{message.channel}" \
                       f"\n**Author ID -->** {message.author.id}" \
                       f"\n**Message ID -->** {message.id}"
            else:
                attach_string = "".join(f"[Here]({attach.proxy_url})" for attach in message.attachments)
                desc = f"**Channel --> {message.channel.mention}**" \
                       f"\n**Author ID -->** {message.author.id}" \
                       f"\n**Message ID -->** {message.id}"
                fields += [("Attachment Link(s)", attach_string, False)]

            embed = Embed(title="Message Deleted",
                          description=desc,
                          colour=self.bot.admin_colour,
                          timestamp=datetime.datetime.utcnow())
            embed.set_author(name=message.author, icon_url=message.author.avatar_url)
            embed.set_footer(text="Message Deleted")

            # Add fields to the embed
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_raw_message_delete(self, payload):
        """Logging Message Deletions Not Stored Within Internal Cache"""

        msg_channel = self.bot.get_channel(payload.channel_id)

        # Get the channel within the cache
        if not isinstance(msg_channel, DMChannel):
            channel = self.bot.get_modlog_for_guild(payload.guild_id)
        else:
            return

        # Only log this message deletion when the message does not exist within the internal cache
        # and modlogs channel is set up
        if channel and not payload.cached_message:
            modlogs_channel = self.bot.get_channel(channel)

            desc = f"**Channel --> {msg_channel.mention} |** #{msg_channel}" \
                   f"\n**Message ID -->** {payload.message_id}" \
                   f"\n**Message Content -->** N/A"
            embed = Embed(title="Raw Message Deleted",
                          description=desc,
                          colour=self.bot.admin_colour,
                          timestamp=datetime.datetime.utcnow())
            embed.set_author(name=modlogs_channel.guild.name, icon_url=modlogs_channel.guild.icon_url)
            embed.set_footer(text="Raw Message Deleted")

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_guild_channel_delete(self, channel):
        """Logging channel deletions within the guild"""

        deleted_at = datetime.datetime.utcnow()

        if modlogs := self.bot.get_modlog_for_guild(channel.guild.id):
            modlogs_channel = self.bot.get_channel(modlogs)

            desc = f"**Channel Deleted |** #{channel.name}\n" \
                   f"**Category |** {channel.category or self.bot.cross}\n" \
                   f"**Position |** #{channel.position} / {len(channel.guild.channels)}\n"
            embed = Embed(description=desc,
                          colour=self.bot.admin_colour,
                          timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Created Date",
                            value=channel.created_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"),
                            inline=True)
            embed.add_field(name="Deleted Date",
                            value=deleted_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"),
                            inline=True)
            embed.set_author(name=modlogs_channel.guild.name, icon_url=modlogs_channel.guild.icon_url)
            embed.set_footer(text="Channel Deleted")

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_guild_channel_create(self, channel):
        """Logging channel creations within the guild"""

        if modlogs := self.bot.get_modlog_for_guild(channel.guild.id):
            modlogs_channel = self.bot.get_channel(modlogs)

            desc = f"**Channel Created |** {channel.mention}\n" \
                   f"**Category |** {channel.category or self.bot.cross}\n" \
                   f"**Position |** #{channel.position} / {len(channel.guild.channels)}\n"
            embed = Embed(description=desc,
                          colour=self.bot.admin_colour,
                          timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Created Date",
                            value=channel.created_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"),
                            inline=True)
            embed.set_author(name=modlogs_channel.guild.name, icon_url=modlogs_channel.guild.icon_url)
            embed.set_footer(text="Channel Created")

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_guild_channel_update(self, before, after):
        """Logging guild channel updates"""

        if modlogs := self.bot.get_modlog_for_guild(after.guild.id):
            modlogs_channel = self.bot.get_channel(modlogs)

            # Logging Channel Name/Category/Position Updates
            if before.name != after.name or before.category != after.category:
                fields = [("Channel Before",
                           f"**Channel Updated -->** #{before}\n"
                           f"**Category -->** {before.category or self.bot.cross}\n"
                           f"**Position -->** #{before.position} / {len(before.guild.channels)}\n", False),
                          ("Channel After",
                           f"**Channel Updated -->** #{after}\n"
                           f"**Category -->** {after.category or self.bot.cross}\n"
                           f"**Position -->** #{after.position} / {len(after.guild.channels)}\n", False)]

                embed = Embed(title="Channel Updated",
                              description=f"**ID -->** {after.id}",
                              colour=self.bot.admin_colour,
                              timestamp=datetime.datetime.utcnow())
                embed.set_author(name=after.guild, icon_url=after.guild.icon_url)
                embed.set_footer(text="Channel Updated")

                # Add fields to the embed
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await modlogs_channel.send(embed=embed)

            # Logging any roles added/removed from channel permissions
            if before.changed_roles != after.changed_roles:
                new_roles = [roles for roles in after.changed_roles]
                old_roles = [roles for roles in before.changed_roles]

                # Get total new_roles in the channel
                new_role_string = string_list(new_roles, 20, "Role")
                # Get total old_roles in the channel
                old_role_string = string_list(old_roles, 20, "Role")

                embed = Embed(title="Role Overrides Updated",
                              description=f"**Channel -->** {after.mention}\n"
                                          f"**ID -->** {after.id}",
                              colour=self.bot.admin_colour,
                              timestamp=datetime.datetime.utcnow())
                embed.set_author(name=after.guild, icon_url=after.guild.icon_url)
                embed.add_field(name="Channel Roles Before",
                                value=old_role_string or after.guild.default_role.mention, inline=False)
                embed.add_field(name="Channel Roles After",
                                value=new_role_string or after.guild.default_role.mention, inline=False)
                embed.set_footer(text="Role Overrides Updated")

                await modlogs_channel.send(embed=embed)

            # TODO: REMEMBER TO TRY AND LOG CHANNEL OVERWRITES

    @Cog.listener()
    async def on_guild_update(self, before, after):
        """Logging guild updates"""

        if modlogs := self.bot.get_modlog_for_guild(after.id):
            modlogs_channel = self.bot.get_channel(modlogs)

            attributes = ["name", "verification_level", "afk_channel", "mfa_level",
                          "default_notifications", "region", "explicit_content_filter"]
            if any(getattr(before, x) != getattr(after, x) for x in attributes):

                fields = [("Guild Before",
                           f"**Guild Name -->** {before}\n"
                           f"**Region -->** {get_region(str(before.region))}\n\n"

                           f"**2-Factor Authentication -->** {self.bot.tick if before.mfa_level == 1 else self.bot.cross}\n"
                           f"**Explicit Content Filter -->** {get_content_filter(before.explicit_content_filter.name)}\n"
                           f"**Verification Level -->** {before.verification_level.name.capitalize()}\n\n"

                           f"**Default Notifications -->** {get_notifs(before.default_notifications)}\n"
                           f"**AFK Channel -->** {before.afk_channel.mention if before.afk_channel else '#N/A'} **|** {before.afk_timeout}s\n",
                           True),
                          ("\u200b", "\u200b", True),
                          ("Guild After",
                           f"**Guild Name -->** {after}\n"
                           f"**Region -->** {get_region(str(after.region))}\n\n"

                           f"**2-Factor Authentication -->** {self.bot.tick if after.mfa_level == 1 else self.bot.cross}\n"
                           f"**Explicit Content Filter -->** {get_content_filter(after.explicit_content_filter.name)}\n"
                           f"**Verification Level -->** {after.verification_level.name.capitalize()}\n\n"

                           f"**Default Notifications -->** {get_notifs(after.default_notifications)}\n"
                           f"**AFK Channel -->** {after.afk_channel.mention if after.afk_channel else '#N/A'} **|** {after.afk_timeout}s\n",
                           True)]

                embed = Embed(title="Guild Updated",
                              description=f"**Owner --> {after.owner.mention} |** {after.owner}\n"
                                          f"**ID -->** {after.id}",
                              colour=self.bot.admin_colour,
                              timestamp=datetime.datetime.utcnow())
                embed.set_author(name=after, icon_url=after.icon_url)
                embed.set_footer(text="Guild Updated")

                # Add fields to the embed
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await modlogs_channel.send(embed=embed)

            if before.banner_url != after.banner_url:
                embed = Embed(title="Banner Updated",
                              colour=self.bot.admin_colour,
                              timestamp=datetime.datetime.utcnow())
                embed.set_author(name=after, icon_url=after.icon_url)
                embed.add_field(name="New Banner",
                                value=f"[Link To New Banner]({after.banner_url})", inline=False)
                embed.set_image(url=after.banner_url)
                embed.set_footer(text="Banner Updated")

                await modlogs_channel.send(embed=embed)

            if before.discovery_splash_url != after.discovery_splash_url:
                embed = Embed(title="Discovery Splash Updated",
                              colour=self.bot.admin_colour,
                              timestamp=datetime.datetime.utcnow())
                embed.set_author(name=after, icon_url=after.icon_url)
                embed.add_field(name="New Discovery Splash",
                                value=f"[Link To New Discovery Splash]({after.discovery_splash_url})", inline=False)
                embed.set_image(url=after.discovery_splash_url)
                embed.set_footer(text="Discovery Splash Updated")

                await modlogs_channel.send(embed=embed)

            if before.splash_url != after.splash_url:
                embed = Embed(title="Splash Updated",
                              colour=self.bot.admin_colour,
                              timestamp=datetime.datetime.utcnow())
                embed.set_author(name=after, icon_url=after.icon_url)
                embed.add_field(name="New Splash",
                                value=f"[Link To New Splash]({after.splash_url})", inline=False)
                embed.set_image(url=after.splash_url)
                embed.set_footer(text="Splash Updated")

                await modlogs_channel.send(embed=embed)

            if before.icon_url != after.icon_url:
                embed = Embed(title="Icon Updated",
                              colour=self.bot.admin_colour,
                              timestamp=datetime.datetime.utcnow())
                embed.set_author(name=after, icon_url=after.icon_url)
                embed.add_field(name="New Icon",
                                value=f"[Link To Icon]({after.icon_url})", inline=False)
                embed.set_image(url=after.icon_url)
                embed.set_footer(text="Icon Updated")

                await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        """Logging any emoji updates"""

        if modlogs := self.bot.get_modlog_for_guild(guild.id):
            modlogs_channel = self.bot.get_channel(modlogs)

            # Logging emoji additions/deletions
            if before != after:
                # Retrieve the emoji that were removed/added to the guild
                new_emojis = [emojis for emojis in after if emojis not in before]
                old_emojis = [emojis for emojis in before if emojis not in after]

                # Determining whether emoji was added or removed
                if len(new_emojis) == 1:
                    text = "Emoji Added"
                    emoji_id = new_emojis[0].id
                    name = new_emojis[0].name
                    animated = self.bot.tick if new_emojis[0].animated else self.bot.cross
                    managed = self.bot.tick if new_emojis[0].managed else self.bot.cross
                    url = new_emojis[0].url
                if len(old_emojis) == 1:
                    text = "Emoji Removed"
                    emoji_id = old_emojis[0].id
                    name = old_emojis[0].name
                    animated = self.bot.tick if old_emojis[0].animated else self.bot.cross
                    managed = self.bot.tick if old_emojis[0].managed else self.bot.cross
                    url = old_emojis[0].url

                # Get total emojis
                emojis = string_list(after, 30, "Emoji")
                embed = Embed(title=text,
                              description=f"**ID -->** {emoji_id}"
                                          f"\n**Name -->** {name}"
                                          f"\n**Animated? -->** {animated}"
                                          f"\n**Managed? -->** {managed}",
                              colour=self.bot.admin_colour,
                              url=str(url),
                              timestamp=datetime.datetime.utcnow())
                embed.set_author(name=guild, icon_url=guild.icon_url)
                embed.add_field(name=f"All Emojis --> {len(guild.emojis)}", value=emojis or "No Emojis", inline=False)
                embed.set_thumbnail(url=str(url))
                embed.set_footer(text=text)

                await modlogs_channel.send(embed=embed)

            # Log emoji name updates
            elif before is not after:
                for b, a in zip(before, after):
                    if b.name != a.name:
                        animated = self.bot.tick if a.animated else self.bot.cross
                        managed = self.bot.tick if a.managed else self.bot.cross

                        embed = Embed(title="Emoji Name Updated",
                                      description=f"**ID -->** {a.id}"
                                                  f"\n**Name -->** {a.name}"
                                                  f"\n**Animated? -->** {animated}"
                                                  f"\n**Managed? -->** {managed}",
                                      colour=self.bot.admin_colour,
                                      url=str(a.url),
                                      timestamp=datetime.datetime.utcnow())
                        embed.set_author(name=guild, icon_url=guild.icon_url)
                        embed.set_thumbnail(url=str(a.url))
                        embed.set_footer(text="Emoji Name Updated")

                        await modlogs_channel.send(embed=embed)
                        break

    @Cog.listener()
    async def on_guild_role_create(self, role):
        """Logging role creations"""

        if modlogs := self.bot.get_modlog_for_guild(role.guild.id):
            modlogs_channel = self.bot.get_channel(modlogs)

            # Returns the permissions that the role has within the guild
            filtered = filter(lambda x: x[1], role.permissions)
            # Replace all "_" with " " in each item and join them together
            _perms = ", ".join(map(lambda x: x[0].replace("_", " "), filtered))
            # Capitalise every word in the array
            permission = string.capwords(_perms)

            # Using emotes to represent bools
            mentionable = self.bot.tick if role.mentionable else self.bot.cross
            hoisted = self.bot.tick if role.hoist else self.bot.cross
            managed = self.bot.tick if role.managed else self.bot.cross

            # Description of the embed
            desc = f"{role.mention} **<-- Colour:** {str(role.colour)}" \
                   f"\n**Position -->** #{role.position} / {len(role.guild.roles)}" \
                   f"\n**ID -->** {role.id}"

            # Set up Embed
            embed = Embed(title=f"Role Created",
                          description=desc,
                          colour=self.bot.admin_colour,
                          timestamp=datetime.datetime.utcnow())
            embed.set_author(name=role.guild, icon_url=role.guild.icon_url)
            embed.set_footer(text=f"Role Created")

            # Setting up fields
            fields = [
                ("Creation At", role.created_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"), True),

                (f"Misc",
                 f"\nMentionable?: {mentionable}"
                 f"\nHoisted?: {hoisted}"
                 f"\nManaged?: {managed}", True),

                ("All Permissions", permission or "No Permissions", False)
            ]

            # Add fields to the embed
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_guild_role_delete(self, role):
        """Logging role deletions"""

        if modlogs := self.bot.get_modlog_for_guild(role.guild.id):
            deleted_at = datetime.datetime.utcnow()
            modlogs_channel = self.bot.get_channel(modlogs)

            # Returns the permissions that the role has within the guild
            filtered = filter(lambda x: x[1], role.permissions)
            # Replace all "_" with " " in each item and join them together
            _perms = ",".join(map(lambda x: x[0].replace("_", " "), filtered))
            # Capitalise every word in the array and filter out the permissions that are defined within the frozenset
            permission = string.capwords("".join(detect_perms(_perms, perms)))

            # Using emotes to represent bools
            mentionable = self.bot.tick if role.mentionable else self.bot.cross
            hoisted = self.bot.tick if role.hoist else self.bot.cross
            managed = self.bot.tick if role.managed else self.bot.cross

            # Description of the embed
            desc = f"@{role} **<-- Colour:** {str(role.colour)}" \
                   f"\n**Position -->** #{role.position} / {len(role.guild.roles)}" \
                   f"\n**ID -->** {role.id}"

            # Set up Embed
            embed = Embed(title=f"Role Deleted",
                          description=desc,
                          colour=self.bot.admin_colour,
                          timestamp=datetime.datetime.utcnow())
            embed.set_author(name=role.guild, icon_url=role.guild.icon_url)
            embed.set_footer(text=f"Role Deleted")

            # Setting up fields
            fields = [
                ("Creation At", role.created_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"), True),
                ("Deletion At", deleted_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"), True),

                (f"Misc",
                 f"\nMentionable?: {mentionable}"
                 f"\nHoisted?: {hoisted}"
                 f"\nManaged?: {managed}", True),

                ("All Permissions Before Deletion", permission or "No Permissions", False)
            ]

            # Add fields to the embed
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_guild_role_update(self, before, after):
        """Logging any updates to roles"""

        if modlogs := self.bot.get_modlog_for_guild(after.guild.id):
            modlogs_channel = self.bot.get_channel(modlogs)

            attributes = ["name", "hoist", "managed", "mentionable", "colour"]
            if any(getattr(before, x) != getattr(after, x) for x in attributes):

                # Using emotes to represent bools
                b_mentionable = self.bot.tick if before.mentionable else self.bot.cross
                b_hoisted = self.bot.tick if before.hoist else self.bot.cross
                b_managed = self.bot.tick if before.managed else self.bot.cross
                # Using emotes to represent bools
                a_mentionable = self.bot.tick if after.mentionable else self.bot.cross
                a_hoisted = self.bot.tick if after.hoist else self.bot.cross
                a_managed = self.bot.tick if after.managed else self.bot.cross

                fields = [("Role Before",
                           f"**Name -->** @{before}"
                           f"\n**Colour -->** {str(before.colour)}"
                           f"\n\n**Mentionable? -->** {b_mentionable}"
                           f"\n**Hoisted? -->** {b_hoisted}"
                           f"\n**Managed? -->** {b_managed}",
                           True),
                          ("Role After",
                           f"**Name -->** @{after}"
                           f"\n**Colour -->** {str(after.colour)}"
                           f"\n\n**Mentionable? -->** {a_mentionable}"
                           f"\n**Hoisted? -->** {a_hoisted}"
                           f"\n**Managed? -->** {a_managed}",
                           True)]

                # Set up Embed
                embed = Embed(title=f"Role Updated",
                              description=f"**Name --> {after.mention} |** @{after}"
                                          f"**\nID -->** {after.id}",
                              colour=self.bot.admin_colour,
                              timestamp=datetime.datetime.utcnow())
                embed.set_author(name=after.guild, icon_url=after.guild.icon_url)
                embed.set_footer(text=f"Role Updated")

                # Add fields to the embed
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await modlogs_channel.send(embed=embed)

            # Logging permission changes to roles
            if before.permissions != after.permissions:
                # Returns the permissions that the role has within the guild
                after_filtered = list(filter(lambda x: x[1], after.permissions))
                before_filtered = list(filter(lambda x: x[1], before.permissions))
                after_perms = string.capwords(", ".join(map(lambda x: x[0].replace("_", " "), after_filtered)))

                # Retrieve the permissions that were enabled/disabled from the role
                new_perm = [perms for perms in after_filtered if perms not in before_filtered]
                old_perm = [perms for perms in before_filtered if perms not in after_filtered]

                # Log the new permissions that were enabled for the role
                if len(new_perm) >= 1 and not old_perm:
                    new_perm_string = string.capwords(", ".join(map(lambda x: x[0].replace("_", " "), new_perm)))

                    # Change the description of the embed depending on how many permissions were enabled
                    if len(new_perm) == 1:
                        field = ("Role Permission Added", new_perm_string, False)
                        footer = "Role Permission Added"
                    else:
                        field = ("Role Permissions Added", new_perm_string, False)
                        footer = "Role Permissions Added"

                    embed = Embed(title=footer,
                                  description=f"{after.mention} **|** @{after} **<-- Colour:** {str(after.colour)}"
                                              f"\n**Position -->** #{after.position} / {len(after.guild.roles)}"
                                              f"\n** ID -->** {after.id}",
                                  colour=self.bot.admin_colour,
                                  timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=after.guild, icon_url=after.guild.icon_url)
                    embed.add_field(name=field[0], value=field[1], inline=field[2])
                    embed.add_field(name="All Permissions", value=after_perms or "No Permissions", inline=False)
                    embed.set_footer(text=footer)

                    await modlogs_channel.send(embed=embed)

                # As long as permissions were disabled, log them
                if len(old_perm) >= 1 and not new_perm:
                    old_perm_string = string.capwords(", ".join(map(lambda x: x[0].replace("_", " "), old_perm)))

                    # Change the description of the embed depending on how many permissions were disabled
                    if len(old_perm) == 1:
                        field = ("Role Permission Removed", old_perm_string, False)
                        footer = "Role Permission Removed"
                    else:
                        field = ("Role Permissions Removed", old_perm_string, False)
                        footer = "Role Permissions Removed"

                    embed = Embed(title=footer,
                                  description=f"{after.mention} **|** @{after} **<-- Colour:** {str(after.colour)}"
                                              f"\n**Position -->** #{after.position} / {len(after.guild.roles)}"
                                              f"\n** ID -->** {after.id}",
                                  colour=self.bot.admin_colour,
                                  timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=after.guild, icon_url=after.guild.icon_url)
                    embed.add_field(name=field[0], value=field[1], inline=field[2])
                    embed.add_field(name="All Permissions", value=after_perms or "No Permissions", inline=False)
                    embed.set_footer(text=footer)

                    await modlogs_channel.send(embed=embed)

                # Log the different permissions that were enabled and disabled
                if len(old_perm) >= 1 and len(new_perm) >= 1:
                    new_perm_string = string.capwords(", ".join(map(lambda x: x[0].replace("_", " "), new_perm)))
                    old_perm_string = string.capwords(", ".join(map(lambda x: x[0].replace("_", " "), old_perm)))

                    # Change the description of the embed depending on how many permissions were enabled
                    if len(new_perm) == 1:
                        new_field = ("Role Permission Added", new_perm_string, False)
                    else:
                        new_field = ("Role Permissions Added", new_perm_string, False)

                    # Change the description of the embed depending on how many permissions were disabled
                    if len(old_perm) == 1:
                        old_field = ("Role Permission Removed", old_perm_string, False)
                    else:
                        old_field = ("Role Permissions Removed", old_perm_string, False)

                    embed = Embed(title="Role Permissions Updated",
                                  description=f"{after.mention} **|** @{after} **<-- Colour:** {str(after.colour)}"
                                              f"\n**Position -->** #{after.position} / {len(after.guild.roles)}"
                                              f"\n** ID -->** {after.id}",
                                  colour=self.bot.admin_colour,
                                  timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=after.guild, icon_url=after.guild.icon_url)
                    embed.add_field(name=new_field[0], value=new_field[1], inline=new_field[2])
                    embed.add_field(name=old_field[0], value=old_field[1], inline=old_field[2])
                    embed.add_field(name="All Permissions", value=after_perms or "No Permissions", inline=False)
                    embed.set_footer(text="Role Permissions Updated")

                    await modlogs_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))


"""
@Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        Logging voice channel updates

        if modlogs := self.bot.get_modlog_for_guild(member.guild.id):
            modlogs_channel = self.bot.get_channel(modlogs)

            if before.channel != after.channel:
                embed = Embed()

@Cog.listener()
    async def on_guild_integrations_update(self, guild):
        Logging updates to integrations

        if modlogs := self.bot.get_modlog_for_guild(guild.id):
            modlogs_channel = self.bot.get_channel(modlogs)

print(before.overwrites)
print(after.overwrites)

before_diffkeys = [k for k in before.overwrites if
                   before.overwrites[k].pair() != after.overwrites[k].pair()]
after_diffkeys = [k for k in after.overwrites if after.overwrites[k].pair() != before.overwrites[k].pair()]

before_array = []
after_array = []
for k in before_diffkeys:
    for pair in k.permissions:
        before_array += [pair]

for k in after_diffkeys:
    for pair in k.permissions:
        after_array += [pair]

old_roles = [p for p in before_array if p in after_array]
after_roles = [p for p in after_array if p in before_array]

print(old_roles)
print(after_roles)
"""
