import asyncio
import discord
from discord.ext import commands

# Bot Prefix
client = commands.Bot(command_prefix='~')

# Instantiates a list for all the cogs
extensions = ['cogs.WaifuImages', 'cogs.FunCommands']



@client.command()
@commands.has_any_role('Hamothy')
async def users(ctx):
    server_id = client.get_guild(663651584399507476)

    await ctx.send(f"""Number of Members: {server_id.member_count}""")

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
@commands.has_any_role('Hamothy')
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


# @client.command(aliases=["Hug"])
# @commands.has_any_role('Hamothy')
# async def bruh(self, ctx):
#    await self.bot.say("hugs {}".format(ctx.message.author.mention()))


# Bot ~roles command allows for an embed message about
@client.command()
@commands.has_any_role('Hamothy')
async def roles(ctx):
    embed = discord.Embed(title="```So you wanna know how the leveled roles system works huh?```",
                          colour=discord.Colour(0x30e419),
                          description="------------------------------------------------")

    embed.set_image(url="https://media.discordapp.net/attachments/669812887564320769/717149671771996180/unknown.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/683490529862090814/715010931620446269/image1.jpg")
    embed.set_author(name="Hamothy",
                     icon_url="https://cdn.discordapp.com/attachments/689525645734182916/717137453651066900"
                              "/Rias_Gremory.png")
    embed.set_footer(
        text="-------------------------------------------------------------------------------------------------------")

    embed.add_field(name="Cooldown", value="**•XP is gained every time you talk with a 2 minute cooldown.**",
                    inline=True),
    embed.add_field(name="Message Length",
                    value="**•XP is not determined by the size of the message. You will not get more XP just because "
                          "the message is bigger.**",
                    inline=True),
    embed.add_field(name="Roles",
                    value="**•As seen below, those are the colours and roles that will be achieved upon gaining that "
                          "amount of experience**",
                    inline=True)

    await ctx.send(embed=embed)


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
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        message = await ctx.send(f'That command is on cooldown. Try again in {error.retry_after:,.2f} seconds.')

        # Let the user read the message for 2.5 seconds
        await asyncio.sleep(2.5)
        # Delete the message
        await message.delete()


client.run('NzE2NzAxNjk5MTQ1NzI4MDk0.XtWFiw.KZrh9Tkp9vTY9JYSgZfpg2P4mlQ')
