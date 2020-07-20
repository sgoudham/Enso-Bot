import urllib.parse

from aiohttp import request
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, command


# Set up the cog
class eightball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="8ball", aliases=['8Ball'])
    @cooldown(1, 1, BucketType.user)
    async def _8ball(self, ctx, *, question):
        """8ball responses!"""

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

        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(eightball(bot))
