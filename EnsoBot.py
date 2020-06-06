import asyncio

import discord
from decouple import config
from discord.ext import commands

# Getting the Bot token from Environment Variables
API_TOKEN = config('DISCORD_TOKEN')

# Bot Prefix
client = commands.Bot(command_prefix='~')
client.remove_command('help')

# Instantiates a list for all the cogs
extensions = ['cogs.WaifuImages', 'cogs.FunCommands', 'cogs.Music', 'cogs.HelpCommands']

# Calls the cogs
if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)


# Bot Status on Discord
@client.event
async def on_ready():
    print('Bot is ready.')
    await client.change_presence(activity=discord.Game(name='Reading Yaoi'))


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
