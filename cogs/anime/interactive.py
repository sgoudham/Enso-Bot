import asyncio
import random

from discord import Colour, Embed, Member
from discord.ext import commands
from discord.ext.commands import cooldown, command, BucketType

import db
import settings
from settings import time, colour_list, enso_ensochancommands_Mention


# Gets the member and user avatar
def getMember(ctx):
    # Set member as the author
    member = ctx.message.author
    # Get the member avatar
    userAvatar = member.avatar_url

    return member, userAvatar


# Error handling function to make sure that the commands only work in "enso-chan-commands"
def error_function():
    return f"**Sorry! I only work in {enso_ensochancommands_Mention}**"


# Set up the Cog
class Interactive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="kiss", aliases=["Kiss"])
    @cooldown(1, 1, BucketType.user)
    async def kiss(self, ctx, target: Member):
        """Allows users to kiss a person in the server"""

        # Use database connection
        with db.connection() as conn:

            # Get the author's row from the Members Table
            select_query = """SELECT * FROM members WHERE discordID = (?)"""
            val = ctx.author.id,
            cursor = conn.cursor()

            # Execute the SQL Query
            cursor.execute(select_query, val)
            result = cursor.fetchone()

            # Error handling to make sure that the user can kiss themselves
            if target.id == ctx.author.id:
                kiss = False
            else:
                kiss = True

        try:
            # Make sure the user isn't trying to kiss someone else besides their partner
            if result[2] is None and kiss:
                await ctx.send("Σ(‘◉⌓◉’) You need to be married in order to use this command! Baka!")
                return
            # Make sure that the married people can only kiss their partner
            elif not str(target.id) == result[2] and kiss:
                await ctx.send("Σ(‘◉⌓◉’) You can only kiss your partner! Baka!")
                return
        except Exception as ex:
            print(ex)

        # Surround with try/except to catch any exceptions that may occur
        try:

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in settings.channels:

                # Open the file containing the kissing gifs
                with open('images/FunCommands/kissing.txt') as file:
                    # Store content of the file in kissing_array
                    kissing_array = file.readlines()

                # Get the member and the userAvatar
                member, userAvatar = getMember(ctx)

                # Set up the embed to display a random kissing gif
                embed = Embed(
                    title=f"<a:huh:676195228872474643> <a:huh:676195228872474643> | **{member.display_name}** kissed **{target.display_name}**",
                    colour=Colour(int(random.choice(colour_list))),
                    timestamp=time)
                embed.set_image(url=random.choice(kissing_array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

                # Send the embedded message to the user
                await ctx.send(embed=embed)

            # else the command is sent in an invalid channel
            else:
                # Call error_function() and display it to the user
                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except FileNotFoundError as e:
            print(e)

    @command(name="kill", aliases=["Kill"])
    @cooldown(1, 1, BucketType.user)
    async def kill(self, ctx, target: Member):
        """Allows users to kill a person in the server"""

        # Surround with try/except to catch any exceptions that may occur
        try:

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in settings.channels:

                # Open the file containing the killing gifs
                with open('images/FunCommands/killing.txt') as file:
                    # Store content of the file in killing_array
                    killing_array = file.readlines()

                # Get the member and the userAvatar
                member, userAvatar = getMember(ctx)

                # Set up the embed to display a random killing gif
                embed = Embed(
                    title=f"<:monkaW:718960264896184380> <:monkaW:718960264896184380> | **{member.display_name}** killed **{target.display_name}**",
                    colour=Colour(int(random.choice(colour_list))),
                    timestamp=time)
                embed.set_image(url=random.choice(killing_array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

                # Send the embedded message to the user
                await ctx.send(embed=embed)

            # else the command is sent in an invalid channel
            else:
                # Call error_function() and display it to the user
                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except FileNotFoundError as e:
            print(e)

    @command(name="cuddle", aliases=["Cuddle"])
    @cooldown(1, 1, BucketType.user)
    async def cuddle(self, ctx, target: Member):
        """Allows users to cuddle a person in the server"""

        # Use database connection
        with db.connection() as conn:

            # Get the author's row from the Members Table
            select_query = """SELECT * FROM members WHERE discordID = (?)"""
            val = ctx.author.id,
            cursor = conn.cursor()

            # Execute the SQL Query
            cursor.execute(select_query, val)
            result = cursor.fetchone()

            # Error handling to make sure that the user can cuddle themselves
            if target.id == ctx.author.id:
                cuddle = False
            else:
                cuddle = True

        try:
            # Make sure the user isn't trying to cuddle someone else besides their partner
            if result[2] is None and cuddle:
                await ctx.send("Σ(‘◉⌓◉’) You need to be married in order to use this command! Baka!")
                return
            # Make sure that the married people can only cuddle their partner
            elif not str(target.id) == result[2] and cuddle:
                await ctx.send("Σ(‘◉⌓◉’) You can only kiss your partner! Baka!")
                return
        except Exception as ex:
            print(ex)

        # Surround with try/except to catch any exceptions that may occur
        try:

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in settings.channels:

                # Open the file containing the cuddling gifs
                with open('images/FunCommands/cuddling.txt') as file:
                    # Store content of the file in cuddling_array
                    cuddling_array = file.readlines()

                # Get the member and the userAvatar
                member, userAvatar = getMember(ctx)

                # Set up the embed to display a random cuddling gif
                embed = Embed(
                    title=f"<:blushlook1:677310734123663363> <:blushlook2:679524467248201769> | **{member.display_name}** cuddled **{target.display_name}**",
                    colour=Colour(int(random.choice(colour_list))),
                    timestamp=time)
                embed.set_image(url=random.choice(cuddling_array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

                # Send the embedded message to the user
                await ctx.send(embed=embed)

            # else the command is sent in an invalid channel
            else:
                # Call error_function() and display it to the user
                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except FileNotFoundError as e:
            print(e)

    @command(name="slap", aliases=["Slap"])
    @cooldown(1, 1, BucketType.user)
    async def slap(self, ctx, target: Member):
        """Allows users to slap a person in the server"""

        # Surround with try/except to catch any exceptions that may occur
        try:

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in settings.channels:

                # Open the file containing the cuddling gifs
                with open('images/FunCommands/slapping.txt') as file:
                    # Store content of the file in cuddling_array
                    slapping_array = file.readlines()

                # Get the member and the userAvatar
                member, userAvatar = getMember(ctx)

                # Set up the embed to display a random slapping gif
                embed = Embed(
                    title=f"<:baka:718942872061083678> <:baka:718942872061083678> | **{member.display_name}** slapped **{target.display_name}**",
                    colour=Colour(int(random.choice(colour_list))),
                    timestamp=time)
                embed.set_image(url=random.choice(slapping_array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

                # Send the embedded message to the user
                await ctx.send(embed=embed)

            # else the command is sent in an invalid channel
            else:
                # Call error_function() and display it to the user
                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except FileNotFoundError as e:
            print(e)

    @command(name="pat", aliases=["Pat"])
    @cooldown(1, 1, BucketType.user)
    async def pat(self, ctx, target: Member):
        """Allows users to cuddle a person in the server"""

        # Surround with try/except to catch any exceptions that may occur
        try:

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in settings.channels:

                # Open the file containing the patting gifs
                with open('images/FunCommands/patting.txt') as file:
                    # Store content of the file in patting_array
                    patting_array = file.readlines()

                # Get the member and the userAvatar
                member, userAvatar = getMember(ctx)

                # Set up the embed to display a random patting gif
                embed = Embed(
                    title=f"<:xoxo:679893117482303564> <:xoxo:679893117482303564> | **{member.display_name}** patted **{target.display_name} on the head**",
                    colour=Colour(int(random.choice(colour_list))),
                    timestamp=time)
                embed.set_image(url=random.choice(patting_array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

                # Send the embedded message to the user
                await ctx.send(embed=embed)

            # else the command is sent in an invalid channel
            else:
                # Call error_function() and display it to the user
                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except FileNotFoundError as e:
            print(e)

    @command(name="lemon", aliases=["Lemon"])
    @cooldown(1, 1, BucketType.user)
    async def lemon(self, ctx, target: Member):
        """Allows users to hand people lemons to members in the user"""

        lemon_array = ["https://media.discordapp.net/attachments/669812887564320769/720093589056520202/lemon.gif",
                       "https://media.discordapp.net/attachments/669812887564320769/720093575492272208/lemon2.gif",
                       "https://media.discordapp.net/attachments/718484280925224981/719629805263257630/lemon.gif"]

        # Surround with try/except to catch any exceptions that may occur
        try:

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in settings.channels:

                # Get the member and the userAvatar
                member, userAvatar = getMember(ctx)

                # Set up the embed to display a random lemon gif
                embed = Embed(
                    title=f"<a:huh:676195228872474643> <a:huh:676195228872474643> | **{member.display_name}** Gives A Lemon To **{target.display_name}**",
                    colour=Colour(int(random.choice(colour_list))),
                    timestamp=time)
                embed.set_image(url=random.choice(lemon_array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

                # Send the embedded message to the user
                await ctx.send(embed=embed)

                # else the command is sent in an invalid channel
            else:
                # Call error_function() and display it to the user
                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except FileNotFoundError as e:
            print(e)

    @command(name="choke", aliases=["Choke"])
    @cooldown(1, 1, BucketType.user)
    async def choke(self, ctx, target: Member):
        """Allows users to choke a person in the server"""

        # Surround with try/except to catch any exceptions that may occur
        try:

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in settings.channels:

                # Open the file containing the choking gifs
                with open('images/FunCommands/choking.txt') as file:
                    # Store content of the file in choking_array
                    choking_array = file.readlines()

                # Get the member and the userAvatar
                member, userAvatar = getMember(ctx)

                # Set up the embed to display a random choking gif
                embed = Embed(
                    title=f"<:qmq:676203031506976768> <:qmq:676203031506976768> | **{member.display_name}** choked **{target.display_name}**",
                    colour=Colour(int(random.choice(colour_list))),
                    timestamp=time)
                embed.set_image(url=random.choice(choking_array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

                # Send the embedded message to the user
                await ctx.send(embed=embed)

            # else the command is sent in an invalid channel
            else:
                # Call error_function() and display it to the user
                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except FileNotFoundError as e:
            print(e)

    @command(name="hug", aliases=["Hug"])
    @cooldown(1, 1, BucketType.user)
    async def hug(self, ctx, target: Member):
        """Allows users to hug a person in the server"""

        # Surround with try/except to catch any exceptions that may occur
        try:

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in settings.channels:

                # Open the file containing the hug gifs
                with open('images/FunCommands/hugging.txt') as file:
                    # Store content of the file in hugging_array
                    hugging_array = file.readlines()

                # Get the member and the userAvatar
                member, userAvatar = getMember(ctx)

                # Set up the embed to display a random hugging gif
                embed = Embed(
                    title=f"<a:huh:676195228872474643> <a:huh:676195228872474643> | **{member.display_name}** hugged **{target.display_name}**",
                    colour=Colour(int(random.choice(colour_list))),
                    timestamp=time)
                embed.set_image(url=random.choice(hugging_array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

                # Send the embedded message to the user
                await ctx.send(embed=embed)

            # else the command is sent in an invalid channel
            else:
                # Call error_function() and display it to the user
                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except FileNotFoundError as e:
            print(e)


def setup(bot):
    bot.add_cog(Interactive(bot))


"""
                if str(ctx.author.id) == row[1] and str(member.id) == row[2]:
                    member = guild.get_member(int(row[2]))
                    await ctx.send(f"You and {member.mention} are married!")
                    return
                elif str(ctx.author.id) != row[1] and str(member.id) == row[2]:
                    member = guild.get_member(int(row[2]))
                    author = guild.get_member(int(row[1]))
                    await ctx.send(f"Sorry! {member.mention} is already married to {author.mention}!")
                elif str(ctx.author.id) != row[1] and str(member.id) == row[1]:
                    member = guild.get_member(int(row[2]))
                    author = guild.get_member(int(row[1]))
                    await ctx.send(f"Sorry! {author.mention} is already married to {member.mention}!")
                    return
                elif str(ctx.author.id) == row[1]:
                    member = guild.get_member(int(row[2]))
                    await ctx.send(f"Sorry! You're currently married to {member.mention}")
                    return
                elif str(ctx.author.id) == row[2]:
                    member = guild.get_member(int(row[1]))
                    await ctx.send(f"Sorry! You're currently married to {member.mention}")
                    return
                elif str(member.id) == row[1]:
                    member = guild.get_member(int(row[2]))
                    await ctx.send(f"Sorry! You're currently married to {ctx.author.mention}")
                    return
                elif str(member.id) == row[2]:
                    member = guild.get_member(int(row[1]))
                    await ctx.send(f"Sorry! You're currently married to {ctx.author.mention}")
                    return
"""
