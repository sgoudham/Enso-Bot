import asyncio
from datetime import datetime

import discord
from decouple import config
from discord.ext import commands

# Getting the Bot token from Environment Variables
API_TOKEN = config('DISCORD_TOKEN')

# Bot Prefix
client = commands.Bot(command_prefix='~')

# Instantiates a list for all the cogs
extensions = ['cogs.WaifuImages', 'cogs.FunCommands']

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


# Bot ~roles command allows for an embed message about
@client.command(aliases=["Rules", "rule", "Rule"])
@commands.has_any_role('Hamothy')
async def rules(ctx, target: discord.Member):
    try:
        embed = discord.Embed(title="```(っ◔◡◔)っ Ensō Rules```", colour=discord.Colour(0xFF69B4),
                              description="``` ヽ(͡◕ ͜ʖ ͡◕)ﾉ Please respect the following rules that are going to be listed below ヽ(͡◕ ͜ʖ ͡◕)ﾉ ```",
                              timestamp=datetime.utcfromtimestamp(1591394941))

        embed.set_thumbnail(url="https://media.discordapp.net/attachments/683490529862090814/715010931620446269"
                                "/image1.jpg?width=658&height=658")
        embed.set_author(name="Hamothy", icon_url="https://cdn.discordapp.com/attachments/689525645734182916"
                                                  "/718510466640642099/Rias_Gremory.png")
        embed.set_footer(text=f"{ctx.message.author}",
                         icon_url="https://media.discordapp.net/attachments/689525645734182916/718510466640642099/Rias_Gremory.png")
        embed.add_field(
            name="\u200b",
            value="**➳ Don't be overly toxic/purposely problematic**" +
                  "\n This one is pretty self explanatory, just treat others the way you want to be treated and you'll get along with everyone :)",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="**➳ Respect all admins and staff**" +
                  "\n They are enforcing these rules to help make and keep this server a fantastic place to hang out.",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="**➳ Keep content organized into their respective channels**" +
                  "\n For example. When connected to a voice channel, all messages relating to the discussion in voice-chat should be sent in #vc-chat",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="**➳ No advertising other servers**" +
                  "\nIt's disrespectful to do that and won't be tolerated in this server",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="**➳ No pornographic/adult/other NSFW material**" +
                  "\n This is a community server and not meant to share this kind of material. Try to stay around PG 13 as most of our users are between 13 - 16",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="**➳ Don't take insults too far**" +
                  "\n Poking fun at others is okay, just don't take it too far. Any disputes can be brought up to a staff member and they will handle it." +
                  "\nIf you end up causing a problem or taking things into your in hands, you will be punished",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="**➳ Explicit Language**" +
                  "\n Swearing is perfectly fine as long as it's not in excess, with some exceptions of course." +
                  "These exceptions being racial, sexual, and ethnic slurs",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="**➳ Discord ToS**" +
                  "\n As well as following the rules we have set forth, please make sure to follow Discord's ToS https://discordapp.com/terms ",
            inline=False)
        embed.add_field(
            name="\u200b \u200b ",
            value="```( ͡°ω ͡°) Disciplinary Actions ( ͡°ω ͡°)```",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="**➳ First Offense**" +
                  "\n Warning",
            inline=True)
        embed.add_field(
            name="\u200b",
            value="**➳ Second Offense**" +
                  "\n1 hour mute",
            inline=True)
        embed.add_field(
            name="\u200b",
            value="**➳ Third Offense**" +
                  "\n12 hour mute",
            inline=True)
        embed.add_field(
            name="\u200b",
            value="**➳ Fourth Offense**" +
                  "\n24 hour mute",
            inline=True)
        embed.add_field(
            name="\u200b",
            value="**➳Fifth Offense**" +
                  "\n Kicked from the server",
            inline=True)
        embed.add_field(
            name="\u200b",
            value="**➳ Sixth Offense**" +
                  "\n Banned from the server",
            inline=True)
        embed.add_field(
            name="\u200b",
            value="**➳ There are, of course, exceptions to these rules based on the severity of the offense. "
                  "Minor offenses will play out as described but major offenses will be dealt with at the discretion of the staff member involved.**",
            inline=False)
        embed.add_field(
            name="\u200b",
            value=f"**➳ Any disputes about a staff members choices or actions can be brought to myself, {ctx.message.author.mention} " +
                  f", or my co-owner, {target.mention}**",
            inline=False)

        await ctx.send(embed=embed)
    except Exception as e:
        print(e)


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
        text="---------------------------------------------------------------------------------")

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
