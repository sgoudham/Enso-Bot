import asyncio
import datetime
from contextlib import closing
from itertools import cycle
from typing import Optional

import discord
import mariadb
from decouple import config
from discord import Embed
from discord.ext import commands, tasks
from discord.ext.commands import when_mentioned_or, has_permissions, guild_only, is_owner

import db
import settings
from settings import blank_space, enso_embedmod_colours, enso_guild_ID, enso_newpeople_ID

# Storing the prefixes and guildID's in the cache
cached_prefixes = {}


# Updating the prefix within the dict and database when the method is called
async def storage_prefix_for_guild(ctx, prefix):
    cached_prefixes[str(ctx.guild.id)] = prefix

    with db.connection() as connection:
        # Update the existing prefix within the database
        update_query = """UPDATE guilds SET prefix = (?) WHERE guildID = (?)"""
        update_vals = prefix, ctx.guild.id,

        # Using the connection cursor
        with closing(connection.cursor()) as cur:
            # Execute the query
            cur.execute(update_query, update_vals)
            print(cur.rowcount, f"Guild prefix has been updated for guild {ctx.guild.name}")

    # Let the user know that the guild prefix has been updated
    await ctx.send(f"**Guild prefix has been updated to `{prefix}`**")


# Method to store the cached prefixes
def cache_prefix(guildid, prefix):
    cached_prefixes[guildid] = prefix


# Deleting the key - value pair for guild
def del_cache_prefix(guildid):
    del cached_prefixes[guildid]


# Get the prefix of the guild that the user is in
def get_prefix_for_guild(guildid):
    prefix = cached_prefixes[guildid]
    if prefix is not None:
        return prefix
    return "defaultPrefix"


# Before initialising the cache. Store the prefixes from the database within the cache
with db.connection() as conn:
    # Grab the prefix of the server from the database
    select_query = """SELECT * FROM guilds"""
    with closing(conn.cursor()) as cursor:
        # Execute the query
        cursor.execute(select_query)
        results = cursor.fetchall()

        # Store the guildids and prefixes within
        for row in results:
            cache_prefix(row[0], row[1])

# Getting the Bot token from Environment Variables
API_TOKEN = config('DISCORD_TOKEN')


# Method to allow the commands to be used with mentioning the bot
async def get_prefix(bot, message):
    if message.guild is None:
        return "~"
    return when_mentioned_or(get_prefix_for_guild(str(message.guild.id)))(bot, message)


def get_version():
    return "v1.7.2"


# Bot Initiation
client = commands.Bot(  # Create a new bot
    command_prefix=get_prefix,  # Set the prefix
    description='All current available commands within Ensō~Chan',  # Set a description for the bot
    owner_id=154840866496839680,  # Your unique User ID
    version=get_version)  # Version number of Ensō~Chan

if __name__ == '__main__':
    for ext in settings.extensions():
        client.load_extension(ext)


# Bot ping command in milliseconds
@client.command(name="ping", aliases=["Ping"])
async def _ping(ctx):
    """Sends the latency of the bot (ms)"""
    await ctx.send(f'Pong! `{round(client.latency * 1000)}ms`')


# Bot prefix command that returns the prefix or updates it
@client.command(name="prefix", aliases=["Prefix"])
@guild_only()
@has_permissions(manage_guild=True)
async def change_prefix(ctx, new: Optional[str]):
    # As long as a new prefix has been given and is less than 5 characters
    if new and len(new) < 5:
        if len(new) > 1:
            spaced_prefix = f"{new} "
            await storage_prefix_for_guild(ctx, spaced_prefix)
        else:
            # Store the new prefix in the dictionary and update the database
            await storage_prefix_for_guild(ctx, new)

    # Making sure that errors are handled if prefix is above 5 characters
    elif new and len(new) > 5:
        await ctx.send("The guild prefix must be less than **5** characters!")

    # if no prefix was provided
    elif not new:
        # Grab the current prefix for the guild within the cached dictionary
        await ctx.send(f"**The current guild prefix is `{get_prefix_for_guild(str(ctx.guild.id))}`**")


# Bot event making sure that messages sent by the bot do nothing
@client.event
async def on_message(message):
    # Making sure that the bot does not take in its own messages
    if message.author.bot:
        return

    # Processing the message
    await client.process_commands(message)


# Choose a random status
looping_statuses = cycle(
    [
        discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(client.users)} Weebs | {get_version()}"),
        discord.Activity(
            type=discord.ActivityType.watching,
            name=f"Hamothy | Real Life | {get_version()}"),
        discord.Activity(
            type=discord.ActivityType.watching,
            name=f"Hamothy Program | {get_version()}"),
        discord.Game(name=f"~help | {get_version()}")
    ]
)


