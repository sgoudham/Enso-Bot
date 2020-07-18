import datetime

from discord import Embed
from discord.ext import commands, menus
from discord.ext.commands import command

from settings import enso_embedmod_colours


# Pages of the help embed
def help_menu(self, guild_icon):
    # Setting up the embed for the Fun Commands
    fun = Embed(title="(っ◔◡◔)っ Fun (っ◔◡◔)っ",
                colour=enso_embedmod_colours,
                timestamp=datetime.datetime.utcnow())

    # Setting thumbnail and author
    fun.set_thumbnail(url=guild_icon)

    # Setting up the fields in a separate array
    fun_fields = [
        (f"**{self.ctx.prefix}comp `<person>`**",
         "\nCompliment a person in the server", True),
        (f"**{self.ctx.prefix}8ball `<text>`**",
         "\nAsk a question and 8ball will give a custom response", True),
        (f"**{self.ctx.prefix}homies `<text>`**",
         "\nGenerates homies meme with given text", True),
        (f"**{self.ctx.prefix}owo `<text>`**",
         "\nTranslates given text to 'owo' format", True),
        (f"**{self.ctx.prefix}flip**",
         "\nDoes a coinflip with big pp Or smol pp", True),
        (f"**{self.ctx.prefix}doggo**",
         "\nLook at images of Doggos", True)]

    # Setting up the embed for the Fun Commands
    interactive = Embed(title="(っ◔◡◔)っ Interactive (っ◔◡◔)っ",
                        colour=enso_embedmod_colours,
                        timestamp=datetime.datetime.utcnow())

    # Setting thumbnail and author
    interactive.set_thumbnail(url=guild_icon)

    # Setting up the fields in a separate array
    interactive_fields = [
        (f"**{self.ctx.prefix}hug `<person>`**",
         "\nHug a User Within The Server", True),
        (f"**{self.ctx.prefix}cuddle `<person>`**",
         "\nCuddle a User Within The Server", True),
        (f"**{self.ctx.prefix}pat `<person>`**",
         "\nPat a User Within The Server", True),
        (f"**{self.ctx.prefix}kiss `<person>`**",
         "\nKiss a User Within The Server", True),
        (f"**{self.ctx.prefix}lemon `<person>`**",
         "\nGive lemon to a User Within The Server", True)]

    # Setting up the embed for the Fun Commands
    interactive_2 = Embed(title="(っ◔◡◔)っ Interactive 2 (っ◔◡◔)っ",
                          colour=enso_embedmod_colours,
                          timestamp=datetime.datetime.utcnow())

    # Setting thumbnail and author
    interactive_2.set_thumbnail(url=guild_icon)

    # Setting up the fields in a separate array
    interactive_fields_2 = [
        (f"**{self.ctx.prefix}slap `<person>`**",
         "\nSlap a User Within The Server", True),
        (f"**{self.ctx.prefix}kill `<person>`**",
         "\nKill a User Within The Server", True),
        (f"**{self.ctx.prefix}choke `<person>`**",
         "\nChoke a User Within The Server", True)]

    # Setting up the embed for Relationship commands
    relationship = Embed(title="(っ◔◡◔)っ Relationship (っ◔◡◔)っ",
                         colour=enso_embedmod_colours,
                         timestamp=datetime.datetime.utcnow())

    # Setting thumbnail and author
    relationship.set_thumbnail(url=guild_icon)

    # Setting up the fields in a separate array
    relationship_fields = [
        (f"**{self.ctx.prefix}marry `<person>`**",
         "\nMarry a User Within The Server", True),
        (f"**{self.ctx.prefix}divorce `<person>`**",
         "\nDivorce The Person You Are Married To", False),
        (f"**{self.ctx.prefix}minfo `<person>`**",
         "\nDisplays information about the user's current marriage" +
         f"\nUsing **{self.ctx.prefix}minfo** by itself will retrieve your marriage information", True)]

    # Setting up the Embed for the Enso commands
    enso = Embed(title="(っ◔◡◔)っ Enso (っ◔◡◔)っ",
                 colour=enso_embedmod_colours,
                 timestamp=datetime.datetime.utcnow())

    # Setting thumbnail and author
    enso.set_thumbnail(url=guild_icon)

    # Setting up the fields in a separate array
    enso_fields = [
        (f"**{self.ctx.prefix}enso `<person>`**",
         "\nShows Specified Image of User" +
         f"\n(Using **{self.ctx.prefix}enso** by itself shows random image of users in the server)",
         True),
        (f"**{self.ctx.prefix}enso `list`**",
         "\nReturns all Users", False),
        (f"**{self.ctx.prefix}rules**",
         "\nFull ruleset for Enso", True),
        (f"**{self.ctx.prefix}roles**",
         "\nLeveling and xp system in Enso", True),
    ]

    # Setting up the embed for the Waifu/Husbandos
    waifu_and_husbando = Embed(title="(っ◔◡◔)っ Waifu/Husbando Commands (っ◔◡◔)っ",
                               colour=enso_embedmod_colours,
                               timestamp=datetime.datetime.utcnow())

    # Setting thumbnail and author
    waifu_and_husbando.set_thumbnail(url=guild_icon)

    # Setting up the fields in a separate array
    waifu_and_husbando_fields = [
        (f"**{self.ctx.prefix}w `<waifu>`**",
         "\nShows Specified Image of Waifu" +
         f"\n(Using **{self.ctx.prefix}w** shows random image of Waifu)", True),
        (f"**{self.ctx.prefix}h `<husbando>`**",
         "\nShows Specified Image of Husbando" +
         f"\n(Using **{self.ctx.prefix}h** shows random image of Husbando)", False),
        (f"**{self.ctx.prefix}w `list`**",
         "\nReturns all Waifus", True),
        (f"**{self.ctx.prefix}h `list`**",
         "\nReturns all Husbandos", True)]

    # Setting up the embed for the Important Commands
    important = Embed(title="(っ◔◡◔)っ Important (っ◔◡◔)っ",
                      colour=enso_embedmod_colours,
                      timestamp=datetime.datetime.utcnow())

    # Setting thumbnail and author
    important.set_thumbnail(url=guild_icon)

    # Setting up the fields in a separate array
    important_fields = [
        (f"**{self.ctx.prefix}userinfo**",
         "\nReturns information about the user", True),
        (f"**{self.ctx.prefix}serverinfo**",
         "\nReturns information about the server", True),
        (f"**{self.ctx.prefix}help**",
         "\nSee every command in the bot", True)]

    # Setting up the embed for modmail
    modmail = Embed(title="(っ◔◡◔)っ ModMail (っ◔◡◔)っ",
                    colour=enso_embedmod_colours,
                    timestamp=datetime.datetime.utcnow())

    # Setting thumbnail and author
    modmail.set_thumbnail(url=guild_icon)

    # Setting up the fields in a separate array
    modmail_fields = [(f"**{self.ctx.prefix}mmsetup setup modmail `<channelID>`**",
                       "Sets up the modmail system in the guild,"
                       "channelID given will be the channel that the user will interact with", False),
                      (f"**{self.ctx.prefix}mmsetup update modmail `<channelID>`**",
                       "Updates the channel that the modmail will be sent to", False),
                      (f"**{self.ctx.prefix}mmsetup delete modmail**",
                       "Existing modmail system will be deleted", False)]

    """    fields = [fun_fields, interactive_fields, interactive_fields_2,
              relationship_fields, enso_fields, waifu_and_husbando_fields,
              important_fields, modmail_fields]
    embeds = [fun, interactive, interactive_2,
              relationship, enso, waifu_and_husbando,
              important, modmail]

    for embed in embeds:
        for field in fields:
            # Add fields to the embed
            for name, value, inline in field:
                embed.add_field(name=name, value=value, inline=inline)"""

    # Add fields to the embed
    for name, value, inline in fun_fields:
        fun.add_field(name=name, value=value, inline=inline)

    # Add fields to the embed
    for name, value, inline in interactive_fields:
        interactive.add_field(name=name, value=value, inline=inline)

    # Add fields to the embed
    for name, value, inline in interactive_fields_2:
        interactive_2.add_field(name=name, value=value, inline=inline)

    # Add fields to the embed
    for name, value, inline in relationship_fields:
        relationship.add_field(name=name, value=value, inline=inline)

    # Add fields to the embed
    for name, value, inline in enso_fields:
        enso.add_field(name=name, value=value, inline=inline)

    # Add fields to the embed
    for name, value, inline in waifu_and_husbando_fields:
        waifu_and_husbando.add_field(name=name, value=value, inline=inline)

    # Add fields to the embed
    for name, value, inline in important_fields:
        important.add_field(name=name, value=value, inline=inline)

    # Add fields to the embed
    for name, value, inline in modmail_fields:
        modmail.add_field(name=name, value=value, inline=inline)

    return fun, interactive, interactive_2, relationship, \
           enso, waifu_and_husbando, important, modmail


