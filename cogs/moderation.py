import datetime
from datetime import timedelta
from typing import Optional

import discord
from discord import Member, Embed
from discord.ext.commands import command, guild_only, has_guild_permissions, bot_has_guild_permissions, Greedy, \
    cooldown, BucketType, Cog

from settings import enso_embedmod_colours, get_modlog_for_guild, storeRoles, clearRoles, get_roles_persist


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
                await clearRoles(ctx=message, member=target, pool=pool)

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


async def mute_members(pool, message, targets, reason, muted):
    """

    Method to allow members to be muted

    2 embeds will be sent, one to the channel that the user is in
    And if the user has the modlogs channel setup, an embed will be logged there

    """

    for target in targets:
        if (message.guild.me.top_role.position > target.top_role.position
                and not target.guild_permissions.administrator):

            # Store the current roles of the user within database
            await storeRoles(pool=pool, target=target, ctx=message, member=target)
            # Give the user the muted role
            await target.edit(roles=[muted], reason=reason)

            # Send confirmation to the channel that the user is in
            embed = Embed(description="✅ **{}** Was Muted! ✅".format(target),
                          colour=enso_embedmod_colours)
            if get_roles_persist(str(message.guild.id)) == 0:
                embed.add_field(name="**WARNING: ROLE PERSIST NOT ENABLED**",
                                value="The bot **will not give** the roles back to the user if they leave the server."
                                      "Allowing the user to bypass the Mute by leaving and rejoining."
                                      f"Please enable Role Persist by doing **{message.guild.prefix}rolepersist enable**",
                                inline=True)

            await message.channel.send(embed=embed)

            await send_to_modlogs(message, target, reason, action="Muted")

        # Send error message if the User could not be muted
        else:
            embed = Embed(description="**{} Could Not Be Muted!**".format(target.mention))
            await message.channel.send(embed=embed)


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
            embed = Embed(description="❌ **Member Is Not In Unban's List!** ❌",
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

                role = discord.utils.get(ctx.guild.roles, name="Muted")

                if role is None:
                    # Setting up the role permissions for the Muted Role
                    muted = await ctx.guild.create_role(name="Muted")
                    # Removes permission to send messages in all channels
                    for channel in ctx.guild.channels:
                        await channel.set_permissions(muted, send_messages=False, read_messages=True)

                    # Send embed of the kicked member
                    await mute_members(self.bot.db, ctx.message, members, reason, muted)
                else:
                    # Send embed of the kicked member
                    await mute_members(self.bot.db, ctx.message, members, reason, role)

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
                # Send embed of the Banned member
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
        """Purge Messages from Channel
        (No Amount Will Default to 50 Messages Deleted)"""

        # When an amount is specified and is between 0 and 100
        if amount:
            if 0 < amount <= 100:

                # Delete the message sent and then the amount specified
                # (Only messages sent within the last 14 days)

                deleted = await ctx.channel.purge(limit=amount + 1,
                                                  after=datetime.datetime.utcnow() - timedelta(days=14))

                await ctx.send(f"Deleted **{(len(deleted)) - 1:,}** messages.", delete_after=5)

            # Send error if amount is not between 0 and 100
            else:
                await ctx.send("The amount provided is not between **0** and **100**")

        # Delete the last 50 messages if no amount is given
        else:

            # Delete the message sent and then the amount specified
            # (Only messages sent within the last 14 days)

            deleted = await ctx.channel.purge(limit=51,
                                              after=datetime.datetime.utcnow() - timedelta(days=14))

            await ctx.send(f"Deleted **{(len(deleted)) - 1:,}** messages.", delete_after=5)

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
                description="**Bulk Delete in {}, {} messages deleted**".format(deleted_msgs_channel.mention,
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

            embed = Embed(description="**{}** A.K.A **{}**".format(member.mention, member),
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

            embed = Embed(description="**{}** A.K.A **{}**".format(member.mention, member),
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

            embed = Embed(description=f"{user.mention} A.K.A **{user}**",
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

            embed = Embed(description=f"{user.mention} A.K.A **{user}**",
                          colour=enso_embedmod_colours,
                          timestamp=datetime.datetime.utcnow())
            embed.set_author(name="Member Unbanned", icon_url=user.avatar_url)
            embed.set_footer(text=f"ID: {user.id}")
            embed.set_thumbnail(url=user.avatar_url)

            await modlogs_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
