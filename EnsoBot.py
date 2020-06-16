import asyncio
import datetime

import discord
from decouple import config
from discord.ext import commands

# Getting the Bot token from Environment Variables
API_TOKEN = config('DISCORD_TOKEN')

# Bot Prefix
client = commands.Bot(command_prefix='~')
client.remove_command('help')

# Instantiates a list for all the cogs
extensions = ['cogs.WaifuImages', 'cogs.FunCommands', 'cogs.Music',
              'cogs.HelpCommands', 'cogs.OwOText', 'cogs.Embeds']

# Calls the cogs
if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)


# Bot Status on Discord
@client.event
async def on_ready():
    print('Bot is ready.')
    await client.change_presence(activity=discord.Game(name="I'm scared"))


# Bot ~Ping command in milliseconds
@client.command(aliases=["Ping"])
@commands.has_any_role('Hamothy', 'Servant')
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


# Bot Event for handling cooldown error
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        message = await ctx.send(f'That command is on cooldown. Try again in {error.retry_after:,.2f} seconds.')

        # Let the user read the message for 2.5 seconds
        await asyncio.sleep(2.5)
        # Delete the message
        await message.delete()


@client.event
async def on_command_error(ctx, target: discord.member):
    if isinstance(target, commands.MissingRequiredArgument):
        message = await ctx.send("Uh oh! Couldn't find anyone to mention! Try again!")

        # Let the user read the message for 2.5 seconds
        await asyncio.sleep(1.5)
        # Delete the message
        await message.delete()


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        message = await ctx.send("Uh oh! You don't have permission to use this command!")

        # Let the user read the message for 2.5 seconds
        await asyncio.sleep(1.5)
        # Delete the message
        await message.delete()


@client.event
async def on_member_join(member):
    channel = client.get_channel(669771571337887765)

    try:
        embed = discord.Embed(title="\n**Welcome To Ensō!**",
                              colour=discord.Colour(0x30e419))

        embed.timestamp = datetime.datetime.utcnow()

        embed.set_thumbnail(url="https://media.discordapp.net/attachments/683490529862090814/715010931620446269"
                                "/image1.jpg?width=658&height=658")
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/714671068941647933/717144047252275270/f4d7de6463d3ada02058a094fd6917ac.gif")
        embed.set_footer(text=f"Hamothy#5619",
                         icon_url="https://media.discordapp.net/attachments/689525645734182916/718510466640642099/Rias_Gremory.png")
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

        await channel.send(embed=embed)
    except Exception as e:
        print(e)


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
@client.event
async def on_message(message, target: discord.Member,):
    player1 = message.author.mention
    player2 = target.mention
    channel = message.channel

    if message.content.startswith('~punch'):
        channel = message.channel
        await channel.send(f"**Deathmatch started! {player1} vs {player2}**"
                           f"\n What do you want to do {message.author}?"
                           f"\n 1) Punch"
                           f"\n 2) Kick")

        def check(m):
            return m.content == 'punch' and m.channel == channel

        msg = await client.wait_for('f"**{player1} punched {player2} for {punch(p2)} damage!**"', check=check)
        await channel.send(msg)
        
        
@client.event
async def on_message(message):
    if message.content.startswith('~hello'):
        channel = message.channel
        await channel.send('Say hello!')

        def check(m):
            return m.content == 'hello' and m.channel == channel

        msg = await client.wait_for('message', check=check)
        await channel.send('Hello {.author}!'.format(msg))
        
        
def check(author):
def inner_check(message):
    return message.author == author and message.content == "Hello"

return inner_check

msg = await client.wait_for('message', check=check(ctx.author), timeout=30)
await ctx.send(msg)

# def check(m):
#    return m.content == 'punch' and m.channel == channel

# = await client.wait_for('message', check=check)
# await channel.send(f"**{player1} punched {player2} for {punch(p2)} damage!**")
except Exception as e:
print(e) 


@client.command(aliases=["dm"])
async def deathmatch(ctx, target: discord.Member):
    player1 = ctx.author.mention
    player2 = target.mention
    channel = ctx.channel

    p1 = 100
    p2 = 100

    await ctx.send(f"**Deathmatch started! {player1} vs {player2}**"
                   f"\n What do you want to do {ctx.author}?"
                   f"\n 1) Punch"
                   f"\n 2) Kick")

    def check(m):
        return m.content == 'punch' and m.channel == channel

    msg = await client.wait_for('message', check=check)
    await channel.send(msg)
    
def punch(p2, player1, player2):
    damage = random.randint(1, 100)
    p2 -= damage
    return f"**{player1} punched {player2} for {punch(p2)} damage!**"
"""
