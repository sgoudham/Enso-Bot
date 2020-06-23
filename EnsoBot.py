import asyncio
import datetime

import discord
from decouple import config
from discord.ext import commands

# Getting the Bot token from Environment Variables
import settings

API_TOKEN = config('DISCORD_TOKEN')

# Bot Initiation
client = commands.Bot(  # Create a new bot
    command_prefix="~",  # Set the prefix
    description='Ensō~Chan!',  # Set a description for the bot
    owner_id=154840866496839680)  # Your unique User ID
# Removes the default help command
client.remove_command('help')

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
    await client.change_presence(activity=discord.Game(name="With Izzy 😏😏"))


# Bot ~Ping command in milliseconds
@client.command(aliases=["Ping"])
@commands.is_owner()
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

    # Surround with try/except to catch any exceptions that may occur
    try:

        # Set up embed for the #newpeople channel
        embed = discord.Embed(title="\n**Welcome To Ensō!**",
                              colour=discord.Colour(0x30e419))

        embed.timestamp = datetime.datetime.utcnow()

        embed.set_thumbnail(url="https://media.discordapp.net/attachments/683490529862090814/715010931620446269"
                                "/image1.jpg?width=658&height=658")
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/714671068941647933/717144047252275270/f4d7de6463d3ada02058a094fd6917ac.gif")
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

        # Set izzyID equal to my id in discord
        izzyID = '<@&664585078487252993>'

        # String for welcoming people in the #general channel
        general_welcome = f"Welcome to the server! {member.mention} I hope you enjoy your stay here <a:huh:676195228872474643> <a:huh:676195228872474643> " \
                          f"\nPlease go into <#722347423913213992> to choose some ping-able roles for events! " \
                          f"\nPlease ping {izzyID} for any questions about the server and of course, the other staff members!"

        # Send welcome message to #general
        await general.send(general_welcome)

    except Exception as ex:
        print(ex)


# Allowing people to get ping-able self roles
@client.command(name="rolemenu")
@commands.is_owner()
async def role_menu(ctx):
    # Surround with try/except to catch any exceptions that may occur
    try:

        # Get the channel id of #self-roles
        channel = client.get_channel(722347423913213992)

        # Set up embed to let people know what ping-able roles can be chosen
        embed = discord.Embed(title="**Role Menu: Ping-Able Roles**", colour=discord.Colour.orange())

        embed.timestamp = datetime.datetime.utcnow()

        embed.set_thumbnail(url="https://media.discordapp.net/attachments/683490529862090814/715010931620446269"
                                "/image1.jpg?width=658&height=658")
        embed.set_author(name="Hamothy", icon_url="https://cdn.discordapp.com/attachments/689525645734182916"
                                                  "/718510466640642099/Rias_Gremory.png")
        embed.set_footer(text=f"{ctx.message.author}",
                         icon_url="https://media.discordapp.net/attachments/689525645734182916/718510466640642099/Rias_Gremory.png")
        embed.add_field(
            name="\u200b",
            value="React to give yourself roles to be pinged for these events!",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="<:MovieNight:722293598938333190> : `Movie Nights`",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="<:Karaoke:722358251932483605> : `Karaoke Nights`",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="<:EnsoBros:722360289345011743> : `Enso Bros Podcasts`",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="<:GameNights:722502073769525268> : `Game Nights`",
            inline=False)

        # Send embed to #self-roles
        await channel.send(embed=embed)

    except Exception as e:
        print(e)


# Bot event for enabling roles to be added to users when they react to the embedded message
@client.event
async def on_raw_reaction_add(payload):
    # Surround with try/except to catch any exceptions that may occur
    try:

        # If the message id equals the self roles message
        if payload.message_id == 722514840559812649:
            # Print out the emoji name
            print(payload.emoji.name)

            # Find a role corresponding to the Emoji name.
            guild_id = payload.guild_id

            # Find the guild Enso and find the role of the emoji that has been reacted to
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
            role = discord.utils.find(lambda r: r.name == payload.emoji.name, guild.roles)

            # if the role does exist
            if role is not None:
                # Print to me that the role was found and display the id of the role
                print(role.name + " was found!")
                print(role.id)

                # Find the member who had reacted to the emoji
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                # Add the role to the member
                await member.add_roles(role)

                # Print to me that the role has been added
                print("done")

    except Exception as e:
        print(e)


# Bot event for enabling roles to be removed from users when they unreact to the embedded messaged
@client.event
async def on_raw_reaction_remove(payload):
    # Surround with try/except to catch any exceptions that may occur
    try:

        # If the message id equals the self roles message
        if payload.message_id == 722514840559812649:
            # Print out the emoji name
            print(payload.emoji.name)

            # Get the server id
            guild_id = payload.guild_id

            # Find the guild Enso and find the role of the emoji that has been unreacted to
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
            role = discord.utils.find(lambda r: r.name == payload.emoji.name, guild.roles)

            # if the role does exist
            if role is not None:
                # Find the member that has the role which the emoji is connected to
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)

                # Remove the role from the member
                await member.remove_roles(role)

    except Exception as ex:
        print(ex)


# ~marry command allows the bot to wed two young lovers together
@client.command()
async def marry(ctx, member: discord.Member):
    # Send a message to the channel mentioning the author and the person they want to wed.
    await ctx.send(f"{ctx.author.mention} **Proposes To** {member.mention} **Do you accept??** "
                   f"\nRespond with [**Y**es/**N**o]")

    # A check that makes sure that the reply is not from the author
    # and that the reply is in the same channel as the proposal
    def check(m):
        return m.author == member and m.channel == ctx.channel

    # Surround with try/except to catch any exceptions that may occur
    try:
        # Wait for the message from the mentioned user
        msg = await client.wait_for('message', check=check, timeout=30)

        # if the person says yes
        if msg.content.lower() in ['y', 'yes', 'yea']:
            # Congratulate them!
            await ctx.send(
                f"Congratulations! ヽ(・∀・)ﾉ {ctx.author.mention} and {member.mention} are now married to each other!")
        # if the person says no
        elif msg.content.lower() in ['n', 'no', 'nah']:
            # Try to console the person and wish them the best in their life
            await ctx.send(f"Unlucky (Ｔ▽Ｔ), maybe another time! {ctx.author.mention}")
        else:
            # Abort the process as the message sent did not make sense
            await ctx.send("Senpaiiii! Speak English Please ⋋_⋌")

    except asyncio.TimeoutError as e:
        print(e)
        # Send out an error message if the user waited too long
        await ctx.send("Awww they waited too long (✖╭╮✖)")


# Allows the bot to echo the dm's that it receives
@client.event
async def on_message(message):
    # Checking if the message is not sent in server
    if message.guild is None:
        # Checking if the owner is sending the message
        if commands.is_owner():
            # Send message to #general
            channel = client.get_channel(663651584399507481)
            await channel.send(message.content)
        else:
            # Send message to #enso-chan~commands
            channel = client.get_channel(721449922838134876)
            await channel.send(message.content)
    else:
        return

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

    # Let the Auser read the message for 2.5 seconds
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

'''
@client.command()
@commands.has_any_role('Hamothy')
async def users(ctx):
    server_id = client.get_guild(663651584399507476)

    await ctx.send(f"""Number of Members: {server_id.member_count}""") 
'''

"""    
         # if the message author id is equal to mine
        author = message.author.name
        discrim = message.author.discriminator
        content = message.content
        time = str(message.created_at)

        with open('logs/dm-logs.txt', "a") as file:
            file.write("\n")
            file.write(time + ": " + author + "#" + discrim + ": " + content)
"""
