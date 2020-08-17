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
import datetime
import random

import aiohttp
import aiomysql
import discord
from decouple import config
from discord import Colour, Embed
from discord.ext import commands, tasks
from discord.ext.commands import when_mentioned_or

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

counter = 0

# Get DB information from .env
password = config('DB_PASS')
host = config('DB_HOST')
user = config('DB_USER')
port = config('DB_PORT')
db = config('DB_NAME')
disc_bots_gg_auth = config('DISCORD_BOTS_BOTS_AUTH')

# Getting the Bot token from Environment Variables
API_TOKEN = config('DISCORD_TOKEN')


class Bot(commands.Bot):
    def __init__(self, **options):

        async def get_prefix(bot, message):
            """Allow the commands to be used with mentioning the bot"""
            if message.guild is None:
                return "~"
            return when_mentioned_or(self.get_prefix_for_guild(str(message.guild.id)))(bot, message)

        super().__init__(command_prefix=get_prefix, **options)
        self.db = None
        self.description = 'All current available commands within Ensō~Chan',  # Set a description for the bot
        self.owner_id = 154840866496839680,  # Your unique User ID
        self.case_insensitive = True  # Commands are now Case Insensitive
        self.admin_colour = Colour(0x62167a)  # Admin Embed Colour
        self.version = "v0.7.2"  # Version number of Ensō~Chan
        self.remove_command("help")  # Remove default help command

        # Define variables that are for Enso only
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

        self.enso_cache = {}

        async def create_connection():
            """Setting up connection using pool/aiomysql"""

            self.db = await aiomysql.create_pool(
                host=host,
                port=int(port),
                user=user,
                password=password,
                db=db,
                loop=self.loop)

        async def startup_cache_log():
            """Store the modlogs/prefixes in cache from the database on startup"""

            # Setup pool
            pool = self.db

            # Setup up pool connection and cursor
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    # Grab the prefix of the server from the database
                    select_query = """SELECT * FROM guilds"""

                    # Execute the query
                    await cur.execute(select_query)
                    results = await cur.fetchall()

                    # Store the guildID's, modlog channels and prefixes within cache
                    for row in results:
                        self.enso_cache[row[0]] = {"Prefix": row[1], "Modlogs": row[2], "RolesPersist": row[3]}

        # Make sure the connection is setup before the bot is ready
        self.loop.run_until_complete(create_connection())
        self.loop.run_until_complete(startup_cache_log())

        async def post_bot_stats():
            """Method To Update Guild Count On discord.bots.gg"""

            async with aiohttp.ClientSession() as session:
                await session.post(f"https://discord.bots.gg/api/v1/bots/{self.user.id}/stats",
                                   data={"guildCount": {len(self.guilds)},
                                         "Content-Type": "application/json"},
                                   headers={'Authorization': disc_bots_gg_auth})
                await session.close()

        @tasks.loop(minutes=10, reconnect=True)
        async def change_status():
            """Creating Custom Statuses as a Background Task"""

            global counter
            # Waiting for the bot to ready
            await self.wait_until_ready()

            # Update Guild Count on discord.bots.gg
            await post_bot_stats()

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
                discord.Game(name=f"~help | {self.version}")
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

    def store_cache(self, guildid, prefix, channel, rolespersist):
        """Storing GuildID, Modlogs Channel and Prefix in Cache"""

        self.enso_cache[guildid] = {"Prefix": prefix, "Modlogs": channel, "RolesPersist": rolespersist}

    def del_cache(self, guildid):
        """Deleting the entry of the guild within the cache"""

        del self.enso_cache[guildid]

    # --------------------------------------------!End Cache Section!---------------------------------------------------

    # --------------------------------------------!RolePersist Section!-------------------------------------------------

    def get_roles_persist(self, guildid):
        """Returning rolespersist value of the guild"""

        return self.enso_cache[guildid]["RolesPersist"]

    async def update_role_persist(self, guildid, value, pool):
        """Update the rolepersist value of the guild (Enabled or Disabled)"""

        self.enso_cache[guildid]["RolesPersist"] = value

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Update the existing prefix within the database
                update_query = """UPDATE guilds SET rolespersist = (%s) WHERE guildID = (%s)"""
                update_vals = value, guildid,

                # Execute the query
                await cur.execute(update_query, update_vals)
                await conn.commit()

    # --------------------------------------------!End RolePersist Section!---------------------------------------------

    # --------------------------------------------!ModLogs Section!-----------------------------------------------------

    async def storage_modlog_for_guild(self, pool, ctx, channelID, setup):
        """Updating the modlog within the dict and database"""

        self.enso_cache[str(ctx.guild.id)]["Modlogs"] = channelID

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Update the existing modlogs channel within the database
                update_query = """UPDATE guilds SET modlogs = (%s) WHERE guildID = (%s)"""
                update_vals = channelID, ctx.guild.id,

                # Execute the query
                await cur.execute(update_query, update_vals)
                await conn.commit()

        # Send custom confirmation messages to log based on the command update or setup
        if setup:
            print(cur.rowcount, f"Modlog channel for guild {ctx.guild.name} has been Setup")
        else:
            print(cur.rowcount, f"Modlog channel for guild {ctx.guild.name} has been Updated")

        if setup:
            # Send confirmation that modmail channel has been setup
            await ctx.send(f"**Modlogs Channel** successfully setup in <#{channelID}>" +
                           f"\nPlease refer to **{ctx.prefix}help** for any information")
        else:
            # Let the user know that the guild modlogs channel has been updated
            channel = ctx.guild.get_channel(channelID)
            await self.generate_embed(ctx,
                                      desc=f"Modlog Channel for **{ctx.guild.name}** has been updated to {channel.mention}")

    def remove_modlog_channel(self, guildid):
        """Remove the value of modlog for the guild specified"""

        self.enso_cache[guildid]["Modlogs"] = None

    def get_modlog_for_guild(self, guildid):
        """Get the modlog channel of the guild that the user is in"""

        channel = self.enso_cache[guildid]["Modlogs"]
        return channel

    # --------------------------------------------!End ModLogs Section!-------------------------------------------------

    # --------------------------------------------!Prefixes Section!----------------------------------------------------

    async def storage_prefix_for_guild(self, pool, ctx, prefix):
        """Updating the prefix within the dict and database when the method is called"""

        self.enso_cache[str(ctx.guild.id)]["Prefix"] = prefix

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Update the existing prefix within the database
                update_query = """UPDATE guilds SET prefix = (%s) WHERE guildID = (%s)"""
                update_vals = prefix, ctx.guild.id,

                # Execute the query
                await cur.execute(update_query, update_vals)
                await conn.commit()
                print(cur.rowcount, f"Guild prefix has been updated for guild {ctx.guild.name}")

                # Let the user know that the guild prefix has been updated
                await self.generate_embed(ctx, desc=f"**Guild prefix has been updated to `{prefix}`**")

    def get_prefix_for_guild(self, guildid):
        """Get the prefix of the guild that the user is in"""

        prefix = self.enso_cache[guildid]["Prefix"]
        if prefix is not None:
            return prefix
        return "~"

    # --------------------------------------------!End Prefixes Section!------------------------------------------------

    # --------------------------------------------!Roles/Colour/Embed Section!------------------------------------------

    @staticmethod
    def random_colour():
        """Generate a random hex colour"""

        return Colour(random.randint(0, 0xFFFFFF))

    async def generate_embed(self, ctx, desc):
        """Generate Embed"""

        embed = Embed(description=desc,
                      colour=self.admin_colour)

        await ctx.send(embed=embed)

    async def storeRoles(self, target, ctx, member):
        """Storing User Roles within Database"""

        pool = self.db

        role_ids = ", ".join([str(r.id) for r in target.roles])

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Store the existing roles of the user within the database
                update_query = """UPDATE members SET mutedroles = (%s) WHERE guildID = (%s) AND discordID = (%s)"""
                update_vals = role_ids, ctx.guild.id, member.id

                # Execute the query
                await cur.execute(update_query, update_vals)
                await conn.commit()
                print(cur.rowcount, f"Roles Added For User {member} in {ctx.guild.name}")

    async def clearRoles(self, member):
        """Clear the roles when the user has been unmuted"""

        pool = self.db

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Clear the existing roles of the user from the database
                update_query = """UPDATE members SET mutedroles = NULL WHERE guildID = (%s) AND discordID = (%s)"""
                update_vals = member.guild.id, member.id

                # Execute the query
                await cur.execute(update_query, update_vals)
                await conn.commit()
                print(cur.rowcount, f"Roles Cleared For User {member} in {member.guild.name}")

    # --------------------------------------------!End Roles/Colour/Embed Section!--------------------------------------

    # --------------------------------------------!Events Section!------------------------------------------------------

    async def on_message(self, message):
        """Make sure bot messages are not tracked"""

        if message.author.bot:
            return
        # Processing the message
        await self.process_commands(message)

    @staticmethod
    async def on_ready():
        """Displaying if Bot is Ready"""
        print("UvU Senpaiii I'm ready\n")

    async def on_guild_join(self, guild):
        """
        Store users in a database
        Store prefix/modlogs in the cache
        """

        # Store guildID, modlogs channel and prefix to cache
        self.store_cache(str(guild.id), channel=None, prefix="~", rolespersist=0)

        # Setup pool
        pool = self.db

        # Grabbing the values to be inserted
        records = ", ".join(map(lambda m: f"({guild.id}, {m.id})", guild.members))

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Define the insert statement for inserting the guild into the guilds table
                insert_query = """INSERT INTO guilds (guildID) VALUES (%s) ON DUPLICATE KEY UPDATE guildID = VALUES(guildID)"""
                val = guild.id,

                # Execute the query
                await cur.execute(insert_query, val)
                await conn.commit()
                print(cur.rowcount, f"Record(s) inserted successfully into Guilds from {guild.name}")

            async with conn.cursor() as cur:
                # Define the insert statement that will insert the user's information
                insert = """INSERT INTO members (guildID, discordID) VALUES {}
                         ON DUPLICATE KEY UPDATE guildID = VALUES(guildID), discordID = VALUES(discordID)""".format(
                    records)

                # Execute the query
                await cur.execute(insert)
                await conn.commit()
                print(cur.rowcount, f"Record(s) inserted successfully into Members from {guild.name}")

    async def on_guild_remove(self, guild):
        """
        Remove users in the database for the guild
        Remove the modlogs/guild from the cache
        """
        # Delete the key - value pairs for the guild
        self.del_cache(str(guild.id))

        # Setup pool
        pool = self.db

        # Setup pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Delete the guild and prefix information as the bot leaves the server
                delete_query = """DELETE FROM guilds WHERE guildID = %s"""
                val = guild.id,

                # Execute the query
                await cur.execute(delete_query, val)
                await conn.commit()
                print(cur.rowcount, f"Record deleted successfully from Guild {guild.name}")

            async with conn.cursor() as cur:
                # Delete the record of the member as the bot leaves the server
                delete_query = """DELETE FROM members WHERE guildID = %s"""
                vals = guild.id,

                # Execute the query
                await cur.execute(delete_query, vals)
                await conn.commit()
                print(cur.rowcount, f"Record(s) deleted successfully from Members from {guild.name}")

    async def on_member_join(self, member):
        """
        Bot event to insert new members into the database
        In the Enso guild, it will send an introduction embed
        """

        # Get the guild
        guild = member.guild

        # Setup pool
        pool = self.db

        role_persist = self.get_roles_persist(str(guild.id))

        # Setup pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Define the insert statement that will insert the user's information
                insert_query = """INSERT INTO members (guildID, discordID) VALUES (%s, %s) 
                ON DUPLICATE KEY UPDATE guildID = VALUES(guildID), discordID = VALUES(discordID)"""
                vals = member.guild.id, member.id,

                # Execute the SQL Query
                await cur.execute(insert_query, vals)
                await conn.commit()
                print(cur.rowcount, f"{member} Joined {member.guild.name}, Record Inserted Into Members")

            async with conn.cursor() as cur:
                # Get the roles of the user from the database
                select_query = """SELECT * FROM members WHERE guildID = (%s) AND discordID = (%s)"""
                vals = member.guild.id, member.id,

                # Execute the SQL Query
                await cur.execute(select_query, vals)
                result = await cur.fetchone()
                role_ids = result[5]

                if role_persist == 1:
                    # Get Enso Chan
                    bot = guild.get_member(self.user.id)

                    # Check permissions of Enso
                    if bot.guild_permissions.manage_roles and role_ids is not None:
                        # Get all the roles of the user before they were muted from the database
                        roles = [member.guild.get_role(int(id_)) for id_ in role_ids.split(", ") if len(id_)]

                        # Give the member their roles back
                        await member.edit(roles=roles)
                        print(f"{member} Had Their Roles Given Back In {member.guild.name}")

                    else:
                        print(f"Insufficient Permissions to Add Roles to {member} in {member.guild.name}")

                # Reset the roles entry for the database
                update_query = """UPDATE members SET roles = NULL WHERE guildID = (%s) AND discordID = (%s)"""
                update_vals = member.guild.id, member.id,

                # Execute the query
                await cur.execute(update_query, update_vals)
                await conn.commit()
                print(cur.rowcount, f"Roles Cleared For {member} in {member.guild.name}")

            # Make sure the guild is Enso
            if guild.id == self.enso_guild_ID:
                # Set the channel id to "newpeople"
                new_people = guild.get_channel(self.enso_newpeople_ID)

                # Set the enso server icon and the welcoming gif
                server_icon = guild.icon_url
                welcome_gif = "https://cdn.discordapp.com/attachments/669808733337157662/730186321913446521/NewPeople.gif"

                # Set up embed for the #newpeople channel
                embed = Embed(title="\n**Welcome To Ensō!**",
                              colour=self.admin_colour,
                              timestamp=datetime.datetime.utcnow())

                embed.set_thumbnail(url=server_icon)
                embed.set_image(url=welcome_gif)
                embed.add_field(
                    name=self.blank_space,
                    value=f"Hello {member.mention}! We hope you enjoy your stay in this server! ",
                    inline=False)
                embed.add_field(
                    name=self.blank_space,
                    value=f"Be sure to check out our <#669815048658747392> channel to read the rules and <#683490529862090814> channel to get caught up with any changes! ",
                    inline=False)
                embed.add_field(
                    name=self.blank_space,
                    value=f"Last but not least, feel free to go into <#669775971297132556> to introduce yourself!",
                    inline=False)

                # Send embed to #newpeople
                await new_people.send(embed=embed)

    async def on_member_remove(self, member):
        """Storing User Roles within Database When User Leaves Guild"""
        role_ids = ", ".join([str(r.id) for r in member.roles if not r.managed])

        # Setup pool
        pool = self.db

        # Setup pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Define the insert statement that will insert the user's information
                update_query = """UPDATE members SET roles = (%s) WHERE guildID = (%s) AND discordID = (%s)"""
                vals = role_ids, member.guild.id, member.id,

                # Execute the SQL Query
                await cur.execute(update_query, vals)
                await conn.commit()
                print(cur.rowcount, f"{member} Left {member.guild.name}, Roles stored into Members")

        # --------------------------------------------!End Events Section!----------------------------------------------

    def run_bot(self):

        # Run the bot, allowing it to come online
        try:
            self.run(API_TOKEN)
        except discord.errors.LoginFailure as e:
            print(e, "Login unsuccessful.")

    # Returns a list of all the cogs
    def extensions(self):
        ext = ['cogs.interactive', 'cogs.anime', 'cogs.relationship',
               'cogs.help', 'cogs.info', 'cogs.guild', 'cogs.fun', "cogs.error",
               'cogs.enso', 'cogs.owner', 'cogs.moderation']

        return ext
