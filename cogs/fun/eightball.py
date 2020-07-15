import asyncio
import random

from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, command

from cogs.anime.interactive import error_function


# Set up the cog
class eightball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="8ball", aliases=['8Ball'])
    @cooldown(1, 1, BucketType.user)
    async def _8ball(self, ctx, *, question):
        """Allows for the user to get a custom response to a question"""

        # Setting up the channels that the commands can be sent in enso-chan-commands and general
        channels = ["enso-chan-commands", "picto-chat"]

        # Surround with try/except to catch any exceptions that may occur
        try:

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in channels:

                # Open the file containing all the custom eightball responses
                with open('images/FunCommands/eightball.txt', encoding="utf8") as file:
                    # Store the eightball responses in an array
                    eightball_array = file.readlines()
                    # Repeat the user question and send out a random response from _8ball_array
                    await ctx.send(f'Question: {question}\nAnswer: {random.choice(eightball_array)}')

            # else the command is sent in an invalid channel
            else:

                # Call error_function() and display it to the user
                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(eightball(bot))
