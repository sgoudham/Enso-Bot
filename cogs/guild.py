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

import asyncpg
from discord import Embed, TextChannel
from discord.ext.commands import has_permissions, Cog, group, bot_has_permissions, BadArgument, MissingRequiredArgument, \
    command, MissingPermissions

from cogs.libs.modmail import Modmail
from cogs.libs.starboard import Starboard


async def get_starboard_from_db(self, ctx, action):
    """Get the starboard record from DB"""

    # Setup up pool connection
    pool = self.bot.db
    async with pool.acquire() as conn:

        # Get the row of the guild from the starboard table
        try:
            select_query = """SELECT * FROM starboard WHERE guild_id = $1"""
            result = await conn.fetchrow(select_query, ctx.guild.id)

        # Catch errors
        except asyncpg.PostgresError as e:
            print("PostGres Error: Starboard Record Could Not Be Retrieved For Starboard", e)

        # Throw error if the guild already exists
        else:
            if action == "setup" and result:
                text = "**Starboard** Already Setup!" \
                       f"\nDo **{ctx.prefix}help starboard** to find out more!"
                await self.bot.generate_embed(ctx, desc=text)
                return None
            elif (action == "update" or action == "delete") and not result:
                text = "**Starboard** Not Setup!" \
                       f"\nDo **{ctx.prefix}help starboard** to find out more!"
                await self.bot.generate_embed(ctx, desc=text)
                return None

        return not None


async def get_modlogs_from_db(self, ctx, action):
    """Get the starboard record from DB"""

    # Setup up pool connection
    pool = self.bot.db
    async with pool.acquire() as conn:

        # Get the entire row of the guild from the guilds table
        try:
            select_query = """SELECT * FROM guilds WHERE guild_id = $1"""
            result = await conn.fetchrow(select_query, ctx.guild.id)

        # Catch errors
        except asyncpg.PostgresError as e:
            print("PostGres Error: Modlog Record Could Not Be Retrieved For Modlogs", e)

        # Throw error if the modlogs already exists
        else:
            if action == "setup" and result["modlogs"]:
                text = "**Modlogs** Already Setup!" \
                       f"\nDo **{ctx.prefix}help modlogs** to find out more!"
                await self.bot.generate_embed(ctx, desc=text)
                return None
            elif (action == "update" or action == "delete") and not result["modlogs"]:
                text = "**Modlogs** Not Setup!" \
                       f"\nDo **{ctx.prefix}help modlogs** to find out more!"
                await self.bot.generate_embed(ctx, desc=text)
                return None

        return not None


async def get_modmail_from_db(self, ctx, action):
    """Get the starboard record from DB"""

    # Setup up pool connection
    pool = self.bot.db
    async with pool.acquire() as conn:

        # Get the entire row of the guild from the guilds table
        try:
            select_query = """SELECT * FROM moderatormail WHERE guild_id = $1"""
            result = await conn.fetchrow(select_query, ctx.guild.id)

        # Catch errors
        except asyncpg.PostgresError as e:
            print("PostGres Error: Modlog Record Could Not Be Retrieved For Modlogs", e)

        # Throw error if the modlogs already exists
        else:
            if action == "setup" and result:
                text = "**Modmail** Already Setup!" \
                       f"\nDo **{ctx.prefix}help modmail** to find out more!"
                await self.bot.generate_embed(ctx, desc=text)
                return None
            elif (action == "update" or action == "delete") and not result:
                text = "**Modmail** Not Setup!" \
                       f"\nDo **{ctx.prefix}help modmail** to find out more!"
                await self.bot.generate_embed(ctx, desc=text)
                return None

        return not None


