import datetime

from discord import Embed, Colour
from discord.ext import commands
from discord.ext import menus
from discord.ext.commands import command


def fun_function(guild_icon, enso_name, enso_icon):
    fun_commands = Embed(title="```(っ◔◡◔)っ Fun Commands (っ◔◡◔)っ```",
                         colour=Colour(0xFF69B4),
                         timestamp=datetime.datetime.utcnow())

    fun_commands.set_thumbnail(url=guild_icon)
    fun_commands.set_author(name=enso_name,
                            icon_url=enso_icon)

    fun_fields = [("\u200b", "`➳ ~attack [person]`" +
                   "\n Allows the user to throw an insult to a person in the server" +
                   "\n *(Perms: Co-Owner)*", True),
                  ("\u200b", "`➳ ~comp [person]`" +
                   "\n Allows the user to compliment a person in the server" +
                   "\n *(Perms: Everyone)*", True),
                  ("\u200b", "`➳ ~8ball [text]`" +
                   "\n Allows the user to ask a question and 8ball will give a custom response" +
                   "\n *(Perms: everyone)*", True),
                  ("\u200b", "`➳ ~lemon [person]`" +
                   "\n Allows the user to give a lemon to a person in the server" +
                   "\n *(Perms: Everyone)*", True),
                  ("\u200b", "`➳ ~slap [person]`" +
                   "\n Allows the user to slap a person in the server" +
                   "\n *(Perms: Everyone)*", True),
                  ("\u200b", "`➳ ~kill [person]`" +
                   "\n Allows the user to kill a person in the server" +
                   "\n *(Perms: Everyone)*", True),
                  ("\u200b", "`➳ ~pat [person]`" +
                   "\n Allows the user to pat a person in the server" +
                   "\n *(Perms: Everyone)*", True),
                  ("\u200b", "`➳ ~kiss [person]`" +
                   "\n Allows the user to kiss a person in the server" +
                   "\n *(Perms: Everyone)*", True),
                  ("\u200b", "`➳ ~cuddle [person]`" +
                   "\n Allows the user to cuddle a person in the server" +
                   "\n *(Perms: Everyone)*", True),
                  ("\u200b", "`➳ ~flip`" +
                   "\n Allows the user to 'throw a coin' and get a response with a 50/50 chance" +
                   "\n *(Perms: Everyone)*", True),
                  ("\u200b", "`➳ ~doggo`" +
                   "\n Allows the user to look at an image of a doggo (Over 20k Images Available" +
                   "\n *(Perms: Everyone)*", True)]

    # Add the fun_commands fields to the embed
    for name, value, inline in fun_fields:
        fun_commands.add_field(name=name, value=value, inline=inline)

    return fun_commands


def waifu_husbando_function(guild_icon, enso_name, enso_icon):
    waifu_husbando_commands = Embed(title="```(っ◔◡◔)っ Waifus/Husbando Commands (っ◔◡◔)っ```",
                                    colour=Colour(0xFF69B4),
                                    timestamp=datetime.datetime.utcnow())

    waifu_husbando_commands.set_thumbnail(url=guild_icon)
    waifu_husbando_commands.set_author(name=enso_name,
                                       icon_url=enso_icon)

    waifu_husbando_fields = [("\u200b", "`➳ ~w [waifu]`" +
                              "\n Allows for a randomly generated image of a Waifu to be shown" +
                              "\n *(Perms: Everyone)*", True),
                             ("\u200b", "`➳ ~h [husbando]`" +
                              "\n Allows for a randomly generated image of a Husbando to be shown" +
                              "\n *(Perms: Everyone)*", True),
                             ("\u200b", "`➳ ~w list`" +
                              "\n Returns a list of Waifu's that are in the bot " +
                              "\n *(Perms: Everyone)*", True),
                             ("\u200b", "`➳ ~h list`" +
                              "\n Returns a list of Husbando's that are in the bot " +
                              "\n *(Perms: Everyone)*", True),
                             ("\u200b", "`➳ ~enso [person]`" +
                              "\n Allows for a randomly generated image of the member specified" +
                              "\n (Using ~enso by itself shall generate a random image of a person within all the server)" +
                              "\n *(Perms: Everyone)*", True),
                             ("\u200b", "`➳ ~enso [person]`" +
                              "\n Allows for a randomly generated image of the member specified" +
                              "\n (Using ~enso by itself shall generate a random image of a person within all the server)" +
                              "\n *(Perms: Everyone)*", True),
                             ("\u200b", "`➳ ~enso list`" +
                              "\n Returns a list of the people's images currently in the bot" +
                              "\n *(Perms: Everyone)*", True)]

    # Add the waifu_husbando_commands fields to the embed
    for name, value, inline in waifu_husbando_fields:
        waifu_husbando_commands.add_field(name=name, value=value, inline=inline)

    return waifu_husbando_commands


