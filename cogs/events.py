import datetime

import asyncpg
from discord import Embed
from discord.ext.commands import Cog


class Events(Cog):
    """Handling all global events"""

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        """Make sure bot messages are not tracked"""

        # Ignoring messages that start with 2 ..
        if message.content.startswith("..") or message.author.bot:
            return

        # Processing the message
        await self.bot.bot.process_commands(message)

    @Cog.listener()
    async def on_ready(self):
        """Display startup message"""

        print("UvU Senpaiii I'm ready\n")

    @Cog.listener()
    async def on_guild_join(self, guild):
        """
        Store users in a database
        Store prefix/modlogs in the cache
        """

        # Store every single record into an array
        records = [(member.id, None, None, guild.id, None, None, None, 0) for member in guild.members]

        # Setup up pool connection
        pool = self.bot.db
        async with pool.acquire() as conn:

            # Insert the guild information into guilds table
            try:
                insert = """INSERT INTO guilds VALUES ($1, $2, $3, $4) ON CONFLICT (guild_id) DO NOTHING"""
                rowcount = await conn.execute(insert, guild.id, ".", None, 0)

            # Catch errors
            except asyncpg.PostgresError as e:
                print(f"PostGres Error: Guild {guild.id} Could Not Be Inserted Into Guilds Table", e)

            # Print success
            else:
                print(rowcount, f"Record(s) inserted successfully into {guild}")
                self.bot.store_cache(guild.id, modlogs=None, prefix=".", roles_persist=0)

            # Query to insert all the member details to members table
            try:
                rowcount = await conn.copy_records_to_table("members", records=records)

            # Catch errors
            except asyncpg.PostgresError as e:
                print(f"PostGres Error: Members Could Not Be Inserted Into Members Table For Guild {guild.id}", e)

            # Store in cache
            else:
                print(rowcount, f"Record(s) inserted successfully into Members from {guild}")

    @Cog.listener()
    async def on_guild_remove(self, guild):
        """
        Remove users in the database for the guild
        Remove the modlogs/guild from the cache
        """

        # Setup pool connection
        pool = self.bot.db
        async with pool.acquire() as conn:

            # Delete the guild information as the bot leaves the server
            try:
                delete = """DELETE FROM guilds WHERE guild_id = $1"""
                rowcount = await conn.execute(delete, guild.id)

            # Catch errors
            except asyncpg.PostgresError as e:
                print(f"PostGres Error: On Guild Remove Event Record Was Not Deleted For {guild.id}", e)

            # Delete the key - value pair for the guild
            else:
                print(rowcount, f"Record deleted successfully from Guild {guild}")
                self.bot.del_cache(guild.id)

            # Delete all records of members from that guild
            try:
                delete = """DELETE FROM members WHERE guild_id = $1"""
                rowcount = await conn.execute(delete, guild.id)

            # Catch errors
            except asyncpg.PostgresError as e:
                print(f"PostGres Error: All Members Could Not Be Deleted From {guild.id}", e)

            # Print success
            else:
                print(rowcount, f"Record(s) deleted successfully from Members from {guild}")
                # Remove any/all members stored in cache from that guild
                self.bot.member_cache.remove_many(guild.id)

            # Delete any starboard information upon leaving the guild
            try:
                delete = """DELETE FROM starboard WHERE guild_id = $1"""
                rowcount = await conn.execute(delete, guild.id)

            # Catch errors
            except asyncpg.PostgresError as e:
                print(
                    f"PostGres Error: On Guild Remove Event Starboard/Starboard Messages Were Not Deleted For {guild.id}",
                    e)

            # Delete all information about the starboard and any messages stored
            else:
                print(rowcount, f"Starboard deleted successfully from Guild {guild}")
                if self.bot.get_starboard_channel(guild.id):
                    self.bot.delete_starboard(guild.id)
                    self.bot.delete_starboard_messages(guild.id)

    @Cog.listener()
    async def on_member_join(self, member):
        """
        Bot event to insert new members into the database
        In the Enso guild, it will send an introduction embed
        """

        # Ignoring bots
        if member.bot: return

        # Get the guild and role persist value of the guild
        guild = member.guild
        role_persist = self.bot.get_roles_persist(guild.id)

        # Setup pool connection
        pool = self.bot.db
        async with pool.acquire() as conn:

            # Define the insert statement that will insert the user's information
            # On conflict, set the left values to null
            try:

                insert = """INSERT INTO members (guild_id, member_id) VALUES ($1, $2)
                ON CONFLICT (guild_id, member_id) DO UPDATE SET left_at = NULL, has_left = 0"""
                rowcount = await conn.execute(insert, member.guild.id, member.id)

            # Catch errors
            except asyncpg.PostgresError as e:
                print(
                    f"PostGres Error: {member} | {member.id} was not be able to be added to {member.guild} | {member.guild.id}",
                    e)

            # Print success
            else:
                print(rowcount, f"{member} Joined {member.guild}, Record Inserted Into Members")
                print(rowcount, f"Roles Cleared For {member} in {member.guild}")

            # Get the roles of the user from the database
            try:
                select_query = """SELECT * FROM members WHERE guild_id = $1 AND member_id = $2"""

                user_joined = await conn.fetchrow(select_query, member.guild.id, member.id)
                role_ids = user_joined["roles"]

            # Catch errors
            except asyncpg.PostgresError as e:
                print(f"PostGres Error: {member} | {member.id} Record Not Found", e)

            # Give roles back to the user if role persist is enabled
            else:
                if role_persist == 1:
                    # Get Enso Chan
                    bot = guild.get_member(self.bot.user.id)
                    # Set flag for what value role_ids is
                    flag = role_ids

                    # Check permissions of Enso
                    if bot.guild_permissions.manage_roles and flag:
                        # Get all the roles of the user before they were muted from the database
                        roles = [member.guild.get_role(int(id_)) for id_ in role_ids.split(", ") if len(id_)]

                        # Give the member their roles back
                        await member.edit(roles=roles)
                        print(f"{member} Had Their Roles Given Back In {member.guild}")

                    # Don't give roles if user has no roles to be given
                    elif bot.guild_permissions.manage_roles and not flag:
                        print(f"Member {member} | {member.id} Had No Roles To Be Given")

                    # No permissions to give roles in the server
                    else:
                        print(
                            f"Insufficient Permissions to Add Roles to {member} | {member.id} in {member.guild} | {member.guild.id}")

            # Reset the roles entry for the database
            try:
                update_query = """UPDATE members SET roles = NULL WHERE guild_id = $1 AND member_id = $2"""
                rowcount = await conn.execute(update_query, member.guild.id, member.id)

            # Catch errors
            except asyncpg.PostgresError as e:
                print(f"PostGres Error: Clearing Member {member.id} Roles in Guild {member.guild.id}", e)

            # Print success
            # Update cache
            else:
                print(rowcount, f"Roles Cleared For {member} in {member.guild}")

        # Make sure the guild is Enso and send welcoming embed to the server
        if guild.id == self.bot.enso_guild_ID:
            new_people = guild.get_channel(self.bot.enso_newpeople_ID)

            server_icon = guild.icon_url
            welcome_gif = "https://cdn.discordapp.com/attachments/669808733337157662/730186321913446521/NewPeople.gif"

            embed = Embed(title="\n**Welcome To Ensō!**",
                          colour=self.bot.admin_colour,
                          timestamp=datetime.datetime.utcnow())

            embed.set_thumbnail(url=server_icon)
            embed.set_image(url=welcome_gif)
            embed.add_field(
                name=self.bot.blank_space,
                value=f"Hello {member.mention}! We hope you enjoy your stay in this server!",
                inline=False)
            embed.add_field(
                name=self.bot.blank_space,
                value=f"Be sure to check out our <#669815048658747392> channel to read the rules and <#683490529862090814> channel to get caught up with any changes! ",
                inline=False)
            embed.add_field(
                name=self.bot.blank_space,
                value=f"Last but not least, feel free to go into <#669775971297132556> to introduce yourself!",
                inline=False)

            # Send embed to #newpeople
            await new_people.send(embed=embed)

    @Cog.listener()
    async def on_member_remove(self, member):
        """Storing member roles within the database when the member leaves"""

        # Ignoring bots
        if member.bot: return

        # Get the datetime of when the user left the guild
        left_at = datetime.datetime.utcnow()

        # Store member roles within a string to insert into database
        role_ids = ", ".join([str(r.id) for r in member.roles if not r.managed])

        # Setup pool connection
        pool = self.bot.db
        async with pool.acquire() as conn:

            # Store member roles within the database
            try:
                update = """UPDATE members SET roles = $1, left_at = $2, has_left = 1
                                  WHERE guild_id = $3 AND member_id = $4"""
                rowcount = await conn.execute(update, role_ids, left_at, member.guild.id, member.id)

            # Catch Error
            except asyncpg.PostgresError as e:
                print(f"PostGres Error: Roles Could Not Be Added To {member} When Leaving {member.guild.id}", e)

            # Print success
            else:
                print(rowcount, f"{member} Left {member.guild.name}, Roles stored into Members")

    @Cog.listener()
    async def on_guild_channel_delete(self, channel):
        """Deleting modlogs/modmail channel if it's deleted in the guild"""

        # Get the modlogs channel (channel or none)
        modlogs = self.bot.get_modlog_for_guild(channel.guild.id)
        # Get the starboard (record or none)
        starboard = self.bot.get_starboard_channel(channel.guild.id)

        # Get the modmail record - (normal and logging channels)
        modmail_record = self.bot.get_modmail(channel.guild.id)
        modmail_channel = modmail_record.get("modmail_channel_id") if modmail_record else None
        modmail_logging_channel = modmail_record.get("modmail_logging_channel_id") if modmail_record else None

        # Get pool
        pool = self.bot.db

        # Delete the modlogs system from the database when modlogs channel is deleted
        if channel.id == modlogs:
            # Setup pool connection
            async with pool.acquire() as conn:

                # Set channel to none
                try:
                    update = """UPDATE guilds SET modlogs = NULL WHERE guild_id = $1"""
                    await conn.execute(update, channel.guild.id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(f"PostGres Error: Guild Modlogs Could Not Be Deleted For {channel.guild.id}", e)

                # Delete channel from cache
                else:
                    self.bot.remove_modlog_channel(channel.guild.id)

        # Delete all of the starboard information when the channel is deleted from the guild
        if channel.id == starboard:
            # Setup pool connection
            async with pool.acquire() as conn:

                # Delete any starboard information upon leaving the guild
                try:
                    delete = """DELETE FROM starboard WHERE guild_id = $1"""
                    rowcount = await conn.execute(delete, channel.guild.id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(
                        f"PostGres Error: On Guild Remove Event Starboard/Starboard Messages Were Not Deleted For {channel.guild.id}",
                        e)

                # Delete all information about the starboard and any messages stored
                else:
                    print(rowcount, f"Starboard deleted successfully from Guild {channel.guild}")
                    self.bot.delete_starboard(channel.guild.id)
                    self.bot.delete_starboard_messages(channel.guild.id)

        # If modmail channels are deleted, delete the entire system
        if channel.id == modmail_channel or channel.id == modmail_logging_channel:
            # Set up pool connection
            async with pool.acquire() as conn:

                # Remove the moderatormail record from the database
                try:
                    delete = """DELETE FROM moderatormail WHERE guild_id = $1"""
                    await conn.execute(delete, channel.guild.id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(f"PostGres Error: ModeratorMail Record Could Not Be Deleted for Guild {channel.guild.id}", e)

                # Delete from cache
                else:
                    self.bot.delete_modmail(channel.guild.id)


def setup(bot):
    bot.add_cog(Events(bot))
