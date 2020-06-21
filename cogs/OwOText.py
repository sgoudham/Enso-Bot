import random

from discord.ext import commands
# OwO Impowt da wibwawy ÙωÙ
from discord.ext.commands import cooldown, BucketType
from owotext import OwO

# Defining an array of all the vowels in lowercase and uppercase
vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']


# -----------------------------------------Code Found Online------------------------------------------------------------
def last_replace(s, old, new):
    li = s.rsplit(old, 1)
    return new.join(li)


def text_to_owo(text):
    """ Converts your text to OwO """
    smileys = [';;w;;', '^w^', '>w<', 'UwU', '(・`ω\´・)', '(´・ω・\`)']

    text = text.replace('L', 'W').replace('l', 'w')
    text = text.replace('R', 'W').replace('r', 'w')

    text = last_replace(text, '!', '! {}'.format(random.choice(smileys)))
    text = last_replace(text, '?', '? owo')
    text = last_replace(text, '.', '. {}'.format(random.choice(smileys)))

    for v in vowels:
        if 'n{}'.format(v) in text:
            text = text.replace('n{}'.format(v), 'ny{}'.format(v))
        if 'N{}'.format(v) in text:
            text = text.replace('N{}'.format(v), 'N{}{}'.format('Y' if v.isupper() else 'y', v))

    return text


# -----------------------------------------Code Found Online------------------------------------------------------------

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
