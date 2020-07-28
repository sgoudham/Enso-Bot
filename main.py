import datetime
import string
from typing import Optional

import discord
from decouple import config
from discord import Embed
from discord.ext import commands, tasks
from discord.ext.commands import when_mentioned_or, is_owner, guild_only, has_permissions

import db
import settings
from cogs.help import HelpPaginator
from db import connection
from settings import blank_space, enso_embedmod_colours, enso_guild_ID, enso_newpeople_ID, get_prefix_for_guild, \
    storage_prefix_for_guild, cache_prefix, del_cache_prefix, del_modlog_channel, cache_modlogs

counter = 0

# Getting the Bot token from Environment Variables
API_TOKEN = config('DISCORD_TOKEN')


# Method to allow the commands to be used with mentioning the bot
async def get_prefix(bot, message):
    if message.guild is None:
        return "~"
    return when_mentioned_or(get_prefix_for_guild(str(message.guild.id)))(bot, message)


def get_version():
    """Return the current version of the bot"""
    return "v1.7.2"


# Bot Initiation
client = commands.Bot(  # Create a new bot
    command_prefix=get_prefix,  # Set the prefix
    description='All current available commands within Ensō~Chan',  # Set a description for the bot
    owner_id=154840866496839680,  # Your unique User ID
    version=get_version)  # Version number of Ensō~Chan
client.remove_command("help")  # Remove default help command

if __name__ == '__main__':
    for ext in settings.extensions():
        client.load_extension(ext)


@client.event
async def on_message(message):
    """Make sure bot messages are not tracked"""

    if message.author.bot:
        return

    # Processing the message
    await client.process_commands(message)


