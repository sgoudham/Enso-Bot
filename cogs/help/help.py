from discord import Embed
from discord.ext import commands, menus
from discord.ext.commands import command

from settings import blank_space, enso_embedmod_colours, time, ensoMention


# Function to allow the first page of the help commands (Fun Commands)
def fun_function(self, guild_icon, enso_name, enso_icon):
    # Setting up the Embed for the Fun Commands
    fun_commands = Embed(title="```(っ◔◡◔)っ Fun Commands (っ◔◡◔)っ```",
                         colour=enso_embedmod_colours,
                         timestamp=time)

    # Setting thumbnail and author
    fun_commands.set_thumbnail(url=guild_icon)
    fun_commands.set_author(name=enso_name,
                            icon_url=enso_icon)

    # Setting up the fields in a separate array
    fun_fields = [
        (blank_space, f"`{self.ctx.prefix}attack [person]`" +
         "\n Allows the user to throw an insult to a person in the server" +
         "\n *(Perms: Co-Owner)*", True),
        (blank_space, f"`{self.ctx.prefix}comp [person]`" +
         "\n Allows the user to compliment a person in the server" +
         "\n *(Perms: Everyone)*", True),
        (blank_space, f"`{self.ctx.prefix}8ball [text]`" +
         "\n Allows the user to ask a question and 8ball will give a custom response" +
         "\n *(Perms: everyone)*", True),
        (blank_space, f"`{self.ctx.prefix}flip`" +
         "\n Allows the user to 'throw a coin' and get a response with a 50/50 chance" +
         "\n *(Perms: Everyone)*", True),
        (blank_space, f"`{self.ctx.prefix}doggo`" +
         "\n Allows the user to look at an image of a doggo (Over 20k Images Available" +
         "\n *(Perms: Everyone)*", True)]

    # Setting up the Embed for the Fun Commands
    fun_commands_2 = Embed(title="```(っ◔◡◔)っ Fun Commands 2 (っ◔◡◔)っ```",
                           colour=enso_embedmod_colours,
                           timestamp=time)

    # Setting thumbnail and author
    fun_commands_2.set_thumbnail(url=guild_icon)
    fun_commands_2.set_author(name=enso_name,
                              icon_url=enso_icon)

    # Setting up the fields in a separate array
    fun_fields_2 = [
        (blank_space, f"`{self.ctx.prefix}lemon [person]`" +
         "\n Allows the user to give a lemon to a person in the server" +
         "\n *(Perms: Everyone)*", True),
        (blank_space, f"`{self.ctx.prefix}slap [person]`" +
         "\n Allows the user to slap a person in the server" +
         "\n *(Perms: Everyone)*", True),
        (blank_space, f"`{self.ctx.prefix}kill [person]`" +
         "\n Allows the user to kill a person in the server" +
         "\n *(Perms: Everyone)*", True),
        (blank_space, f"`{self.ctx.prefix}pat [person]`" +
         "\n Allows the user to pat a person in the server" +
         "\n *(Perms: Everyone)*", True),
        (blank_space, f"`{self.ctx.prefix}kiss [person]`" +
         "\n Allows the user to kiss a person in the server" +
         "\n *(Perms: Everyone)*", True),
        (blank_space, f"`{self.ctx.prefix}cuddle [person]`" +
         "\n Allows the user to cuddle a person in the server" +
         "\n *(Perms: Everyone)*", True)]

    # Add the fun_commands fields to the embed
    for name, value, inline in fun_fields:
        fun_commands.add_field(name=name, value=value, inline=inline)

    # Add the fun_commands_2 fields to the embed
    for name, value, inline in fun_fields_2:
        fun_commands_2.add_field(name=name, value=value, inline=inline)

    return fun_commands, fun_commands_2


# Function to allow the second page of the help commands (Waifu/Husbandos)
def waifu_husbando_function(self, guild_icon, enso_name, enso_icon):
    # Setting up the Embed for the Waifu/Husbandos
    waifu_husbando_commands = Embed(title="```(っ◔◡◔)っ Waifus/Husbando Commands (っ◔◡◔)っ```",
                                    colour=enso_embedmod_colours,
                                    timestamp=time)

    # Setting thumbnail and author
    waifu_husbando_commands.set_thumbnail(url=guild_icon)
    waifu_husbando_commands.set_author(name=enso_name,
                                       icon_url=enso_icon)

    # Setting up the fields in a separate array
    waifu_husbando_fields = [
        (blank_space, f"`{self.ctx.prefix}w [waifu]`" +
         "\n Allows for a image of the Waifu specified to be shown" +
         f"\n (Using {self.ctx.prefix}w by itself shall randomly generated image of a Waifu to be shown)" +
         "\n *(Perms: Everyone)*", True),
        (blank_space, f"`{self.ctx.prefix}h [husbando]`" +
         "\n Allows for a image of a Husbando specified to be shown" +
         f"\n (Using {self.ctx.prefix}h by itself shall randomly generated image of a Husbando to be shown)" +
         "\n *(Perms: Everyone)*", True),
        (blank_space, f"`{self.ctx.prefix}w list`" +
         "\n Returns a list of Waifu's that are in the bot " +
         "\n *(Perms: Everyone)*", True),
        (blank_space, f"`{self.ctx.prefix}h list`" +
         "\n Returns a list of Husbando's that are in the bot " +
         "\n *(Perms: Everyone)*", True),
        (blank_space, f"`{self.ctx.prefix}enso [person]`" +
         "\n Allows for a randomly generated image of the member specified" +
         f"\n (Using {self.ctx.prefix}enso by itself shall generate a random image of a person within all the server)" +
         "\n *(Perms: Everyone)*", True),
        (blank_space, f"`{self.ctx.prefix}enso list`" +
         "\n Returns a list of the people's images currently in the bot" +
         "\n *(Perms: Everyone)*", True)]

    # Add the waifu_husbando_commands fields to the embed
    for name, value, inline in waifu_husbando_fields:
        waifu_husbando_commands.add_field(name=name, value=value, inline=inline)

    return waifu_husbando_commands


