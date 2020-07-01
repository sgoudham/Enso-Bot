import asyncio

from discord.ext import commands
from discord.ext.commands import command


class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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


"""
    @commands.Cog.listener()
    @commands.is.owner()
    async def ():
        time_left = [float(i) for i in str(datetime.now().time()).split(":")]
        time_left = timedelta(hours=2) - timedelta(hours=time_left[0] % 2, minutes=time_left[1], seconds=time_left[2])
        sleep(round(time_left.total_seconds()))

        while True:
            await ctx.send("Bump the Server Idiots")
            sleep(7200)

    _thread.start_new_thread(ex(self=self, ctx), ())
"""


def setup(bot):
    bot.add_cog(Reminder(bot))
