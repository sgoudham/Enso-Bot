import asyncio
import datetime

import discord
from discord.ext import commands


# Set up the Cog
class CustomHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ~help command allows the user to look at the list of commands
    @commands.command(aliases=["Help"])
    async def help(self, ctx):

        # Allowing the bot to dm the user
        author = ctx.message.author

        # Surround with try/except to catch any exceptions that may occur
        try:

            # Set up embed to list all the commands within the bot
            embed = discord.Embed(title="```(っ◔◡◔)っ Ensō Commands```", colour=discord.Colour.orange())

            embed.timestamp = datetime.datetime.utcnow()

            embed.set_thumbnail(url="https://media.discordapp.net/attachments/683490529862090814/715010931620446269"
                                    "/image1.jpg?width=658&height=658")
            embed.set_author(name="Hamothy", icon_url="https://cdn.discordapp.com/attachments/689525645734182916"
                                                      "/718510466640642099/Rias_Gremory.png")
            embed.set_footer(text=f"{ctx.message.author}",
                             icon_url="https://media.discordapp.net/attachments/689525645734182916/718510466640642099/Rias_Gremory.png")
            embed.add_field(
                name="\u200b",
                value="```css" +
                      "\n ( ͡°ω ͡°) Fun Commands ( ͡°ω ͡°)" +
                      "```",
                inline=False)
            embed.add_field(
                name="\u200b",
                value="**➳ ~attack [person]**" +
                      "\n Allows the user to throw an insult to a person in the server" +
                      "\n *(Perms: Co-Owner)*",
                inline=True)
            embed.add_field(
                name="\u200b",
                value="**➳ ~compliment [person]**" +
                      "\n Allows the user to compliment a person in the server" +
                      "\n *(Perms: Everyone)*",
                inline=True)
            embed.add_field(
                name="\u200b\u200b",
                value="**➳ ~8ball [text]**" +
                      "\n Allows the user to ask a question and 8ball will give a custom response" +
                      "\n *(Perms: everyone)*",
                inline=True)
            embed.add_field(
                name="\u200b\u200b",
                value="**➳ ~owo [text]**" +
                      "\n Converts the sentence typed into 'owo' text " +
                      "\n *(Perms: everyone)*",
                inline=True)
            embed.add_field(
                name="\u200b",
                value="**➳ ~lemon [person]**" +
                      "\n Allows the user to give a lemon to a person in the server" +
                      "\n *(Perms: Everyone)*",
                inline=True)
            embed.add_field(
                name="\u200b",
                value="**➳ ~slap [person]**" +
                      "\n Allows the user to slap a person in the server" +
                      "\n *(Perms: Everyone)*",
                inline=True)
            embed.add_field(
                name="\u200b",
                value="**➳ ~kill [person]**" +
                      "\n Allows the user to kill a person in the server" +
                      "\n *(Perms: Everyone)*",
                inline=True)
            embed.add_field(
                name="\u200b",
                value="**➳ ~pat [person]**" +
                      "\n Allows the user to pat a person in the server" +
                      "\n *(Perms: Everyone)*",
                inline=True)
            embed.add_field(
                name="\u200b",
                value="**➳ ~kiss [person]**" +
                      "\n Allows the user to kiss a person in the server" +
                      "\n *(Perms: Everyone)*",
                inline=True)
            embed.add_field(
                name="\u200b",
                value="**➳ ~cuddle [person]**" +
                      "\n Allows the user to cuddle a person in the server" +
                      "\n *(Perms: Everyone)*",
                inline=True)
            embed.add_field(
                name="\u200b",
                value="**➳ ~flip**" +
                      "\n Allows the user to 'throw a coin' and get a response with a 50/50 chance" +
                      "\n *(Perms: Everyone)*",
                inline=True)
            embed.add_field(
                name="\u200b",
                value="**➳ ~doggo**" +
                      "\n Allows the user to look at an image of a doggo (Over 20k Images Available" +
                      "\n *(Perms: Everyone)*",
                inline=True)
            embed.add_field(
                name="\u200b",
                value="```css" +
                      "\n ( ͡°ω ͡°) Waifus/Husbando Commands ( ͡°ω ͡°)" +
                      "```",
                inline=False)
            embed.add_field(
                name="\u200b\u200b",
                value="**➳ ~w [waifu]**" +
                      "\n Allows for a randomly generated image of a Waifu to be shown" +
                      "\n *(Perms: Everyone)*",
                inline=True)
            embed.add_field(
                name="\u200b\u200b",
                value="**➳ ~h [husbando]**" +
                      "\n Allows for a randomly generated image of a Husbando to be shown" +
                      "\n *(Perms: Everyone)*",
                inline=True)
            embed.add_field(
                name="\u200b\u200b",
                value="**➳ ~w list**" +
                      "\n Returns a list of Waifu's that are in the bot " +
                      "\n *(Perms: Everyone)*",
                inline=True)
            embed.add_field(
                name="\u200b\u200b",
                value="**➳ ~h list**" +
                      "\n Returns a list of Husbando's that are in the bot " +
                      "\n *(Perms: Everyone)*",
                inline=True)
            embed.add_field(
                name="\u200b\u200b",
                value="**➳ ~enso [person]**" +
                      "\n Allows for a randomly generated image of the member specified" +
                      "\n (Using ~enso by itself shall generate a random image of a person within all the server)" +
                      "\n *(Perms: Everyone)*",
                inline=True)
            embed.add_field(
                name="\u200b\u200b",
                value="**➳ ~enso list**" +
                      "\n Returns a list of the people's images currently in the bot" +
                      "\n *(Perms: Everyone)*",
                inline=True)
            embed.add_field(
                name="\u200b",
                value="```css" +
                      "\n ( ͡°ω ͡°) Misc Commands ( ͡°ω ͡°)" +
                      "```",
                inline=False)
            embed.add_field(
                name="\u200b\u200b",
                value="**➳ ~ping**" +
                      "\n Returns Pong! Along With The Latency in ms" +
                      "\n *(Perms: Co-Owner)*",
                inline=True)
            embed.add_field(
                name="\u200b\u200b",
                value="**➳ ~rolemenu**"
                      "\n Allows for the users to get self ping-able roles" +
                      "\n *(Perms: Co-Owner)*",
                inline=True)
            embed.add_field(
                name="\u200b\u200b",
                value="**➳ ~dm [person]**" +
                      "\n Allows Hammmy to dm anyone in the server through Enso~Chan!" +
                      "\n *(Perms: Co-Owner)*",
                inline=True)
            embed.add_field(
                name="\u200b",
                value="**➳ ~rules**" +
                      "\n Returns the entire ruleset for the server" +
                      "\n *(Perms: Everyone)*",
                inline=True)
            embed.add_field(
                name="\u200b",
                value="**➳ ~roles**" +
                      "\n Shows you how the leveling and xp system works, as well as displaying the order of leveled roles" +
                      "\n *(Perms: Everyone)*",
                inline=True)
            embed.add_field(
                name="\u200b\u200b",
                value="**➳ ~remindme [time] [text]**" +
                      "\n Allows the user to get Enso~Chan to remind them in dms of anything that they want" +
                      "\n *(Perms: Everyone)*",
                inline=True)

            # Dm the user the embedded message
            await author.send(embed=embed)

            # Send the helpDm() message to the channel that the user is in
            message = await ctx.send(helpDm())

            # Let the user read the message for 2.5 seconds
            await asyncio.sleep(10)
            # Delete the message
            await message.delete()

        except Exception as e:
            print(e)

    # ~rules command allows for an embed message about the leveled roles and xp system
    @commands.command(aliases=["Rules", "rule", "Rule"])
    async def rules(self, ctx):

        # Allowing the bot to dm the user
        author = ctx.message.author
        # Define Izzy's roles ID
        izzyID = '<@397944038440828928'

        # Surround with try/except to catch any exceptions that may occur
        try:

            # Set up embed to list all the rules within the server
            embed = discord.Embed(title="```(っ◔◡◔)っ Ensō Rules```", colour=discord.Colour(0xFF69B4),
                                  description="``` ヽ(͡◕ ͜ʖ ͡◕)ﾉ Please respect the following rules that are going to be listed below ヽ(͡◕ ͜ʖ ͡◕)ﾉ ```")

            embed.timestamp = datetime.datetime.utcnow()

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
                      f", or my co-owner, {izzyID}**",
                inline=False)

            # Dm the user the embedded message
            await author.send(embed=embed)

            # Send the helpDm() message to the channel that the user is in
            message = await ctx.send(helpDm())

            # Let the user read the message for 2.5 seconds
            await asyncio.sleep(10)
            # Delete the message
            await message.delete()

        except Exception as e:
            print(e)

    # ~roles command allows for an embed message about roles
    @commands.command(aliases=["Roles"])
    async def roles(self, ctx):

        # Allowing the bot to dm the user
        author = ctx.message.author

        # Surround with try/except to catch any exceptions that may occur
        try:

            # Setting up embedded message about the leveled roles systme within the server
            embed = discord.Embed(title="```So you wanna know how the leveled roles system works huh?```",
                                  colour=discord.Colour(0x30e419),
                                  description="------------------------------------------------")

            embed.timestamp = datetime.datetime.utcnow()

            embed.set_image(
                url="https://media.discordapp.net/attachments/669812887564320769/717149671771996180/unknown.png")
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/683490529862090814/715010931620446269/image1.jpg")
            embed.set_author(name="Hamothy",
                             icon_url="https://cdn.discordapp.com/attachments/689525645734182916/717137453651066900"
                                      "/Rias_Gremory.png")
            embed.set_footer(
                text="---------------------------------------------------------------------------------")

            embed.add_field(name="Cooldown", value="**•XP is gained every time you talk with a 2 minute cooldown.**",
                            inline=False),
            embed.add_field(name="Message Length",
                            value="**•XP is not determined by the size of the message. You will not get more XP just because "
                                  "the message is bigger.**",
                            inline=False),
            embed.add_field(name="Roles",
                            value="**•As seen below, those are the colours and roles that will be achieved upon gaining that "
                                  "amount of experience**",
                            inline=False)

            # Dm the user the embedded message
            await author.send(embed=embed)

            # Send the helpDm() message to the channel that the user is in
            message = await ctx.send(helpDm())

            # Let the user read the message for 2.5 seconds
            await asyncio.sleep(10)
            # Delete the message
            await message.delete()

        except Exception as e:
            print(e)


# Send a message to the channel that Enso~Chan has dm'ed them!
def helpDm():
    hamothyID = '<@&715412394968350756>'

    return f"I've just pinged your dms UwU! <a:huh:676195228872474643> <a:huh:676195228872474643>" \
           f"\nPlease ping my owner {hamothyID} for any issues/questions you have!"


def setup(bot):
    bot.add_cog(CustomHelp(bot))
