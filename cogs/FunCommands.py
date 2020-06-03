import random
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Attack'])
    @commands.has_any_role('Hamothy', "izzy")
    async def attack(self, ctx, target: discord.Member):
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
            f"I bet {target.mention} you likes eating watermelon with the rind.",
            f"{target.mention} You were the first creation to make god say oops",
            f"{target.mention} You have delusions of adequacy",
            f"{target.mention} I treasure the time I don't spend with you",
            f"Don't be ashamed of yourself {target.mention}, that's your parent's job",
            f"I don't have the energy to pretend I like {target.mention} today",
            f"I know this was made for me to insult but it’s kinda hard to be a hateful cunt like {target.mention} :star_struck::star_struck:",
            f"#{target.mention}IsOverParty",
            f"I hope {target.mention} drops dead with a curable disease that doctors simply didn’t feel like curing :)",
            f"{target.mention} You know there's no vaccine for stupidity right?",
            f"{target.mention} bruh moment",
            f"",
            f"",
            f"",
        ]

        await ctx.send(random.choice(responses))

    @commands.command(aliases=['comp', 'Compliment', 'Comp'])
    @commands.has_any_role('Hamothy', "izzy")
    async def compliment(self, ctx, target: discord.Member):
        responses = [
            f"{target.mention} is the most adorable uwu :heart_eyes: :heart_eyes:",
            f"{target.mention} You have my ENTIRE HEART UvU",
            f"{target.mention} Hun you're CUTE UwU :pleading_face: :flushed: :pleading_face: :flushed: :pleading_face:",
            f"I love {target.mention} so so much :heartbeat: :heartbeat: :heartbeat: ",
            f"My heart is full of love for you {target.mention}",
            f"{target.mention} I admire your greatness so much that I consider making a fan club to become your #1 fan (´꒳`)",
            f"{target.mention} has no flaws, only special effects :))",
            f"{target.mention}'s smile is brighter than sunlight, so smile more often ( ◠‿◠ )",
            f"{target.mention} Your smile is so beautiful it blinds me :heart_eyes: :heart_eyes:",
            f"Being on a journey all my life, I will never meet a person as amazing as you are {target.mention}",
            f"Such a pleasure to be on the same sever with you {target.mention}",
            f"",
            f"",
            f"",
            f"",
            f"",
            f"",
            f"",
            f"",
            f"",

        ]

        # await ctx.send(random.choice(responses))
        await ctx.send(random.choice(responses))

    # @client.command(aliases=["Hug"])
    # @commands.has_any_role('Hamothy')
    # async def hug(self, ctx):
    #    await self.bot.say("hugs {}".format(ctx.message.author.mention()))

    # Bot ~8Ball command
    @commands.command(aliases=['8ball', '8Ball'])
    @cooldown(1, 5, BucketType.channel)
    async def _8ball(self, ctx, *, question):

        channels = ["bot-commands"]

        with open('eightball.txt') as file:
            _8ball_array = file.readlines()

            if str(ctx.channel) in channels:

                await ctx.send(f'Question: {question}\nAnswer: {random.choice(_8ball_array)}')

            else:
                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

            file.close()


def error_function():
    return "Sorry! I only work in #bot-commands!"


def setup(bot):
    bot.add_cog(Fun(bot))
