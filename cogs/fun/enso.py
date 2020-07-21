import asyncio
import datetime
import random
import string

from discord import Embed, Colour
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, command

import settings
from settings import colour_list, enso_guild_ID, enso_ensochancommands_Mention, blank_space, enso_embedmod_colours


# Error handling function to make sure that the commands only work in "enso-chan-commands"
def error_function():
    return f"**Sorry! I only work in {enso_ensochancommands_Mention}**"


# Send a message to the channel that Enso~Chan has dm'ed them!
def helpDm():
    hamothyID = '<@&715412394968350756>'

    # Returning F String to send to the User
    return f"I've just pinged your dms UwU! <a:huh:676195228872474643> <a:huh:676195228872474643>" \
           f"\nPlease ping my owner {hamothyID} for any issues/questions you have!"


# Method to retrieve information about the user and the guild
def get_user_info(self, ctx):
    # Allowing the bot to dm the user
    author = ctx.author

    # Define guild icon, enso bot icon and enso bot name
    guild_icon = ctx.guild.icon_url
    enso_icon = self.bot.user.avatar_url
    enso_name = self.bot.user.display_name

    return author, guild_icon, enso_icon, enso_name


# Gets the member and user avatar
def getMember(ctx):
    # Set member as the author
    member = ctx.message.author
    # Get the member avatar
    userAvatar = member.avatar_url

    return member, userAvatar


# Function to display all the images requested of the people
def displayServerImage(array, ctx, name):
    # Get the member and the userAvatar
    member, userAvatar = getMember(ctx)

    # Set embed up for the person requested by the user
    embed = Embed(
        title=f"**Look At What A Cutie {name.capitalize()} is! <a:huh:676195228872474643> <a:huh:676195228872474643> **",
        colour=Colour(random.choice(colour_list)),
        timestamp=datetime.datetime.utcnow())
    embed.set_image(url=random.choice(array))
    embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

    return embed