# Page 9
def misc_function(self, guild_icon):
    # Setting up the Embed for the Miscellaneous commands
    misc_commands = Embed(title="(っ◔◡◔)っ Misc (っ◔◡◔)っ",
                          colour=enso_embedmod_colours,
                          timestamp=datetime.datetime.utcnow())

    # Setting thumbnail and author
    misc_commands.set_thumbnail(url=guild_icon)

    # Setting up the fields in a separate array
    misc_fields = [
        (f"**{self.ctx.prefix}ping**",
         "\nReturns latency in ms", True),
        (f"**{self.ctx.prefix}dm `<person>`**",
         f"\nFor admins to DM Users" +
         "\n**(Perms: Co-Owner)**", True),
        (f"**{self.ctx.prefix}remindme `<time>` `<text>`**",
         "\nGet Enso~Chan to remind you in DMs", True)]

    # Add fields to the embed
    for name, value, inline in misc_fields:
        misc_commands.add_field(name=name, value=value, inline=inline)

    return misc_commands


def embeds(self):
    # Define guild icon
    guild_icon = self.ctx.guild.icon_url

    # Set the different pages of the embed
    page1, page2, page3, \
    page4, page5, page6, \
    page7, page8 = help_menu(self, guild_icon)
    page9 = misc_function(self, guild_icon)

    # Store all the categories of the menu to an array called pages
    pages = [page1, page2, page3,
             page4, page5, page6,
             page7, page8, page9]

    return pages


