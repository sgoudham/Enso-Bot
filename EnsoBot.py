import discord
import random
from discord.ext import commands

# Bot Prefix
client = commands.Bot(command_prefix='~')


# Bot Status on Discord
@client.event
async def on_ready():
    print('Bot is ready.')
    await client.change_presence(activity=discord.Game(name='Reading Yaoi'))


# Bot ~Ping command in milliseconds
@client.command(aliases=["ping"])
@commands.has_any_role('Hamothy')
async def Ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


# Bot ~8Ball command
@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    Responses = ["Hamothy is preoccupied with catching a case",
                 "Kate decides it will come true",
                 "Josh doesn't believe",
                 "Izzy can't predict this",
                 "Idk idiot lmao",
                 "Why are you even asking me",
                 "It's not like I can read your question",
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
                 "Get the fuck back to horny jail RIGHT NOW",
                 "Nick Cock Bro",
                 "Nice Tits"]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(Responses)}')


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
                     icon_url="https://cdn.discordapp.com/attachments/689525645734182916/717137453651066900/Rias_Gremory.png")
    embed.set_footer(
        text="-------------------------------------------------------------------------------------------------------")

    embed.add_field(name="Cooldown", value="**•XP is gained every time you talk with a 2 minute cooldown.**",
                    inline=True),
    embed.add_field(name="Message Length",
                    value="**•XP is not determined by the size of the message. You will not get more XP just because the message is bigger.**",
                    inline=True),
    embed.add_field(name="Roles",
                    value="**•As seen below, those are the colours and roles that will be achieved upon gaining that amount of experience**",
                    inline=True)

    await ctx.send(embed=embed)

