import datetime

from discord import Embed
from discord.ext import commands, menus
from discord.ext.commands import command

from settings import enso_embedmod_colours, hammyMention


# Function to allow pages 1-4 of the help commands (Fun Commands)
def fun_function(self, guild_icon):
    # Setting up the Embed for the Fun Commands
    fun_commands = Embed(title="(っ◔◡◔)っ Fun (っ◔◡◔)っ",
                         colour=enso_embedmod_colours,
                         timestamp=datetime.datetime.utcnow())

    # Setting thumbnail and author
    fun_commands.set_thumbnail(url=guild_icon)

    # Setting up the fields in a separate array
    fun_fields = [
        (f"**{self.ctx.prefix}comp `<person>`**",
         "\nCompliment a person in the server", True),
        (f"**{self.ctx.prefix}8ball `<text>`**",
         "\nAsk a question and 8ball will give a custom response", True),
        (f"**{self.ctx.prefix}flip**",
         "\nDoes a coinflip with Big PP Or Smol PP", True),
        (f"**{self.ctx.prefix}doggo**",
         "\nLook at images of Doggos", True),
        (f"**{self.ctx.prefix}homies `<text>`**",
         "\nGenerates Homies Meme with given text", True),
        (f"**{self.ctx.prefix}owo `<text>`**",
         "\nTranslates given text to 'owo' format", True)]

    # Setting up the Embed for the Fun Commands
    fun_commands_2 = Embed(title="(っ◔◡◔)っ Interactive (っ◔◡◔)っ",
                           colour=enso_embedmod_colours,
                           timestamp=datetime.datetime.utcnow())

    # Setting thumbnail and author
    fun_commands_2.set_thumbnail(url=guild_icon)

    # Setting up the fields in a separate array
    fun_fields_2 = [
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

    # Setting up the Embed for the Fun Commands
    fun_commands_3 = Embed(title="(っ◔◡◔)っ Interactive 2 (っ◔◡◔)っ",
                           colour=enso_embedmod_colours,
                           timestamp=datetime.datetime.utcnow())

    # Setting thumbnail and author
    fun_commands_3.set_thumbnail(url=guild_icon)

    # Setting up the fields in a separate array
    fun_fields_3 = [
        (f"**{self.ctx.prefix}slap `<person>`**",
         "\nSlap a User Within The Server", True),
        (f"**{self.ctx.prefix}kill `<person>`**",
         "\nKill a User Within The Server", True),
        (f"**{self.ctx.prefix}choke `<person>`**",
         "\nChoke a User Within The Server", True)]

    # Setting up the Embed for the Fun Commands
    fun_commands_4 = Embed(title="(っ◔◡◔)っ Relationship (っ◔◡◔)っ",
                           colour=enso_embedmod_colours,
                           timestamp=datetime.datetime.utcnow())

    # Setting thumbnail and author
    fun_commands_4.set_thumbnail(url=guild_icon)

    # Setting up the fields in a separate array
    fun_fields_4 = [
        (f"**{self.ctx.prefix}marry `<person>`**",
         "\nMarry a User Within The Server", True),
        (f"**{self.ctx.prefix}divorce `<person>`**",
         "\nDivorce The Person You Are Married To", False),
        (f"**{self.ctx.prefix}minfo `<person>`**",
         "\nDisplays information about the user's current marriage" +
         f"Using {self.ctx.prefix}minfo by itself will retrieve your marriage information", True)]

    # Add the fun_commands fields to the embed
    for name, value, inline in fun_fields:
        fun_commands.add_field(name=name, value=value, inline=inline)

    # Add the fun_commands_2 fields to the embed
    for name, value, inline in fun_fields_2:
        fun_commands_2.add_field(name=name, value=value, inline=inline)

    # Add the fun_commands_3 fields to the embed
    for name, value, inline in fun_fields_3:
        fun_commands_3.add_field(name=name, value=value, inline=inline)

    # Add the fun_commands_4 fields to the embed
    for name, value, inline in fun_fields_4:
        fun_commands_4.add_field(name=name, value=value, inline=inline)

    return fun_commands, fun_commands_2, fun_commands_3, fun_commands_4


# Function to allow the second page of the help commands (Waifu/Husbandos)
def waifu_husbando_function(self, guild_icon):
    # Setting up the Embed for the Waifu/Husbandos
    waifu_husbando_commands = Embed(title="(っ◔◡◔)っ Waifus/Husbando Commands (っ◔◡◔)っ",
                                    colour=enso_embedmod_colours,
                                    timestamp=datetime.datetime.utcnow())

    # Setting thumbnail and author
    waifu_husbando_commands.set_thumbnail(url=guild_icon)

    # Setting up the fields in a separate array
    waifu_husbando_fields = [
        (f"**{self.ctx.prefix}w `list`**",
         "\nReturns all Waifus", True),
        (f"**{self.ctx.prefix}h `list`**",
         "\nReturns all Husbandos", True),
        (f"**{self.ctx.prefix}w `<waifu>`**",
         "\nShows Specified Image of Waifu" +
         f"\n(Using **{self.ctx.prefix}w shows random image of Waifu)", True),
        (f"**{self.ctx.prefix}h `<husbando>`**",
         "\nShows Specified Image of Husbando" +
         f"\n(Using **{self.ctx.prefix}h shows random image of Husbando", True)]

    # Add the waifu_husbando_commands fields to the embed
    for name, value, inline in waifu_husbando_fields:
        waifu_husbando_commands.add_field(name=name, value=value, inline=inline)

    return waifu_husbando_commands


# Function to allow the fifth page of the help commands (~enso commands)
def _enso(self, guild_icon):
    # Setting up the Embed for the ~Enso command
    _enso_commands = Embed(title="(っ◔◡◔)っ Enso (っ◔◡◔)っ",
                           colour=enso_embedmod_colours,
                           timestamp=datetime.datetime.utcnow())

    # Setting thumbnail and author
    _enso_commands.set_thumbnail(url=guild_icon)

    # Setting up the fields in a separate array
    _enso_fields = [
        (f"**{self.ctx.prefix}rules**",
         "\nFull ruleset for Enso", True),
        (f"**{self.ctx.prefix}roles**",
         "\nLeveling and xp system in Enso", True),
        (f"**{self.ctx.prefix}enso `<person>`**",
         "\nShows Specified Image of User" +
         f"\n(Using {self.ctx.prefix}enso by itself shall generate a random image of a person within all the server)",
         True),
        (f"**{self.ctx.prefix}enso `list`**",
         "\nReturns all Users", True)]

    # Add the _enso_commands fields to the embed
    for name, value, inline in _enso_fields:
        _enso_commands.add_field(name=name, value=value, inline=inline)

    return _enso_commands


# Function to allow the third page of the help commands (Miscellaneous)
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
         f"\nFor {hammyMention} to DM Users" +
         "\n**(Perms: Co-Owner)**", True),
        (f"**{self.ctx.prefix}remindme `<time>` `<text>`**",
         "\nGet Enso~Chan to remind you in DMs", True)]

    # Add the misc_commands fields to the embed
    for name, value, inline in misc_fields:
        misc_commands.add_field(name=name, value=value, inline=inline)

    return misc_commands


