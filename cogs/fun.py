import asyncio
import datetime
import random
import string
import textwrap
import urllib.parse

import discord
from PIL import Image, ImageDraw, ImageFont
from aiohttp import request
from discord import Member, Colour, Embed
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, command, has_permissions
from discord.ext.commands import is_owner, bot_has_permissions
from owotext import OwO

from settings import colour_list


def generate_meme(image_path, top_text, bottom_text='', font_path='homies/impact/Impacted.ttf', font_size=9):
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

    # Save meme
    get_image.save("AllMyHomiesHateMeme.jpg")


# Set up the cog
class Fun(commands.Cog):
    """Fun Commands! (8ball, Doggo etc!)"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Printing out that Cog is ready on startup"""
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @command(name="attack", aliases=['Attack'], hidden=True)
    @is_owner()
    async def attack(self, ctx, target: Member):
        """Throw Insults at Members"""

        # Set up array of insults to throw at people
        responses = [
            f"{target.mention} is stinky",
            f"{target.mention} is ugly",
            f"{target.mention} has a gigantic nose",
            f"{target.mention} gets no views on their tiktok",
            f"{target.mention} is obviously compensating for something :eyes:",
            f"{target.mention} DIE DIE DIE :knife: :skull:",
            f"{target.mention} is so annoying smh :rolling_eyes:",
            f"I'd say {target.mention} was dropped as a child but they would have be to held to dropped in the first place",
            f"I hate {target.mention}",
            f"{target.mention} close your legs, it smells like clam chowder :face_vomiting: :face_vomiting: :nauseated_face: :nauseated_face:",
            f"I bet {target.mention} can't reach the wall cabinets without a booster chair",
            f"{target.mention} Browses 4Chan and Reddit all day looking for love",
            f"{target.mention} Your forehead could be used as a landing pad",
            f"I bet {target.mention} likes eating watermelon with the rind.",
            f"{target.mention} You were the first creation to make god say oops",
            f"{target.mention} You have delusions of adequacy",
            f"{target.mention} I treasure the time I don't spend with you",
            f"Don't be ashamed of yourself {target.mention}, that's your parent's job",
            f"I don't have the energy to pretend I like {target.mention} today",
            f"I know this was made for me to insult but it’s kinda hard to be a hateful cunt like {target.mention} :star_struck::star_struck:",
            f"#{target.mention}IsOverParty",
            f"I hope {target.mention} drops dead with a curable disease that doctors simply didn’t feel like curing :)",
            f"{target.mention} You know there's no vaccine for stupidity right?",
            f"{target.mention} You are not very epic at all",
            f"You make Kpop Fancams 24/7 for validation on the internet {target.mention}",
            f"Your mother wanted to drop you on the head when you were little {target.mention}",
            f"{target.mention} You're the CEO of Racism",
            f"{target.mention} has no common sense"
        ]

        # Sending out a random insult from the array "responses"
        await ctx.send(random.choice(responses))

    @command(name="comp", aliases=['Comp', 'Compliment'])
    @cooldown(1, 1, BucketType.user)
    async def compliment(self, ctx, target: Member):
        """Give Compliments to Members"""

        # Set up array of compliments to throw at people
        responses = [
            f"{target.mention} is the most adorable uwu <:awie:676201100793085952> <:awie:676201100793085952> <:awie:676201100793085952>",
            f"{target.mention} You have my ENTIRE HEART <:blushlook1:677310734123663363> <:blushlook2:679524467248201769>",
            f"{target.mention} Hun you're CUTE uwu :pleading_face: :flushed: :pleading_face: :flushed: :pleading_face:",
            f"I love {target.mention} so so much :heartbeat: :heartbeat: :heartbeat: ",
            f"My heart is full of love for you {target.mention} <:Kawaii:676203363922214953> <:Kawaii:676203363922214953>",
            f"{target.mention} I admire your greatness so much that I consider making a fan club to become your #1 fan (´꒳`)",
            f"{target.mention} has no flaws, only special effects :))",
            f"{target.mention}'s smile is brighter than sunlight, so smile more often ( ◠‿◠ )",
            f"{target.mention} Your smile is so beautiful it blinds me :heart_eyes: :heart_eyes:",
            f"Being on a journey all my life, I will never meet a person as amazing as you are {target.mention}",
            f"Such a pleasure to be on the same server with {target.mention} <:boneappleteeth:676202300573876252> <:boneappleteeth:676202300573876252>",
            f"With {target.mention}, even the worst day will be filled with joy <:hug:718248629034549299> <:hug:718248629034549299>",
            f"There's no better antidepressant than {target.mention}",
            f"{target.mention} You're great, keep going Σd(˘ꇴ˘๑)",
            f"I'd simp for {target.mention} anyday :flushed: :heart_eyes: :flushed: ",
            f"{target.mention} Even the ugliest clothes won't ruin your look (｡•̀ᴗ -)☆",
            f"{target.mention} You’re that “nothing” when people ask me what I’m thinking about <:Kawaii:676203363922214953> <:Kawaii:676203363922214953>",
            f"{target.mention} Somehow you make time stop and fly at the same time <:awie:676201100793085952> <:blushlook1:677310734123663363>",
            f"{target.mention} is a whole ass SWAGMEAL <:Kawaii:676203363922214953> <:Kawaii:676203363922214953>",
            f"After meeting {target.mention}, I couldn't imagine living my life without them",
            f"Take me into your arms and tell me you love me <:blushlook1:677310734123663363> <:blushlook2:679524467248201769> {target.mention}",
            f"{target.mention} I would spend eternity cuddling with you :flushed: :flushed:",
            f"Would you want to go on an e-date together? :pleading_face: :point_right: :point_left: {target.mention}",
            f"Let me shoot my shot to you :see_no_evil: :see_no_evil: {target.mention}",
            f"Your existence makes me feel so much better {target.mention}",
            f"You're so hot, even hotter than hell :heart_eyes: {target.mention}",
            f"{target.mention} You’re so cute that Taz will simp for you anytime :flushed: :heart_eyes: :flushed:",
            f"{target.mention} The thought of you leaving me is too much to bear. Stay with me forever :pleading_face: :pleading_face:",
            f"You're... You're SHREKTACULAR :heart_eyes: :flushed: :heart_eyes: {target.mention}",
            f"{target.mention} Your beauty renders me speechless... :heart_eyes: :heart_eyes:",
            f"Your taste in music is impeccable {target.mention}",
            f"{target.mention} I can't stop thinking about you :see_no_evil: :see_no_evil:",
            f"{target.mention} Your wedding will be wonderful, but the y is silent <a:huh:676195228872474643> <a:huh:676195228872474643>",
            f"{target.mention} I would give up my lifelong goals just to have a chance with you <a:huh:676195228872474643> <a:huh:676195228872474643>",
            f"{target.mention} Will you be the **yee** to my **haw**? :pleading_face: :pleading_face:",
            f"{target.mention} is the definition of perfection :heart_eyes: :heart_eyes:",
            f"{target.mention} My love for you is bigger than the amount of code Hammy has written <:Kawaii:676203363922214953> <:Kawaii:676203363922214953> <:Kawaii:676203363922214953>"
        ]

        # Sending out a random compliment from the array "responses"
        await ctx.send(random.choice(responses))

    @command(name="flip", aliases=['Flip'])
    @cooldown(1, 1, BucketType.user)
    async def flip(self, ctx):
        """Flip a Coin (Huge pp/Smol pp)"""

        # Define array with only 2 entries to create 50/50 chance
        pp_array = ["Smol pp", "Huge pp"]

        # Send out one of the responses stored in the array
        await ctx.send(f"{ctx.author.mention} {random.choice(pp_array)}")

    @command(name="dm", aliases=["DM", "dM"])
    @is_owner()
    @has_permissions(administrator=True)
    async def dm(self, ctx, member: Member, *, text):
        """DM users"""

        # Send the message typed the mentioned user
        await member.send(text)
        # Delete the message sent instantly
        await ctx.message.delete()

    @command(name="digby", aliases=["Digby"], hidden=True)
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
                colour=Colour(int(random.choice(colour_list))),
                timestamp=datetime.datetime.utcnow())
            embed.set_image(url=random.choice(digby_array))
            embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

            # Send the embedded message to the user
            await ctx.send(embed=embed)

        except FileNotFoundError as e:
            print(e)

    @command(name="doggo", aliases=["Doggo"])
    @bot_has_permissions(embed_links=True)
    @cooldown(1, 1, BucketType.user)
    async def doggo(self, ctx, breed=None):
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
                        f"Doggo Not Found! Please do **{ctx.prefix}doggo breeds** to see the full list of Doggos!")

    @command(name="8ball", aliases=['8Ball'])
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

    @command(name="homies", aliases=["Homies", "homie", "Homie"])
    @cooldown(1, 10, BucketType.user)
    @bot_has_permissions(attach_files=True)
    async def homies(self, ctx, *, text):
        """Summoning the Homies"""

        try:
            # Make sure the text entered is less than 20 characters
            if len(text) >= 20:
                await ctx.send("Please make sure the prompt is below **20** characters!")
                return
            else:

                # Define the text to be drawn on the top and the bottom
                top_text = f"Ayo fuck {text}"
                bottom_text = f"All my homies hate {text}"

                # Call the method to generate the image
                generate_meme('homies/AllMyHomies.jpg', top_text=top_text, bottom_text=bottom_text)

                # Send the image file stored in the directory
                await ctx.send(file=discord.File('AllMyHomiesHateMeme.jpg'))

        except commands.BadArgument as e:
            raise e

    @command(name="owo", aliases=["Owo", "OwO"])
    @cooldown(1, 1, BucketType.user)
    async def owo(self, ctx, *, text):
        """Converts given text to 'OwO' format"""

        # Convert to "OwO" text
        uwu = OwO()
        owo = uwu.whatsthis(text)

        # Send the text back
        await ctx.message.channel.send(owo)

    @command(name="remindme", aliases=["Remindme", "rm"])
    async def remind_me(self, ctx, time=None, *, text):
        """Remind you in DMs"""

        # Grab the author and store it in "author"
        author = ctx.author

        # If a value for time as been given
        if time:

            # Send a confirmation message
            await ctx.send(f"{author.mention} I will remind you in {time} seconds with the message '{text}'")

            # Sleep the thread for the amount of time specified by the user
            await asyncio.sleep(float(time))

            # Remind the user in the channel and then send message to user's dms
            await ctx.send(f"I've reminded you in your dms! {ctx.author.mention}")
            await author.send(text)

        # else no time has been given
        else:
            # Instantly Send message to user's dms
            await author.send(text)


def setup(bot):
    bot.add_cog(Fun(bot))
