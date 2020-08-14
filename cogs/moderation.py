import datetime
from datetime import timedelta
from typing import Optional

import discord
from discord import Member, Embed
from discord.ext.commands import command, guild_only, has_guild_permissions, bot_has_guild_permissions, Greedy, \
    cooldown, BucketType, Cog

from settings import enso_embedmod_colours, get_modlog_for_guild, storeRoles, clearRoles, get_roles_persist, \
    generate_embed


async def send_to_modlogs(message, target, reason, action):
    """
    Function to send the moderation actions to modlogs channel
    """

    # Get the channel of the modlog within the guild
    modlog = get_modlog_for_guild(str(message.guild.id))

    if modlog is not None:

        channel = message.guild.get_channel(int(modlog))

        embed = Embed(title=f"Member {action}",
                      colour=enso_embedmod_colours,
                      timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url=target.avatar_url)

        fields = [("Member", target.mention, False),
                  ("Actioned by", message.author.mention, False),
                  ("Reason", reason, False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await channel.send(embed=embed)


async def check(ctx, members):
    """
    Check Function
    
    - Checks if all arguments are given
    - Checks if user mentions themselves
    
    Error will be thrown in these two cases
    """

    if not len(members):
        embed = Embed(description="Not Correct Syntax!"
                                  f"\nUse **{ctx.prefix}help** to find how to use **{ctx.command}**",
                      colour=enso_embedmod_colours)
        await ctx.send(embed=embed)
        return True

    elif ctx.author in members:
        embed = Embed(description=f"**❌ Forbidden Action ❌**",
                      colour=enso_embedmod_colours)
        await ctx.send(embed=embed)
        return True


async def ummute_members(self, message, targets, reason):
    """

    Method to allow members to be unmuted

    2 embeds will be sent, one to the channel that the user is in
    And if the user has the modlogs channel setup, an embed will be logged there

    """

    # Setup pool
    pool = self.bot.db

    for target in targets:
        if (message.guild.me.top_role.position > target.top_role.position
                and not target.guild_permissions.administrator):

            # Setup up pool connection and cursor
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    # Get the roles of the user from the database
                    select_query = """SELECT * FROM members WHERE guildID = (%s) AND discordID = (%s)"""
                    select_vals = message.guild.id, target.id,

                    # Execute the SQL Query
                    await cur.execute(select_query, select_vals)
                    result = await cur.fetchone()
                    role_ids = result[4]

                # Get all the roles of the user before they were muted from the database
                roles = [message.guild.get_role(int(id_)) for id_ in role_ids.split(", ") if len(id_)]

                # Clear all the roles of the user
                await clearRoles(member=target, pool=pool)

            await target.edit(roles=roles)

            # Send confirmation to the channel that the user is in
            embed = Embed(description="✅ **{}** Was Unmuted! ✅".format(target),
                          colour=enso_embedmod_colours)
            await message.channel.send(embed=embed)

            await send_to_modlogs(message, target, reason, action="Unmuted")

        # Send error message if the User could not be muted
        else:
            embed = Embed(description="**{} Could Not Be Unmuted!**".format(target.mention))
            await message.channel.send(embed=embed)


async def mute_members(pool, ctx, targets, reason, muted):
    """

    Method to allow members to be muted

    2 embeds will be sent, one to the channel that the user is in
    And if the user has the modlogs channel setup, an embed will be logged there

    """

    for target in targets:

        # When user is already muted, send error message
        if muted in target.roles:
            embed = Embed(description="**❌ User Is Already Muted! ❌**",
                          colour=enso_embedmod_colours)
            await ctx.send(embed=embed)

        else:

            # Store managed roles into the list of roles to be added to the user (including muted)
            roles = [role for role in target.roles if role.managed]
            roles.append(muted)

            if (ctx.message.guild.me.top_role.position > target.top_role.position
                    and not target.guild_permissions.administrator):

                # Store the current roles of the user within database
                await storeRoles(pool=pool, target=target, ctx=ctx.message, member=target)
                # Give the user the muted role (and any integration roles if need be)
                await target.edit(roles=roles, reason=reason)

                # Send confirmation to the channel that the user is in
                embed = Embed(description="✅ **{}** Was Muted! ✅".format(target),
                              colour=enso_embedmod_colours)
                if get_roles_persist(str(ctx.message.guild.id)) == 0:
                    embed.add_field(name="**WARNING: ROLE PERSIST NOT ENABLED**",
                                    value="The bot **will not give** the roles back to the user if they leave the server."
                                          "\nAllowing the user to bypass the Mute by leaving and rejoining."
                                          f"\nPlease enable Role Persist by doing **{ctx.prefix}rolepersist enable**",
                                    inline=True)

                await ctx.message.channel.send(embed=embed)

                await send_to_modlogs(ctx.message, target, reason, action="Muted")

            # Send error message if the User could not be muted
            else:
                embed = Embed(description="**{} Could Not Be Muted!**".format(target.mention),
                              colour=enso_embedmod_colours)
                await ctx.message.channel.send(embed=embed)


async def ban_members(message, targets, reason):
    """

    Method to allow members to be banned

    2 embeds will be sent, one to the channel that the user is in
    And if the user has the modlogs channel setup, an embed will be logged there

    """

    for target in targets:
        if (message.guild.me.top_role.position > target.top_role.position
                and not target.guild_permissions.administrator):
            await target.ban(reason=reason)

            embed = Embed(description="✅ **{}** Was Banned! ✅".format(target),
                          colour=enso_embedmod_colours)
            await message.channel.send(embed=embed)

            await send_to_modlogs(message, target, reason, action="Banned")

        # Send error message if the User could not be banned
        else:
            embed = Embed(description="**{} Could Not Be Banned!**".format(target.mention))
            await message.channel.send(embed=embed)


async def unban_members(self, message, targets, reason):
    """

    Method to allow members to be unbanned

    2 embeds will be sent, one to the channel that the user is in
    And if the user has the modlogs channel setup, an embed will be logged there

    """

    # Get the list of banned users from the server
    bans = await message.guild.bans()
    ban_ids = list(map(lambda m: m.user.id, bans))

    for target in targets:
        if target not in ban_ids:
            embed = Embed(description="❌ **Member Is Not In Ban's List!** ❌",
                          colour=enso_embedmod_colours)
            await message.channel.send(embed=embed)
        else:

            # Get the member and unban them
            user = await self.bot.fetch_user(target)
            await message.guild.unban(user, reason=reason)

            # Send confirmation to the channel that the user is in
            embed = Embed(description="✅ **{}** Was Unbanned! ✅".format(user),
                          colour=enso_embedmod_colours)
            await  message.channel.send(embed=embed)

            await send_to_modlogs(message, user, reason, action="Unbanned")


async def kick_members(message, targets, reason):
    """

    Method to allow the kick member log to be sent to the modlog channel

    2 embeds will be sent, one to the channel that the user is in
    And if the user has the modlogs channel setup, an embed will be logged there

    """
    await message.delete()

    for target in targets:
        if (message.guild.me.top_role.position > target.top_role.position
                and not target.guild_permissions.administrator):
            await target.kick(reason=reason)

            embed = Embed(description="✅ **{}** Was Kicked! ✅".format(target),
                          colour=enso_embedmod_colours)
            await message.channel.send(embed=embed)

            await send_to_modlogs(message, target, reason, action="Kicked")

        # Send error message if the User could not be kicked
        else:
            embed = Embed(description="**{} Could Not Be Kicked!**".format(target.mention))
            await message.channel.send(embed=embed)


class Moderation(Cog):
    """Moderation Commands! (Kick/Ban/Mute etc)"""

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @command(name="kick", aliases=["Kick"], usage="`<member>...` `[reason]`")
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
                await kick_members(ctx.message, members, reason)

    @command(name="mute", aliases=["Mute"], usage="`<member>...` `[reason]`")
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
                        await channel.set_permissions(muted, read_messages=True, send_messages=False,
                                                      read_message_history=False)

                    await mute_members(self.bot.db, ctx, members, reason, muted)

                # Make sure that the Muted Role has the correct permissions before muting member(s)
                else:
                    for channel in ctx.guild.channels:
                        perms = channel.overwrites_for(role)

                        # Set the read_messages to True, only when the read_messages is False or None
                        if not perms.read_messages or perms.read_messages is None:
                            perms.read_messages = True

                        # Set the send_messages to True, only when the send_messages is False or None
                        if perms.send_messages or perms.send_messages is None:
                            perms.send_messages = False

                        # Set the read_message_history to True, only when the read_message_history is False or None
                        if perms.read_message_history or perms.read_message_history is None:
                            perms.read_message_history = False

                        # Overwrite the permissions if any perms were changed
                        if perms.read_messages or perms.send_messages or perms.read_message_history:
                            await channel.set_permissions(role, overwrite=perms)

                    await mute_members(self.bot.db, ctx, members, reason, role)

    @command(name="unmute", aliases=["Unmute"], usage="`<member>...` `[reason]`")
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
                                  colour=enso_embedmod_colours)
                    await ctx.send(embed=embed)

                else:

                    for member in members:
                        if role in member.roles:
                            await ummute_members(self, ctx.message, members, reason)
                            unmute = True

                        if role not in member.roles and unmute is False:
                            embed = Embed(description=f"**❌ {member.mention} Is Not Muted! ❌**",
                                          colour=enso_embedmod_colours)
                            await ctx.send(embed=embed)

    @command(name="ban", aliases=["Ban"], usage="`<member>...` `[reason]`")
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
                await ban_members(ctx.message, members, reason)

    @command(name="unban", aliases=["Unban"], usage="`<member>...` `[reason]`")
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
                await unban_members(self, ctx.message, members, reason)

    @command(name="purge", aliases=["Purge"])
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
                ctx.message.delete()
                deleted = await ctx.channel.purge(limit=amount,
                                                  after=datetime.datetime.utcnow() - timedelta(days=14))

                await ctx.send(f"Deleted **{deleted:,}** messages.", delete_after=5)

            # Send error if amount is not between 0 and 100
            else:
                await generate_embed(ctx, desc="The amount provided is not between **0** and **100**")

        # Delete the last 50 messages if no amount is given
        else:

            # Delete the message sent and then the amount specified
            # (Only messages sent within the last 14 days)

            ctx.message.delete()
            deleted = await ctx.channel.purge(limit=50,
                                              after=datetime.datetime.utcnow() - timedelta(days=14))

            await ctx.send(f"Deleted **{deleted:,}** messages.", delete_after=5)

    @Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        """Logging Bulk Message Deletion from Server"""

        # Get the channel within the cache
        channel = get_modlog_for_guild(str(payload.guild_id))

        # When no modlogs channel is returned, do nothing
        if channel is not None:
            # Get the modlogs channel and channel that the messages were deleted in
            modlogs_channel = self.bot.get_channel(int(channel))
            deleted_msgs_channel = self.bot.get_channel(payload.channel_id)

            # Set up embed showing the messages deleted and what channel they were deleted in
            embed = Embed(
                description="**Bulk Delete in {} | {} messages deleted**".format(deleted_msgs_channel.mention,
                                                                                 len(payload.message_ids)),
                colour=enso_embedmod_colours,
                timestamp=datetime.datetime.utcnow())
            embed.set_author(name=deleted_msgs_channel.guild.name, icon_url=deleted_msgs_channel.guild.icon_url)

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_remove(self, member):
        """Log Member Leaves from Server"""

        # Get the channel within the cache
        channel = get_modlog_for_guild(str(member.guild.id))

        # When no modlogs channel is returned, do nothing
        if channel is not None:
            # Get the modlogs channel
            modlogs_channel = self.bot.get_channel(int(channel))

            embed = Embed(description="**{}** | **{}**".format(member.mention, member),
                          colour=enso_embedmod_colours,
                          timestamp=datetime.datetime.utcnow())
            embed.set_author(name="Member Left", icon_url=member.avatar_url)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text="ID: {}".format(member.id))

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_join(self, member):
        """Log Member Joins to Server"""

        # Get the channel within the cache
        channel = get_modlog_for_guild(str(member.guild.id))

        # When no modlogs channel is returned, do nothing
        if channel is not None:
            # Get the modlogs channel
            modlogs_channel = self.bot.get_channel(int(channel))

            embed = Embed(description="**{}** | **{}**".format(member.mention, member),
                          colour=enso_embedmod_colours,
                          timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Account Creation Date",
                            value=member.created_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"),
                            inline=False)
            embed.set_author(name="Member Joined", icon_url=member.avatar_url)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text="ID: {}".format(member.id))

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_ban(self, guild, user):
        """Logs Member Bans to Server"""

        # Get the channel within the cache
        channel = get_modlog_for_guild(str(guild.id))

        # When no modlogs channel is returned, do nothing
        if channel is not None:
            # Get the modlogs channel
            modlogs_channel = self.bot.get_channel(int(channel))

            embed = Embed(description=f"{user.mention} | **{user}**",
                          colour=enso_embedmod_colours,
                          timestamp=datetime.datetime.utcnow())
            embed.set_author(name="Member Banned", icon_url=user.avatar_url)
            embed.set_footer(text=f"ID: {user.id}")
            embed.set_thumbnail(url=user.avatar_url)

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_unban(self, guild, user):
        """Logs Member Unbans to Server"""

        # Get the channel within the cache
        channel = get_modlog_for_guild(str(guild.id))

        # When no modlogs channel is returned, do nothing
        if channel is not None:
            # Get the modlogs channel
            modlogs_channel = self.bot.get_channel(int(channel))

            embed = Embed(description=f"{user.mention} | **{user}**",
                          colour=enso_embedmod_colours,
                          timestamp=datetime.datetime.utcnow())
            embed.set_author(name="Member Unbanned", icon_url=user.avatar_url)
            embed.set_footer(text=f"ID: {user.id}")
            embed.set_thumbnail(url=user.avatar_url)

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_update(self, before, after):
        """Logging Member Profile Updates"""

        # Get the channel within the cache
        channel = get_modlog_for_guild(str(after.guild.id))

        # When no modlogs channel is returned, do nothing
        if channel is not None:
            # Get the modlogs channel
            modlogs_channel = self.bot.get_channel(int(channel))

            # Logging Nickname Updates
            if before.nick != after.nick:
                embed = Embed(description=f"**{after.mention}'s Nickname Changed**",
                              colour=enso_embedmod_colours,
                              timestamp=datetime.datetime.utcnow())
                embed.set_author(name=after, icon_url=after.avatar_url)
                embed.add_field(name="Before",
                                value=before.nick, inline=False)
                embed.add_field(name="After",
                                value=after.nick, inline=False)
                embed.set_footer(text=f"ID: {after.id}")

                await modlogs_channel.send(embed=embed)

            # Logging Role additions/removals from Members
            if after.roles != before.roles:
                # Retrieve the roles that were added/removed to/from the Member
                new_roles = [roles for roles in after.roles if roles not in before.roles]
                old_roles = [roles for roles in before.roles if roles not in after.roles]

                # As long as roles were added to the Member, log the role(s) that were given
                if len(new_roles) >= 1:
                    new_roles_string = ", ".join(f"`{r.name}`" for r in new_roles)

                    # Change the description of the embed depending on how many roles were added
                    if len(new_roles) == 1:
                        desc = f"**{after.mention} was given the role** `{new_roles_string}`"
                    else:
                        desc = f"**Roles Added To {after.mention}\nRoles:** {new_roles_string}"

                    embed = Embed(description=desc,
                                  colour=enso_embedmod_colours,
                                  timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=after, icon_url=after.avatar_url)
                    embed.set_footer(text=f"ID: {after.id}")

                    await modlogs_channel.send(embed=embed)

                # As long as roles were removed from the member, log the role(s) that were removed
                if len(old_roles) >= 1:
                    old_roles_string = ", ".join(f"`{r.name}`" for r in old_roles)

                    # Change the description of the embed depending on how many roles were removed
                    if len(old_roles) == 1:
                        desc = f"**{after.mention} was removed from the role {old_roles_string}**"
                    else:
                        desc = f"**Roles Removed From {after.mention}\nRoles: {old_roles_string}**"

                    embed = Embed(description=desc,
                                  colour=enso_embedmod_colours,
                                  timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=after, icon_url=after.avatar_url)
                    embed.set_footer(text=f"ID: {after.id}")

                    await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before, after):
        """Logging Message Edits (Within Cache)"""

        # Get the channel within the cache
        channel = get_modlog_for_guild(str(after.guild.id))

        # When no modlogs channel is returned, do nothing
        if channel is not None:
            # Get the modlogs channel
            modlogs_channel = self.bot.get_channel(int(channel))

            # Logging Message Content Edits
            # Not logging any message edits from bots
            if before.content != after.content and after.author != after.author.bot:
                desc = f"**Message Edited Within** <#{after.channel.id}>\n[Jump To Message]({after.jump_url})"

                # When the message context exceeds 500 characters, only display the first 500 characters in the logs
                before_value = f"{before.content[:500]} ..." if len(before.content) >= 500 else before.content
                after_value = f"{after.content[:500]} ..." if len(after.content) >= 500 else after.content

                embed = Embed(description=desc,
                              colour=enso_embedmod_colours,
                              timestamp=datetime.datetime.utcnow())
                embed.set_author(name=after.author, icon_url=after.author.avatar_url)
                embed.add_field(name="Before",
                                value=before_value, inline=False)
                embed.add_field(name="After",
                                value=after_value, inline=False)
                embed.set_footer(text=f"ID: {after.author.id}")

                await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_raw_message_edit(self, payload):
        """Logging Message Edits Not Stored Within Internal Cache"""

        # Get the channel within the cache
        channel = get_modlog_for_guild(str(payload.data["guild_id"]))

        # Only log this message if the message does not exist within the internal cache and modlogs channel is set up
        if channel is not None and not payload.cached_message:
            # Get the modlogs channel
            modlogs_channel = self.bot.get_channel(int(channel))

            desc = f"**Message Was Edited Within <#{payload.channel_id}>\nMessage Content Not Displayable**"
            embed = Embed(description=desc,
                          colour=enso_embedmod_colours,
                          timestamp=datetime.datetime.utcnow())
            embed.set_author(name=modlogs_channel.guild.name, icon_url=modlogs_channel.guild.icon_url)
            embed.set_footer(text=f"Message ID: {payload.message_id}")

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message):
        """Logging Message Deletions (Within Cache)"""

        # Get the channel within the cache
        channel = get_modlog_for_guild(str(message.guild.id))

        # When no modlogs channel is returned, do nothing
        if channel is not None:
            # Get the modlogs channel
            modlogs_channel = self.bot.get_channel(int(channel))

            desc = f"**Message Sent By {message.author.mention} Deleted In {message.channel.mention}" \
                   f"\nMessage Content:** {message.content}"
            embed = Embed(description=desc,
                          colour=enso_embedmod_colours,
                          timestamp=datetime.datetime.utcnow())
            embed.set_author(name=message.author, icon_url=message.author.avatar_url)
            embed.set_footer(text=f"Author ID: {message.author.id} | Message ID: {message.id}")

            await modlogs_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
