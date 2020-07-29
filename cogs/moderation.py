import datetime
from datetime import timedelta
from typing import Optional

from discord import Member, Embed
from discord.ext.commands import command, guild_only, has_guild_permissions, bot_has_guild_permissions, Greedy, \
    has_permissions, bot_has_permissions, cooldown, BucketType, Cog, group

import db
from db import connection
from settings import enso_embedmod_colours, get_modlog_for_guild, storage_modlog_for_guild, remove_modlog_channel


async def ban_members(message, targets, reason):
    """

    Method to allow members to be banned

    If no channel has been detected in the cache, it will send the embed
    to the current channel that the user is in

    """

    # Get the channel of the modlog within the guild
    modlog = get_modlog_for_guild(str(message.guild.id))
    if modlog is None:
        channel = message.channel
    else:
        channel = message.guild.get_channel(int(modlog))

    # With every member, ban them and send an embed confirming the ban
    # The embed will either be sent to the current channel or the modlogs channel
    for target in targets:
        if (message.guild.me.top_role.position > target.top_role.position
                and not target.guild_permissions.administrator):
            await target.ban(reason=reason)

            embed = Embed(title="Member Banned",
                          colour=enso_embedmod_colours,
                          timestamp=datetime.datetime.utcnow())

            embed.set_thumbnail(url=target.avatar_url)

            fields = [("Member", target.mention, False),
                      ("Actioned by", message.author.mention, False),
                      ("Reason", reason, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await channel.send(embed=embed)

        # Send error message if the User could not be banned
        else:
            embed = Embed(description="**{} Could Not Be Banned!**".format(target.mention))
            await message.channel.send(embed=embed)


async def kick_members(message, targets, reason):
    """

    Method to allow the kick member log to be sent to the modlog channel

    If no channel has been detected in the cache, it will send the embed
    to the current channel that the user is in

    """

    # Get the channel of the modlog within the guild
    modlog = get_modlog_for_guild(str(message.guild.id))
    if modlog is None:
        channel = message.channel
    else:
        channel = message.guild.get_channel(int(modlog))

    # With every member, kick them and send an embed confirming the kick
    # The embed will either be sent to the current channel or the modlogs channel
    for target in targets:
        if (message.guild.me.top_role.position > target.top_role.position
                and not target.guild_permissions.administrator):
            await target.kick(reason=reason)

            embed = Embed(title="Member Kicked",
                          colour=enso_embedmod_colours,
                          timestamp=datetime.datetime.utcnow())

            embed.set_thumbnail(url=target.avatar_url)

            fields = [("Member", target.mention, False),
                      ("Actioned by", message.author.mention, False),
                      ("Reason", reason, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await channel.send(embed=embed)

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

    @group(invoke_without_command=True, usage="`[argument...]`")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    @cooldown(1, 1, BucketType.user)
    async def modlogs(self, ctx):
        """Setup/Update/Delete Modlogs System"""
        pass

    @modlogs.command()
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    @cooldown(1, 1, BucketType.user)
    async def setup(self, ctx, channelID: int):
        """Setup a Channel for the Kick/Ban/Mute Actions to be Logged In"""

        # Retrieve a list of channel id's in the guild
        channels = [channel.id for channel in ctx.guild.channels]

        # Setup pool
        pool = await connection(db.loop)

        # Setup pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Get the row of the guild
                select_query = """SELECT * FROM guilds WHERE guildID = (%s)"""
                val = ctx.guild.id,

                # Execute the SQL Query
                await cur.execute(select_query, val)
                result = await cur.fetchone()

        # Throw error if the modlog channel already exists and then stop the function
        if result[2] is not None:
            await ctx.send("Looks like this guild already has a **Modlogs Channel** set up!" +
                           f"\nPlease check **{ctx.prefix}help** for information on how to update/delete existing information")
            return

        # Abort the process if the channel does not exist within the guild
        if channelID not in channels:
            await ctx.send("**Invalid ChannelID Detected... Aborting Process**")

        else:
            # Set up the modlogs channel within the guild
            mod_log_setup = True
            await storage_modlog_for_guild(ctx, channelID, mod_log_setup)

    @modlogs.command()
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    @cooldown(1, 1, BucketType.user)
    async def update(self, ctx, channelID: int):
        """Change the Channel that your Modlogs are Sent to"""

        # Retrieve a list of channel id's in the guild
        channels = [channel.id for channel in ctx.guild.channels]

        # Setup pool
        pool = await db.connection(db.loop)

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Get the guilds row from the guilds table
                select_query = """SELECT * FROM guilds WHERE guildID = (%s)"""
                vals = ctx.guild.id,

                # Execute the SQL Query
                await cur.execute(select_query, vals)
                result = await cur.fetchone()

        # Throw error if the modlog channel already exists and then stop the function
        if result[2] is None:
            await ctx.send("Looks like this guild has not setup a **Modlogs Channel**" +
                           f"\nPlease check **{ctx.prefix}help** for information on how to update/delete existing information")
            return

        # Abort the process if the channel does not exist within the guild
        if channelID not in channels:
            await ctx.send("**Invalid ChannelID Detected... Aborting Process**")

        else:
            # Update the modlog channel within the database and cache
            mod_log_setup = False
            await storage_modlog_for_guild(ctx, channelID, mod_log_setup)

    @modlogs.command()
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    @cooldown(1, 1, BucketType.user)
    async def delete(self, ctx):
        """Delete the Existing Modlogs System"""

        # Setup pool
        pool = await db.connection(db.loop)

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Get the guilds row from the guilds table
                select_query = """SELECT * FROM guilds WHERE guildID = (%s)"""
                vals = ctx.guild.id,

                # Execute the SQL Query
                await cur.execute(select_query, vals)
                result = await cur.fetchone()

        # Throw error if the modlog channel already exists and then stop the function
        if result[2] is None:
            await ctx.send("Looks like this guild has not setup a **Modlogs Channel**" +
                           f"\nPlease check **{ctx.prefix}help** for information on how to update/delete existing information")
            return

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Update the existing prefix within the database
                update_query = """UPDATE guilds SET modlogs = NULL WHERE guildID = (%s)"""
                update_vals = ctx.guild.id,

                # Execute the query
                await cur.execute(update_query, update_vals)
                await conn.commit()

        # Delete channel from cache
        remove_modlog_channel(str(ctx.guild.id))

        # Sending confirmation message that the modmail system has been deleted
        await ctx.send("**Modlogs System** successfully deleted!" +
                       f"\nPlease do **{ctx.prefix}help** to find out how to set Modmail again!")

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

        # When no members are entered. Throw an error
        if not len(members):
            embed = Embed(description="Not Correct Syntax!"
                                      "\nUse **{}help** to find how to use **{}**".format(ctx.prefix, ctx.command))
            await ctx.send(embed=embed)

        # As long as all members are valid
        else:
            # Send embed of the kicked member
            await kick_members(ctx.message, members, reason)

    @command(name="ban", aliases=["Ban"], usage="`<member>...` `[reason]`")
    @guild_only()
    @has_guild_permissions(ban_members=True)
    @bot_has_guild_permissions(ban_members=True)
    @cooldown(1, 1, BucketType.user)
    async def ban(self, ctx, members: Greedy[Member], *, reason: Optional[str] = "No reason provided."):
        """
        Ban Member(s) from Server
        Multiple Members can be banned at once
        """

        # When no members are entered. Throw an error
        if not len(members):
            embed = Embed(description="Not Correct Syntax!"
                                      "\nUse **{}help** to find how to use **{}**".format(ctx.prefix, ctx.command))
            await ctx.send(embed=embed)

        # As long as all members are valid
        else:
            # Send embed of the Banned member
            await ban_members(ctx.message, members, reason)

    @command(name="unban", aliases=["Unban"], usage="`<member>` `[reason]`")
    @guild_only()
    @has_guild_permissions(ban_members=True)
    @bot_has_guild_permissions(ban_members=True)
    @cooldown(1, 1, BucketType.user)
    async def unban(self, ctx, member: int, *, reason=None):
        """Unban Member from Server"""

        # Check if reason has been given
        if reason:
            reason = reason
        # Set default reason to None
        else:
            reason = "No Reason Given"

        # Get the member and unban them
        member = await self.bot.fetch_user(member)
        await ctx.guild.unban(member, reason=reason)

        # Confirm that the user has been unbanned
        await ctx.send(f"{ctx.author.name} **unbanned** {member.name}"
                       f"\n**Reason:** '{reason}'")

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
                await ctx.message.delete()
                deleted = await ctx.channel.purge(limit=amount,
                                                  after=datetime.datetime.utcnow() - timedelta(days=14))

                await ctx.send(f"Deleted **{len(deleted):,}** messages.", delete_after=5)

            # Send error if amount is not between 0 and 100
            else:
                await ctx.send("The amount provided is not between **0** and **100**")

        # Delete the last 50 messages if no amount is given
        else:

            # Delete the message sent and then the amount specified
            # (Only messages sent within the last 14 days)
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=50,
                                              after=datetime.datetime.utcnow() - timedelta(days=14))

            await ctx.send(f"Deleted **{len(deleted):,}** messages.", delete_after=5)

    @Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        """Logging Bulk Message Deletion from Server"""

        # Get the guild within the cache
        guild = get_modlog_for_guild(str(payload.guild_id))

        # When no modlogs channel is returned, do nothing
        if guild is None:
            pass
        # Send the embed to the modlogs channel
        else:

            # Get the modlogs channel and channel that the messages were deleted in
            modlogs_channel = self.bot.get_channel(int(guild))
            channel = self.bot.get_channel(payload.channel_id)

            # Set up embed showing the messages deleted and what channel they were deleted in
            embed = Embed(
                description="**Bulk Delete in {}, {} messages deleted**".format(channel.mention,
                                                                                len(payload.message_ids)),
                colour=enso_embedmod_colours,
                timestamp=datetime.datetime.utcnow())
            embed.set_author(name=channel.guild.name, icon_url=channel.guild.icon_url)

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_remove(self, member):
        """Log Member Leaves from Server"""

        # Get the guild within the cache
        guild = get_modlog_for_guild(str(member.guild.id))

        # When no modlogs channel is returned, do nothing
        if guild is None:
            pass
        # Send the embed to the modlogs channel
        else:

            # Get the modlogs channel
            modlogs_channel = self.bot.get_channel(int(guild))

            embed = Embed(description="{} A.K.A {}".format(member.mention, member),
                          colour=enso_embedmod_colours,
                          timestamp=datetime.datetime.utcnow())
            embed.set_author(name="Member Left", icon_url=member.avatar_url)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text="ID: {}".format(member.id))

            await modlogs_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_join(self, member):
        """Log Member Joins to Server"""

        # Get the guild within the cache
        guild = get_modlog_for_guild(str(member.guild.id))

        # When no modlogs channel is returned, do nothing
        if guild is None:
            pass
        # Send the embed to the modlogs channel
        else:

            # Get the modlogs channel
            modlogs_channel = self.bot.get_channel(int(guild))

            embed = Embed(description="{} A.K.A {}".format(member.mention, member),
                          colour=enso_embedmod_colours,
                          timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Account Creation Date",
                            value=member.created_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"),
                            inline=False)
            embed.set_author(name="Member Joined", icon_url=member.avatar_url)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text="ID: {}".format(member.id))

            await modlogs_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