@tasks.loop(seconds=180.0, reconnect=True)
async def change_status():
    """Creating Custom Statuses as a Background Task"""

    # Waiting for the bot to ready
    await client.wait_until_ready()

    # Display the next status in the loop
    await client.change_presence(activity=next(looping_statuses))


# Start the background task
change_status.start()


@client.command(name="restart", hidden=True)
@is_owner()
async def restart(ctx):
    """Restart the Bot"""
    await client.logout()


# Bot Status on Discord
@client.event
async def on_ready():
    # Tells me that the bot is ready and logged in
    print('Bot is ready.')


# Bot event for the bot joining a new guild, storing all users in the database
@client.event
async def on_guild_join(guild):
    # Store the default prefix when the bot joins a guild
    cache_prefix(str(guild.id), prefix="~")

    try:
        # Set up connection to database
        with db.connection() as conn:
            # Iterate through every member within the guild
            for member in guild.members:
                name = f"{member.name}#{member.discriminator}"

                # Define the insert statement that will insert the user's information
                insert_query = """INSERT INTO members (guildID, discordUser, discordID) VALUES (?, ?, ?)"""
                vals = guild.id, name, member.id,
                with closing(conn.cursor()) as cursor:
                    # Execute the query
                    cursor.execute(insert_query, vals)
                    print(cursor.rowcount, f"Record inserted successfully into Members from {guild.name}")

            # Define the insert statement for inserting the guild into the guilds table
            insert_query = """INSERT INTO guilds (guildID) VALUES (?)"""
            val = guild.id,
            with closing(conn.cursor()) as cursor:
                # Execute the query
                cursor.execute(insert_query, val)
                print(cursor.rowcount, f"Record inserted successfully into Guilds from {guild.name}")

    except mariadb.Error as ex:
        print("Parameterized Query Failed: {}".format(ex))


# Bot event for the bot leaving a guild, deleted all users stored in the database
@client.event
async def on_guild_remove(guild):
    # Delete the key - value pair for the guild
    del_cache_prefix(str(guild.id))

    try:
        # Set up connection to database
        with db.connection() as conn:
            for member in guild.members:
                # Delete the record of the member as the bot leaves the server
                delete_query = """DELETE FROM members WHERE discordID = (?) AND guildID = (?)"""
                vals = member.id, guild.id,
                with closing(conn.cursor()) as cursor:
                    # Execute the SQL Query
                    cursor.execute(delete_query, vals)
                    print(cursor.rowcount, f"Record deleted successfully from Members from {guild.name}")

            # Delete the guild and prefix information as the bot leaves the server
            delete_query = """DELETE FROM guilds WHERE guildID = (?)"""
            val = guild.id,
            with closing(conn.cursor()) as cursor:
                # Execute the query
                cursor.execute(delete_query, val)
                print(cursor.rowcount, f"Record deleted successfully from Guild {guild.name}")

    except mariadb.Error as ex:
        print("Parameterized Query Failed: {}".format(ex))


# Bot event for new member joining, sending an embed introducing them to the server
@client.event
async def on_member_join(member):
    # Get the guild
    guild = member.guild

    try:
        # Set up connection to database
        with db.connection() as conn:
            name = f"{member.name}#{member.discriminator}"

            # Define the insert statement that will insert the user's information
            insert_query = """INSERT INTO members (guildID, discordUser, discordID) VALUES (?, ?, ?)"""
            vals = member.guild.id, name, member.id,
            cursor = conn.cursor()

            # Execute the SQL Query
            cursor.execute(insert_query, vals)
            conn.commit()
            print(cursor.rowcount, "Record inserted successfully into Members")

    except mariadb.Error as ex:
        print("Parameterized Query Failed: {}".format(ex))

    # Make sure the guild is Enso
    if guild.id != enso_guild_ID:
        return

    # Set the channel id to "newpeople"
    new_people = guild.get_channel(enso_newpeople_ID)

    # Set the enso server icon and the welcoming gif
    server_icon = guild.icon_url
    welcome_gif = "https://cdn.discordapp.com/attachments/669808733337157662/730186321913446521/NewPeople.gif"

    # Set up embed for the #newpeople channel
    embed = Embed(title="\n**Welcome To Ensō!**",
                  colour=enso_embedmod_colours,
                  timestamp=datetime.datetime.utcnow())

    embed.set_thumbnail(url=server_icon)
    embed.set_image(url=welcome_gif)
    embed.add_field(
        name=blank_space,
        value=f"Hello {member.mention}! We hope you enjoy your stay in this server! ",
        inline=False)
    embed.add_field(
        name=blank_space,
        value=f"Be sure to check out our <#669815048658747392> channel to read the rules and <#683490529862090814> channel to get caught up with any changes! ",
        inline=False)
    embed.add_field(
        name=blank_space,
        value=f"Last but not least, feel free to go into <#669775971297132556> to introduce yourself!",
        inline=False)

    # Send embed to #newpeople
    await new_people.send(embed=embed)


