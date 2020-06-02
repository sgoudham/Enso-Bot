import random
import asyncio
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Bot ~8Ball command
    @commands.command(aliases=['8ball', '8Ball'])
    @cooldown(1, 3, BucketType.channel)
    async def _8ball(self, ctx, *, question):
        channels = ["bot-commands"]
        if str(ctx.channel) not in channels:
            message = await ctx.send("Sorry! I only work in #bot-commands!")

            # Let the user read the message for 2.5 seconds
            await asyncio.sleep(2.5)
            # Delete the message
            await message.delete()
            responses = [
                "Hamothy is preoccupied with catching a case",
                "The prophet Kate believes it will come true",
                "Josh doesn't believe in the outcome :(",
                "Izzy can't predict this",
                "Idk idiot lmao",
                "Why are you even asking me",
                "It's not like I can read your question",
                "Shut the fuck up NOW",
                "Zara wants to protest your question",
                "Stitch will definitely get back to you",
                "*Kakashi slams you to the wall*",
                "Kate is too busy reading yaoi to answer your question",
                "It- It's not lik- It's not like I want to answer your question or anything *tsundere noises*",
                "Connor is too busy making tea and simping for beautiful women to reply to this",
                "Maybe",
                "Who said you could ask that question?",
                "Ifrah cannot answer that",
                "Hussein be spitting too much fire to look at your weak ass question",
                "Literally no one gives a shit",
                "N O spells NO",
                "Find something better to do with your spare time smh",
                "Sure but did you know that Izzy smells?",
                "No but did you know that Stitch smells?",
                "Get your dick back in your pants smh",
                "Get the fuck back to horny jail RIGHT NOW",
                "Nick Cock Bro",
                "Nice Tits",
                "Dm Cloud for the answer",
                "No",
                "Yes",
                "Pffft you wish",
                "Never in a million years",
                "Pathetic. You're wasting your time",
                "Taz is too busy simping over Anonymous to care",
                "Leave me alone. I'm sad :(",
                "Shoot your Shot King",
                "Of course!",
                "If you believe hard enough, it'll come true!!",
                "Inna likes this question, but you'll have to answer it yourself ╮(︶▽︶)╭",
                "Dm Taz to truly find out the answer to this one",
                "Hussein approves of these FIRE bars",
                "Why you gotta ask me a question when I'm just vibin bro :pensive: ",
                "Hamothy LOVES this question and nods approvingly",
                "I don't have the energy to answer this question...",
                "The Swedish fish agrees",
                "You're better off asking Dyno, Ensō is in a bad mood right now :(",
                "The answer lies within your heart",
                "All the signs point to yes!",
                "Marshall would love to agree with you",
                "That's so litty titty bro",
                "I'm Izzy and I approve of this message",
                "Naughty naughty girl",
                "Hamothy has used his godlike like powers to align the stars for you, it must be true",
                "Gabriel appears out of thin air and smites you",
                "Yes yes yes!!!",
                "No I don't care about your question, where is my podcast!??!?"
            ]
            await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

def setup(bot):
    bot.add_cog(Fun(bot))
