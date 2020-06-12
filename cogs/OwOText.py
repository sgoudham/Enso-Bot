import random

from discord.ext import commands
# OwO Impowt da wibwawy ÙωÙ
from discord.ext.commands import cooldown, BucketType
from owotext import OwO

vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']


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

    print(text)
    return text


class OwOText(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    @cooldown(1, 1.5, BucketType.channel)
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith("owo"):
            msg = message.content.split("owo ", 1)

            uwu = OwO()
            owo = uwu.whatsthis(str(msg[-1]))

            await message.channel.send(owo)


def setup(bot):
    bot.add_cog(OwOText(bot))
