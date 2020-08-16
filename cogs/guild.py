# Ensō~Chan - A Multi Purpose Discord Bot That Has Everything Your Server Needs!
# Copyright (C) 2020  Goudham Suresh

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

import asyncio
import datetime
import io
import random

import discord
from discord import Embed, TextChannel
from discord import File
from discord.ext.commands import has_permissions, Cog, group, bot_has_permissions, BadArgument


# Method to ask the user if they want to be anonymous or not
def anon_or_not(self, author):
    # Set up embed to let the user how to start sending modmail
    AnonModMailEmbed = Embed(title="**Want to send it Anonymously?**",
                             colour=self.bot.admin_colour,
                             timestamp=datetime.datetime.utcnow())

    AnonModMailEmbed.set_thumbnail(url=author.avatar_url)
    AnonModMailEmbed.set_footer(text=f"Sent by {author}")

    fields = [(self.bot.blank_space, "**We understand that for some things,"
                                     "you may want to remain Anonymous."
                                     "\nUse the reactions below to choose!**", False),
              (self.bot.blank_space, "**Use :white_check_mark: for** `Yes`", True),
              (self.bot.blank_space, "**Use :x: for** `No`", True),
              (self.bot.blank_space, self.bot.blank_space, True),
              (self.bot.blank_space,
               "The Staff will not know who is sending this"
               "\nPurely negative feedback will not be considered.", True)]

    for name, value, inline in fields:
        AnonModMailEmbed.add_field(name=name, value=value, inline=inline)

    return AnonModMailEmbed


# Method to send an embed to to let the user know to type into chat
def send_instructions(self, author):
    # Set up embed to let the user know that they have aborted the modmail
    SendModMailEmbed = Embed(title="**Please enter a message for it to be sent to the staff!**",
                             colour=self.bot.admin_colour,
                             timestamp=datetime.datetime.utcnow())

    SendModMailEmbed.set_thumbnail(url=author.avatar_url)
    SendModMailEmbed.set_footer(text=f"Sent by {author}")

    fields = [("**Make sure that the message is above **50** and below **1024** characters!**",
               "**Include as much detail as possible :P**",
               False)]

    for name, value, inline in fields:
        SendModMailEmbed.add_field(name=name, value=value, inline=inline)

    return SendModMailEmbed


# Method to let the user know that the message must be above 50 characters
def error_handling(self, author):
    # Set up embed to let the user know that the message must be above 50 characters
    ErrorHandlingEmbed = Embed(
        title="Uh Oh! Please make sure the message is above **50** and below **1024** characters!",
        colour=self.bot.admin_colour,
        timestamp=datetime.datetime.utcnow())

    ErrorHandlingEmbed.set_thumbnail(url=author.avatar_url)
    ErrorHandlingEmbed.set_footer(text=f"Sent by {author}")

    fields = [("Please enter in a message which is above **50** and below **1024** characters!",
               "**This helps us reduce spam and allows you to include more detail in your mail!**",
               False)]

    for name, value, inline in fields:
        ErrorHandlingEmbed.add_field(name=name, value=value, inline=inline)

    return ErrorHandlingEmbed


# Method to send an embed into chat to let the user know that their mail has been sent successfully
def message_sent_confirmation(self, author):
    # Set up embed to let the user know that they have sent the mail
    ConfirmationEmbed = Embed(title="**Message relayed to Staff!!**",
                              colour=self.bot.admin_colour,
                              timestamp=datetime.datetime.utcnow())

    ConfirmationEmbed.set_thumbnail(url=author.avatar_url)
    ConfirmationEmbed.set_footer(text=f"Sent by {author}")

    fields = [("Thank you for your input! The staff team appreciate it very much!",
               f"\n As mentioned previously, please don't be hesistant to DM the Staff for anything! :P",
               False)]

    for name, value, inline in fields:
        ConfirmationEmbed.add_field(name=name, value=value, inline=inline)

    return ConfirmationEmbed


