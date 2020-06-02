import discord
import random
from discord.ext import commands

client = commands.Bot(command_prefix = '~')

@client.event
async def on_ready():
    print('Bot is ready.')
    await client.change_presence(activity=discord.Game(name='Reading Yaoi'))

@client.event
async def on_member_join(member):
    print (f'{member} has joined the server')

@client.event
async def on_member_removed(member):
    print (f'{member} has has left the server')

@client.command(aliases = ["ping"])
@commands.has_any_role('Hamothy')
async def Ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases = ['8ball'])
async def _8ball(ctx, *, question):
    Responses = ["Hamothy is preoccupied with catching a case",
                 "Kate decides it will come true",
                 "Josh doesn't believe",
                 "Izzy can't predict this",
                 "Idk idiot lmao",
                 "Why are you even asking me",
                 "Tt's not like I can read your question",
                 "Shut the fuck up NOW",
                 "Zara wants to protest your question",
                 "Stitch will definitely get back to you",
                 "*Kakashi slams you to the wall*",
                 "Kate is too busy reading yaoi to answer your question",
                 "Marshall says Yes",
                 "It- It's not lik- It's not like I want to answer your question or anything *tsundere noises*",
                 "Connor is too busy making tea and simping for beautiful women to reply to this",
                 "Maybe",
                 "Who said you could ask that question?",
                 "Ifrah cannot answer that",
                 "Hussein be spitting too much fire to look at your weak ass question",
                 "Literally no one gives a shit",
                 "N O spells NO",
                 "Find something better to do with your spare time smh",
                 "Sure but did you know that Izzy smells?",
                 "No but did you know that Stitch smells?",
                 "Get your dick back in your pants smh",
                 "Get the fuck back to horny jail RIGHT NOW"]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(Responses)}')

@client.command()
@commands.has_any_role('Hamothy')
async def roles(ctx):
    embed = discord.Embed(title="```So you wanna know how the leveled roles system works huh?```", colour=discord.Colour(0x30e419), description="------------------------------------------------")

    embed.set_image(url="https://media.discordapp.net/attachments/669812887564320769/717149671771996180/unknown.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/683490529862090814/715010931620446269/image1.jpg")
    embed.set_author(name="Hamothy", icon_url="https://cdn.discordapp.com/attachments/689525645734182916/717137453651066900/Rias_Gremory.png")
    embed.set_footer(text="-------------------------------------------------------------------------------------------------------")

    embed.add_field(name = "Cooldown", value="**•XP is gained every time you talk with a 2 minute cooldown.**", inline=True),
    embed.add_field(name = "Message Length",value = "**•XP is not determined by the size of the message. You will not get more XP just because the message is bigger.**", inline = True),
    embed.add_field(name = "Roles",value="**•As seen below, those are the colours and roles that will be achieved upon gaining that amount of experience**", inline = True)

    await ctx.send(embed=embed)


client.run('NzE2NzAxNjk5MTQ1NzI4MDk0.XtWFiw.KZrh9Tkp9vTY9JYSgZfpg2P4mlQ')