# Set up the Cog
class Guild(Cog):
    """All Guild Systems (Modmail/Modlogs/RolePersist)"""

    def __init__(self, bot):
        self.bot = bot
        self.modmail = Modmail(self.bot)
        self.starboard = Starboard(self.bot)

    @Cog.listener()
    async def on_ready(self):
        """Printing out that Cog is ready on startup"""
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @command(name="modstatus", aliases=["logsstatus"])
    @bot_has_permissions(embed_links=True)
    async def all_statuses(self, ctx):
        """Status of all the moderation systems (Modlogs/Modmail/RolePersist)"""
        desc = ""

        # Get status of mod
        if self.bot.get_roles_persist(ctx.guild.id) == 0:
            desc += f"**{self.bot.cross} Role Persist**\n"
        else:
            desc += f"**{self.bot.tick} Role Persist**\n"

        # Get status of modlogs
        if ml_channel := self.bot.get_modlog_for_guild(ctx.guild.id):
            channel = ctx.guild.get_channel(ml_channel)
            desc += f"**{self.bot.tick} Modlogs | {channel.mention}**\n"
        else:
            desc += f"**{self.bot.cross} Modlogs**\n"

        # Get status of modmail
        if modmail := self.bot.get_modmail(ctx.guild.id):
            modmail_channel = ctx.guild.get_channel(modmail["modmail_channel_id"])
            modmail_logging = ctx.guild.get_channel(modmail["modmail_logging_channel_id"])

            desc += f"**{self.bot.tick} Modmail | Channel:  {modmail_channel.mention} | Logging: {modmail_logging.mention}**\n"
        else:
            desc += f"**{self.bot.cross} Modmail**\n"

        if starboard := self.bot.get_starboard_channel(ctx.guild.id):
            channel = self.bot.get_channel(starboard)
            min_stars = self.bot.get_starboard_min_stars(ctx.guild.id)
            desc += f"**{self.bot.tick} Starboard | Channel: {channel.mention} | Minimum Stars: {min_stars} :star:**\n"
        else:
            desc += f"**{self.bot.cross} Starboard**\n"

        embed = Embed(title="Moderation Systems",
                      description=desc,
                      colour=self.bot.random_colour(),
                      timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @group(name="rolepersist", case_insensitive=True, usage="`<enable|disable>`")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(manage_roles=True)
    async def roles_persist(self, ctx):
        """Role Persist! Keep user roles when they leave/join!"""

    @roles_persist.command(name="enable")
    async def rp_enable(self, ctx):
        """Enabling role persist within the guild"""

        if self.bot.get_roles_persist(ctx.guild.id) == 0:
            await self.bot.update_role_persist(ctx.guild.id, value=1)
            await self.bot.generate_embed(ctx, desc=f"**Role Persist has been enabled within {ctx.guild}!**")
        else:
            await self.bot.generate_embed(ctx, desc=f"**Role Persist is already enabled within {ctx.guild}!**")

    @roles_persist.command(name="disable")
    async def rp_disable(self, ctx):
        """Disabling role persist within the guild"""

        if self.bot.get_roles_persist(ctx.guild.id) == 1:
            await self.bot.update_role_persist(ctx.guild.id, value=0)
            await self.bot.generate_embed(ctx, desc=f"**Role Persist has been disabled within {ctx.guild}!**")
        else:
            await self.bot.generate_embed(ctx, desc=f"**Role Persist is already disabled within {ctx.guild}!**")

    @group(name="starboard", case_insensitive=True, usage="`<setup|update|delete|stars>`")
    @bot_has_permissions(embed_links=True)
    @has_permissions(manage_guild=True)
    async def starboard(self, ctx):
        """
        Starboard! Let the community star messages!
        """

    @starboard.command(name="stars")
    @bot_has_permissions(embed_links=True)
    async def sb_min_stars(self, ctx, stars: int):
        """Update the minimum amount of stars needed for the message to appear on the starboard"""

        if await get_starboard_from_db(self, ctx, "update") and stars > 0:
            # Setup up pool connection
            pool = self.bot.db
            async with pool.acquire() as conn:

                # Update the starboard min_stars in the database
                try:
                    update_query = """UPDATE starboard SET min_stars = $1 WHERE guild_id = $2"""
                    await conn.execute(update_query, stars, ctx.guild.id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(f"PostGres Error: Starboard Record Could Not Be Updated For Guild {ctx.guild.id}", e)

                # Send confirmation that the channel has been updated
                else:
                    star_channel = self.bot.get_starboard_channel(ctx.guild.id)
                    channel = self.bot.get_channel(star_channel)
                    text = "**Minimum Stars Updated!**" \
                           f"\nMessages will now need {stars} :star: to appear in {channel.mention}"
                    await self.bot.generate_embed(ctx, desc=text)

                    # Update cache
                    self.bot.update_starboard_min_stars(ctx.guild.id, stars)

        elif stars <= 0:
            await self.bot.generate_embed(ctx, desc="Minimum Stars Must Be Over or Equal to 1!")

    @starboard.command(name="setup", usage="`<#channel>`")
    @bot_has_permissions(embed_links=True)
    async def sb_setup(self, ctx, starboard_channel: TextChannel):
        """
        Setup Starboard
        First Argument: Input Channel(Mention or ID) where starred messages will be sent
        """

        if await get_starboard_from_db(self, ctx, "setup"):
            # Setup up pool connection
            pool = self.bot.db
            async with pool.acquire() as conn:

                # Insert the information about the starboard into database
                try:
                    insert_query = """INSERT INTO starboard (guild_id, channel_id) VALUES ($1, $2)"""
                    await conn.execute(insert_query, ctx.guild.id, starboard_channel.id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(f"PostGres Error: Starboard Record Could Not Be Inserted For Guild {ctx.guild.id}", e)

                # Send confirmation message
                else:
                    text = "**Starboard** is successfully set up!" \
                           f"\nRefer to **{ctx.prefix}help starboard** for more information"
                    await self.bot.generate_embed(ctx, desc=text)

                    # Store into cache
                    self.bot.cache_store_starboard(ctx.guild.id, starboard_channel.id, 1)

    @starboard.command(name="update", usage="`<channel>`")
    @bot_has_permissions(embed_links=True)
    async def sb_update(self, ctx, starboard_channel: TextChannel):
        """
        Update the channel that the starred messages are sent to
        You can Mention or use the Channel ID
        """

        if await get_starboard_from_db(self, ctx, "update"):
            # Setup up pool connection
            pool = self.bot.db
            async with pool.acquire() as conn:

                # Update the starboard channel in the database
                try:
                    update_query = """UPDATE starboard SET channel_id = $1 WHERE guild_id = $2"""
                    await conn.execute(update_query, starboard_channel.id, ctx.guild.id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(f"PostGres Error: Starboard Record Could Not Be Updated For Guild {ctx.guild.id}", e)

                # Send confirmation that the channel has been updated
                else:
                    text = "**Channel Updated**" \
                           f"\nNew Starred Messages will be sent to {starboard_channel.mention}"
                    await self.bot.generate_embed(ctx, desc=text)

                    # Update cache
                    self.bot.update_starboard_channel(ctx.guild.id, starboard_channel.id)

    @starboard.command(name="delete")
    @bot_has_permissions(embed_links=True)
    async def sb_delete(self, ctx):
        """Delete the starboard from the guild"""

        if await get_starboard_from_db(self, ctx, "delete"):
            # Setup up pool connection
            pool = self.bot.db
            async with pool.acquire() as conn:

                # Remove the starboard record from the database
                try:
                    delete_query = """DELETE FROM starboard WHERE guild_id = $1"""
                    await conn.execute(delete_query, ctx.guild.id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(f"PostGres Error: Starboard Record Could Not Be Deleted for Guild {ctx.guild.id}", e)

                # Sending confirmation message that the starboard has been deleted
                else:
                    text = "**Starboard** successfully deleted!" \
                           f"\nDo **{ctx.prefix}help starboard** to find out more!"
                    await self.bot.generate_embed(ctx, desc=text)

                    # Delete from cache
                    self.bot.delete_starboard(ctx.guild.id)

    @group(name="modlogs", case_insensitive=True, usage="`<setup|update|delete>`")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(embed_links=True)
    async def modlogs(self, ctx):
        """
        Log updates in your server! (Nicknames/Deleted Msgs/etc!)
        """

    @modlogs.command(name="setup", usage="`<#channel>`")
    async def mlsetup(self, ctx, user_channel: TextChannel):
        """Setup a channel for Kick/Ban/Mute actions to be logged"""

        if await get_modlogs_from_db(self, ctx, "setup"):
            # Set up the modlogs channel within the guild
            mod_log_setup = True
            await self.bot.storage_modlog_for_guild(ctx, user_channel.id, mod_log_setup)

    @modlogs.command(name="update", usage="`<#channel>`")
    async def mlupdate(self, ctx, user_channel: TextChannel):
        """Change the channel that your modlogs are sent to"""

        if await get_modlogs_from_db(self, ctx, "update"):
            # Update the modlog channel within the database and cache
            mod_log_setup = False
            await self.bot.storage_modlog_for_guild(ctx, user_channel.id, mod_log_setup)

    @modlogs.command("delete")
    async def mldelete(self, ctx):
        """Delete the existing modlogs channel"""

        if await get_modlogs_from_db(self, ctx, "delete"):
            # Setup up pool connection
            pool = self.bot.db
            async with pool.acquire() as conn:

                # Update the existing modlogs for guild
                try:
                    update = """UPDATE guilds SET modlogs = NULL WHERE guild_id = $1"""
                    await conn.execute(update, ctx.guild.id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(f"PostGres Error: Guild Modlogs Could Not Be Deleted For {ctx.guild.id}", e)

                # Delete channel from cache
                else:
                    text = "**Modlogs System** successfully deleted!" \
                           f"\nDo **{ctx.prefix}help modlogs** to setup Modlogs again!"
                    await self.bot.generate_embed(ctx, desc=text)

                    self.bot.remove_modlog_channel(ctx.guild.id)

    @group(name="modmail", case_insensitive=True, usage="`<setup|update|delete>`")
    @bot_has_permissions(manage_channels=True, embed_links=True, add_reactions=True, manage_messages=True,
                         attach_files=True, read_message_history=True, manage_roles=True)
    @has_permissions(manage_guild=True)
    async def mod_mail(self, ctx):
        """
        Modmail! Allow your members to send mail to the staff team!
        """

    @mod_mail.command(name="setup")
    async def mmsetup(self, ctx, modmail: TextChannel, modmail_logging: TextChannel):
        """
        Setup Modmail System
        First Argument: Input Channel(Mention or ID) where members can send modmail
        Second Argument: Input Channel(Mention or ID) where the members mail should be sent
        """

        if await get_modmail_from_db(self, ctx, "setup"):

            # Set up embed to let the user how to start sending modmail
            desc = "React to this message if you want to send a message to the Staff Team!" \
                   "\n\n**React with ✅**" \
                   "\n\nWe encourage all suggestions/thoughts and opinions on the server!" \
                   "\nAs long as it is **valid** criticism." \
                   "\n\n\n**Purely negative feedback will not be considered.**"

            ModMail = Embed(title="**Welcome to Modmail!**",
                            description=desc,
                            colour=self.bot.admin_colour,
                            timestamp=datetime.datetime.utcnow())
            ModMail.set_thumbnail(url=self.bot.user.avatar_url)

            # Send modmail embed to the specified channel and auto add the ✅ reaction
            modmail_message = await modmail.send(embed=ModMail)
            await modmail_message.add_reaction('✅')

            # Setup up pool connection
            pool = self.bot.db
            async with pool.acquire() as conn:

                # Insert the information about the modmail system into database
                try:
                    insert_query = """INSERT INTO moderatormail (guild_id, modmail_channel_id, message_id, modmail_logging_channel_id) 
                                      VALUES ($1, $2, $3, $4)"""
                    await conn.execute(insert_query, ctx.guild.id, modmail.id, modmail_message.id, modmail_logging.id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(f"PostGres Error: Modmail System Record Could Not Be Inserted For Guild {ctx.guild.id}", e)

                # Send confirmation message
                else:
                    text = "**Modmail System** is successfully set up!" \
                           f"\nRefer to **{ctx.prefix}help modmail** for more information"
                    await self.bot.generate_embed(ctx, desc=text)

                    # Store into cache
                    self.bot.cache_store_modmail(ctx.guild.id, modmail.id, modmail_message.id, modmail_logging.id)

    @mod_mail.command(name="update")
    async def mmupdate(self, ctx, modmail_logging_channel: TextChannel):
        """
        Update the Channel that the Modmail is logged to
        You can Mention or use the Channel ID
        """

        if await get_modmail_from_db(self, ctx, "update"):

            pool = self.bot.db
            async with pool.acquire() as conn:
                # Update the modmail channel in the database
                try:
                    update_query = """UPDATE moderatormail SET modmail_logging_channel_id = $1 WHERE guild_id = $2"""
                    await conn.execute(update_query, modmail_logging_channel.id, ctx.guild.id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(f"PostGres Error: Modmail System Record Could Not Be Updated For Guild {ctx.guild.id}", e)

                # Send confirmation that the channel has been updated
                else:
                    text = "**Channel Updated**" \
                           f"\nNew Modmail will be sent to {modmail_logging_channel.mention}"
                    await self.bot.generate_embed(ctx, desc=text)
                    # Update cache
                    self.bot.update_modmail(ctx.guild.id, modmail_logging_channel.id)

    @mod_mail.command(name="delete")
    async def mmdelete(self, ctx):
        """Delete the entire modmail system from the guild"""

        if await get_modmail_from_db(self, ctx, "delete"):

            # Setup up pool connection
            pool = self.bot.db
            async with pool.acquire() as conn:

                # Remove the moderatormail record from the database
                try:
                    delete_query = """DELETE FROM moderatormail WHERE guild_id = $1"""
                    await conn.execute(delete_query, ctx.guild.id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(f"PostGres Error: ModeratorMail Record Could Not Be Deleted for Guild {ctx.guild.id}", e)

                # Sending confirmation message that the modmail system has been deleted
                else:
                    text = "**Modmail System** successfully deleted!" \
                           f"\nDo **{ctx.prefix}help modmail** to find out more!"
                    await self.bot.generate_embed(ctx, desc=text)

                    # Delete from cache
                    self.bot.delete_modmail(ctx.guild.id)

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Listening for reactions relating to modmail/starboard"""

        await self.modmail.modmail(payload)
        await self.starboard.send_starboard_and_update_db(payload, action="added")

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Editing the message if a star reaction was removed"""

        await self.starboard.send_starboard_and_update_db(payload, action="removed")

    @mlsetup.error
    @mlupdate.error
    @mmsetup.error
    @mmupdate.error
    @sb_setup.error
    @sb_update.error
    async def mlsetup_command_error(self, ctx, exc):
        """Catching error if channel is not recognised"""

        if isinstance(exc, BadArgument):
            text = "**Channel Not Detected... Aborting Process**"
            await self.bot.generate_embed(ctx, desc=text)
        elif isinstance(exc, MissingRequiredArgument):
            text = "Required Argument(s) Missing!" \
                   f"\nUse **{ctx.prefix}help** to find how to use **{ctx.command}**"
            await self.bot.generate_embed(ctx, desc=text)
        elif isinstance(exc, MissingPermissions):
            missing_perms = string.capwords(", ".join(exc.missing_perms).replace("_", " "))

            text = f"{self.bot.cross} Uh oh! You Need **{missing_perms}** Permission(s) To Execute This Command! {self.bot.cross}"
            await self.bot.generate_embed(ctx, desc=text)


def setup(bot):
    bot.add_cog(Guild(bot))