# Method to actually allow the message to be sent to #mod-mail
def send_modmail(self, msg, author):
    embed = Embed(title="Modmail",
                  colour=self.bot.admin_colour,
                  timestamp=datetime.datetime.utcnow())

    if self.anon:

        embed.set_thumbnail(url=random.choice(self.avatars))
        embed.set_footer(text=f"Sent By Anon Member")

        fields = [("Member", "Anon Member", False),
                  ("Message", msg.content, False)]
    else:

        embed.set_thumbnail(url=author.avatar_url)
        embed.set_footer(text=f"Sent By {author}")

        fields = [("Member", author, False),
                  ("Message", msg.content, False)]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    return embed


# Set up the Cog
class Guild(Cog):
    """Modmail System!"""

    def __init__(self, bot):
        self.bot = bot
        self.anon = None
        self.avatars = ["https://cdn.discordapp.com/embed/avatars/0.png",
                        "https://cdn.discordapp.com/embed/avatars/1.png",
                        "https://cdn.discordapp.com/embed/avatars/2.png",
                        "https://cdn.discordapp.com/embed/avatars/3.png",
                        "https://cdn.discordapp.com/embed/avatars/4.png"]

    @Cog.listener()
    async def on_ready(self):
        """Printing out that Cog is ready on startup"""
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @group(name="rolepersist", invoke_without_command=True, case_insensitive=True, usage="`[argument...]`")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    async def roles_persist(self, ctx):
        """Role Persist! Keep user roles when they leave/join!"""
        pass

    @roles_persist.command(name="status")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    async def rp_status(self, ctx):
        """Showing the status of the role persist within the guild"""

        if self.bot.get_roles_persist(str(ctx.guild.id)) == 0:
            await self.bot.generate_embed(ctx, desc=f"**Role Persist is currently disabled within {ctx.guild}**")
        else:
            await self.bot.generate_embed(ctx, desc=f"**Role Persist is currently enabled within {ctx.guild}**")

    @roles_persist.command(name="enable")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    async def rp_enable(self, ctx):
        """Enabling role persist within the guild"""

        pool = self.bot.db

        if self.bot.get_roles_persist(str(ctx.guild.id)) == 0:
            await self.bot.update_role_persist(str(ctx.guild.id), value=1, pool=pool)
            await self.bot.generate_embed(ctx, desc=f"**Role Persist has been enabled within {ctx.guild}!**")
        else:
            await self.bot.generate_embed(ctx, desc=f"**Role Persist is already enabled within {ctx.guild}!**")

    @roles_persist.command(name="disable")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    async def rp_disable(self, ctx):
        """Disabling role persist within the guild"""

        pool = self.bot.db

        if self.bot.get_roles_persist(str(ctx.guild.id)) == 1:
            await self.bot.update_role_persist(str(ctx.guild.id), value=0, pool=pool)
            await self.bot.generate_embed(ctx, desc=f"**Role Persist has been disabled within {ctx.guild}!**")
        else:
            await self.bot.generate_embed(ctx, desc=f"**Role Persist is already disabled within {ctx.guild}!**")

    @group(name="modlogs", invoke_without_command=True, case_insensitive=True, usage="`[argument...]`")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    async def modlogs(self, ctx):
        """
        Show Current Modlogs Channel (If Setup)
        """

        ml_channel = self.bot.get_modlog_for_guild(str(ctx.guild.id))

        # Send current modlogs channel only if it is setup
        # Send error if no modlogs channel has been setup
        if ml_channel is not None:

            # Get the modlog channel for the current guild
            channel = ctx.guild.get_channel(int(ml_channel))

            text = f"**The current modlogs channel is set to {channel.mention}**"
            await self.bot.generate_embed(ctx, desc=text)
        else:

            text = "**Modlogs Channel** already set up!" \
                   f"\nDo **{ctx.prefix}help modlogs** to find out more!"
            await self.bot.generate_embed(ctx, desc=text)

    @modlogs.command(name="setup")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    async def mlsetup(self, ctx, user_channel: TextChannel):
        """Setup a Channel for the Kick/Ban/Mute Actions to be Logged In"""

        # Setup pool
        pool = self.bot.db

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
            text = "**Modlogs Channel** already set up!" \
                   f"\nDo **{ctx.prefix}help modlogs** to find out more!"
            await self.bot.generate_embed(ctx, desc=text)
            return

        else:
            # Set up the modlogs channel within the guild
            mod_log_setup = True
            await self.bot.storage_modlog_for_guild(self.bot.db, ctx, user_channel.id, mod_log_setup)

    @modlogs.command(name="update")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    async def mlupdate(self, ctx, user_channel: TextChannel):
        """Change the Channel that your Modlogs are Sent to"""

        # Setup pool
        pool = self.bot.db

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
            text = "**Modlogs Channel** not set up!" \
                   f"\nDo **{ctx.prefix}help modlogs** to find out more!"
            await self.bot.generate_embed(ctx, desc=text)

        else:
            # Update the modlog channel within the database and cache
            mod_log_setup = False
            await self.bot.storage_modlog_for_guild(self.bot.db, ctx, user_channel.id, mod_log_setup)

    @modlogs.command("delete")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    async def mldelete(self, ctx):
        """Delete the Existing Modlogs System"""

        # Setup pool
        pool = self.bot.db

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Get the guilds row from the guilds table
                select_query = """SELECT * FROM guilds WHERE guildID = (%s)"""
                vals = ctx.guild.id,

                # Execute the SQL Query
                await cur.execute(select_query, vals)
                result = await cur.fetchone()

        # Throw error is modlogs error has not been setup before performing a delete action
        if result[2] is None:
            text = "**Modlogs Channel** not set up!" \
                   f"\nDo **{ctx.prefix}help modlogs** to find out more!"
            await self.bot.generate_embed(ctx, desc=text)
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
        self.bot.remove_modlog_channel(str(ctx.guild.id))

        text = "**Modlogs System** successfully deleted!" \
               f"\nDo **{ctx.prefix}help modlogs** to setup Modlogs again!"
        await self.bot.generate_embed(ctx, desc=text)

    @group(name="modmail", invoke_without_command=True, case_insensitive=True, usage="`[argument...]`")
    @bot_has_permissions(administrator=True)
    async def modmail(self, ctx):
        """
        Show Current Modlogs Channel (If Setup)
        Setup/Update/Delete Modmail System
        """
        pass

    @modmail.command(name="setup")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    async def mmsetup(self, ctx, user_channel: TextChannel, modmail_channel: TextChannel):
        """
        Setup Modmail System
        First Argument: Input Channel(Mention or ID) where members can send modmail
        Second Argument: Input Channel(Mention or ID) where the members mail should be sent
        """

        # Setup pool
        pool = self.bot.db

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Get the author's row from the Members Table
                select_query = """SELECT * FROM moderatormail WHERE guildID = (%s)"""
                val = ctx.guild.id,

                # Execute the SQL Query
                await cur.execute(select_query, val)
                result = await cur.fetchone()

        # Throw error if the guild already exists and then stop the function
        if result is not None:
            text = "**Modmail System** already set up!" \
                   f"\nDo **{ctx.prefix}help modmail** to find out more!"
            await self.bot.generate_embed(ctx, desc=text)
            return

        desc = "React to this message if you want to send a message to the Staff Team!" \
               "\n\n**React with ✅**" \
               "\n\nWe encourage all suggestions/thoughts and opinions on the server!" \
               "\nAs long as it is **valid** criticism." \
               "\n\n\n**Purely negative feedback will not be considered.**"

        # Set up embed to let the user how to start sending modmail
        ModMail = Embed(title="**Welcome to Modmail!**",
                        description=desc,
                        colour=self.bot.admin_colour,
                        timestamp=datetime.datetime.utcnow())
        ModMail.set_thumbnail(url=self.bot.user.avatar_url)

        modmail_message = await user_channel.send(embed=ModMail)

        # Auto add the ✅ reaction
        await modmail_message.add_reaction('✅')

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Define the insert statement that will insert information about the modmail channel
                insert_query = """INSERT INTO moderatormail (guildID, channelID, messageID, modmailChannelID) VALUES (%s, %s, %s, %s)"""
                vals = ctx.guild.id, user_channel.id, modmail_message.id, modmail_channel.id,

                # Execute the SQL Query
                await cur.execute(insert_query, vals)
                await conn.commit()

            text = "**Modmail System** is successfully set up!" \
                   f"\nRefer to **{ctx.prefix}help modmail** for more information"
            await self.bot.generate_embed(ctx, desc=text)

    @modmail.command(name="update")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    async def mmupdate(self, ctx, modmail_channel: TextChannel):
        """
        Update the Channel that the Modmail is logged to
        You can Mention or use the Channel ID
        """

        # Setup pool
        pool = self.bot.db

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Get the author's row from the Members Table
                select_query = """SELECT * FROM moderatormail WHERE guildID = (%s)"""
                vals = ctx.guild.id,

                # Execute the SQL Query
                await cur.execute(select_query, vals)
                result = await cur.fetchone()

            # Throw error if the guild already exists and then stop the function
            if result is None:
                text = "**Modmail System** not set up!" \
                       f"\nDo **{ctx.prefix}help modmail** to find out more!"
                await self.bot.generate_embed(ctx, desc=text)
                return

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Define the update statement that will insert information about the modmail channel
                update_query = """UPDATE moderatormail SET modmailChannelID = (%s) WHERE guildID = (%s)"""
                vals = modmail_channel.id, ctx.guild.id

                # Execute the SQL Query
                await cur.execute(update_query, vals)
                await conn.commit()

        # Send confirmation that the channel has been updated
        text = "**Channel Updated**" \
               f"\nNew Modmail will be sent to {modmail_channel.mention}"
        await self.bot.generate_embed(ctx, desc=text)

    @modmail.command(name="delete")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    async def mmdelete(self, ctx):
        """Delete the Entire Modmail System from the Guild"""

        # Setup pool
        pool = self.bot.db

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Get the author's row from the Members Table
                select_query = """SELECT * FROM moderatormail WHERE guildID = (%s)"""
                vals = ctx.author.guild.id,

                # Execute the SQL Query
                await cur.execute(select_query, vals)
                result = await cur.fetchone()

            # Throw error if modmail system does not exist already
            if result is None:
                text = "**Modmail System** not set up!" \
                       f"\nDo **{ctx.prefix}help modmail** to find out more!"
                await self.bot.generate_embed(ctx, desc=text)
                return

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Define the delete statement to remove all information about the guild
                delete_query = """DELETE FROM moderatormail WHERE guildID = (%s)"""
                vals = ctx.author.guild.id,

                # Execute the SQL Query
                await cur.execute(delete_query, vals)
                await conn.commit()

            # Sending confirmation message that the modmail system has been deleted
            text = "**Modmail System** successfully deleted!" \
                   f"\nDo **{ctx.prefix}help modmail** to find out more!"
            await self.bot.generate_embed(ctx, desc=text)

    # Setting up Listener to listen for reactions within the modmail channel created
    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Don't count reactions that are made by the bot
        if payload.user_id == self.bot.user.id:
            return

        # Don't count other reactions other than ✅ and ❌
        elif payload.user_id:
            if str(payload.emoji) not in ['✅', '❌']:
                return

        # Find a role corresponding to the Emoji name.
        guildid = payload.guild_id

        # Setup pool
        pool = self.bot.db

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Get the author's row from the Members Table
                select_query = """SELECT * FROM moderatormail WHERE guildID = (%s)"""
                val = guildid,

                # Execute the SQL Query
                await cur.execute(select_query, val)
                result = await cur.fetchone()

            # Adding error handling
            if result is None:
                return

            # Define variables
            guild_id = int(result[0])
            channel_id = int(result[1])
            message_id = int(result[2])
            modmail_channel_id = int(result[3])

        # Bunch of checks to make sure it has the right guild, channel, message and reaction
        if payload.guild_id == guild_id and payload.channel_id == channel_id and payload.message_id == message_id and payload.emoji.name == "✅":

            # Get the guild
            guild = self.bot.get_guild(payload.guild_id)
            # Get the member
            member = guild.get_member(payload.user_id)
            # Get the setup modmail channel
            channel = guild.get_channel(payload.channel_id)
            # Get the modmail logging channel
            modmail_channel = guild.get_channel(modmail_channel_id)

            # Fetch the message and remove the reaction
            reaction = await channel.fetch_message(message_id)
            await reaction.remove_reaction('✅', member)

            # Setting up the channel permissions for the new channel that will be created
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                guild.me: discord.PermissionOverwrite(administrator=True),
                member: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }

            # Saving this for later within when discord.py 1.4 comes out
            # user_channel = await guild.create_category_channel("Member", overwrites=overwrites, position=7)

            # Create the text channel
            user_channel = await guild.create_text_channel("Member", overwrites=overwrites,
                                                           position=0)

            # Mention the user to make sure that they get pinged
            mention = await user_channel.send(member.mention)
            await mention.delete()

            try:

                # Send the embed if they want to remain anonymous or not
                Anon_or_Not = await user_channel.send(embed=anon_or_not(self, member))
                # Add reactions to the message
                await Anon_or_Not.add_reaction('✅')
                await Anon_or_Not.add_reaction('❌')

                # Checking if the user reacted with ✅ with response to sending staff a message
                def emoji_check(reaction, user):
                    return user == member and str(reaction.emoji) in ['✅', '❌']

                # Surround with try/except to catch any exceptions that may occur
                try:
                    # Wait for the user to add a reaction
                    reaction, user = await self.bot.wait_for('reaction_add', check=emoji_check)
                except Exception as ex:
                    print(ex)
                    return
                else:

                    # Making sure that the reply is from the author
                    def check(m):
                        return m.author == payload.member and user_channel.id == instructions.channel.id

                    if str(reaction.emoji) == "✅":
                        self.anon = True

                    if str(reaction.emoji) == "❌":
                        self.anon = False

                    # Delete the old embed
                    await Anon_or_Not.delete()

                    # Tell the user to type their mail into the chat
                    instructions = await user_channel.send(embed=send_instructions(self, member))

                    # Wait for the message from the author
                    msg = await self.bot.wait_for('message', check=check)

                    # Making sure that the message is below 50 characters and the message was sent in the channel
                    while len(msg.content) < 50 and msg.channel == user_channel:
                        await user_channel.send(embed=error_handling(self, member))

                        # Wait for the message from the author
                        msg = await self.bot.wait_for('message', check=check)

                    # As long as the message is above 50 characters and in the correct channel
                    if len(msg.content) > 50 and msg.channel == user_channel:
                        # Delete the previous embed
                        await instructions.delete()

                        # Store all text in the channel in a bytesio object
                        text = ""
                        async for message in user_channel.history(limit=300):
                            text += "".join(f"{message.created_at} : {message.content}\n")
                        text_bytes = str.encode(text)

                        file = io.BytesIO(text_bytes)

                        file_name = "Anon.txt" if self.anon else f"{member.name}.txt"

                        # Send the message to the modmail channel
                        await modmail_channel.send(embed=send_modmail(self, msg, member),
                                                   file=File(file, file_name))

                        # Make sure the user knows that their message has been sent
                        await user_channel.send(embed=message_sent_confirmation(self, member))

                        # Let the user read the message for 5 seconds
                        await asyncio.sleep(5)

                        # Delete the channel and then stop the function
                        await user_channel.delete()

                    # If the user types anywhere else, delete the channel
                    else:
                        await user_channel.delete()

            except Exception as ex:
                print(ex)

                # Send out an error message if the user waited too long
                await user_channel.send(
                    "Sorry! Something seems to have gone wrong and the modmail will be aborting."
                    "\nRemember to make sure it's under **1024** characters!!")

                await asyncio.sleep(5)
                await user_channel.delete()

    @mlsetup.error
    @mlupdate.error
    @mmsetup.error
    @mmupdate.error
    async def mlsetup_command_error(self, ctx, exc):
        """Catching error if channel is not recognised"""

        if isinstance(exc, BadArgument):
            text = "**Channel Not Detected... Aborting Process**"
            await self.bot.generate_embed(ctx, desc=text)


def setup(bot):
    bot.add_cog(Guild(bot))