def modmailEmbed(self, guild_icon):
    # Setting up the Embed for the Miscellaneous commands
    modmailPage = Embed(title="(っ◔◡◔)っ ModMail (っ◔◡◔)っ",
                        colour=enso_embedmod_colours,
                        timestamp=datetime.datetime.utcnow())

    # Setting thumbnail and author
    modmailPage.set_thumbnail(url=guild_icon)

    # Setting up the fields in a separate array
    misc_fields = [(f"**{self.ctx.prefix}", "", True)]

    # Add the misc_commands fields to the embed
    for name, value, inline in misc_fields:
        modmailPage.add_field(name=name, value=value, inline=inline)

    return modmailPage


# Function to allow the fourth page of the help commands (Important)
def important_function(self, guild_icon):
    # Setting up the Embed for the Important Commands
    important_commands = Embed(title="(っ◔◡◔)っ Important (っ◔◡◔)っ",
                               colour=enso_embedmod_colours,
                               timestamp=datetime.datetime.utcnow())

    # Setting thumbnail and author
    important_commands.set_thumbnail(url=guild_icon)

    # Setting up the fields in a separate array
    important_fields = [
        (f"**{self.ctx.prefix}userinfo**",
         "\nReturns information about the user", True),
        (f"**{self.ctx.prefix}serverinfo**",
         "\nReturns information about the server", True),
        (f"**{self.ctx.prefix}help**",
         "\nSee every command in the bot", True)]

    # Add the important_fields to the embed
    for name, value, inline in important_fields:
        important_commands.add_field(name=name, value=value, inline=inline)

    return important_commands


def embeds(self):
    # Define guild icon
    guild_icon = self.ctx.guild.icon_url

    # Set the different pages of the embed
    page1, page2, page3, page4 = fun_function(self, guild_icon)
    page5 = _enso(self, guild_icon)
    page6 = waifu_husbando_function(self, guild_icon)
    page7 = misc_function(self, guild_icon)
    page8 = important_function(self, guild_icon)

    # Store all the categories of the menu to an array called pages
    pages = [page1, page2, page3, page4, page5, page6, page7, page8]

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

    @command(name="help2", aliases=["Help"])
    async def help(self, ctx):
        """Returns a menu for help commands controlled by reactions"""

        # Local Variable i to allow the index of the pages[] to be modified
        i = 0

        # Send the menu to the display
        menu = HelpMenu(i, self)
        await menu.start(ctx)


def setup(bot):
    bot.add_cog(ReactionMenu(bot))
