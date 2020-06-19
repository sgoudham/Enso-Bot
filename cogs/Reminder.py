import _thread
from datetime import datetime
from datetime import timedelta
from time import sleep

from discord.ext import commands


class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    @commands.has_any_role('Hamothy')
    async def ex(self, ctx):
        time_left = [float(i) for i in str(datetime.now().time()).split(":")]
        time_left = timedelta(hours=2) - timedelta(hours=time_left[0] % 2, minutes=time_left[1], seconds=time_left[2])
        sleep(round(time_left.total_seconds()))

        while True:
            await ctx.send("Bump the Server Idiots")
            sleep(7200)

    _thread.start_new_thread(ex, ())


def setup(bot):
    bot.add_cog(Reminder(bot))
