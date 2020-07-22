import datetime

from discord import Embed
from discord.ext import commands
from discord.ext.commands import is_owner

from settings import enso_embedmod_colours


class helper(commands.Cog, command_attrs=dict(hidden=True)):
    """Help Command!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @is_owner()
    async def help2(self, ctx, *cog):
        if not cog:
            coggers = Embed(title="(っ◔◡◔)っ Custom Help (っ◔◡◔)っ",
                            description="Use ~help *cog* to find out more about them!",
                            colour=enso_embedmod_colours,
                            timestamp=datetime.datetime.utcnow())
            coggers.set_thumbnail(url=ctx.guild.icon_url)
            cog_desc = ''
            for x in self.bot.cogs:
                cog_desc += f"**{x}** - {self.bot.cogs[x].__doc__}\n"
            coggers.add_field(name="Cogs", value=cog_desc[0:len(cog_desc) - 1], inline=False)
            await ctx.message.add_reaction(emoji="✉️")
            await ctx.send(embed=coggers)
        else:
            if len(cog) > 1:
                coggers = Embed(title="Error!",
                                description="Too Many Cogs!",
                                colour=enso_embedmod_colours)
                await ctx.send(embed=coggers)
            else:
                found = False
                for x in self.bot.cogs:
                    for y in cog:
                        if x == y:
                            coggers = Embed(colour=enso_embedmod_colours)
                            cogger_info = ''
                            for c in self.bot.get_cog(y).walk_commands():
                                if not c.hidden:
                                    cogger_info += f"**{c.qualified_name}** - {c.help}\n"
                            coggers.add_field(name=f"{cog[0]} Module - {self.bot.cogs[cog[0]].__doc__}",
                                              value=cogger_info)
                            found = True
                if not found:
                    for x in self.bot.cogs:
                        for c in self.bot.get_cog(x).walk_commands():
                            if c.name == cog[0]:
                                coggers = Embed(colour=enso_embedmod_colours)
                                coggers.add_field(name=f"{c.name} - {c.help}",
                                                  value=f"Proper Syntax: `{c.qualified_name} {c.signature}`")
                                found = True
                    if not found:
                        coggers = Embed(title="Error!",
                                        description=f"How do you even use `{cog[0]}`?",
                                        colour=enso_embedmod_colours)
                else:
                    await ctx.message.add_reaction(emoji="✉️")
                await ctx.send(embed=coggers)


def setup(bot):
    bot.add_cog(helper(bot))
