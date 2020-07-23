import datetime

from discord import Embed
from discord.ext import commands
from discord.ext.commands import is_owner

from settings import enso_embedmod_colours, blank_space


class helper(commands.Cog, command_attrs=dict(hidden=True)):
    """Help Command!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @is_owner()
    async def help2(self, ctx, *cog):
        group_found = False
        if not cog:
            coggers = Embed(title="(っ◔◡◔)っ Custom Help (っ◔◡◔)っ",
                            description=f"Use **{ctx.prefix}help** `<cog>` to find out more about them!"
                                        f"\n\n`[]` | **Optional**"
                                        f"\n`<>` | **Required**",
                            colour=enso_embedmod_colours,
                            timestamp=datetime.datetime.utcnow())
            coggers.set_footer(text=f"Requested by {ctx.author}", icon_url='{}'.format(ctx.author.avatar_url))
            coggers.set_thumbnail(url=ctx.guild.icon_url)
            cog_desc = ''
            for x in self.bot.cogs:
                cog_desc += f"**{x}** - {self.bot.cogs[x].__doc__}\n"
            coggers.add_field(name=blank_space, value=cog_desc[0:len(cog_desc) - 1], inline=False)
            await ctx.message.add_reaction(emoji="✉️")
            await ctx.send(embed=coggers)
        else:
            found = False
            for x in self.bot.cogs:
                for y in cog:
                    if x == y:
                        coggers = Embed(title=f"(っ◔◡◔)っ {cog[0]} (っ◔◡◔)っ", colour=enso_embedmod_colours,
                                        timestamp=datetime.datetime.utcnow())
                        coggers.set_footer(text=f"Requested by {ctx.author}",
                                           icon_url='{}'.format(ctx.author.avatar_url))
                        for c in self.bot.get_cog(y).walk_commands():
                            if not c.hidden:
                                if c.signature:
                                    cogger_info = c.help
                                    coggers.add_field(name=f"**{ctx.prefix}{c.qualified_name}** `{c.signature}`",
                                                      value=cogger_info, inline=False)
                                else:
                                    cogger_info = c.help
                                    coggers.add_field(name=f"**{ctx.prefix}{c.qualified_name}**",
                                                      value=cogger_info, inline=False)
                        await ctx.message.add_reaction(emoji="✉️")
                        found = True
            if not found:
                for x in self.bot.cogs:
                    for c in self.bot.get_cog(x).walk_commands():
                        if c.name == cog[0]:
                            if isinstance(c, commands.Group):
                                string = " ".join(cog)
                                group_found = True
                                for val in c.commands:
                                    if string == val.qualified_name:
                                        coggers = Embed(title="Proper Syntax",
                                                        description=f"**{val.help}"
                                                                    f"\n{ctx.prefix}{val.qualified_name}** `{val.signature}`",
                                                        colour=enso_embedmod_colours,
                                                        timestamp=datetime.datetime.utcnow())
                                        coggers.set_footer(text=f"Requested by {ctx.author}",
                                                           icon_url='{}'.format(ctx.author.avatar_url))
                                        await ctx.message.add_reaction(emoji="✉️")
                            else:
                                coggers = Embed(title=f"Proper Syntax",
                                                description=f"**{ctx.prefix}{c.qualified_name}** `{c.signature}` | {c.help}",
                                                colour=enso_embedmod_colours, timestamp=datetime.datetime.utcnow())
                                coggers.set_footer(text=f"Requested by {ctx.author}",
                                                   icon_url='{}'.format(ctx.author.avatar_url))
                                await ctx.message.add_reaction(emoji="✉️")
                            found = True
                if not found:
                    if group_found:
                        coggers = Embed(title="Error!",
                                        description=f"How do you even use `{string}`?",
                                        colour=enso_embedmod_colours,
                                        timestamp=datetime.datetime.utcnow())
                    else:
                        coggers = Embed(title="Error!",
                                        description=f"How do you even use `{cog[0]}`?",
                                        colour=enso_embedmod_colours,
                                        timestamp=datetime.datetime.utcnow())
            else:
                await ctx.message.add_reaction(emoji="✉️")
            await ctx.send(embed=coggers)


def setup(bot):
    bot.add_cog(helper(bot))