# Bot event for new member joining, sending an embed introducing them to the server
@client.event
async def on_member_remove(member):
    # Get the guild
    guild = member.guild

    try:
        # With the database connection
        with db.connection() as conn:

            # Delete the record of the member as they leave the server
            delete_query = """DELETE FROM members WHERE discordID = (?) AND guildID = (?)"""
            vals = member.id, guild.id,
            cursor = conn.cursor()

            # Execute the SQL Query
            cursor.execute(delete_query, vals)
            conn.commit()
            print(cursor.rowcount, "Record deleted successfully from Members")

    except mariadb.Error as ex:
        print("Parameterized Query Failed: {}".format(ex))


# Bot Event for handling all errors within discord.commands
@client.event
async def on_command_error(ctx, args2):
    discord.errors.Forbidden = getattr(discord.errors.Forbidden, "original", discord.errors.Forbidden)

    # if the user did not specify an user
    if isinstance(args2, commands.MissingRequiredArgument):
        await on_command_missing_user(ctx)
    # if the user has spammed a command and invoked a cooldown
    elif isinstance(args2, commands.CommandOnCooldown):
        await on_command_cooldown(ctx, args2)
    # if the user does not the correct permissions to call a command
    elif isinstance(args2, commands.CheckFailure):
        await on_command_permission(ctx)
    # if the user tries to access a command that isn't available
    elif isinstance(args2, commands.CommandNotFound):
        await on_command_not_found(ctx)
    # if the user provides an argument that isn't recognised
    elif isinstance(args2, commands.BadArgument):
        await on_command_bad_argument(ctx)
    # if the bot does not permissions to send the command
    elif isinstance(args2, discord.errors.Forbidden):
        await on_command_forbidden(ctx)


# Async def for handling command bad argument error
async def on_command_forbidden(ctx):
    # Send an error message to the user telling them that the member specified could not be found
    message = await ctx.send(f"**I don't have permissions to execute this command**")

    # Let the user read the message for 5 seconds
    await asyncio.sleep(5)
    # Delete the message
    await message.delete()


# Async def for handling command bad argument error
async def on_command_bad_argument(ctx):
    # Send an error message to the user telling them that the member specified could not be found
    message = await ctx.send(f'**I could not find that member!**')

    # Let the user read the message for 5 seconds
    await asyncio.sleep(5)
    # Delete the message
    await message.delete()


# Async def for handling command not found error
async def on_command_not_found(ctx):
    # Send an error message to the user telling them that the command doesn't exist
    message = await ctx.send(f'**Command Not Found! Please use `{ctx.prefix}help` to see all commands**')

    # Let the user read the message for 5 seconds
    await asyncio.sleep(5)
    # Delete the message
    await message.delete()


# Async def for handling cooldown error/permission errors
async def on_command_cooldown(ctx, error):
    # Send an error message to the user telling them that the command is on cooldown
    message = await ctx.send(f'That command is on cooldown. Try again in **{error.retry_after:,.2f}** seconds.')

    # Let the user read the message for 5 seconds
    await asyncio.sleep(5)
    # Delete the message
    await message.delete()


# Async def for handling permission errors
async def on_command_permission(ctx):
    # Send an error message to the user saying that they don't have permission to use this command
    message = await ctx.send("**Uh oh! You don't have permission to use this command!**")

    # Let the user read the message for 5 seconds
    await asyncio.sleep(5)
    # Delete the message
    await message.delete()


async def on_command_missing_user(ctx):
    # Send an error message to the user saying that an argument is missing
    message = await ctx.send("**Uh oh! Couldn't find anyone to mention! Try again!**")

    # Let the user read the message for 5 seconds
    await asyncio.sleep(5)
    # Delete the message
    await message.delete()


# Run the bot, allowing it to come online
try:
    client.run(API_TOKEN)
except discord.errors.LoginFailure as e:
    print("Login unsuccessful.")