#Bot ~Kakashi command for Zara
@client.command(aliases=['kakashi'])
async def Kakashi(ctx):
    kakashi1 = "https://cdn.discordapp.com/attachments/714671068941647933/717201077346238514/image0.jpg"
    kakashi2 = "https://cdn.discordapp.com/attachments/714671068941647933/717201077669331036/image1.jpg"
    kakashi3 = "https://cdn.discordapp.com/attachments/714671068941647933/717201077941829722/image2.jpg"
    kakashi4 = "https://cdn.discordapp.com/attachments/714671068941647933/717201078633889913/image4.jpg"
    kakashi5 = "https://cdn.discordapp.com/attachments/714671068941647933/717201078885810176/image5.jpg"
    kakashi6 = "https://cdn.discordapp.com/attachments/714671068941647933/717203540048871456/40964a8ec3616dd143db1ac63c4090ee.jpg"
    kakashi7 = "https://media.discordapp.net/attachments/714671068941647933/717203546772340846/4707601f950c412dd6978c8264308632.jpg"
    kakashi8 = "https://media.discordapp.net/attachments/714671068941647933/717203597774946354/7941b52067df70825ae3a9051acfd98d.jpg"
    kakashi9 = "https://media.discordapp.net/attachments/714671068941647933/717203650333900840/dafb0bc78adc3548e9c9b24460d7c10d.jpg"
    kakashi10 = "https://media.discordapp.net/attachments/714671068941647933/717203693925040188/aad4edeac8e034683b5602cf01a41333.jpg?width=465&height=658"
    kakashi11 = "https://media.discordapp.net/attachments/714671068941647933/717203717085986836/5851485577679be2a09bdebef7e35522.jpg?width=390&height=658"
    kakashi12 = "https://media.discordapp.net/attachments/714671068941647933/717203783016513626/e2a746123c1e36d995fa95c44a3c3f85.jpg"
    kakashi13 = "https://media.discordapp.net/attachments/714671068941647933/717203811923394611/268a3266d4c255b72925a3eb541f4cf5.jpg?width=517&height=657"
    kakashi14 = "https://media.discordapp.net/attachments/714671068941647933/717203866986479636/b283f71be006957107926e1d5d9ab60e.jpg?width=591&height=658"
    kakashi15 = "https://cdn.discordapp.com/attachments/714671068941647933/717203972925947984/6f46bb96761b673f1c4f4b5584bf1ba8.jpg"
    kakashi16 = "https://cdn.discordapp.com/attachments/714671068941647933/717204020711915581/4025c1241a206406555bd6ab53640291.jpg"
    kakashi17 = "https://cdn.discordapp.com/attachments/714671068941647933/717204198491422770/94287174f2f5e5316144981190a38c66.jpg"
    kakashi18 = "https://cdn.discordapp.com/attachments/714671068941647933/717204289755283547/a9868fb38857dd51ccc93a3e202644ff.gif"
    kakashi19 = "https://cdn.discordapp.com/attachments/714671068941647933/717204351638175784/3967dabc9b069080daded9a38f1d9e49.jpg"
    kakashi20 = "https://cdn.discordapp.com/attachments/714671068941647933/717204405178597396/3d063a07af0cfa320a100e169c959ff4.jpg"
    kakashi21 = "https://cdn.discordapp.com/attachments/714671068941647933/717204454264537151/4c607bbcc9a360257e1d14b5c9858b21.jpg"
    kakashi22 = "https://cdn.discordapp.com/attachments/714671068941647933/717204495939141692/9d85777e4a452f2f38464f8a11dece5b.jpg"
    kakashi23 = "https://cdn.discordapp.com/attachments/714671068941647933/717204530760122478/edeaa333ed2fb68aa1205a783d0bb783.jpg"
    kakashi24 = "https://cdn.discordapp.com/attachments/714671068941647933/717204561936252958/4f39f6de439a99b4113f6a33fd803079.jpg"
    kakashi25 = "https://cdn.discordapp.com/attachments/714671068941647933/717204627484967012/ebb8b6713aff32745503d6cbe8996569.jpg"
    kakashi26 = "https://cdn.discordapp.com/attachments/714671068941647933/717204713648685126/a6cb9a07745c163d14d736e077765ec8.gif"
    kakashi27 = "https://cdn.discordapp.com/attachments/714671068941647933/717204734905417738/3a081283ef670fd5326a694b7d41d35d.jpg"
    kakashi28 = "https://cdn.discordapp.com/attachments/714671068941647933/717204879155921006/864704a29ef1201f78f7f8fd71f57cf7.gif"
    kakashi29 = "https://cdn.discordapp.com/attachments/714671068941647933/717204999792361472/d9b273a711ccf1e6af531443a4cf06b5.jpg"
    kakashi30 = "https://cdn.discordapp.com/attachments/714671068941647933/717205121259405332/d2426eff482c18af2586e1fd2499d3d5.jpg"
    kakashi31 = "https://cdn.discordapp.com/attachments/714671068941647933/717205186463924224/7e27f5a97a80444ab5fc773e4d09d1bb.jpg"
    kakashi32 = "https://cdn.discordapp.com/attachments/714671068941647933/717205371835514930/IMG_20191212_215715_438.jpg"
    kakashi33 = "https://cdn.discordapp.com/attachments/714671068941647933/717205515519655976/df09731e2b38c1f50cc57f4600d937f5.jpg"
    kakashi34 = "https://cdn.discordapp.com/attachments/714671068941647933/717206154882842695/image0.jpg"
    kakashi35 = "https://cdn.discordapp.com/attachments/714671068941647933/717206155356798986/image1.jpg"
    kakashi36 = "https://cdn.discordapp.com/attachments/714671068941647933/717206155562057780/image2.jpg"
    kakashi37 = "https://cdn.discordapp.com/attachments/714671068941647933/717206155797200896/image3.jpg"
    kakashi38 = "https://cdn.discordapp.com/attachments/714671068941647933/717206156031819786/image4.jpg"
    kakashi39 = "https://cdn.discordapp.com/attachments/714671068941647933/717206156191334460/image5.jpg"
    kakashi40 = "https://cdn.discordapp.com/attachments/714671068941647933/717206156673679380/image6.gif"

    kakashiArray = [kakashi1, kakashi2, kakashi3, kakashi4, kakashi5, kakashi6, kakashi7, kakashi8, kakashi9, kakashi10,
                    kakashi11, kakashi12, kakashi13, kakashi14, kakashi15, kakashi16, kakashi17, kakashi18, kakashi19, kakashi20,
                    kakashi21, kakashi22, kakashi23, kakashi24, kakashi25, kakashi26, kakashi27, kakashi28, kakashi29, kakashi30,
                    kakashi31, kakashi32, kakashi33, kakashi34, kakashi35, kakashi36, kakashi37, kakashi38, kakashi39, kakashi40]

    embed = discord.Embed(title="```Random Kakashi Image```", colour=discord.Colour(0xff0000),)
    embed.set_image(url=random.choice(kakashiArray))
    await ctx.send(embed=embed)


client.run('NzE2NzAxNjk5MTQ1NzI4MDk0.XtWFiw.KZrh9Tkp9vTY9JYSgZfpg2P4mlQ')