# Set up the Cog
class HelpMenu(menus.Menu):
    def __init__(self, i, bot):
        super().__init__()
        self.i = i
        self.bot = bot

    # Message to be sent on the initial command ~help
    async def send_initial_message(self, ctx, channel):
        # Set the first embed to the first element in the pages[]
        initial = embeds(self)[self.i]

        # Send embed
        return await channel.send(embed=initial)

    # Reaction to allow user to go to the previous page in the embed
    @menus.button('\N{LEFTWARDS BLACK ARROW}')
    async def on_left_arrow(self, payload):

        # Simple check to make sure that the reaction is performed by the user
        def check(m):
            return m.author == payload.member

        # Do nothing if the check does not return true
        if not check(self.ctx):
            return
        # Allow the page number to be decreased
        else:

            # Set self.i to (i - 1) remainder length of the array
            self.i = (self.i - 1) % len(embeds(self))
            prev_page = embeds(self)[self.i]

            # Send the embed and remove the reaction of the user
            await self.message.edit(embed=prev_page)
            await self.message.remove_reaction("⬅", self.ctx.author)

    # Reaction to allow user to go to the next page in the embed
    @menus.button('\N{BLACK RIGHTWARDS ARROW}')
    async def on_right_arrow(self, payload):

        # Simple check to make sure that the reaction is performed by the user
        def check(m):
            return m.author == payload.member

        # Do nothing if the check does not return true
        if not check(self.ctx):
            return
        # Allow the page number to be increased
        else:

            # Set self.i to (i + 1) remainder length of the array
            self.i = (self.i + 1) % len(embeds(self))
            next_page = embeds(self)[self.i]

            # Send the embed and remove the reaction of the user
            await self.message.edit(embed=next_page)
            await self.message.remove_reaction("➡", self.ctx.author)

    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def on_stop(self, payload):

        # Simple check to make sure that the reaction is performed by the user
        def check(m):
            return m.author == payload.member

        # Do nothing if the check does not return true
        if not check(self.ctx):
            return
        # Allow the embed to be deleted
        else:

            # Delete the embed and stop the function from running
            await self.message.delete()
            self.stop()


# Set up the cog
class ReactionMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @command(name="help", aliases=["Help"])
    async def help(self, ctx):
        """Returns a menu for help commands controlled by reactions"""

        # Local Variable i to allow the index of the pages[] to be modified
        i = 0

        # Send the menu to the display
        menu = HelpMenu(i, self)
        await menu.start(ctx)


def setup(bot):
    bot.add_cog(ReactionMenu(bot))
