from discord.ext import commands
# OwO Impowt da wibwawy ÙωÙ
from discord.ext.commands import BucketType, cooldown, command
from owotext import OwO


# Initiate the cog
class OwOText(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ~owo command allows for text to be 'converted to OWO'
    @command(name="owo", aliases=["Owo", "OwO"])
    @cooldown(1, 1, BucketType.user)
    async def owo(self, ctx):
        # Making sure that the string that gets converted is excluding the ~owo
        if ctx.message.content.startswith("~owo"):
            # Get the message to be converted
            msg = ctx.message.content.split("~owo ", 1)

            # Convert the message into owo text
            uwu = OwO()
            owo = uwu.whatsthis(str(msg[-1]))

            # Send the owo version of the text to the channel
            await ctx.message.channel.send(owo)


def setup(bot):
    bot.add_cog(OwOText(bot))
