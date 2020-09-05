# Ensō~Chan - A Multi Purpose Discord Bot That Has Everything Your Server Needs!
# Copyright (C) 2020  Hamothy

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import datetime

import aiohttp
from decouple import config
from discord import Embed
from discord.ext.commands import Cog, group, bot_has_permissions, command

from cogs.libs.paginators import SimpleMenu, MWLMenu

my_waifu_list_auth = config('MYWAIFULIST_AUTH')


class WaifuCommandNotFound(Exception):
    """Exception raised for errors when user does not use the right arguments for waifu command

    Attributes:
        waifu -- input command which cause the error
        message -- explanation of the error
    """

    def __init__(self, waifu, ctx):
        self.command = waifu
        self.bot = ctx.bot
        self.message = f"Error! Use **{ctx.prefix}help {self.command}** to see {self.command} commands"
        super().__init__(self.message)

    def __str__(self):
        return f'{self.command} -> {self.message}'


def store_in_dict(_dict, api):
    """Store the waifu data in dicts"""

    # Store all the shows with the name as the key
    for item in api:
        _dict[item["name"]] = {}
        for value in item:
            store_dict(_dict, item, value)


def store_dict(dict_, key, value):
    """Method to store waifu's in the new dict"""

    dict_[key["name"]][value] = key[value]


async def get_from_api(self, ctx, url):
    """Retrieving data from API"""

    url = f"https://mywaifulist.moe/api/v1/{url}"

    # Retrieve random or daily waifu from API
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=self.headers) as resp:

            # Store waifu's in dict when request is successful, else send an error
            if resp.status == 200:
                api_dict = await resp.json()
                _dict = api_dict["data"]

            # Send error if something went wrong internally/while grabbing data from API
            else:
                await self.bot.generate_embed(ctx, desc="**Something went wrong with MyWaifuList!**")

    return _dict


async def post_from_api(self, i, ctx, term, _dict, url):
    """Posting information to the API and getting data back"""

    data = {"term": term,
            'content-type': "application/json"}

    # Searching API for waifu(s)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=self.headers) as resp:
            # Store waifu's in dict when request is successful, else send an error
            if resp.status == 200:
                api_data = await resp.json()

            # Send error if something went wrong internally/while grabbing data from API
            else:
                await self.bot.generate_embed(ctx, desc="**Something went wrong with MyWaifuList!**")

    # As long as data is returned
    # Store all data from the api in dict
    if len(api_data["data"]) > 0:
        for item in api_data["data"]:
            _dict[item["name"]] = {}
            for value in item:
                store_dict(_dict, item, value)

    # When no waifu has been retrieved, send error message to the user
    else:
        await self.bot.generate_embed(ctx, desc="**Waifu/Anime Not Found!**")
        return False

    # Get the instance of the bot
    bot = ctx.guild.get_member(self.bot.user.id)
    # Get the permissions of the channel
    perms = bot.permissions_in(ctx.message.channel)

    # Send the menu to the display
    menu = MWLMenu(i, perms, _dict, self.bot)

    return menu


def anime_embed(self, anime):
    """Generate embed of single anime's"""

    # Get all the data to be displayed in the embed
    name = anime["name"]
    anime_id = anime["id"]
    og_name = anime["original_name"]
    picture = anime["display_picture"]
    url = anime["url"]
    romaji_name = anime["romaji_name"]
    release_date = anime["release_date"]
    airing_start = anime["airing_start"]
    airing_end = anime["airing_end"]
    episode_count = anime["episode_count"]

    # Only setting the description if original name is returned from the API
    desc = og_name if og_name else Embed.Empty

    # Only setting the series date information if they exist
    rel_date = release_date if release_date else self.bot.cross
    air_start = airing_start if airing_start else self.bot.cross
    air_end = airing_end if airing_end else self.bot.cross
    ep_count = episode_count if episode_count else self.bot.cross

    fields = [("Airing Start Date", air_start, True),
              ("Airing End Date", air_end, True),
              ("\u200b", "\u200b", True),
              ("Release Date", rel_date, True),
              ("Episode Count", ep_count, True),
              ("\u200b", "\u200b", True)]

    embed = Embed(title=name, description=desc,
                  url=url,
                  colour=self.bot.random_colour())
    embed.set_author(name=f"ID: {anime_id}")
    embed.set_image(url=picture)
    if romaji_name:
        embed.set_footer(text=f"{romaji_name} | Powered by MyWaifuList")
    else:
        embed.set_footer(text="Powered By MyWaifuList")

    # Add fields to the embed
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    return embed


