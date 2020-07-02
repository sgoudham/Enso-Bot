import datetime
import random

from discord import Colour, Embed, DMChannel
from discord.ext import commands

import settings


# Set up the Cog
class Modmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Allows for the modmail system
    @commands.Cog.listener()
    async def on_message(self, message):
        # Making sure that the bot doesn't reply to itself
        if message.author == self.bot:
            return

        # Get the mod-mail channel
        channel = self.bot.get_channel(728083016290926623)

        if isinstance(message.channel, DMChannel):
            if len(message.content) < 50:
                await message.channel.send("Your message should be at least 50 characters in length.")

            else:
                guild = self.bot.get_guild(663651584399507476)
                member = guild.get_member(message.author.id)
                embed = Embed(title="**Modmail**",
                              colour=Colour(random.choice(settings.colour_list)),
                              timestamp=datetime.datetime.utcnow())

                embed.set_thumbnail(url=message.author.avatar_url)
                embed.set_footer(text=f"Requested by {member}")

                fields = [("Member", member, False),
                          ("Message", message.content, False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await channel.send(embed=embed)
                await message.channel.send("**Message relayed to Staff! Thank you for your input!**")


def setup(bot):
    bot.add_cog(Modmail(bot))
