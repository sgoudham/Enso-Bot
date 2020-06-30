import asyncio
import datetime

from discord import Embed, Colour
from discord.ext import commands
from discord.ext.commands import command


# Set up the Cog
class CustomHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ~rules command allows for an embed message about the leveled roles and xp system
    @command(aliases=["Rules", "rule", "Rule"])
    async def rules(self, ctx):

        # Allowing the bot to dm the user
        author = ctx.author
        # Define Izzy's roles ID
        izzyID = '<@397944038440828928>'

        # Define guild icon, enso bot icon and enso bot name
        guild_icon = ctx.guild.icon_url
        enso_icon = self.bot.user.avatar_url
        enso_name = self.bot.user.display_name

        # Surround with try/except to catch any exceptions that may occur
        try:

            # Set up embed to list all the rules within the server
            embed = Embed(title="```(っ◔◡◔)っ Ensō Rules```",
                          colour=Colour(0xFF69B4),
                          description="``` ヽ(͡◕ ͜ʖ ͡◕)ﾉ Please respect the following rules that are going to be listed below ヽ(͡◕ ͜ʖ ͡◕)ﾉ ```",
                          timestamp=datetime.datetime.utcnow())

            embed.set_thumbnail(url=guild_icon)
            embed.set_author(name=enso_name,
                             icon_url=enso_icon)

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
    @command(aliases=["Roles"])
    async def roles(self, ctx):

        # Allowing the bot to dm the user
        author = ctx.author

        # Define guild icon, enso bot icon and enso bot name
        guild_icon = ctx.guild.icon_url
        enso_icon = self.bot.user.avatar_url
        enso_name = self.bot.user.display_name

        # Get the url of the leveled roles image
        roles_image = "https://media.discordapp.net/attachments/669812887564320769/717149671771996180/unknown.png"

        # Surround with try/except to catch any exceptions that may occur
        try:

            # Setting up embedded message about the leveled roles system within the server
            embed = Embed(title="```So you wanna know how the leveled roles system works huh?```",
                          colour=Colour(0xFF69B4),
                          description="------------------------------------------------",
                          timestamp=datetime.datetime.utcnow())

            embed.set_image(url=roles_image)
            embed.set_thumbnail(url=guild_icon)
            embed.set_author(name=enso_name,
                             icon_url=enso_icon)

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

            # Let the user read the message for 10 seconds
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