def waifu_embed(self, waifu, _type):
    """Generate embed of single waifu's"""

    # Get all the data to be displayed in the embed
    name = waifu["name"]
    og_name = waifu["original_name"]
    picture = waifu["display_picture"]
    url = waifu["url"]
    waifu_id = waifu["id"]
    likes = waifu["likes"]
    trash = waifu["trash"]
    waifu_type = waifu["type"]

    # Set different values for description based on the command
    if _type == "random":
        desc = f"{og_name} | Random {waifu_type}" if waifu["original_name"] else f"Random {waifu_type}"
    elif _type == "daily":
        desc = f"{og_name} | Daily {waifu_type}" if waifu["original_name"] else f"Daily {waifu_type}"

    embed = Embed(title=name, description=desc,
                  colour=self.bot.random_colour(),
                  url=url)
    embed.set_author(name=f"ID: {waifu_id}")
    embed.set_image(url=picture)
    embed.set_footer(text=f"❤️ {likes} 🗑️ {trash} | Powered by MyWaifuList")

    return embed


async def detailed_waifu_embed(self, waifu, author, ctx):
    """Generate embed of single waifu's (detailed)"""

    not_found = "https://media.discordapp.net/attachments/741072426984538122/748586578074664980/DzEZ4UsXgAAcFjN.png?width=423&height=658"

    # Get all the data to be displayed in the embed
    name = waifu["name"]
    waifu_id = waifu["id"]
    url = waifu["url"]
    picture = waifu["display_picture"]
    likes = waifu["likes"]
    trash = waifu["trash"]

    og_name = waifu["original_name"]
    romaji_name = waifu["romaji_name"]
    age = waifu["age"]
    b_day = waifu["birthday_day"]
    b_month = waifu["birthday_month"]
    b_year = waifu["birthday_year"]
    popularity_rank = waifu["popularity_rank"]
    like_rank = waifu["like_rank"]
    trash_rank = waifu["trash_rank"]

    height = waifu["height"]
    weight = waifu["weight"]
    waist = waifu["waist"]
    bust = waifu["bust"]
    hip = waifu["hip"]

    # Only setting up description if waifu og_name has a value
    desc = f"**Waifu ID:** {waifu_id}\n"
    desc += f"**Original Name:** {og_name}\n" if og_name else f"**Original Name:** {self.bot.cross}\n"
    desc += f"**Romaji Name:** {romaji_name}\n" if romaji_name else f"**Romaji Name:** {self.bot.cross}\n"

    desc += f"\n**Age:** {age}\n" if age else f"**Age:** {self.bot.cross}\n"
    desc += f"**Birthday-Day:** {b_day}\n" if b_day else f"**Birthday-Day:** {self.bot.cross}\n"
    desc += f"**Birthday-Month:** {b_month}\n" if b_month else f"**Birthday-Month:** {self.bot.cross}\n"
    desc += f"**Birthday-Year:** {b_year}\n" if b_year else f"**Birthday-Year:** {self.bot.cross}\n"

    height = f"**Height:** {height}cm" if height != "0.00" else f"**Height:** {self.bot.cross}"
    weight = f"**Weight:** {weight}kg" if weight != "0.00" else f"**Weight:** {self.bot.cross}"
    waist = f"**Waist:** {waist}cm" if waist != "0.00" else f"**Waist:** {self.bot.cross}"
    bust = f"**Bust:** {bust}cm" if bust != "0.00" else f"**Bust:** {self.bot.cross}"
    hip = f"**Hip:** {hip}cm" if hip != "0.00" else f"**Hip:** {self.bot.cross}"

    # Only setting up the ranks if they are returned
    pop_rank_string = f"**Popularity Rank:** {popularity_rank}\n" if popularity_rank else f"**Popularity Rank:** {self.bot.cross}\n"
    like_rank_string = f"**Like Rank:** {like_rank}\n" if like_rank else f"**Like Rank:** {self.bot.cross}\n"
    trash_rank_string = f"**Trash Rank:** {trash_rank}\n" if trash_rank else f"**Trash Rank:** {self.bot.cross}\n"

    fields = [("Measurements",
               f"{height}"
               f"\n{weight}"
               f"\n{waist}"
               f"\n{bust}"
               f"\n{hip}", True),

              ("Ranks",
               f"{pop_rank_string}"
               f"{like_rank_string}"
               f"{trash_rank_string}", True)]

    # Only using image if it can be displayed, else display 404 image
    picture_url = picture if picture.endswith((".jpeg", ".png", ".jpg")) else not_found
    # Different titles depending on if author was given or not
    title = f"True Love | {name}" if author else f"Detailed Waifu | {name}"

    detailed = Embed(title=title, description=desc,
                     colour=self.bot.random_colour(),
                     url=url)
    detailed.set_image(url=picture_url)
    detailed.set_footer(text=f"❤️ {likes} 🗑️ {trash} | Powered by MyWaifuList")

    # Add fields to the embed
    for name, value, inline in fields:
        detailed.add_field(name=name, value=value, inline=inline)

    # Get the permissions of the channel
    perms = ctx.guild.me.permissions_in(ctx.message.channel)

    if author:
        menu = SimpleMenu(0, "User Information", perms, [author, detailed], self)
        await menu.start(ctx)
    else:
        return detailed


