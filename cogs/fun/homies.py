import textwrap

import discord
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from discord.ext.commands import command, cooldown, BucketType


def generate_meme(image_path, top_text, bottom_text='', font_path='homies/impact/impacted.ttf', font_size=9):
    get_image = Image.open(image_path)
    draw = ImageDraw.Draw(get_image)
    image_width, image_height = get_image.size

    # Load font
    font = ImageFont.truetype(font=font_path, size=int(image_height * font_size) // 100)

    # Convert text to uppercase
    top_text = top_text.upper()
    bottom_text = bottom_text.upper()

    # Text wrapping
    char_width, char_height = font.getsize('A')
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(top_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)

    # Draw top lines
    y = 10
    for line in top_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        draw.text((x, y), line, fill='white', font=font)
        y += line_height

    # Draw bottom lines
    y = image_height - char_height * len(bottom_lines) - 15
    for line in bottom_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        draw.text((x, y), line, fill='white', font=font)
        y += line_height

    # Save meme
    get_image.save('meme-' + get_image.filename.split('/')[-1])


# Set up the cog
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="homies", aliases=["Homies", "homie", "Homie"])
    @cooldown(1, 180, BucketType.channel)
    async def homies(self, ctx, *, user_word):
        """Allows people to summon the homies"""

        if len(user_word) >= 20:
            await ctx.send("Please make sure the prompt is below **20** characters!")
            return
        else:

            top_text = f"Ayo fuck {user_word}"
            bottom_text = f"All my homies hate {user_word}"

            generate_meme('homies/AllMyHomies.jpg', top_text=top_text, bottom_text=bottom_text)

            await ctx.send(file=discord.File('meme-AllMyHomies.jpg'))


def setup(bot):
    bot.add_cog(Fun(bot))


"""      # Set up the embed to display a random kissing gif
embed = Embed(
title=f"**The Homies**",
colour=Colour(int(random.choice(settings.colour_list))),
timestamp=datetime.datetime.utcnow())
embed.set_image(url=f"{image}")
embed.set_footer(text=f"Requested by {ctx.author}", icon_url='{}'.format(ctx.author.avatar_url))
"""