class Enso(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Bot ~ensoPerson command for the server members
    @command(name="enso", aliases=['Enso'])
    @cooldown(1, 1, BucketType.user)
    async def enso_person(self, ctx, name=None):

        # Making sure this command only works in Enso
        if not ctx.guild.id == enso_guild_ID:
            await ctx.send("**Sorry! That command is only for a certain guild!**")
            return

        # Defining array of all the people that have images stored in the bot
        array = ['hammy', 'hussein', 'inna', 'kate', 'calvin',
                 'lukas', 'stitch', 'corona', 'ging', 'ash',
                 'gria', 'lilu', 'ifrah', 'skye', 'chloe',
                 'connor', 'taz', 'ryder', 'ange', 'rin',
                 'izzy', 'david', 'clarity', 'angel', "studentjon"]

        # If the channel that the command has been sent is in the list of accepted channels
        if str(ctx.channel) in settings.channels:

            # if a name is specified
            if name:
                # Get the lowercase
                proper_name = name.lower()

                # Surround with try/except to catch any exceptions that may occur
                try:

                    # if the user does ~enso list
                    if proper_name == "list":
                        # Tell the user to try the names in the array
                        await ctx.send(f"Try the names listed below!")

                        # Send the list of members in the bot to the channel
                        server_members = string.capwords(', '.join(map(str, array)))
                        await ctx.send(server_members)

                    else:

                        # Retrieve image of the member specified
                        with open(f'images/ServerMembers/{proper_name}.txt') as file:
                            images_array = file.readlines()

                        # Embed the image into a message and send it to the channel
                        embed = displayServerImage(images_array, ctx, proper_name)
                        await ctx.send(embed=embed)

                except Exception as e:
                    print(e)

                    # Send error message saying that the person isn't recognised
                    await ctx.send(f"Sorry! That person doesn't exist! Try the names listed below!")

                    # Send the list of available members to the channel
                    nice = string.capwords(', '.join(map(str, array)))
                    await ctx.send(nice)

            # Else if the name is not specified
            else:

                # Retrieve a random image of a member in the bot
                with open(f'images/ServerMembers/{random.choice(array)}.txt') as file:
                    array = file.readlines()

                # Get the member and the userAvatar
                member, userAvatar = getMember(ctx)

                # Embed the image in a message and send it to the channel
                embed = Embed(
                    title=f"Oh Look! A Cute Person <a:huh:676195228872474643> <a:huh:676195228872474643> ",
                    colour=Colour(random.choice(colour_list)),
                    timestamp=datetime.datetime.utcnow())
                embed.set_image(url=random.choice(array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

                await ctx.send(embed=embed)

        else:

            message = await ctx.send(error_function())

            # Let the user read the message for 2.5 seconds
            await asyncio.sleep(2.5)
            # Delete the message
            await message.delete()

    @command(name="rules", aliases=["Rules"])
    @cooldown(1, 5, BucketType.user)
    async def rules(self, ctx):
        """Ruleset for Ensō"""

        # Making sure this command only works in Enso
        if not ctx.guild.id == enso_guild_ID:
            await ctx.send("**Sorry! That command is only for a certain guild!**")
            return

        # Define Izzy's roles ID
        izzyID = '<@397944038440828928>'

        # Get information about the user and the guild
        author, guild_icon, enso_icon, enso_name = get_user_info(self, ctx)

        # Set up embed to list all the rules within the server
        embed = Embed(title="(っ◔◡◔)っ Ensō Rules",
                      colour=enso_embedmod_colours,
                      description="ヽ(͡◕ ͜ʖ ͡◕)ﾉ Please respect the following rules that are going to be listed below ヽ(͡◕ ͜ʖ ͡◕)ﾉ",
                      timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url=guild_icon)
        embed.set_author(name=enso_name,
                         icon_url=enso_icon)

        fields = [
            (blank_space,
             "**➳ Don't be overly toxic/purposely problematic** \n This one is pretty self explanatory, just treat others the way you want to be treated and you'll get along with everyone :)",
             False),
            (blank_space,
             "**➳ Respect all admins and staff** \n They are enforcing these rules to help make and keep this server a fantastic place to hang out.",
             False),
            (blank_space,
             "**➳ Keep content organized into their respective channels** \n For example. When connected to a voice channel, all messages relating to the discussion in voice-chat should be sent in #vc-chat",
             False),
            (blank_space,
             "**➳ No advertising other servers** \nIt's disrespectful to do that and won't be tolerated in this server",
             False),
            (blank_space,
             "**➳ No pornographic/adult/other NSFW material** \n This is a community server and not meant to share this kind of material. Try to stay around PG 13 as most of our users are between 13 - 16",
             False),
            (blank_space,
             "**➳ Don't take insults too far** \n Poking fun at others is okay, just don't take it too far. Any disputes can be brought up to a staff member and they will handle it." +
             "\nIf you end up causing a problem or taking things into your in hands, you will be punished",
             False),
            (blank_space,
             "**➳ Explicit Language** \n Swearing is perfectly fine as long as it's not in excess, with some exceptions of course." +
             "These exceptions being racial, sexual, and ethnic slurs",
             False),
            (blank_space,
             "**➳ Discord ToS** \n As well as following the rules we have set forth, please make sure to follow Discord's ToS https://discordapp.com/terms ",
             False),
            (blank_space,
             "```( ͡°ω ͡°) Disciplinary Actions ( ͡°ω ͡°)```", False),
            (blank_space,
             "**➳ First Offense** \n Warning",
             True),
            (blank_space,
             "**➳ Second Offense** \n1 hour mute",
             True),
            (blank_space,
             "**➳ Third Offense** \n12 hour mute",
             True),
            (blank_space,
             "**➳ Fourth Offense** \n24 hour mute",
             True),
            (blank_space,
             "**➳Fifth Offense** \n Kicked from the server",
             True),
            (blank_space,
             "**➳ Sixth Offense** \n Banned from the server",
             True),
            (blank_space,
             "**➳ There are, of course, exceptions to these rules based on the severity of the offense Minor offenses will play out as described but major offenses will be dealt with at the discretion of the staff member involved.**",
             False),
            (blank_space,
             f"**➳ Any disputes about a staff members choices or actions can be brought to myself, {ctx.message.author.mention} or my co-owner, {izzyID}**",
             False)]

        # Add fields to the embed
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        # Dm the user the embedded message
        await author.send(embed=embed)

        # Send the helpDm() message to the channel that the user is in
        message = await ctx.send(helpDm())

        # Let the user read the message for 10 seconds
        await asyncio.sleep(10)
        # Delete the message
        await message.delete()

    @command(name="roles", aliases=["Roles"])
    @cooldown(1, 5, BucketType.user)
    async def roles(self, ctx):
        """Leveled role/xp system for Ensō"""

        if not ctx.guild.id == enso_guild_ID:
            await ctx.send("**Sorry! That command is only for a certain guild!**")
            return

        # Get the url of the leveled roles image
        roles_image = "https://media.discordapp.net/attachments/669812887564320769/717149671771996180/unknown.png"

        # Setting up embedded message about the leveled roles system within the server
        embed = Embed(title="```So you wanna know how the leveled roles system works huh?```",
                      colour=enso_embedmod_colours,
                      description="------------------------------------------------",
                      timestamp=datetime.datetime.utcnow())

        # Get information about the user and the guild
        author, guild_icon, enso_icon, enso_name = get_user_info(self, ctx)

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


def setup(bot):
    bot.add_cog(Enso(bot))
