import datetime
import random
import string

from aiohttp import request
from discord import Colour, Embed
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, command

from settings import colour_list


# Set up the cog
class Doggo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="doggo", aliases=["Doggo"])
    @cooldown(1, 1, BucketType.user)
    async def doggo(self, ctx, breed=None):
        """Allows an API to grab images of dogs"""

        # Set member as the author
        member = ctx.message.author
        # Get the member avatar
        userAvatar = member.avatar_url

        # Initialise array to store doggo pics
        b_list = []

        # If a breed if specified
        if breed:
            # Get the lowercase string input
            lowercase_breed = breed.lower()

            # If the user wants to know what breeds there are
            if lowercase_breed == "breeds":
                # Get the list of breeds
                breed_url = "https://dog.ceo/api/breeds/list/all"

                # Using API, retrieve the full list of breeds available
                async with request("GET", breed_url, headers={}) as response:
                    if response.status == 200:
                        data = await response.json()
                        breed_link = data["message"]

                        # Store every Doggo in an array
                        for doggo in breed_link:
                            b_list.append(doggo)

                        # Join together all the breeds into a string
                        doggo_string = string.capwords(", ".join(b_list))

                        # Tell the user to try the breeds listed below
                        await ctx.send(f"Try the Breeds listed below!\n{doggo_string}")

            # If no breed has been specified
            else:

                # Grab a random image of a doggo with the breed specified
                image_url = f"https://dog.ceo/api/breed/{lowercase_breed}/images/random"

                # Using API, retrieve the image of a doggo of the breed specified
                async with request("GET", image_url, headers={}) as response:
                    if response.status == 200:
                        data = await response.json()
                        image_link = data["message"]

                        # Set up the embed for a doggo image
                        doggo_embed = Embed(
                            title=f"**It's a {lowercase_breed.capitalize()} Doggo!!** ",
                            colour=Colour(random.choice(colour_list)),
                            timestamp=datetime.datetime.utcnow())
                        doggo_embed.set_image(url=image_link)
                        doggo_embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

                        # Send the doggo image
                        await ctx.send(embed=doggo_embed)

                    else:

                        # Send error message that Doggo was not found!
                        await ctx.send(
                            "Doggo Not Found! Please do **~doggo `breeds`** to see the full list of Doggos!")
        else:

            # Grab a random image of a doggo of any breed
            image_url = "https://dog.ceo/api/breeds/image/random"

            # Using API, retrieve the image of a doggo of any breed
            async with request("GET", image_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["message"]

                    # Set up the embed for a random doggo image
                    doggo_embed = Embed(
                        title=f"**Doggo!** ",
                        colour=Colour(random.choice(colour_list)),
                        timestamp=datetime.datetime.utcnow())
                    doggo_embed.set_image(url=image_link)
                    doggo_embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

                    # Send random doggo image to the channel
                    await ctx.send(embed=doggo_embed)

                else:

                    # Send error message that Doggo was not found!
                    await ctx.send(
                        "Doggo Not Found! Please do **~doggo `breeds`** to see the full list of Doggos!")


def setup(bot):
    bot.add_cog(Doggo(bot))
