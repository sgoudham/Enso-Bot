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
from datetime import timedelta
from typing import Optional

import discord
from discord import Member, Embed, DMChannel, NotFound
from discord.ext.commands import command, guild_only, has_guild_permissions, bot_has_guild_permissions, Greedy, \
    cooldown, BucketType, Cog

from cogs.libs.functions import string_list, get_region, get_content_filter, get_notifs

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

        desc = f"**Member -->{target.mention} | {target}\nID -->** {target.id}" \
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


async def ban_members(self, ctx, targets, reason):
    """

    Method to allow members to be banned

    2 embeds will be sent, one to the channel that the user is in
    And if the user has the modlogs channel setup, an embed will be logged there

    """

    for target in targets:
        if (ctx.guild.me.top_role.position > target.top_role.position
                and not target.guild_permissions.administrator):

            await target.ban(reason=reason)

            await self.bot.generate_embed(ctx, desc=f"{ctx.bot.tick} **{target}** Was Banned! {ctx.bot.tick}")

            await send_to_modlogs(self, ctx, target, reason, action="Banned")

        # Send error message if the User could not be banned
        else:
            await self.bot.generate_embed(ctx, desc=f"**{target.mention} Could Not Be Banned!**")


async def unban_members(self, ctx, targets, reason):
    """

    Method to allow members to be unbanned

    2 embeds will be sent, one to the channel that the user is in
    And if the user has the modlogs channel setup, an embed will be logged there

    """

    # Get the list of banned users from the server
    bans = await ctx.guild.bans()
    ban_ids = list(map(lambda m: m.user.id, bans))

    for target in targets:
        if target not in ban_ids:
            await self.bot.generate_embed(ctx, desc=f"{ctx.bot.cross} **Member Is Not In Ban's List!** {ctx.bot.cross}")

        else:
            # Get the member and unban them
            user = await self.bot.fetch_user(target)
            await ctx.guild.unban(user, reason=reason)

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
                if role is None:
                    muted = await ctx.guild.create_role(name="Muted")
                    for channel in ctx.guild.channels:
                        await channel.set_permissions(muted, send_messages=False)

                    await mute_members(self, ctx, members, reason, muted)

                else:
                    await mute_members(self, ctx, members, reason, role)

    @command(name="unmute", usage="`<member>...` `[reason]`")
    @has_guild_permissions(manage_roles=True)
    @bot_has_guild_permissions(manage_roles=True)
    async def unmute(self, ctx, members: Greedy[Member], *, reason: Optional[str] = "No Reason Given"):
        """
        Unmute Member(s) from Server
        Multiple Members can be unmuted at once
        """
        unmute = False

        if not await check(ctx, members):
            with ctx.typing():
                role = discord.utils.get(ctx.guild.roles, name="Muted")

                if role is None:
                    embed = Embed(description="**❌ No Muted Role Was Found! ❌**",
                                  colour=self.bot.admin_colour)
                    await ctx.send(embed=embed)

                else:

                    for member in members:
                        if role in member.roles:
                            await ummute_members(self, ctx, members, reason)
                            unmute = True

                        if role not in member.roles and unmute is False:
                            embed = Embed(description=f"**❌ {member.mention} Is Not Muted! ❌**",
                                          colour=self.bot.admin_colour)
                            await ctx.send(embed=embed)

    @command(name="ban", usage="`<member>...` `[reason]`")
    @guild_only()
    @has_guild_permissions(ban_members=True)
    @bot_has_guild_permissions(ban_members=True)
    @cooldown(1, 1, BucketType.user)
    async def ban(self, ctx, members: Greedy[Member], *, reason: Optional[str] = "No Reason Given"):
        """
        Ban Member(s) from Server
        Multiple Members can be banned at once
        """

        if not await check(ctx, members):
            with ctx.typing():
                await ban_members(self, ctx, members, reason)

    @command(name="forceban", aliases=["powerban", "ultraban"], usage="`<member>...` `[reason]`")
    @guild_only()
    @has_guild_permissions(ban_members=True)
    @bot_has_guild_permissions(ban_members=True)
    @cooldown(1, 1, BucketType.user)
    async def force_ban(self, ctx, users: Greedy[int], *, reason: Optional[str] = "No Reason Given"):
        """Ban User(s) from Server (MUST PROVIDE ID)"""

        if not await check(ctx, users):
            # Get the list of banned users from the server
            bans = await ctx.guild.bans()
            ban_ids = list(map(lambda m: m.user.id, bans))

            # Power ban users from guilds without them being in there
            for user in users:
                if user in ban_ids:
                    await self.bot.generate_embed(ctx, desc="❌ **Member Is Already Banned!** ❌")
                else:
                    await ctx.guild.ban(discord.Object(id=user))
                    target = await self.bot.fetch_user(user)
                    # Send confirmation to the channel that the user is in
                    await self.bot.generate_embed(ctx, desc=f"✅ **{target}** Was Power Banned! ✅")

                    await send_to_modlogs(self, ctx, target, reason, action="Power Banned")

    @command(name="unban", usage="`<member>...` `[reason]`")
    @guild_only()
    @has_guild_permissions(ban_members=True)
    @bot_has_guild_permissions(ban_members=True)
    @cooldown(1, 1, BucketType.user)
    async def unban(self, ctx, members: Greedy[int], *, reason: Optional[str] = "No Reason Given"):
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
    @force_ban.error
    async def ban_command_error(self, ctx, exc):
        """Catching error if channel is not recognised"""

        error = getattr(exc, "original", exc)

        if isinstance(error, NotFound):
            text = "**❌ User Not Detected... Aborting Process** ❌"
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

        if before == self.bot.user: return

        if modlogs := self.bot.get_modlog_for_guild(after.guild.id):
            modlogs_channel = self.bot.get_channel(modlogs)

            # Logging Member Updates when nickname changes
            if before.nick != after.nick and not after.bot:

                # Getting emoji of status from dict
                for key, value in member_status.items():
                    if key == str(before.status):
                        before_status = value
                    if key == str(after.status):
                        after_status = value

                # Getting status of the member
                after_activity = f"{after.activity.emoji or '' if after.activity.type.name == 'custom' else ''} {after.activity.name}" if after.activity else "None"

                fields = [("Before",
                           f"**Nickname -->** {before.nick or 'None'}\n"
                           f"**Status -->** {before_status or 'None'}\n"
                           f"**Activity -->** {after_activity}\n", False),
                          ("After",
                           f"**Nickname -->** {after.nick or 'None'}\n"
                           f"**Status -->** {after_status or 'None'}\n"
                           f"**Activity -->** {after_activity}\n", False)]

                embed = Embed(title="Member Updated",
                              description=f"**Member --> {after.mention} |** {after}"
                                          f"\n**ID -->** {after.id}",
                              colour=self.bot.admin_colour,
                              timestamp=datetime.datetime.utcnow())
                embed.set_author(name=after, icon_url=after.avatar_url)
                embed.set_footer(text="Member Updated")

                # Add fields to the embed
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await modlogs_channel.send(embed=embed)

            # Logging Role additions/removals from Members
            if after.roles != before.roles:

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
                        field = ("Role Added", new_roles_string, False)
                        footer = "Role Added"
                    else:
                        field = ("Roles Added", new_roles_string, False)
                        footer = "Roles Added"

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
                        field = ("Role Removed", old_roles_string, False)
                        footer = "Role Removed"
                    else:
                        field = ("Roles Removed", old_roles_string, False)
                        footer = "Roles Removed"

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
                desc = f"**Channel -->** <#{after.channel.id}>" \
                       f"\n**Message ID -->** {after.id}" \
                       f"\n**Edited Message -->** [Jump To Message]({after.jump_url})"

                # When the message context exceeds 500 characters, only display the first 500 characters in the logs
                before_value = f"{before.content[:1000]} ..." if len(before.content) >= 1000 else before.content
                after_value = f"{after.content[:1000]} ..." if len(after.content) >= 1000 else after.content

                embed = Embed(title="Message Edited",
                              description=desc,
                              colour=self.bot.admin_colour,
                              timestamp=datetime.datetime.utcnow())
                embed.set_author(name=after.author, icon_url=after.author.avatar_url)
                embed.add_field(name="Before",
                                value=before_value or "No Content", inline=False)
                embed.add_field(name="After",
                                value=after_value or "No Content", inline=False)
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

            desc = f"**Channel -->** {msg_channel.mention}" \
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

            if not message.attachments:
                desc = f"**Channel --> {message.channel.mention}**" \
                       f"\n**Author ID -->** {message.author.id}" \
                       f"\n**Message ID -->** {message.id}"
                fields = [("Message Content", message.content or "No Content", False)]
            else:
                attach_string = "".join(f"[Here]({attach.proxy_url})" for attach in message.attachments)
                desc = f"**Channel --> {message.channel.mention}**" \
                       f"\n**Author ID -->** {message.author.id}" \
                       f"\n**Message ID -->** {message.id}"
                fields = [("Message Content", message.content or "View Attachment", False),
                          ("Attachment Link(s)", attach_string, False)]

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

            desc = f"**Channel -->** {msg_channel.mention}" \
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
            if before.name != after.name or before.category != after.category or before.position != after.position:
                fields = [("Before",
                           f"**Channel Updated -->** #{before}\n"
                           f"**Category -->** {before.category or self.bot.cross}\n"
                           f"**Position -->** #{before.position} / {len(before.guild.channels)}\n", False),
                          ("After",
                           f"**Channel Updated -->** #{after}\n"
                           f"**Category -->** {after.category or self.bot.cross}\n"
                           f"**Position -->** #{after.position} / {len(after.guild.channels)}\n", False)]

                embed = Embed(title="Channel Updated",
                              description=f"**ID -->** {after.id}",
                              colour=self.bot.admin_colour,
                              timestamp=datetime.datetime.utcnow())
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
                embed.add_field(name="Before",
                                value=old_role_string or after.guild.default_role.mention, inline=False)
                embed.add_field(name="After",
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

                fields = [("Before",
                           f"**Guild Name -->** {before}\n"
                           f"**Region -->** {get_region(str(before.region))}\n\n"

                           f"**2-Factor Authentication -->** {self.bot.tick if before.mfa_level == 1 else self.bot.cross}\n"
                           f"**Explicit Content Filter -->** {get_content_filter(before.explicit_content_filter.name)}\n"
                           f"**Verification Level -->** {before.verification_level.name.capitalize()}\n\n"

                           f"**Default Notifications -->** {get_notifs(before.default_notifications)}\n"
                           f"**AFK Channel -->** {before.afk_channel.mention if before.afk_channel else '#N/A'} **|** {before.afk_timeout}s\n",
                           True),
                          ("\u200b", "\u200b", True),
                          ("After",
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


def setup(bot):
    bot.add_cog(Moderation(bot))


"""

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