async def user_embed(self, user, ctx):
    """Generate embed of user profile information"""

    love = False

    # Get all the data to be displayed in the embed
    name = user["name"]
    avatar = user["avatar"] if user[
        "avatar"] else "https://media.discordapp.net/attachments/741072426984538122/748586578074664980/DzEZ4UsXgAAcFjN.png?width=423&height=658"
    joined = user["joined"]
    id = user["id"]
    waifus_created = user["waifus_created"]
    waifus_liked = user["waifus_liked"]
    waifus_trashed = user["waifus_trashed"]
    main_love = user["true_love"]
    profile_url = f"https://mywaifulist.moe/user/{id}"

    date_time_obj = datetime.datetime.strptime(joined, '%Y-%m-%d %H:%M:%S')
    joined_at = date_time_obj.strftime("%a, %b %d, %Y\n%I:%M:%S %p")

    desc = f"**Waifu's Created:** {waifus_created}" \
           f"\n**Waifu's Liked:** {waifus_liked}" \
           f"\n**Waifu's Trashed:** {waifus_trashed}"
    author = Embed(title=name, description=desc,
                   colour=self.bot.random_colour(),
                   url=profile_url)
    author.add_field(name="Joined Date", value=joined_at, inline=False)
    author.set_thumbnail(url=avatar)
    author.set_footer(text=f"User ID: {id} | Powered by MyWaifuList")

    if main_love["slug"]:
        love = True
        slug = main_love["slug"]

        # Get true love details from the API
        true_love = await get_from_api(self, ctx, f"waifu/{slug}")
        await detailed_waifu_embed(self, true_love, author, ctx)

    return author, love


