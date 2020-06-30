import asyncio
import datetime
import random

from aiohttp import request
from discord import Member, Colour, Embed
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, command, has_any_role, is_owner

import settings
from cogs.Embeds import error_function


# Set up the cog
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ~attack command for only co-owners only
    @command(name="attack", aliases=['Attack'])
    @has_any_role(664585078487252993, 715412394968350756)
    async def attack(self, ctx, target: Member):

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

    # ~compliment command for everyone to use to compliment someone
    @command(name="comp", aliases=['Comp', 'Compliment'])
    # Added a cooldown, only 1 instance of the command can be sent every second per user
    @cooldown(1, 1, BucketType.user)
    async def compliment(self, ctx, target: Member):

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
            f"Such a pleasure to be on the same sever with {target.mention} <:boneappleteeth:676202300573876252> <:boneappleteeth:676202300573876252>",
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
            f"Josh would kill Toga for you anyday {target.mention}",
            f"Zara would pick you over Kakashi :heart_eyes: :heart_eyes: {target.mention}",
            f"{target.mention} The thought of you leaving me is too much to bear. Stay with me forever :pleading_face: :pleading_face:",
            f"{target.mention}From a scale of 1-10, you’re 9 I’m the 1 you need <:Kawaii:676203363922214953> <:Kawaii:676203363922214953> <:Kawaii:676203363922214953> ",
            f"You're... You're SHREKTACULAR :heart_eyes: :flushed: :heart_eyes: {target.mention}",
            f"{target.mention} Your beauty renders me speechless... :heart_eyes: :heart_eyes:",
            f"Your taste in music is impeccable {target.mention}",
            f"{target.mention}I can't stop thinking about you :see_no_evil: :see_no_evil:",
            f"{target.mention} Your wedding will be wonderful, but the y is silent <a:huh:676195228872474643> <a:huh:676195228872474643>",
            f"{target.mention} Hammy would give up his lifelong goals just to have a chance with you <a:huh:676195228872474643> <a:huh:676195228872474643>",
        ]

        # Sending out a random compliment from the array "responses"
        await ctx.send(random.choice(responses))

    # ~8Ball command
    @command(name="8ball", aliases=['8Ball'])
    # Added a cooldown, only 1 instance of the command can be sent every second per user
    @cooldown(1, 1, BucketType.user)
    async def _8ball(self, ctx, *, question):

        # Setting up the channels that the commands can be sent in enso-chan-commands and general
        channels = ["enso-chan-commands", "general", "picto-chat"]

        # Surround with try/except to catch any exceptions that may occur
        try:

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in channels:

                # Open the file containing all the custom eightball responses
                with open('images/FunCommands/eightball.txt') as file:
                    # Store the eightball responses in an array
                    _8ball_array = file.readlines()
                    # Repeat the user question and send out a random response from _8ball_array
                    await ctx.send(f'Question: {question}\nAnswer: {random.choice(_8ball_array)}')

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

    # ~Lukas command that only Lukas can use
    @command(name="lukas", aliases=['Lukas'])
    # Added a cooldown, only 1 instance of the command can be sent every second per user
    @cooldown(1, 1, BucketType.user)
    @has_any_role('Lukas (Server Booster)')
    async def lukas(self, ctx):

        # Define the id's of Bubz and Lukas
        lukasID = '<@395653002050011166>'
        bubzID = '<@422588717744652289>'

        # Set up array of responses that Lukas wants the bot to display
        responses = [
            f"{lukasID} loves {bubzID} with all his heart <:awie:676201100793085952> <:awie:676201100793085952>",
            f"{lukasID} and {bubzID} are raising their rabbits <:blushlook1:677310734123663363> <:blushlook2:679524467248201769>",
            f"{lukasID} is having a cult meeting",
            f"{bubzID} is {lukasID}’s Ehefrau"]

        # Send one of the responses of the responses array to Lukas
        await ctx.send(random.choice(responses))

    # ~Flip command to allow for 50/50 chance decisions
    @command(name="flip", aliases=['Flip'])
    @cooldown(1, 1, BucketType.user)
    async def flip(self, ctx):

        # Define 3 arrays that only have 2 strings stored in them
        pp_array = ["Smol pp", "Huge pp"]
        pewds_array = ["Floor Gang", "Ceiling Gang"]

        # Creating a 50/50 chance by choosing the array first
        responses = random.choice([pp_array, pewds_array])

        # Send out one of the responses stored in the array
        await ctx.send(f"{ctx.author.mention} {random.choice(responses)}")

    # ~dm only allows me to dm anyone through the bot
    @command(name="dm", aliases=["DM", "dM"])
    @is_owner()
    async def dm(self, ctx, member: Member, *, text):
        # Send the message typed the mentioned user
        await member.send(text)
        # Delete the message sent instantly
        await ctx.message.delete()

    # ~remindme command to allow the bot to dm you to remind you of something
    @command(name="remindme", aliases=["Remindme", "rm"])
    async def remind_me(self, ctx, time=None, *, text):
        # Grab the author and store it in "author"
        author = ctx.author

        # If a value for time as been given
        if time:
            # Sleep the thread for the amount of time specified by the user
            await asyncio.sleep(float(time))
            # Send message to user's dms
            await author.send(text)

        # else no time has been given
        else:
            # Instantly Send message to user's dms
            await author.send(text)

    # ~digby command that allows users to see a picture of digby
    @command(name="digby", aliases=["Digby"])
    async def digby(self, ctx):

        # Surround with try/except to catch any exceptions that may occur
        try:

            # Open the file containing the digby images
            with open('images/digby.txt') as file:
                # Store content of the file in digby_array
                digby_array = file.readlines()

            # Set member as the author
            member = ctx.message.author
            # Get the member avatar
            userAvatar = member.avatar_url

            # Set up the embed to display a random image of digby
            embed = Embed(
                title=f"**A cute picture of Digby!**",
                colour=Colour(int(random.choice(settings.colour_list))),
                timestamp=datetime.datetime.utcnow())
            embed.set_image(url=random.choice(digby_array))
            embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

            # Send the embedded message to the user
            await ctx.send(embed=embed)

        except FileNotFoundError as e:
            print(e)

    # ~Doggo command that uses an API to grab images of dogs
    @command(name="doggo", aliases=["Doggo"])
    @cooldown(1, 1, BucketType.user)
    async def doggo(self, ctx, breed=None):

        # If the channel that the command has been sent is in the list of accepted channels
        if str(ctx.channel) in settings.channels:

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

                            # Define a new string to store the Doggo's nicely formatted
                            string = " "
                            for b in b_list:
                                string += (b + ", ").capitalize()

                            # Tell the user to try the breeds listed below
                            await ctx.send(f"Try the Breeds listed below!" +
                                           f"\n {string}")

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
                                colour=Colour(random.choice(settings.colour_list)),
                                timestamp=datetime.datetime.utcnow())
                            doggo_embed.set_image(url=image_link)
                            doggo_embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

                            # Send the doggo image
                            await ctx.send(embed=doggo_embed)

                        else:

                            # Send error message that Doggo was not found!
                            await ctx.send(
                                "Doggo Not Found! Please do **~doggo breeds** to see the full list of Doggos!")
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
                            title=f"**Doggo!!** ",
                            colour=Colour(random.choice(settings.colour_list)),
                            timestamp=datetime.datetime.utcnow())
                        doggo_embed.set_image(url=image_link)
                        doggo_embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

                        # Send random doggo image to the channel
                        await ctx.send(embed=doggo_embed)

                    else:

                        # Send error message that Doggo was not found!
                        await ctx.send(
                            "Doggo Not Found! Please do **~doggo breeds** to see the full list of Doggos!")
        else:

            # Call error_function() and display it to the user
            message = await ctx.send(error_function())

            # Let the user read the message for 2.5 seconds
            await asyncio.sleep(2.5)
            # Delete the message
            await message.delete()


def setup(bot):
    bot.add_cog(Fun(bot))
