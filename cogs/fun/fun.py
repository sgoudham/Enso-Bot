import random

from discord import Member, Colour, Embed
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, command, has_any_role, is_owner

from settings import time, colour_list


# Set up the cog
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="attack", aliases=['Attack'])
    @has_any_role(664585078487252993, 715412394968350756)
    async def attack(self, ctx, target: Member):
        """Allows Co-Owners to throw insults at people"""

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
        """Allows users to compliment other people"""

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
            f"{target.mention} is the definition of perfection :heart_eyes: :heart_eyes:"
            f"{target.mention} My love for you is bigger than the amount of code Hammy has written <:Kawaii:676203363922214953> <:Kawaii:676203363922214953> <:Kawaii:676203363922214953>"
        ]

        # Sending out a random compliment from the array "responses"
        await ctx.send(random.choice(responses))

    @command(name="flip", aliases=['Flip'])
    @cooldown(1, 1, BucketType.user)
    async def flip(self, ctx):
        """"Allows for 50 / 50 chance decisions"""

        # Define 3 arrays that only have 2 strings stored in them
        pp_array = ["Smol pp", "Huge pp"]
        pewds_array = ["Floor Gang", "Ceiling Gang"]

        # Creating a 50/50 chance by choosing the array first
        responses = random.choice([pp_array, pewds_array])

        # Send out one of the responses stored in the array
        await ctx.send(f"{ctx.author.mention} {random.choice(responses)}")

    @command(name="dm", aliases=["DM", "dM"])
    @is_owner()
    async def dm(self, ctx, member: Member, *, text):
        """Allows me to DM anyone through the bot"""

        # Send the message typed the mentioned user
        await member.send(text)
        # Delete the message sent instantly
        await ctx.message.delete()

    @command(name="digby", aliases=["Digby"])
    async def digby(self, ctx):
        """Allows users to see a picture of Digby"""

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
                timestamp=time)
            embed.set_image(url=random.choice(digby_array))
            embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

            # Send the embedded message to the user
            await ctx.send(embed=embed)

        except FileNotFoundError as e:
            print(e)


def setup(bot):
    bot.add_cog(Fun(bot))