def misc_function(guild_icon, enso_name, enso_icon):
    misc_commands = Embed(title="```(っ◔◡◔)っ Misc Commands (っ◔◡◔)っ```",
                          colour=Colour(0xFF69B4),
                          timestamp=datetime.datetime.utcnow())

    misc_commands.set_thumbnail(url=guild_icon)
    misc_commands.set_author(name=enso_name,
                             icon_url=enso_icon)

    misc_fields = [("\u200b", "`➳ ~ping`" +
                    "\n Returns Pong! Along With The Latency in ms" +
                    "\n *(Perms: Co-Owner)*", True),
                   ("\u200b", "`➳ ~rolemenu`" +
                    "\n Allows for the users to get self ping-able roles" +
                    "\n *(Perms: Co-Owner)*", True),
                   ("\u200b", "`➳ ~dm [person]`" +
                    "\n Allows Hammmy to dm anyone in the server through Enso~Chan!" +
                    "\n *(Perms: Co-Owner)*", True),
                   ("\u200b", "`➳ ~userinfo`" +
                    "\n Returns information about the user (Name, Roles, Joined Date, Created Date, etc)" +
                    "\n *(Perms: Everyone)*", True),
                   ("\u200b", "`➳ ~serverinfo`" +
                    "\n Returns information about the server (Owner, Members, Region, Bots etc etc)" +
                    "\n *(Perms: Everyone)*", True),
                   ("\u200b", "`➳ ~rules`" +
                    "\n Returns the entire ruleset for the server" +
                    "\n *(Perms: Everyone)*", True),
                   ("\u200b", "`➳ ~roles`" +
                    "\n Shows you how the leveling and xp system works, as well as displaying the order of leveled roles" +
                    "\n *(Perms: Everyone)*", True),
                   ("\u200b", "`➳ ~remindme [time] [text]`" +
                    "\n Allows the user to get Enso~Chan to remind them in dms of anything that they want" +
                    "\n *(Perms: Everyone)*", True),
                   ("\u200b", "`➳ ~help`" +
                    "\n Allows you to see every command in the bot so far" +
                    "\n *(Perms: Everyone)*", True)]

    # Add the misc_commands fields to the embed
    for name, value, inline in misc_fields:
        misc_commands.add_field(name=name, value=value, inline=inline)

    return misc_commands


def stop_embed(enso_name, enso_icon):
    misc_commands = Embed(title="```Help Commands Embed Closed!```",
                          colour=Colour(0xFF69B4),
                          timestamp=datetime.datetime.utcnow())

    misc_commands.set_author(name=enso_name,
                             icon_url=enso_icon)

    return misc_commands


def embeds(self):
    try:
        # Define guild icon, enso bot icon and enso bot name
        guild_icon = self.ctx.guild.icon_url
        enso_icon = self.bot.user.avatar_url
        enso_name = self.bot.user.display_name

        page1 = fun_function(guild_icon, enso_name, enso_icon)
        page2 = waifu_husbando_function(guild_icon, enso_name, enso_icon)
        page3 = misc_function(guild_icon, enso_name, enso_icon)
        page4 = stop_embed(enso_name, enso_icon)

        # Store all the categories of the menu to an array called pages
        pages = [page1, page2, page3, page4]

        return pages

    except Exception as ex:
        print(ex)


class HelpMenu(menus.Menu):
    def __init__(self, i):
        super().__init__()
        self.i = i

    async def send_initial_message(self, ctx, channel):
        initial = embeds(self)[self.i]
        return await channel.send(embed=initial)

    @menus.button('\N{LEFTWARDS BLACK ARROW}')
    async def on_left_arrow(self, payload):
        def check(m):
            return m.author == payload.member

        if check(self.ctx):
            self.i = (self.i - 1) % len(embeds(self))
            prev_page = embeds(self)[self.i]

            await self.message.edit(embed=prev_page)
            await self.message.remove_reaction("⬅", self.ctx.author)
        else:
            return

    @menus.button('\N{BLACK RIGHTWARDS ARROW}')
    async def on_right_arrow(self, payload):
        def check(m):
            return m.author == payload.member

        if check(self.ctx):
            self.i = (self.i + 1) % len(embeds(self))
            next_page = embeds(self)[self.i]

            await self.message.edit(embed=next_page)
            await self.message.remove_reaction("➡", self.ctx.author)
        else:
            return

    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def on_stop(self, payload):
        stop = embeds(self)[-1]
        await self.message.edit(embed=stop)
        self.stop()


# Set up the cog
class ReactionMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="help", aliases=["Help"])
    async def menu_example(self, ctx):
        i = 0
        m = HelpMenu(i)
        await m.start(ctx)


def setup(bot):
    bot.add_cog(ReactionMenu(bot))
