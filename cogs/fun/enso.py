import asyncio
import random
import string

from discord import Embed, Colour
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, command

import settings
from cogs.anime.interactive import error_function
from settings import time, colour_list


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
        title=f"**Look At What A Cutie {name.capitalize()} is!! <a:huh:676195228872474643> <a:huh:676195228872474643> **",
        colour=Colour(random.choice(colour_list)),
        timestamp=time)
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

        # Defining array of all the people that have images stored in the bot
        array = ['hammy', 'hussein', 'inna', 'kate',
                 'lukas', 'stitch', 'corona', 'ging',
                 'gria', 'lilu', 'ifrah', 'skye', 'chloe',
                 'connor', 'taz', 'ryder', 'ange', 'rin',
                 'izzy', 'david', 'clarity', 'angel']

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
                    await ctx.send(f"Sorry! That person doesn't exist!! Try the names listed below!")

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
                    timestamp=time)
                embed.set_image(url=random.choice(array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

                await ctx.send(embed=embed)

        else:

            message = await ctx.send(error_function())

            # Let the user read the message for 2.5 seconds
            await asyncio.sleep(2.5)
            # Delete the message
            await message.delete()


def setup(bot):
    bot.add_cog(Enso(bot))
