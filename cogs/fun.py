# Ensō~Chan - A Multi Purpose Discord Bot That Has Everything Your Server Needs!
# Copyright (C) 2020  Goudham Suresh

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import datetime
import io
import random
import string
import textwrap
import urllib.parse
from typing import Optional

import discord
from PIL import Image, ImageDraw, ImageFont
from aiohttp import request
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, command, Cog
from discord.ext.commands import is_owner, bot_has_permissions
from owotext import OwO


def generate_meme(image_path, top_text, bottom_text='', font_path='images/homies/impact/Impacted.ttf', font_size=9):
    get_image = Image.open(image_path)
    draw = ImageDraw.Draw(get_image)
    image_width, image_height = get_image.size

    # Load font
    font = ImageFont.truetype(font=font_path, size=int(image_height * font_size) // 100)

    # Convert text to uppercase
    top_text = top_text.upper()
    bottom_text = bottom_text.upper()

    # Text wrapping
    char_width, char_height = font.getsize('A')
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(top_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)

    # Draw top lines
    y = 10
    for line in top_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        draw.text((x, y), line, fill='white', font=font)
        y += line_height

    # Draw bottom lines
    y = image_height - char_height * len(bottom_lines) - 15
    for line in bottom_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        draw.text((x, y), line, fill='white', font=font)
        y += line_height

    # Save meme as bytes
    file = io.BytesIO()
    get_image.save(file, format='PNG')
    file.seek(0)
    return file


# Set up the cog
class Fun(Cog):
    """Fun Commands! (8ball, Doggo etc!)"""

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        """Printing out that Cog is ready on startup"""
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @command(name="attack", hidden=True)
    @is_owner()
    async def attack(self, ctx, member: Member):
        """Throw Insults at Members"""

        # Set up array of insults to throw at people
        responses = [
            f"{member.mention} is stinky",
            f"{member.mention} is ugly",
            f"{member.mention} has a gigantic nose",
            f"{member.mention} gets no views on their tiktok",
            f"{member.mention} is obviously compensating for something :eyes:",
            f"{member.mention} DIE DIE DIE :knife: :skull:",
            f"{member.mention} is so annoying smh :rolling_eyes:",
            f"I'd say {member.mention} was dropped as a child but they would have to be held to be dropped in the first place",
            f"I hate {member.mention}",
            f"{member.mention} close your legs, it smells like clam chowder :face_vomiting: :face_vomiting: :nauseated_face: :nauseated_face:",
            f"I bet {member.mention} can't reach the wall cabinets without a booster chair",
            f"{member.mention} Browses 4Chan and Reddit all day looking for love",
            f"{member.mention} Your forehead could be used as a landing pad",
            f"I bet {member.mention} likes eating watermelon with the rind.",
            f"{member.mention} You were the first creation to make god say oops",
            f"{member.mention} You have delusions of adequacy",
            f"{member.mention} I treasure the time I don't spend with you",
            f"Don't be ashamed of yourself {member.mention}, that's your parent's job",
            f"I don't have the energy to pretend I like {member.mention} today",
            f"I know this was made for me to insult but it’s kinda hard to be a hateful cunt like {member.mention} :star_struck::star_struck:",
            f"#{member.mention}IsOverParty",
            f"I hope {member.mention} drops dead with a curable disease that doctors simply didn’t feel like curing :)",
            f"{member.mention} You know there's no vaccine for stupidity right?",
            f"{member.mention} You are not very epic at all",
            f"You make Kpop Fancams 24/7 for validation on the internet {member.mention}",
            f"Your mother wanted to drop you on the head when you were little {member.mention}",
            f"{member.mention} You're the CEO of Racism",
            f"{member.mention} has no common sense"
        ]

        # Sending out a random insult from the array "responses"
        await ctx.send(random.choice(responses))

    @command(name="comp")
    @cooldown(1, 1, BucketType.user)
    async def compliment(self, ctx, member: Member):
        """Give Compliments to Members"""

        # Set up array of compliments to throw at people
        responses = [
            f"{member.mention} is the most adorable uwu <:awie:676201100793085952> <:awie:676201100793085952> <:awie:676201100793085952>",
            f"{member.mention} You have my ENTIRE HEART <:blushlook1:677310734123663363> <:blushlook2:679524467248201769>",
            f"{member.mention} Hun you're CUTE uwu :pleading_face: :flushed: :pleading_face: :flushed: :pleading_face:",
            f"I love {member.mention} so so much :heartbeat: :heartbeat: :heartbeat: ",
            f"My heart is full of love for you {member.mention} <:Kawaii:676203363922214953> <:Kawaii:676203363922214953>",
            f"{member.mention} I admire your greatness so much that I consider making a fan club to become your #1 fan (´꒳`)",
            f"{member.mention} has no flaws, only special effects :))",
            f"{member.mention}'s smile is brighter than sunlight, so smile more often ( ◠‿◠ )",
            f"{member.mention} Your smile is so beautiful it blinds me :heart_eyes: :heart_eyes:",
            f"Being on a journey all my life, I will never meet a person as amazing as you are {member.mention}",
            f"Such a pleasure to be on the same server with {member.mention} <:boneappleteeth:676202300573876252> <:boneappleteeth:676202300573876252>",
            f"With {member.mention}, even the worst day will be filled with joy <:hug:718248629034549299> <:hug:718248629034549299>",
            f"There's no better antidepressant than {member.mention}",
            f"{member.mention} You're great, keep going Σd(˘ꇴ˘๑)",
            f"I'd simp for {member.mention} anyday :flushed: :heart_eyes: :flushed: ",
            f"{member.mention} Even the ugliest clothes won't ruin your look (｡•̀ᴗ -)☆",
            f"{member.mention} You’re that “nothing” when people ask me what I’m thinking about <:Kawaii:676203363922214953> <:Kawaii:676203363922214953>",
            f"{member.mention} Somehow you make time stop and fly at the same time <:awie:676201100793085952> <:blushlook1:677310734123663363>",
            f"{member.mention} is a whole ass SWAGMEAL <:Kawaii:676203363922214953> <:Kawaii:676203363922214953>",
            f"After meeting {member.mention}, I couldn't imagine living my life without them",
            f"Take me into your arms and tell me you love me <:blushlook1:677310734123663363> <:blushlook2:679524467248201769> {member.mention}",
            f"{member.mention} I would spend eternity cuddling with you :flushed: :flushed:",
            f"Would you want to go on an e-date together? :pleading_face: :point_right: :point_left: {member.mention}",
            f"Let me shoot my shot to you :see_no_evil: :see_no_evil: {member.mention}",
            f"Your existence makes me feel so much better {member.mention}",
            f"You're so hot, even hotter than hell :heart_eyes: {member.mention}",
            f"{member.mention} You’re so cute that Taz will simp for you anytime :flushed: :heart_eyes: :flushed:",
            f"{member.mention} The thought of you leaving me is too much to bear. Stay with me forever :pleading_face: :pleading_face:",
            f"You're... You're SHREKTACULAR :heart_eyes: :flushed: :heart_eyes: {member.mention}",
            f"{member.mention} Your beauty renders me speechless... :heart_eyes: :heart_eyes:",
            f"Your taste in music is impeccable {member.mention}",
            f"{member.mention} I can't stop thinking about you :see_no_evil: :see_no_evil:",
            f"{member.mention} Your wedding will be wonderful, but the y is silent <a:huh:676195228872474643> <a:huh:676195228872474643>",
            f"{member.mention} I would give up my lifelong goals just to have a chance with you <a:huh:676195228872474643> <a:huh:676195228872474643>",
            f"{member.mention} Will you be the **yee** to my **haw**? :pleading_face: :pleading_face:",
            f"{member.mention} is the definition of perfection :heart_eyes: :heart_eyes:",
            f"{member.mention} My love for you is bigger than the amount of code Hammy has written <:Kawaii:676203363922214953> <:Kawaii:676203363922214953> <:Kawaii:676203363922214953>",
            f"{member.mention} Why jump off a cliff when you can jump into my arms :flushed: :flushed:"
        ]

        # Sending out a random compliment from the array "responses"
        await ctx.send(random.choice(responses))

    @command(name="flip")
    @cooldown(1, 1, BucketType.user)
    async def flip(self, ctx):
        """Flip a Coin (Huge pp/Smol pp)"""

        # Define array with only 2 entries to create 50/50 chance
        pp_array = ["Smol pp", "Huge pp"]

        # Send out one of the responses stored in the array
        await ctx.send(f"{ctx.author.mention} {random.choice(pp_array)}")

    @command(name="digby", hidden=True)
    @cooldown(1, 1, BucketType.user)
    @bot_has_permissions(embed_links=True)
    async def digby(self, ctx):
        """Pictures of Digby!"""

        # Surround with try/except to catch any exceptions that may occur
        try:

            # Open the file containing the digby images
            with open('images/FunCommands/digby.txt') as file:
                # Store content of the file in digby_array
                digby_array = file.readlines()

            # Set member as the author
            member = ctx.message.author
            # Get the member avatar
            userAvatar = member.avatar_url

            # Set up the embed to display a random image of digby
            embed = Embed(
                title=f"**A cute picture of Digby!**",
                colour=self.bot.random_colour(),
                timestamp=datetime.datetime.utcnow())
            embed.set_image(url=random.choice(digby_array))
            embed.set_footer(text=f"Requested by {member}", icon_url=userAvatar)

            # Send the embedded message to the user
            await ctx.send(embed=embed)

        except FileNotFoundError as e:
            print(e)

    @command(name="doggo")
    @bot_has_permissions(embed_links=True)
    @cooldown(1, 1, BucketType.user)
    async def doggo(self, ctx, breed: Optional[str] = None):
        """Pictures of Doggos!"""

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
                        desc = f"Try the Breeds listed below!\n{doggo_string}"
                        await self.bot.generate_embed(ctx, desc=desc)

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
                            colour=self.bot.random_colour(),
                            timestamp=datetime.datetime.utcnow())
                        doggo_embed.set_image(url=image_link)
                        doggo_embed.set_footer(text=f"Requested by {member}", icon_url=userAvatar)

                        # Send the doggo image
                        await ctx.send(embed=doggo_embed)

                    else:

                        # Send error message that Doggo was not found!
                        desc = f"Doggo Not Found!\nPlease do **{ctx.prefix}doggo breeds** to see the full list of Doggos!"
                        await self.bot.generate_embed(ctx, desc=desc)
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
                        colour=self.bot.random_colour(),
                        timestamp=datetime.datetime.utcnow())
                    doggo_embed.set_image(url=image_link)
                    doggo_embed.set_footer(text=f"Requested by {member}", icon_url=userAvatar)

                    # Send random doggo image to the channel
                    await ctx.send(embed=doggo_embed)

                else:
                    # Send error message that Doggo was not found!
                    desc = f"Doggo Not Found!\nPlease do **{ctx.prefix}doggo breeds** to see the full list of Doggos!"
                    await self.bot.generate_embed(ctx, desc=desc)

    @command(name="8ball")
    @cooldown(1, 1, BucketType.user)
    async def _8ball(self, ctx, *, question):
        """8ball Responses!"""

        try:
            # Make the text readable to the api
            eightball_question = urllib.parse.quote(question)

            # Using API, make a connection to 8ball API
            async with request("GET", f"https://8ball.delegator.com/magic/JSON/{eightball_question}",
                               headers={}) as response:

                # With a successful connection
                # Get the answer
                if response.status == 200:
                    data = await response.json()
                    api_question = data["magic"]
                    api_answer = api_question["answer"]

            await ctx.send(api_answer)

        except commands.BadArgument as e:
            raise e

    @command(name="homies")
    @cooldown(1, 10, BucketType.user)
    @bot_has_permissions(attach_files=True)
    async def homies(self, ctx, *, text):
        """Summoning the Homies"""

        # Make sure the text entered is less than 20 characters
        if len(text) >= 20:
            await self.bot.generate_embed(ctx, desc="Please make sure the prompt is below **20** characters!")
            return
        else:

            # Define the text to be drawn on the top and the bottom
            top_text = f"Ayo fuck {text}"
            bottom_text = f"All my homies hate {text}"

            # Call the method to generate the image
            file = generate_meme('images/homies/AllMyHomies.jpg', top_text=top_text, bottom_text=bottom_text)

            # Send the bytes object as an image file
            await ctx.send(file=discord.File(file, "homies.png"))

    @command(name="owo", aliases=["uwu"])
    @cooldown(1, 1, BucketType.user)
    @bot_has_permissions(manage_messages=True)
    async def owo(self, ctx, *, text):
        """Converts given text to 'OwO' format"""

        # Delete the message sent by the user
        await ctx.message.delete()

        # Convert to "OwO" text
        uwu = OwO()
        owo = uwu.whatsthis(text)

        # Send the text back
        await ctx.message.channel.send(owo)

    @command(name="grayscale", aliases=["gs"])
    @cooldown(1, 5, BucketType.user)
    @bot_has_permissions(attach_files=True)
    async def image_to_text(self, ctx):
        """Display grayscale version of image uploaded"""

        if ctx.message.attachments:
            for attachments in ctx.message.attachments:
                attach = await attachments.read()
                image = Image.open(io.BytesIO(attach)).convert('LA')

                # Save new grayscale image as bytes
                file = io.BytesIO()
                image.save(file, format='PNG')
                file.seek(0)

                # Send Grayscale Image
                await ctx.send(file=discord.File(file, "gp.png"))
        else:
            await self.bot.generate_embed(ctx, desc="**Image Not Detected!**")


def setup(bot):
    bot.add_cog(Fun(bot))