# Function to allow the third page of the help commands (Miscellaneous)
def misc_function(self, guild_icon, enso_name, enso_icon):
    # Setting up the Embed for the Miscellaneous commands
    misc_commands = Embed(title="```(っ◔◡◔)っ Misc Commands (っ◔◡◔)っ```",
                          colour=enso_embedmod_colours,
                          timestamp=time)

    # Setting thumbnail and author
    misc_commands.set_thumbnail(url=guild_icon)
    misc_commands.set_author(name=enso_name,
                             icon_url=enso_icon)

    # Setting up the fields in a separate array
    misc_fields = [
        (blank_space, f"`{self.ctx.prefix}ping`" +
         "\n Returns Pong! Along With The Latency in ms" +
         "\n *(Perms: Co-Owner)*", True),
        (blank_space, f"`{self.ctx.prefix}rolemenu`" +
         "\n Allows for the users to get self ping-able roles" +
         "\n *(Perms: Co-Owner)*", True),
        (blank_space, f"`{self.ctx.prefix}dm [person]`" +
         "\n Allows Hammy to dm anyone in the server through Enso~Chan!" +
         "\n *(Perms: Co-Owner)*", True),
        (blank_space, f"`{self.ctx.prefix}remindme [time] [text]`" +
         "\n Allows the user to get Enso~Chan to remind them in dms of anything that they want" +
         "\n *(Perms: Everyone)*", True)]

    # Add the misc_commands fields to the embed
    for name, value, inline in misc_fields:
        misc_commands.add_field(name=name, value=value, inline=inline)

    return misc_commands


# Function to allow the fourth page of the help commands (Important)
def important_function(self, guild_icon, enso_name, enso_icon):
    # Setting up the Embed for the Important Commands
    important_commands = Embed(title="```(っ◔◡◔)っ Important Commands (っ◔◡◔)っ```",
                               colour=enso_embedmod_colours,
                               timestamp=time)

    # Setting thumbnail and author
    important_commands.set_thumbnail(url=guild_icon)
    important_commands.set_author(name=enso_name,
                                  icon_url=enso_icon)

    # Setting up the fields in a separate array
    important_fields = [
        (blank_space, f"`{self.ctx.prefix}userinfo`" +
         "\n Returns information about the user (Name, Roles, Joined Date, Created Date, etc)" +
         "\n *(Perms: Everyone)*", True),
        (blank_space, f"`{self.ctx.prefix}serverinfo`" +
         "\n Returns information about the server (Owner, Members, Region, Bots etc etc)" +
         "\n *(Perms: Everyone)*", True),
        (blank_space, f"`{self.ctx.prefix}rules`" +
         "\n Returns the entire ruleset for the server" +
         "\n *(Perms: Everyone)*", True),
        (blank_space, f"`{self.ctx.prefix}roles`" +
         "\n Shows you how the leveling and xp system works, as well as displaying the order of leveled roles" +
         "\n *(Perms: Everyone)*", True),
        (blank_space, f"`{self.ctx.prefix}help`" +
         "\n Allows you to see every command in the bot so far" +
         "\n *(Perms: Everyone)*", True),
        (blank_space, f"`{self.ctx.prefix}mm/modmail`" +
         "\n Allows you to send mail to the staff team!" +
         f"(Done through the dms with {ensoMention}!)" +
         "\n *(Perms: Everyone)*", True)]

    # Add the important_fields to the embed
    for name, value, inline in important_fields:
        important_commands.add_field(name=name, value=value, inline=inline)

    return important_commands


def stop_embed(self):
    # Define enso bot icon and enso bot name
    enso_icon = self.bot.user.avatar_url
    enso_name = self.bot.user.display_name

    # Set up the Embed to display when the user reacts with the stop reaction
    stop = Embed(title="**Help Commands Embed Closed!**",
                 colour=enso_embedmod_colours,
                 timestamp=time)

    # Set the name and the icon for Enso~Chan
    stop.set_author(name=enso_name,
                    icon_url=enso_icon)

    return stop


def embeds(self):
    # Define guild icon, enso bot icon and enso bot name
    guild_icon = self.ctx.guild.icon_url
    enso_icon = self.bot.user.avatar_url
    enso_name = self.bot.user.display_name

    # Set the different pages of the embed
    page1, page2 = fun_function(self, guild_icon, enso_name, enso_icon)
    page3 = waifu_husbando_function(self, guild_icon, enso_name, enso_icon)
    page4 = misc_function(self, guild_icon, enso_name, enso_icon)
    page5 = important_function(self, guild_icon, enso_name, enso_icon)

    # Store all the categories of the menu to an array called pages
    pages = [page1, page2, page3, page4, page5]

    return pages


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

        if not check(self.ctx):
            return
        else:
            # Send the stop embed which shows that the help commands embed is no longer accessible
            stop = stop_embed(self)
            await self.message.edit(embed=stop)

            # Clear the reactions in the message and stop the function
            await self.message.clear_reactions()
            self.stop()


# Set up the cog
class ReactionMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Remove default help command
        self.bot.remove_command("help")

    # ~help command that returns a menu for help commands controlled by reactions
    @command(name="help", aliases=["Help"])
    async def help(self, ctx):
        # Local Variable i to allow the index of the pages[] to be modified
        i = 0

        # Send the menu to the display
        menu = HelpMenu(i, self)
        await menu.start(ctx)


def setup(bot):
    bot.add_cog(ReactionMenu(bot))
