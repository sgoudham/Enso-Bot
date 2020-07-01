import asyncio
import datetime

import discord
from decouple import config
from discord import Embed, Colour
from discord.ext import commands
from discord.ext.commands import is_owner

import settings

# Getting the Bot token from Environment Variables
API_TOKEN = config('DISCORD_TOKEN')

# Bot Initiation
client = commands.Bot(  # Create a new bot
    command_prefix="~",  # Set the prefix
    description='Ensō~Chan!',  # Set a description for the bot
    owner_id=154840866496839680)  # Your unique User ID

# Calls the cogs from the settings.py file and loads them
if __name__ == '__main__':
    for ext in settings.extensions:
        client.load_extension(ext)


# Bot Status on Discord
@client.event
async def on_ready():
    # Tells me that the bot is ready and logged in
    print('Bot is ready.')

    # Sets the bots status on discord for everyone to view
    await client.change_presence(activity=discord.Game(name="Feeling Pretty Good :))"))


# Bot ~Ping command in milliseconds
@client.command(name="ping", aliases=["Ping"])
@is_owner()
async def ping(ctx):
    # Send the latency of the bot (ms)
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


# Bot event for new member joining, sending an embed introducing them to the server
@client.event
async def on_member_join(member):
    # Set the channel id to "newpeople"
    new_people = client.get_channel(669771571337887765)
    # Set the channel id to "general"
    general = client.get_channel(663651584399507481)

    # Set the enso server icon and the welcoming gif
    server_icon = "https://media.discordapp.net/attachments/683490529862090814/715010931620446269/image1.jpg?width=658&height=658"
    welcome_gif = "https://cdn.discordapp.com/attachments/714671068941647933/717144047252275270/f4d7de6463d3ada02058a094fd6917ac.gif"

    # Set up embed for the #newpeople channel
    embed = Embed(title="\n**Welcome To Ensō!**",
                  colour=Colour(0x30e419),
                  timestamp=datetime.datetime.utcnow())

    embed.set_thumbnail(url=server_icon)
    embed.set_image(url=welcome_gif)
    embed.add_field(
        name="\u200b",
        value=f"Hello {member.mention}! We hope you enjoy your stay in this server! ",
        inline=False)
    embed.add_field(
        name="\u200b",
        value=f"Be sure to check out our <#669815048658747392> channel to read the rules and <#683490529862090814> channel to get caught up with any changes! ",
        inline=False)
    embed.add_field(
        name="\u200b",
        value=f"Last but not least, feel free to go into <#669775971297132556> to introduce yourself!",
        inline=False)

    # Send embed to #newpeople
    await new_people.send(embed=embed)

    # Set hamothyID equal to my id in discord
    hamothyID = '<@&715412394968350756>'

    # String for welcoming people in the #general channel
    general_welcome = f"Welcome to the server! {member.mention} I hope you enjoy your stay here <a:huh:676195228872474643> <a:huh:676195228872474643> " \
                      f"\nPlease go into <#722347423913213992> to choose some ping-able roles for events! " \
                      f"\nPlease ping {hamothyID} for any questions about the server and of course, the other staff members!"

    # Send welcome message to #general
    await general.send(general_welcome)


# Allows the bot to echo the dm's that it receives
@client.event
async def on_message(message):
    # Making sure that the bot doesn't reply to itself
    if message.author == client.user:
        return

    # Setting the id of myself
    author = message.author.id

    # Checking if the message is not sent in server
    if message.guild is None:
        # Checking if the owner is sending the message
        if author == client.owner_id:

            # Send message to #general
            channel = client.get_channel(663651584399507481)
            await channel.send(message.content)

        else:
            # Sends error message if the person is not the owner
            message = await message.channel.send("Sorry, you don't have permission to echo dms!")

            # Let the user read the message for 2.5 seconds
            await asyncio.sleep(2.5)
            # Delete the message
            await message.delete()

    await client.process_commands(message)


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
    message = await ctx.send(f'That command is on cooldown. Try again in {error.retry_after:,.2f} seconds.')

    # Let the User read the message for 2.5 seconds
    await asyncio.sleep(2.5)
    # Delete the message
    await message.delete()


# Async def for handling permission errors
async def on_command_permission(ctx):
    # Send an error message to the user saying that they don't have permission to use this command
    message = await ctx.send("Uh oh! You don't have permission to use this command!")

    # Let the user read the message for 2.5 seconds
    await asyncio.sleep(2.5)
    # Delete the message
    await message.delete()


async def on_command_missing_user(ctx):
    # Send an error message to the user saying that an argument is missing
    message = await ctx.send("Uh oh! Couldn't find anyone to mention! Try again!")

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