@tasks.loop(seconds=120, reconnect=True)
async def change_status():
    """Creating Custom Statuses as a Background Task"""

    global counter
    # Waiting for the bot to ready
    await client.wait_until_ready()

    # Define array of statuses
    looping_statuses = [
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

    # Check if the counter is at the end of the array
    if counter == (len(looping_statuses) - 1):
        # Reset the loop
        counter = 0
    else:
        # Increase the counter
        counter += 1

    # Display the next status in the loop
    await client.change_presence(activity=looping_statuses[counter])


# Start the background task
change_status.start()


@client.event
async def on_ready():
    """Displaying if Bot is Ready"""

    print("UvU Senpaiii I'm weady")


@client.command(name="ping", aliases=["Ping"])
async def _ping(ctx):
    """Latency of the Bot (ms)"""

    await ctx.send(f"Pong! `{round(client.latency * 1000)}ms`")


@client.command(name="leave", aliases=["Leave"], hidden=True)
@is_owner()
async def leave(ctx):
    """Leaves the guild"""

    await ctx.send("**Leaving the guild... Bye Bye uvu**")
    await ctx.guild.leave()


@client.command(name="restart", hidden=True)
@is_owner()
async def restart(ctx):
    """Restart the Bot"""

    await ctx.send("**Success Senpai! Bot has been restarted**")
    await client.logout()


@client.command(name='help', aliases=["Help"])
async def _help(ctx, *, command: Optional[str] = None):
    """Shows help about a command or the bot"""

    try:
        if command is None:
            p = await HelpPaginator.from_bot(ctx)
        else:
            entity = ctx.bot.get_cog(command) or ctx.bot.get_command(command)

            if entity is None:
                clean = command.replace('@', '@\u200b')
                return await ctx.send(f"**Command or Category '{clean}' Not Found.**")
            elif isinstance(entity, commands.Command):
                p = await HelpPaginator.from_command(ctx, entity)
            else:
                p = await HelpPaginator.from_cog(ctx, entity)

        await p.paginate()
    except Exception as ex:
        await ctx.send("**{}**".format(ex))


@client.command(name="reloaddb", hidden=True)
@is_owner()
async def reload_db(ctx):
    # Setup pool
    pool = await connection(db.loop)

    # Setup up pool connection and cursor
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Define the insert statement that will insert the user's information
            insert = """INSERT INTO members (guildID, discordID) VALUES """ + ", ".join(
                map(lambda m: f"({ctx.guild.id}, {m.id})",
                    ctx.guild.members)) + """ ON DUPLICATE KEY UPDATE guildID = VALUES(guildID), discordID = VALUES(discordID)"""

            # Execute the insert statement
            await cur.execute(insert)
            await conn.commit()
            print(cur.rowcount, f"Record(s) inserted successfully into Members from {ctx.guild.name}")

            # Sending confirmation message
            await ctx.send("**Database Reloaded Successfully for Guild {}**".format(ctx.guild.name))


@client.command(name="prefix", aliases=["Prefix"])
@guild_only()
@has_permissions(manage_guild=True)
async def change_prefix(ctx, new: Optional[str] = None):
    """View/Change Guild Prefix"""

    # As long as a new prefix has been given and is less than 5 characters
    if new and len(new) <= 5:
        # Store the new prefix in the dictionary and update the database
        await storage_prefix_for_guild(ctx, new)

    # Making sure that errors are handled if prefix is above 5 characters
    elif new and len(new) > 5:
        await ctx.send("The guild prefix must be less than or equal to **5** characters!")

    # if no prefix was provided
    elif not new:
        # Grab the current prefix for the guild within the cached dictionary
        await ctx.send(f"**The current guild prefix is `{get_prefix_for_guild(str(ctx.guild.id))}`**")


# Bot event for the bot joining a new guild, storing all users in the database
@client.event
async def on_guild_join(guild):
    """Store users in a database when the bot has joined a new guild"""

    # Store default prefix within cache
    cache_prefix(str(guild.id), prefix="~")
    # Store default modlogs channel within cache
    cache_modlogs(str(guild.id), channel=None)

    # Setup pool
    pool = await connection(db.loop)

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

    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Define the insert statement that will insert the user's information
            insert = """INSERT INTO members (guildID, discordID) VALUES""" + ", ".join(
                map(lambda m: f"({guild.id}, {m.id})",
                    guild.members)) + """ ON DUPLICATE KEY UPDATE guildID = VALUES(guildID), discordID = VALUES(discordID)"""

            # Execute the query
            await cur.execute(insert)
            await conn.commit()
            print(cur.rowcount, f"Record(s) inserted successfully into Members from {guild.name}")


# Bot event for the bot leaving a guild, deleted all users stored in the database
@client.event
async def on_guild_remove(guild):
    """Remove users in the database for the guild"""

    # Delete the key - value pairs for the guild
    del_cache_prefix(str(guild.id))
    del_modlog_channel(str(guild.id))

    # Setup pool
    pool = await connection(db.loop)

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

    # Setup pool connection and cursor
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Delete the record of the member as the bot leaves the server
            delete_query = """DELETE FROM members WHERE guildID = %s"""
            vals = guild.id,

            # Execute the query
            await cur.execute(delete_query, vals)
            await conn.commit()
            print(cur.rowcount, f"Record(s) deleted successfully from Members from {guild.name}")


# Bot event for new member joining, sending an embed introducing them to the server
@client.event
async def on_member_join(member):
    # Get the guild
    guild = member.guild

    # Setup pool
    pool = await db.connection(db.loop)

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
            print(cur.rowcount, "Record(s) inserted successfully into Members")

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


# Bot Event for handling all errors within discord.commands
@client.event
async def on_command_error(ctx, args2):
    # if the user did not specify an user
    if isinstance(args2, commands.MissingRequiredArgument):
        await on_command_missing_argument(ctx)
    # if the user has spammed a command and invoked a cooldown
    elif isinstance(args2, commands.CommandOnCooldown):
        await on_command_cooldown(ctx, args2)
    # if the user tries to access a command that isn't available
    elif isinstance(args2, commands.CommandNotFound):
        await on_command_not_found(ctx)
    # if the user provides an argument that isn't recognised
    elif isinstance(args2, commands.BadArgument):
        await on_command_bad_argument(ctx)
    # if the user does not the correct permissions to call a command
    elif isinstance(args2, commands.MissingPermissions):
        await on_command_permission(ctx)
    elif isinstance(args2, commands.BotMissingPermissions):
        await on_bot_forbidden(ctx, args2)
    elif isinstance(args2, commands.NotOwner):
        await on_not_owner(ctx)


# Async def for handling command bad argument error
async def on_bot_forbidden(ctx, args2):
    # Convert list into string of the missing permissions
    missing_perms = string.capwords(", ".join(args2.missing_perms).replace("_", " "))

    # Send an error message to the user notifying them of the permissions that are missing from the bot
    embed = Embed(description="❌ I Need **{}** Permission(s) to Execute This Command! ❌".format(missing_perms))
    await ctx.send(embed=embed)


# Async def for handling command bad argument error
async def on_command_forbidden(ctx):
    # Send an error message to the user telling them that the member specified could not be found
    await ctx.send(f"**I don't have permissions to execute this command**")


# Async def for handling command bad argument error
async def on_command_bad_argument(ctx):
    # Send an error message to the user telling them that the member specified could not be found
    embed = Embed(description="**❌ Uh oh! Couldn't find anyone to mention! Try again! ❌**")
    await ctx.send(embed=embed)


# Async def for handling command not found error
async def on_command_not_found(ctx):
    # Send an error message to the user telling them that the command doesn't exist
    embed = Embed(description="Command Not Found! ❌ Please use **{}help** to see all commands".format(ctx.prefix))
    await ctx.send(embed=embed)


# Async def for handling cooldown error/permission errors
async def on_command_cooldown(ctx, error):
    # Send an error message to the user telling them that the command is on cooldown
    embed = Embed(description="That command is on cooldown. Try again in **{:,.2f}** seconds".format(error.retry_after))
    await ctx.send(embed=embed)


# Async def for handling permission errors
async def on_command_permission(ctx):
    # Send an error message to the user saying that they don't have permission to use this command
    embed = Embed(description="**❌ Uh oh! You don't have permission to use this command! ❌**")
    await ctx.send(embed=embed)


async def on_command_missing_argument(ctx):
    # Send an error message to the user saying that an argument is missing
    embed = Embed(description="Required Argument(s) Missing!"
                              "\nUse **{}help** to find how to use **{}**".format(ctx.prefix,
                                                                                  ctx.command))
    await ctx.send(embed=embed)


# Async def for handling permission errors
async def on_not_owner(ctx):
    # Send an error message to the user saying that they don't have permission to use this command
    embed = Embed(description="**❌ Owner Only Command ❌**")
    await ctx.send(embed=embed)


# Run the bot, allowing it to come online
try:
    client.run(API_TOKEN)
except discord.errors.LoginFailure as e:
    print("Login unsuccessful.")

"""    
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
    
colour_change.start()
@client.command()
@guild_only()
@cooldown(1, 300, BucketType.guild)
async def someone(ctx):
    """"""Tags Someone Randomly in the Server""""""

    await ctx.send(random.choice(tuple(member.mention for member in ctx.guild.members if not member.bot)))
    
    

"""