"""    
def write_to_dm_file(time, author, content):
    with open('images/logs/dm-logs.txt', mode='a') as dm_logs_file:
    dm_logs_file.write(f"{time}: {author}: {content}")
    
    # File Writing Variables
    time = message.created_at
    msg_time = time.strftime('%Y-%m-%dT%H:%M:%S')
    msg_author = message.author
    msg_content = message.content
    

 # Don't count messages that are taken in the dms
    if not isinstance(message.channel, DMChannel):
        # Using connection to the database
        with db.connection() as conn:

            # Make sure that mariaDB errors are handled properly
            try:
                msg_name = message.author.name
                msg_discrim = message.author.discriminator
                time = message.created_at

                # Get:
                guild_id = message.guild.id  # Guild of the message
                msg_time = time.strftime('%Y-%m-%d %H:%M:%S')  # Time of the Message
                msg_author = f"{msg_name}#{msg_discrim}"  # DiscordID
                msg_content = message.content  # Content of the message

                # Store the variables
                val = guild_id, msg_time, msg_author, msg_content,

                # If an attachment (link) has been sent
                if message.attachments:

                    # Loop through all attachments
                    for attachment in message.attachments:
                        # Get the message content and the link that was used
                        attach = "".join(f"Message: {message.content} Link: {attachment.url}")

                    # Define the new variables to send
                    val = guild_id, msg_time, msg_author, attach,

                # Define the Insert Into Statement inserting into the database
                insert_query = """"""INSERT INTO messages (guildID, messageTime, discordID, messageContent) VALUES (?, ?, ?, ?)""""""
                cursor = conn.cursor()

                # Execute the SQL Query
                cursor.execute(insert_query, val)
                conn.commit()
                print(cursor.rowcount, "Record inserted successfully into Logs")

            except mariadb.Error as ex:
                print("Parameterized Query Failed: {}".format(ex))
                
        
        
 # Using database connection
    with db.connection() as conn:
        # Grab the guild and prefix information of the guild that the message was sent in
        select_query = """"""SELECT * FROM guilds WHERE guildID = (?)""""""
        select_val = ctx.guild.id,

        # Using connection cursor
        with closing(conn.cursor()) as cursor:

            # Execute the query
            cursor.execute(select_query, select_val)
            result = cursor.fetchone()

            # Grab the guild prefix
            curr_prefix = result[1]

        # If no argument has been given, display the current prefix
        if not new:
            await ctx.send(f"**The current guild prefix is `{curr_prefix}`**")

        # Update the prefix for the guild
        else:
        
DON'T USE - BANNABLE CODE 
colours = [
    discord.Colour(0x000000),
    discord.Colour(0xFFFFFF),
    discord.Colour(0x1ABC9C),
    discord.Colour(0x2ECC71),
    discord.Colour(0x3498DB),
    discord.Colour(0x9B59B6),
    discord.Colour(0xE91E63),
    discord.Colour(0xF1C40F),
    discord.Colour(0xE67E22),
    discord.Colour(0xE74C3C),
    discord.Colour(0x95A5A6),
    discord.Colour(0x34495E),
    discord.Colour(0x11806A),
    discord.Colour(0x1F8B4C),
    discord.Colour(0x206694),
    discord.Colour(0x71368A),
    discord.Colour(0xAD1457),
    discord.Colour(0xC27C0E),
    discord.Colour(0xA84300),
    discord.Colour(0x992D22),
    discord.Colour(0x979C9F),
    discord.Colour(0x7F8C8D),
    discord.Colour(0xBCC0C0),
    discord.Colour(0x2C3E50),
    discord.Colour(0x7289DA),
    discord.Colour(0x99AAB5),
    discord.Colour(0x2C2F33),
    discord.Colour(0x23272A),
    discord.Colour(0xDC143C),
    discord.Colour(0xFF69B4),
    discord.Colour(0xFF69B4),
    discord.Colour(0xFF00FF),
    discord.Colour(0xEE82EE),
    discord.Colour(0x008080),
    discord.Colour(0x191970),
    discord.Colour(0xFFE4E1),
    discord.Colour(0x2E8B57),
    discord.Colour(0xC71585)]
guild_id = 663651584399507476
role_name = "Rainbow"


@loop(seconds=5.0)
async def colour_change():
    try:
        await role_to_change.edit(colour=random.choice(colours))
    except Exception as ex:
        print(ex)


@colour_change.before_loop
async def colour_change_before():
    global role_to_change
    await client.wait_until_ready()
    guild = client.get_guild(guild_id)
    role_to_change = get(guild.roles, name=role_name)


colour_change.start()"""