class Anime(Cog):
    """
    Search MyWaifuList for Waifu's, Anime's and more!
    Please keep in mind that this API is in ALPHA (And it is a community driven website.)
    Searches might not return fully detailed results and images may be missing
    """

    # TODO: ADD AIRING SHOWS BY SEASON COMMAND
    # TODO: ADD USER WAIFUS COMMAND

    def __init__(self, bot):
        self.bot = bot
        self.headers = {'apikey': my_waifu_list_auth}

    @Cog.listener()
    async def on_ready(self):
        """Printing out that Cog is ready on startup"""
        print(f"{self.__class__.__name__} Cog has been loaded!\n-----")

    @group(name="airing", invoke_without_command=True, case_insensitive=True, usage="`anime|best|popular|trash`")
    @bot_has_permissions(embed_links=True, add_reactions=True)
    async def airing(self, ctx):
        """
        Display's airing anime and waifu's within those anime's
        """

        error = WaifuCommandNotFound(ctx.command, ctx)
        await self.bot.generate_embed(ctx, desc=error.message)

    @airing.command(name="trash", aliases=["worst", "garbage"])
    @bot_has_permissions(embed_links=True, add_reactions=True)
    async def airing_trash(self, ctx):
        """Get the worst waifu’s from the airing anime"""

        # Variables to set up the reaction menu
        i = 0
        airing_trash = {}
        trash_waifus = await get_from_api(self, ctx, "airing/trash")
        store_in_dict(airing_trash, trash_waifus)

        # Get the instance of the bot
        bot = ctx.guild.get_member(self.bot.user.id)
        # Get the permissions of the channel
        perms = bot.permissions_in(ctx.message.channel)

        # Send the menu to the display
        menu = MWLMenu(i, perms, airing_trash, self.bot)
        await menu.start(ctx)

    @airing.command(name="popular", aliases=["pop"])
    @bot_has_permissions(embed_links=True, add_reactions=True)
    async def airing_popular(self, ctx):
        """Get the most popular waifu’s from the airing anime"""

        # Variables to setup the reaction menu
        i = 0
        airing_popular = {}
        popular_waifus = await get_from_api(self, ctx, "airing/popular")
        store_in_dict(airing_popular, popular_waifus)

        # Get the instance of the bot
        bot = ctx.guild.get_member(self.bot.user.id)
        # Get the permissions of the channel
        perms = bot.permissions_in(ctx.message.channel)

        # Send the menu to the display
        menu = MWLMenu(i, perms, airing_popular, self.bot)
        await menu.start(ctx)

    @airing.command(name="best")
    @bot_has_permissions(embed_links=True, add_reactions=True)
    async def airing_best(self, ctx):
        """Get the best waifu’s from the airing anime"""

        # Local Variable i to allow the pages to be modified
        i = 0
        airing_best = {}
        best_waifus = await get_from_api(self, ctx, "airing/best")
        store_in_dict(airing_best, best_waifus)

        # Get the instance of the bot
        bot = ctx.guild.get_member(self.bot.user.id)
        # Get the permissions of the channel
        perms = bot.permissions_in(ctx.message.channel)

        # Send the menu to the display
        menu = MWLMenu(i, perms, airing_best, self.bot)
        await menu.start(ctx)

    @airing.command(name="anime", aliases=["show", "series"])
    @bot_has_permissions(embed_links=True, add_reactions=True)
    async def airing_anime(self, ctx):
        """Display the current airing anime"""

        # Local Variable i to allow the pages to be modified
        i = 0
        anime_dict = {}
        animes = await get_from_api(self, ctx, "airing")
        store_in_dict(anime_dict, animes)

        # Get the instance of the bot
        bot = ctx.guild.get_member(self.bot.user.id)
        # Get the permissions of the channel
        perms = bot.permissions_in(ctx.message.channel)

        # Send the menu to the display
        menu = MWLMenu(i, perms, anime_dict, self.bot)
        await menu.start(ctx)

    @group(name="waifu", invoke_without_command=True, case_insensitive=True, usage="`daily|random`")
    @bot_has_permissions(embed_links=True)
    async def waifu(self, ctx):
        """
        Waifu's that are retrieved from MyWaifuList
        """

        error = WaifuCommandNotFound(ctx.command, ctx)
        await self.bot.generate_embed(ctx, desc=error.message)

    @waifu.command(name="daily")
    @bot_has_permissions(embed_links=True)
    async def daily_waifu(self, ctx):
        """Returns the Daily Waifu from MyWaifuList"""

        waifu = await get_from_api(self, ctx, "meta/daily")
        await ctx.send(embed=waifu_embed(self, waifu, "daily"))

    @waifu.command(name="random", aliases=["rnd"])
    @bot_has_permissions(embed_links=True)
    async def random_waifu(self, ctx):
        """Returning a Random Waifu from MyWaifuList"""

        waifu = await get_from_api(self, ctx, "meta/random")
        await ctx.send(embed=waifu_embed(self, waifu, "random"))

    @group(name="anime", aliases=["series", "shows"],
           invoke_without_command=True, case_insensitive=True,
           usage="`<MWLAnimeID>`")
    @bot_has_permissions(embed_links=True)
    async def anime(self, ctx, term: int):
        """Returning information about a given series (MWL ID ONLY)"""

        anime = await get_from_api(self, ctx, f"series/{term}")
        await ctx.send(embed=anime_embed(self, anime))

    @anime.command(name="waifu", usage="`<MWLAnimeID>`")
    @bot_has_permissions(embed_links=True)
    async def anime_waifus(self, ctx, term: int):
        """Return the waifu's of the given anime (MWL ID ONLY)"""

        i = 0
        anime_waifus = {}
        waifus = await get_from_api(self, ctx, f"series/{term}/waifus")

        for item in waifus:
            # Don't bother storing Hentai's or Games (Not yet until I figure out what data they send)
            if item["type"] in ["Waifu", "Husbando"]:
                anime_waifus[item["name"]] = {}
                for value in item:
                    store_dict(anime_waifus, item, value)

        # Get the instance of the bot
        bot = ctx.guild.get_member(self.bot.user.id)
        # Get the permissions of the channel
        perms = bot.permissions_in(ctx.message.channel)

        # Send the menu to the display
        menu = MWLMenu(i, perms, anime_waifus, self.bot)
        await menu.start(ctx)

    @command("detailedwaifu", aliases=["dwaifu"], usage="`<MWLWaifuID>`")
    @bot_has_permissions(embed_links=True)
    async def detailed_waifu(self, ctx, term: int):
        """Returns detailed information about a waifu (MWL ID ONLY)"""

        waifu = await get_from_api(self, ctx, f"waifu/{term}")
        embed = await detailed_waifu_embed(self, waifu, None, ctx)
        await ctx.send(embed=embed)

    @command(name="profile", aliases=["user"], usage="`<MWLUserID>`")
    @bot_has_permissions(embed_links=True)
    async def mwl_user_profile(self, ctx, term: int):
        """Returning the MWL User Profile requested"""

        user = await get_from_api(self, ctx, f"user/{term}")
        embed, love = await user_embed(self, user, ctx)
        if not love:
            await ctx.send(embed=embed)

    @command(name="search", aliases=["lookup"], usage="`<waifu|anime>`")
    @bot_has_permissions(embed_links=True, add_reactions=True)
    async def search(self, ctx, *, term: str):
        """Search the entire website! (Anime|Manga|Waifus|Husbandos)"""

        # Local Variable i to allow the index of the embeds to be modified
        i = 0

        anime_or_waifu = {}
        url = "https://mywaifulist.moe/api/v1/search/"

        if menu := await post_from_api(self, i, ctx, term, anime_or_waifu, url):
            await menu.start(ctx)

    @command(name="betasearch", aliases=["bsearch"], usage="`<waifu|anime>`")
    @bot_has_permissions(embed_links=True, add_reactions=True)
    async def beta_search(self, ctx, *, term: str):
        """Search the entire website - more aggressive searching! (Anime|Manga|Waifus|Husbandos)"""

        # Local Variable i to allow the index of the embeds to be modified
        i = 0

        anime_or_waifu = {}
        url = "https://mywaifulist.moe/api/v1/search/beta"

        if menu := await post_from_api(self, i, ctx, term, anime_or_waifu, url):
            await menu.start(ctx)


def setup(bot):
    bot.add_cog(Anime(bot))
