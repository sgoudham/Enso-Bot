from discord.ext import commands
# OwO Impowt da wibwawy ÙωÙ
from discord.ext.commands import BucketType, cooldown
from owotext import OwO


# Initiate the cog
class OwOText(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ~owo command allows for text to be 'converted to OWO'
    @commands.command()
    @cooldown(1, 1, BucketType.user)
    async def owo(self, ctx):
        if ctx.message.content.startswith("~owo"):
            msg = ctx.message.content.split("~owo ", 1)

            uwu = OwO()
            owo = uwu.whatsthis(str(msg[-1]))

            await ctx.message.channel.send(owo)


def setup(bot):
    bot.add_cog(OwOText(bot))
