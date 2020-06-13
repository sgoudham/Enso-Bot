import asyncio
import datetime
import random

import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown

colours = [0xff0000, 0x5825ff, 0xff80ed, 0xa0f684, 0x7700cc, 0x0b04d9, 0x3d04ae, 0x000033,
           0x00FFFF,
           0x120A8F, 0x7FFF0, 0xcc3300,
           0x5E260, 0xcc0000, 0x0066cc, 0x7632cd, 0x76a7cd, 0xffa7cd, 0xff24cd, 0xff2443,
           0xff7d43,
           0xb52243, 0xb522ce, 0xb5f43d]


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Attack'])
    @commands.has_any_role('Hamothy', "izzy", "Servant", "pubic relations")
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
            f"{target.mention} You are not very epic at all"
            f"You make Kpop Fancams 24/7 for validation on the internet {target.mention}",
            f"Your mother wanted to drop you on the head when you were little {target.mention}",
            f"{target.mention} You're the CEO of Racism",
            f"{target.mention} has no common sense"
        ]

        # Sending out a random insult from the array "responses"
        await ctx.send(random.choice(responses))

    @commands.command(aliases=['comp', 'Compliment', 'Comp'])
    @cooldown(1, 2, BucketType.channel)
    async def compliment(self, ctx, target: discord.Member):

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
            f"{target.mention} Your beauty renders me speechless... :heart_eyes: :heart_eyes:"
            f"Your taste in music is impeccable {target.mention}",
            f"{target.mention}I can't stop thinking about you :see_no_evil: :see_no_evil:",
        ]

        # Sending out a random compliment from the array "responses"
        await ctx.send(random.choice(responses))

    @commands.command(aliases=["Kiss", "kiss"])
    @cooldown(1, 0.5, BucketType.channel)
    async def kissing(self, ctx, target: discord.Member):

        channels = ["bot-commands"]

        try:
            if str(ctx.channel) in channels:

                with open('images/kissing.txt') as file:
                    kissing_array = file.readlines()

                    # set member as the author
                    member = ctx.message.author
                    userAvatar = member.avatar_url

                    embed = discord.Embed(
                        title=f"<:blushlook1:677310734123663363> <:blushlook2:679524467248201769> | **{member.display_name}** kissed **{target.display_name}**",
                        colour=discord.Colour(int(random.choice(colours))))
                    embed.set_image(url=random.choice(kissing_array))
                    embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url='{}'.format(userAvatar))
                    embed.timestamp = datetime.datetime.utcnow()

                    await ctx.send(embed=embed)

            else:

                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()
        except FileNotFoundError as e:
            print(e)

    @commands.command(aliases=["Cuddle", "cdle", "cud"])
    @cooldown(1, 0.5, BucketType.channel)
    async def cuddle(self, ctx, target: discord.Member):

        channels = ["bot-commands"]

        try:
            if str(ctx.channel) in channels:

                with open('images/cuddling.txt') as file:
                    cuddling_array = file.readlines()

                    # set member as the author
                    member = ctx.message.author
                    userAvatar = member.avatar_url

                    embed = discord.Embed(
                        title=f"<a:huh:676195228872474643> <a:huh:676195228872474643> | **{member.display_name}** cuddles **{target.display_name}**",
                        colour=discord.Colour(int(random.choice(colours))))
                    embed.set_image(url=random.choice(cuddling_array))
                    embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url='{}'.format(userAvatar))
                    embed.timestamp = datetime.datetime.utcnow()

                    await ctx.send(embed=embed)

            else:

                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()
        except FileNotFoundError as e:
            print(e)

    @commands.command(aliases=["lem", "Lemon", "Lem"])
    @cooldown(1, 2, BucketType.channel)
    async def lemon(self, ctx, target: discord.Member):

        channels = ["bot-commands", "general"]
        lemon_array = ["https://media.discordapp.net/attachments/669812887564320769/720093589056520202/lemon.gif",
                       "https://media.discordapp.net/attachments/669812887564320769/720093575492272208/lemon2.gif",
                       "https://media.discordapp.net/attachments/718484280925224981/719629805263257630/lemon.gif"]
        try:
            if str(ctx.channel) in channels:

                # set member as the author
                member = ctx.message.author
                userAvatar = member.avatar_url

                embed = discord.Embed(
                    title=f"<a:huh:676195228872474643> <a:huh:676195228872474643> | **{member.display_name}** Gives A Lemon To **{target.display_name}**",
                    colour=discord.Colour(int(random.choice(colours))))
                embed.set_image(url=random.choice(lemon_array))
                embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url='{}'.format(userAvatar))
                embed.timestamp = datetime.datetime.utcnow()

                await ctx.send(embed=embed)

            else:

                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()
        except FileNotFoundError as e:
            print(e)

    # Bot ~8Ball command
    @commands.command(aliases=['8ball', '8Ball'])
    @cooldown(1, 0.5, BucketType.channel)
    async def _8ball(self, ctx, *, question):

        channels = ["bot-commands", "general"]

        try:
            if str(ctx.channel) in channels:

                with open('images/eightball.txt') as file:
                    _8ball_array = file.readlines()

                    await ctx.send(f'Question: {question}\nAnswer: {random.choice(_8ball_array)}')

            else:

                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()
        except FileNotFoundError as e:
            print(e)


def error_function():
    return "Sorry! I only work in #bot-commands!"


def setup(bot):
    bot.add_cog(Fun(bot))
