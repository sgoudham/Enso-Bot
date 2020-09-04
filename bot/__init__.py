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

import os
import random

import asyncpg as asyncpg
import discord
from decouple import config
from discord import Colour, Embed
from discord.ext import commands, tasks
from discord.ext.commands import when_mentioned_or

from bot.libs.cache import MyCoolCache

# Counter for cycling statuses
counter = 0

# Get DB information from .env
password = config('DB_PASS')
host = config('DB_HOST')
user = config('DB_USER')
port = config('DB_PORT')
db = config('DB_NAME')

# Getting the bot token from environment variables
API_TOKEN = config('DISCORD_TOKEN')


class Bot(commands.Bot):
    def __init__(self, **options):

        async def get_prefix(bot, message):
            """Allow the commands to be used with mentioning the bot"""

            if message.guild is None:
                return "."
            return when_mentioned_or(self.get_prefix_for_guild(message.guild.id))(bot, message)

        super().__init__(command_prefix=get_prefix, case_insensitive=True, **options)
        self.db = None
        self.description = 'All current available commands within Ensō~Chan',
        self.owner_id = 154840866496839680  # Your unique User ID
        self.admin_colour = Colour(0x62167a)  # Admin Embed Colour
        self.version = "0.8.2"  # Version number of Ensō~Chan
        self.remove_command("help")  # Remove default help command

        # Instance variables for Enso
        self.hammyMention = '<@154840866496839680>'
        self.hammy_role_ID = "<@&715412394968350756>"
        self.blank_space = "\u200b"
        self.enso_embedmod_colours = Colour(0x62167a)
        self.enso_ensochancommands_Mention = "<#721449922838134876>"
        self.enso_ensochancommands_ID = 721449922838134876
        self.enso_verification_ID = 728034083678060594
        self.enso_selfroles_ID = 722347423913213992
        self.enso_guild_ID = 663651584399507476
        self.enso_newpeople_ID = 669771571337887765
        self.enso_modmail_ID = 728083016290926623
        self.enso_feedback_ID = 739807803438268427

        # Cross/Tick Emojis
        self.cross = "<:xMark:746834944629932032>"
        self.tick = "<:greenTick:746834932936212570>"

        # Instance variables for cache
        self.enso_cache = {}
        self.modmail_cache = {}
        self.starboard_cache = {}
        self.starboard_messages_cache = {}
        self.member_cache = MyCoolCache(100)

        async def create_connection():
            """Setting up connection using asyncpg"""

            self.db = await asyncpg.create_pool(
                host=host,
                port=int(port),
                user=user,
                password=password,
                database=db,
                loop=self.loop)

        async def startup_cache_log():
            """Store the guilds/modmail systems in cache from the database on startup"""

            # Setup up pool connection
            pool = self.db
            async with pool.acquire() as conn:

                # Query to get all records of guilds that the bot is in
                try:
                    results = await conn.fetch("""SELECT * FROM guilds""")

                    # Store the guilds information within cache
                    for row in results:
                        self.enso_cache[row["guild_id"]] = {"prefix": row["prefix"],
                                                            "modlogs": row["modlogs"],
                                                            "roles_persist": row["roles_persist"]}
                # Catch errors
                except asyncpg.PostgresError as e:
                    print("PostGres Error: Guild Records Could Not Be Loaded Into Cache On Startup", e)

                # Query to get all records of modmails within guilds
                try:
                    results = await conn.fetch("""SELECT * FROM moderatormail""")

                    # Store the information for modmail within cache
                    for row in results:
                        self.modmail_cache[row["guild_id"]] = {"modmail_channel_id": row["modmail_channel_id"],
                                                               "message_id": row["message_id"],
                                                               "modmail_logging_channel_id":
                                                                   row["modmail_logging_channel_id"]}
                # Catch errors
                except asyncpg.PostgresError as e:
                    print("PostGres Error: Modmail Records Could Not Be Loaded Into Cache On Startup", e)

                # Query to get all records of starboards within guilds
                try:
                    results = await conn.fetch("SELECT * FROM starboard")

                    # Store the information for starboard within cache
                    for row in results:
                        self.starboard_cache[row["guild_id"]] = {"channel_id": row["channel_id"],
                                                                 "min_stars": row["min_stars"]}

                # Catch errors
                except asyncpg.PostgresError as e:
                    print("PostGres Error: Starboard Records Could Not Be Loaded Into Cache On Startup", e)

                # Query to get all records of starboard messages within guilds
                try:
                    results = await conn.fetch("SELECT * FROM starboard_messages")

                    for row in results:
                        self.starboard_messages_cache[(row["root_message_id"], row["guild_id"])] = {
                            "star_message_id": row["star_message_id"],
                            "stars": row["stars"]}

                # Catch errors
                except asyncpg.PostgresError as e:
                    print("PostGres Error: Starboard Records Could Not Be Loaded Into Cache On Startup", e)

        # Establish Database Connection
        self.loop.run_until_complete(create_connection())
        # Load Information Into Cache
        self.loop.run_until_complete(startup_cache_log())

        @tasks.loop(minutes=2, reconnect=True)
        async def change_status():
            """Creating custom statuses as background task"""

            global counter
            # Waiting for the bot to ready
            await self.wait_until_ready()

            # Define array of statuses
            looping_statuses = [
                discord.Activity(
                    type=discord.ActivityType.watching,
                    name=f"{len(self.users)} Weebs | {self.version}"),
                discord.Activity(
                    type=discord.ActivityType.watching,
                    name=f"Hamothy | Real Life | {self.version}"),
                discord.Activity(
                    type=discord.ActivityType.watching,
                    name=f"Hamothy Program | {self.version}"),
                discord.Game(name=f".help | {self.version}")
            ]

            # Check if the counter is at the end of the array
            if counter == (len(looping_statuses) - 1):
                # Reset the loop
                counter = 0
            else:
                # Increase the counter
                counter += 1

            # Display the next status in the loop
            await self.change_presence(activity=looping_statuses[counter])

        # Start the background task(s)
        change_status.start()

    # --------------------------------------------!Cache Section!-------------------------------------------------------

    def store_cache(self, guild_id, prefix, modlogs, roles_persist):
        """Storing guild information within cache"""

        self.enso_cache[guild_id] = {"prefix": prefix,
                                     "modlogs": modlogs,
                                     "roles_persist": roles_persist}

    def del_cache(self, guild_id):
        """Deleting the entry of the guild within the cache"""

        del self.enso_cache[guild_id]

    async def check_cache(self, member_id, guild_id):
        """Checks if member is in the member cache"""

        # Return key-value pair if member is already in the cache
        if (member_id, guild_id) in self.member_cache.cache:
            return self.member_cache.cache[member_id, guild_id]

        else:
            # Setup pool connection
            pool = self.db
            async with pool.acquire() as conn:

                # Get the author's/members row from the Members Table
                try:
                    select_query = """SELECT * FROM members WHERE member_id = $1 and guild_id = $2"""
                    result = await conn.fetchrow(select_query, member_id, guild_id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(f"PostGres Error: Member {member_id} From Guild {guild_id}"
                          "Record Could Not Be Retrieved When Checking Cache", e)

                # Store it in cache
                else:
                    dict_items = {"married": result["married"],
                                  "married_date": result["married_date"],
                                  "muted_roles": result["muted_roles"],
                                  "roles": result["roles"]}
                    self.member_cache.store_cache((member_id, guild_id), dict_items)

                    return self.member_cache.cache[member_id, guild_id]

    # --------------------------------------------!End Cache Section!---------------------------------------------------

    # --------------------------------------------!Starboard Section!---------------------------------------------------

    def cache_store_starboard(self, guild_id, channel_id, min_stars):
        """Storing starboard within cache"""

        self.starboard_cache[guild_id] = {"channel_id": channel_id,
                                          "min_stars": min_stars}

    def get_starboard_channel(self, guild_id):
        """Returning the starboard channel of the guild"""

        starboard = self.starboard_cache.get(guild_id)
        return starboard.get("channel_id") if starboard else None

    def get_starboard_min_stars(self, guild_id):
        """Returning the starboard minimum stars of the guild"""

        starboard = self.starboard_cache.get(guild_id)
        return starboard.get("min_stars") if starboard else None

    def update_starboard_channel(self, guild_id, channel_id):
        """Update the starboard channel"""

        self.starboard_cache[guild_id]["channel_id"] = channel_id

    def update_starboard_min_stars(self, guild_id, min_stars):
        """Update the starboard minimum stars"""

        self.starboard_cache[guild_id]["min_stars"] = min_stars

    def delete_starboard(self, guild_id):
        """Deleting the starboard of the guild"""

        del self.starboard_cache[guild_id]

    def delete_starboard_messages(self, in_guild_id):

        # Array to store keys to be removed
        keys_to_remove = []

        # For every starboard message in cache
        for (root_msg_id, guild_id) in self.starboard_messages_cache:
            # if the guild_id passed in is equal to the guild_id within the cache
            if in_guild_id == guild_id:
                # Store key within array
                keys_to_remove.append((root_msg_id, guild_id))

        # Iterate through the array and then pop the keys from cache
        for key in keys_to_remove:
            self.starboard_messages_cache.pop(key)

    def cache_store_starboard_message(self, root_message_id, guild_id, star_message_id):
        """Store the starboard messages within cache"""

        self.starboard_messages_cache[root_message_id, guild_id] = {"star_message_id": star_message_id,
                                                                    "stars": 1}

    def update_starboard_message_id(self, root_message_id, guild_id, star_message_id):
        """Update the stored starboard message"""

        self.starboard_messages_cache[root_message_id, guild_id]["star_message_id"] = star_message_id

    def del_starboard_star_message_id(self, root_message_id, guild_id):
        """Set the star message id to None"""

        self.starboard_messages_cache[root_message_id, guild_id]["star_message_id"] = None

    def update_starboard_message_stars(self, root_message_id, guild_id, reactions):
        """Update the stored starboard message"""

        self.starboard_messages_cache[root_message_id, guild_id]["stars"] = reactions

    def check_root_message_id(self, root_message_id, guild_id):
        """Check if the original message is stored within the cache"""

        # Return value if message is already in the cache
        if (root_message_id, guild_id) in self.starboard_messages_cache:
            return True
        else:
            return False

    async def check_starboard_messages_cache(self, root_message_id, guild_id):
        """Check if the message is already in the cache"""

        # Return value if message is already in the cache
        if (root_message_id, guild_id) in self.starboard_messages_cache:
            return self.starboard_messages_cache[root_message_id, guild_id]["star_message_id"], \
                   self.starboard_messages_cache[root_message_id, guild_id]["stars"]

        else:
            # Setup pool connection
            pool = self.db
            async with pool.acquire() as conn:

                # Get the starboard row from the starboard_messages table
                try:
                    select_query = """SELECT * FROM starboard_messages WHERE root_message_id = $1 AND guild_id = $2"""
                    result = await conn.fetchrow(select_query, root_message_id, guild_id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(e)

                # Store it in cache
                else:
                    if result:
                        self.starboard_messages_cache[root_message_id, guild_id] = {
                            "star_message_id": result["star_message_id"],
                            "stars": result["stars"]}

                        return self.starboard_messages_cache[root_message_id, guild_id]["star_message_id"], \
                               self.starboard_messages_cache[root_message_id, guild_id]["stars"]
                    else:
                        return None, 0

    # --------------------------------------------!EndStarboard Section!-------------------------------------------------

    # --------------------------------------------!Modmail Section!-----------------------------------------------------

    def cache_store_modmail(self, guild_id, modmail_channel, message, modmail_logging_channel):
        """Storing all modmail channels within cache"""

        self.modmail_cache[guild_id] = {"modmail_channel_id": modmail_channel,
                                        "message_id": message,
                                        "modmail_logging_channel_id": modmail_logging_channel}

    def get_modmail(self, guild_id):
        """Returning the modmail system of the guild"""

        return self.modmail_cache.get(guild_id)

    def update_modmail(self, guild_id, channel_id):
        """Update the modmail channel"""

        self.modmail_cache[guild_id]["modmail_logging_channel_id"] = channel_id

    def delete_modmail(self, guild_id):
        """Deleting the modmail system of the guild within the Cache"""

        del self.modmail_cache[guild_id]

    # --------------------------------------------!EndModmail Section!--------------------------------------------------

    # --------------------------------------------!RolePersist Section!-------------------------------------------------

    def get_roles_persist(self, guild_id):
        """Returning rolespersist value of the guild"""

        role_persist = self.enso_cache.get(guild_id)
        return role_persist.get("roles_persist") if role_persist else None

    async def update_role_persist(self, guild_id, value):
        """Update the rolepersist value of the guild (Enabled or Disabled)"""

        # Setup up pool connection
        pool = self.db
        async with pool.acquire() as conn:

            # Query for updating rolepersist values For guilds
            try:
                update_query = """UPDATE guilds SET roles_persist = $1 WHERE guild_id = $2"""
                await conn.execute(update_query, value, guild_id)

            # Catch error
            except asyncpg.PostgresError as e:
                print(f"PostGres Error: RolePersist For Guild {guild_id} Could Not Be Updated", e)

            # Store in cache
            else:
                self.enso_cache[guild_id]["roles_persist"] = value

    # --------------------------------------------!End RolePersist Section!---------------------------------------------

    # --------------------------------------------!ModLogs Section!-----------------------------------------------------

    async def storage_modlog_for_guild(self, ctx, channel_id, setup):
        """Updating the modlog within the dict and database"""

        # Setup up pool connection
        pool = self.db
        async with pool.acquire() as conn:

            # Query to update modlogs within the database
            try:
                update_query = """UPDATE guilds SET modlogs = $1 WHERE guild_id = $2"""
                rowcount = await conn.execute(update_query, channel_id, ctx.guild.id)

            # Catch errors
            except asyncpg.PostgresError as e:
                print("PostGres Error: Modlogs Value In Guilds Table Could Not Be Updated/Setup", e)

            # Let the user know that modlogs channel has been updated/setup
            else:
                if setup:
                    print(rowcount, f"Modlog channel for guild {ctx.guild} has been Setup")
                    await self.generate_embed(ctx, desc=f"**Modlogs Channel** successfully setup in <#{channel_id}>" +
                                                        f"\nPlease refer to **{ctx.prefix}help** for any information")
                else:
                    print(rowcount, f"Modlog channel for guild {ctx.guild} has been Updated")
                    await self.generate_embed(ctx,
                                              desc=f"Modlog Channel for **{ctx.guild}** has been updated to <#{channel_id}>")

                # Store in cache
                self.enso_cache[ctx.guild.id]["modlogs"] = channel_id

    def remove_modlog_channel(self, guild_id):
        """Remove the value of modlog for the guild specified"""

        self.enso_cache[guild_id]["modlogs"] = None

    def get_modlog_for_guild(self, guild_id):
        """Get the modlog channel of the guild that the user is in"""

        modlogs = self.enso_cache.get(guild_id)
        return modlogs.get("modlogs") if modlogs else None

    # --------------------------------------------!End ModLogs Section!-------------------------------------------------

    # --------------------------------------------!Prefixes Section!----------------------------------------------------

    async def storage_prefix_for_guild(self, ctx, prefix):
        """Updating the prefix within the dict and database when the method is called"""

        # Setup up pool connection
        pool = self.db
        async with pool.acquire() as conn:

            # Query to update the existing prefix within the database
            try:
                update_query = """UPDATE guilds SET prefix = $1 WHERE guild_id = $2"""
                rowcount = await conn.execute(update_query, prefix, ctx.guild.id)

            # Catch errors
            except asyncpg.PostgresError as e:
                print(f"PostGres Error: Prefix For Guild {ctx.guild.id} Could Not Be Updated", e)

            # Let the user know that the guild prefix has been updated
            else:
                print(rowcount, f"Guild prefix has been updated for guild {ctx.guild}")
                await self.generate_embed(ctx, desc=f"Guild prefix has been updated to **{prefix}**")

                # Store in cache
                self.enso_cache[ctx.guild.id]["prefix"] = prefix

    def get_prefix_for_guild(self, guild_id):
        """Get the prefix of the guild that the user is in"""

        prefix = self.enso_cache[guild_id]["prefix"]
        if prefix:
            return prefix
        return "."

    # --------------------------------------------!End Prefixes Section!------------------------------------------------

    # --------------------------------------------!Roles/Colour/Embed Section!------------------------------------------

    @staticmethod
    def random_colour():
        """Generate a random hex colour"""

        return Colour(random.randint(0, 0xFFFFFF))

    async def generate_embed(self, ctx, desc):
        """Generate embed"""

        embed = Embed(description=desc,
                      colour=self.admin_colour)

        await ctx.send(embed=embed)

    async def store_roles(self, target, ctx, member):
        """Storing user roles within database"""

        role_ids = ", ".join([str(r.id) for r in target.roles])

        # Setup up pool connection
        pool = self.db
        async with pool.acquire() as conn:

            # Query to store existing roles of the member within the database
            try:
                update_query = """UPDATE members SET muted_roles = $1 WHERE guild_id = $2 AND member_id = $3"""
                rowcount = await conn.execute(update_query, role_ids, ctx.guild.id, member.id)
                result = await self.check_cache(member.id, member.guild.id)

            # Catch errors
            except asyncpg.PostgresError as e:
                print(f"PostGres Error: Roles Could Not Be Stored For Member {member.id} in Guild {member.guild.id}", e)

            # Print success
            # Update cache
            else:
                result["muted_roles"] = role_ids
                print(rowcount, f"Roles Added For User {member} in {ctx.guild}")

    async def clear_roles(self, member):
        """Clear the roles when the user has been unmuted"""

        # Setup up pool connection
        pool = self.db
        async with pool.acquire() as conn:

            # Query to clear the existing role of the member from the database
            try:
                update = """UPDATE members SET muted_roles = NULL WHERE guild_id = $1 AND member_id = $2"""
                rowcount = await conn.execute(update, member.guild.id, member.id)
                result = await self.check_cache(member.id, member.guild.id)

            # Catch error
            except asyncpg.PostgresError as e:
                print(f"PostGres Error: Roles Could Not Be Cleared for Member {member.id} in Guild {member.guild.id}",
                      e)

            # Print success
            # Update cache
            else:
                result["muted_roles"] = None
                print(rowcount, f"Roles Cleared For User {member} in {member.guild.name}")

    # --------------------------------------------!End Roles/Colour/Embed Section!--------------------------------------

    def execute(self):
        """Load the cogs and then run the bot"""

        for file in os.listdir(f'.{os.sep}cogs'):
            if file.endswith('.py'):
                self.load_extension(f"cogs.{file[:-3]}")

        # Run the bot, allowing it to come online
        try:
            self.run(API_TOKEN)
        except discord.errors.LoginFailure as e:
            print(e, "Login unsuccessful.")
