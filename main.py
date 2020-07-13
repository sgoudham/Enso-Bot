import asyncio

import discord
import mariadb
from decouple import config
from discord import Embed, DMChannel
from discord.ext import commands

import db
import settings
from settings import blank_space, enso_embedmod_colours, time, enso_guild_ID, enso_newpeople_ID

# Getting the Bot token from Environment Variables
API_TOKEN = config('DISCORD_TOKEN')

# Bot Initiation
client = commands.Bot(  # Create a new bot
    command_prefix="~",  # Set the prefix
    description='Ensō~Chan!',  # Set a description for the bot
    owner_id=154840866496839680)  # Your unique User ID

# Calls the cogs from the settings.py file and loads them
(anime, helps, fun) = settings.extensions()
complete_list = anime + helps + fun
if __name__ == '__main__':
    for ext in complete_list:
        client.load_extension(ext)


@client.event
async def on_message(message):
    # Making sure that the bot does not take in its own messages
    if message.author.bot:
        return

    # Don't count messages that are taken in the dms
    if isinstance(message.channel, DMChannel):
        pass
    else:

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
                val = guild_id, msg_time, msg_author, msg_content

                attach = ""
                # If an attachment (link) has been sent
                if message.attachments:
                    # Loop through all attachments
                    for attachment in message.attachments:
                        # Get the message content and the link that was used
                        attach += f"Message: {message.content} Link: {attachment.url}"
                    # Define the new variables to send
                    val = guild_id, msg_time, msg_author, attach
                else:
                    pass

                # Define the Insert Into Statement inserting into the database
                insert_query = """INSERT INTO messages (guildID, messageTime, discordID, messageContent) VALUES (?, ?, ?, ?)"""
                cursor = conn.cursor()

                # Execute the SQL Query
                cursor.execute(insert_query, val)
                conn.commit()
                print(cursor.rowcount, "Record inserted successfully into Logs")

            except mariadb.Error as ex:
                print("Parameterized Query Failed: {}".format(ex))

    # Processing the message
    await client.process_commands(message)


# Bot Status on Discord
@client.event
async def on_ready():
    # Tells me that the bot is ready and logged in
    print('Bot is ready.')

    # Sets the bots status on discord for everyone to view
    await client.change_presence(
        activity=discord.Game(name="with yo Feelings 😍 😳 🙈"))
    # await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Spider Man 3"))


# Bot ~Ping command in milliseconds
@client.command(name="ping", aliases=["Ping"])
@commands.is_owner()
async def ping(ctx):
    """Send the latency of the bot (ms)"""
    await ctx.send(f'Pong! `{round(client.latency * 1000)}ms`')


# Bot event for new member joining, sending an embed introducing them to the server
@client.event
async def on_member_join(member):
    # Get the guild
    guild = member.guild

    # Make sure the guild is Enso
    if guild.id != enso_guild_ID:
        return

    try:
        # Set up connection to database
        with db.connection() as conn:
            name = f"{member.name}#{member.discriminator}"
            # Define the Insert Into Statement inserting into the database
            insert_query = """INSERT INTO members (discordUser, discordID) VALUES (?, ?)"""
            vals = name, member.id
            cursor = conn.cursor()

            # Execute the SQL Query
            cursor.execute(insert_query, vals)
            conn.commit()
            print(cursor.rowcount, "Record inserted successfully into Members")

    except mariadb.Error as ex:
        print("Parameterized Query Failed: {}".format(ex))

    # Set the channel id to "newpeople"
    new_people = guild.get_channel(enso_newpeople_ID)

    # Set the enso server icon and the welcoming gif
    server_icon = guild.icon_url
    welcome_gif = "https://cdn.discordapp.com/attachments/669808733337157662/730186321913446521/NewPeople.gif"

    # Set up embed for the #newpeople channel
    embed = Embed(title="\n**Welcome To Ensō!**",
                  colour=enso_embedmod_colours,
                  timestamp=time)

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

    # Make sure the guild is Enso
    if guild.id != enso_guild_ID:
        return

    try:
        # With the database connection
        with db.connection() as conn:

            # Delete the record of the member as they leave the server
            insert_query = """DELETE FROM members WHERE discordID = (?)"""
            val = member.id,
            cursor = conn.cursor()

            # Execute the SQL Query
            cursor.execute(insert_query, val)
            conn.commit()
            print(cursor.rowcount, "Record Deleted successfully from Members")

    except mariadb.Error as ex:
        print("Parameterized Query Failed: {}".format(ex))


# Bot Event for handling all errors within discord.commands
@client.event
async def on_command_error(ctx, args2):
    # if the user did not specify an user
    if isinstance(args2, commands.MissingRequiredArgument):
        await on_command_missing_user(ctx)
    # if the user has spammed a command and invoked a cooldown
    elif isinstance(args2, commands.CommandOnCooldown):
        await on_command_cooldown(ctx, args2)
    # if the user does not the correct permissions to call a command
    elif isinstance(args2, commands.CheckFailure):
        await on_command_permission(ctx)


# Async def for handling cooldown error/permission errors
async def on_command_cooldown(ctx, error):
    # Send an error message to the user telling them that the command is on cooldown
    message = await ctx.send(f'That command is on cooldown. Try again in **{error.retry_after:,.2f}** seconds.')

    # Let the User read the message for 2.5 seconds
    await asyncio.sleep(2.5)
    # Delete the message
    await message.delete()


# Async def for handling permission errors
async def on_command_permission(ctx):
    # Send an error message to the user saying that they don't have permission to use this command
    message = await ctx.send("**Uh oh! You don't have permission to use this command!**")

    # Let the user read the message for 2.5 seconds
    await asyncio.sleep(2.5)
    # Delete the message
    await message.delete()


async def on_command_missing_user(ctx):
    # Send an error message to the user saying that an argument is missing
    message = await ctx.send("**Uh oh! Couldn't find anyone to mention! Try again!**")

    # Let the user read the message for 2.5 seconds
    await asyncio.sleep(2.5)
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
"""
