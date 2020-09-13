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
import io
import string
from asyncio.subprocess import Process
from platform import python_version
from time import time
from typing import Optional, Union

from PIL import Image
from PIL.ImageOps import invert
from discord import Embed, Role, File
from discord import Member, TextChannel
from discord import __version__ as discord_version
from discord.ext.commands import bot_has_permissions, guild_only, Cog, group, cooldown, BucketType
from discord.ext.commands import command
from psutil import Process, virtual_memory

from cogs.libs.functions import string_list, get_region, perms, detect_perms
from cogs.libs.paginators import SimpleMenu


def add_perms(embed, _list):
    """Add all the permission in the list to embed fields"""

    i = 0
    while i < len(_list):
        embed.add_field(name=str(_list[i].split(":")[0]).strip(),
                        value=f"<{_list[i].split('<')[1]}",
                        inline=True)
        i += 1

    return embed


class Info(Cog):
    """(User/Server/Bot etc) Information!"""

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        """Printing out that Cog is ready on startup"""
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @command(name="ping")
    async def ping(self, ctx):
        """Latency of the Bot (ms)"""

        await self.bot.generate_embed(ctx, desc=f"Pong! **{round(self.bot.latency * 1000)}ms**")

    @command(name="roleinfo", aliases=["ri"])
    @guild_only()
    async def role_info(self, ctx, *, role: Role):
        """Retrieve information about any role!"""

        # Returns the permissions that the role has within the guild
        filtered = filter(lambda x: x[1], role.permissions)
        # Replace all "_" with " " in each item and join them together
        _perms = ",".join(map(lambda x: x[0].replace("_", " "), filtered))

        # Capitalise every word in the array and filter out the permissions that are defined within the frozenset
        permission = string.capwords("".join(detect_perms(_perms, perms)))
        # Get all members within role
        member = string_list(role.members, 30, "Member")

        # Using emotes to represent bools
        mentionable = self.bot.tick if role.mention else self.bot.cross
        hoisted = self.bot.tick if role.hoist else self.bot.cross
        managed = self.bot.tick if role.managed else self.bot.cross

        # Description of the embed
        desc = f"{role.mention} **|** @{role} **<-- Colour:** {str(role.colour)}" \
               f"\n**Position -->** #{role.position} / {len(ctx.guild.roles)}" \
               f"\n** ID -->** {role.id}"

        # Set up Embed
        embed = Embed(title=f"@{role.name} Information",
                      description=desc,
                      colour=role.colour,
                      timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text=f"ID: {role.id}")

        # Setting up fields
        fields = [
            ("Creation At", role.created_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"), True),

            (f"Members ({len(role.members)})",
             f"\nHumans: {len(list(filter(lambda m: not m.bot, role.members)))}" +
             f"\nBots: {len(list(filter(lambda m: m.bot, role.members)))}", True),

            (f"Misc",
             f"\nMentionable?: {mentionable}"
             f"\nHoisted?: {hoisted}"
             f"\nManaged?: {managed}", True),

            (f"List of Members ({len(role.members)})", member or "No Members In Role", False),
            ("Key Permissions", permission or "No Key Permissions", False)
        ]

        # Add fields to the embed
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @command(name="permissions", aliases=["perms"], usage="`[Member|Role]`")
    @guild_only()
    @bot_has_permissions(embed_links=True, add_reactions=True)
    async def perms(self, ctx, *, item: Optional[Union[Member, Role]]):
        """View all permissions for any Member/Role!"""

        # Defaults to author if no argument is given
        item = item if item else ctx.author

        if isinstance(item, Member):
            # Iterating through list of perms
            perms = [f"{perm.title().replace('_', ' ')}: {self.bot.tick if value else self.bot.cross}" for perm, value
                     in item.guild_permissions]

        else:
            # Iterating through list of perms
            perms = [f"{perm.title().replace('_', ' ')}: {self.bot.tick if value else self.bot.cross}" for perm, value
                     in item.permissions]

        middle = len(perms) // 2
        f_half = perms[:middle]
        s_half = perms[middle:]

        first_page = Embed(description=f"**Item:** {item}",
                           colour=self.bot.admin_colour,
                           timestamp=datetime.datetime.utcnow())
        first_page.set_footer(text=f"ID: {item.id}")

        second_page = Embed(description=f"**Item:** {item}",
                            colour=self.bot.admin_colour,
                            timestamp=datetime.datetime.utcnow())
        second_page.set_footer(text=f"ID: {item.id}")

        # Add permissions to both of the embeds
        first = add_perms(first_page, f_half)
        second = add_perms(second_page, s_half)

        # Get the permissions of the channel
        perms = ctx.guild.me.permissions_in(ctx.message.channel)

        menu = SimpleMenu(0, item, perms, [first, second], self)
        await menu.start(ctx)

    @command(name="rolelist", aliases=["rl"])
    @guild_only()
    async def role_list(self, ctx):
        """Retrieve list of all roles in the server!"""

        # More readable name
        guild_roles = ctx.guild.roles
        # Get all guild roles
        role = string_list(guild_roles, 50, "Role")

        embed = Embed(title=f"{ctx.guild}'s Roles --> {len(ctx.guild.roles)}",
                      description=role or "Guild Has No Roles",
                      color=self.bot.random_colour(),
                      timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"Guild ID: {ctx.guild.id}", icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @command(name="userinfo", aliases=["ui"])
    @guild_only()
    @bot_has_permissions(embed_links=True)
    async def user_info(self, ctx, member: Optional[Member] = None):
        """User Information! (Created At/Joined/Roles etc)"""

        # Use member when mentioned
        # Use author if no member is mentioned
        member = ctx.author if not member else member

        # Get the member avatar
        userAvatar = member.avatar_url
        # Get total member roles
        role = string_list(member.roles, 20, "Role")

        # Returns the permissions that the user has within the guild
        filtered = filter(lambda x: x[1], member.guild_permissions)
        # Replace all "_" with " " in each item and join them together
        perms = ",".join(map(lambda x: x[0].replace("_", " "), filtered))
        # Capitalise every word in the array and filter out the permissions that are defined within the frozenset
        permission = string.capwords("".join(map(str, detect_perms(perms, perms))))

        embed = Embed(
            title=f"**User Information**",
            colour=self.bot.random_colour(),
            timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=userAvatar)
        embed.set_footer(text=f"ID: {member.id}", icon_url=userAvatar)

        embed_fields = [("Name", member.mention, True),
                        ("Tag", member.name, True),
                        ("Discrim", f"#{member.discriminator}", True),
                        ("Registered", member.created_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"), True),
                        ("Joined", member.joined_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"), True),
                        ("Top Role", member.top_role.mention, False),
                        ("Roles", role or "No Roles", False),
                        ("Key Permissions", permission or "No Key Permissions", False),
                        ("Status", str(member.status).title(), True),
                        ("Boosting Server", bool(member.premium_since), True),
                        ("Bot", member.bot, True)]

        # Add fields to the embed
        for name, value, inline in embed_fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @command(name="serverinfo", aliases=["si", "guildinfo", "gi"])
    @guild_only()
    @bot_has_permissions(embed_links=True)
    async def server_info(self, ctx):
        """Guild Information! (Owner/Roles/Emojis etc)"""

        # Define guild icon and id
        guild_icon = ctx.guild.icon_url
        guild_id = ctx.guild.id

        # Getting permissions of the bot within the channel
        perms = ctx.guild.me.permissions_in(ctx.message.channel)

        # Retrieve the top role of the guild
        top_role = ctx.guild.roles[-1]
        # Get total guild roles
        role_string = string_list(ctx.guild.roles, 20, "Role")
        # Get total emojis
        emojis = string_list(ctx.guild.emojis, 20, "Emoji")

        # Defining a dictionary of the statuses
        member_status = {
            "online": 0,
            "idle": 0,
            "dnd": 0,
            "offline": 0
        }

        # Iterating over the members and then storing the numbers in the dictionary
        for m in ctx.guild.members:
            member_status[str(m.status)] += 1

        # Storing the statuses in an array
        statuses = [member_status["online"],
                    member_status["idle"],
                    member_status["dnd"],
                    member_status["offline"]]

        # Set up embed to display all the server information
        embed = Embed(title="**Server Information**",
                      colour=self.bot.random_colour(),
                      timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=guild_icon)
        embed.set_footer(text=f"ID: {guild_id}", icon_url=guild_icon)

        # Get the list of banned users from the server
        bans = len(await ctx.guild.bans()) if perms.ban_members else f"No Perms {self.bot.cross}"
        # Get the list of invites created for the server
        invites = len(await ctx.guild.invites()) if perms.manage_guild else f"No Perms {self.bot.cross}"

        # Define fields to be added into the embed
        fields = [("Owner", ctx.guild.owner.mention, True),
                  ("Created", ctx.guild.created_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"), False),
                  ("Region", get_region(str(ctx.guild.region)), False),
                  ("Statuses", f"<a:online:753214525272096831>  {statuses[0]}  "
                               f"<a:idle:753214548756004924>  {statuses[1]}  "
                               f"<a:dnd:753214555999567953>  {statuses[2]}  "
                               f"<a:offline:753214562970501171>  {statuses[3]}  ", False),

                  (f"Members ({len(ctx.guild.members)})",
                   f"\nHumans: {len(list(filter(lambda m: not m.bot, ctx.guild.members)))}"
                   f"\nBots: {len(list(filter(lambda m: m.bot, ctx.guild.members)))}"
                   f"\nBanned: {bans}", True),

                  (f"Channels ({len(ctx.guild.channels)})",
                   f"\nText: {len(ctx.guild.text_channels)}"
                   f"\nVoice: {len(ctx.guild.voice_channels)}"
                   f"\nCategories: {len(ctx.guild.categories)}", True),

                  ("Misc",
                   f"Invites: {invites}"
                   f"\nVerif Level: {ctx.guild.verification_level.name.capitalize()}"
                   f"\nNitro Boosters: {len(ctx.guild.premium_subscribers)}", True),
                  ("Top Role", top_role.mention, False),
                  (f"Roles ({len(ctx.guild.roles)})", role_string or "No Roles In Guild", True),
                  (f"Emojis ({len(ctx.guild.emojis)})", emojis or "No Emojis In Guild", False)]

        # Add fields to the embed
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @command(name="channelinfo", aliases=["chinfo"])
    @guild_only()
    @bot_has_permissions(embed_links=True)
    async def channel_info(self, ctx, channel: Optional[TextChannel] = None):
        """Channel Statistics! (Category/Created At etc)"""

        # Get information about the channel
        channel = ctx.channel if not channel else channel
        perms_synced = self.bot.tick if channel.permissions_synced else self.bot.cross
        nsfw = self.bot.tick if channel.is_nsfw() else self.bot.cross

        # Set up Embed
        desc = f"**Guild -->** {ctx.guild}" \
               f"\n**Position -->** {f'#{channel.position} / {len(ctx.guild.channels)}'}"
        embed = Embed(title=f"Statistics For #{channel.name}",
                      description=desc,
                      timestamp=datetime.datetime.utcnow(),
                      colour=self.bot.random_colour())
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text=f"ID: {channel.id}")

        # Setting up fields
        fields = [("Category", channel.category or self.bot.cross, True),
                  ("Topic", channel.topic or self.bot.cross, True),
                  ("\u200b", "\u200b", True),
                  ("Perms Synced?", perms_synced, True),
                  ("Nsfw?", nsfw, True),
                  ("Creation At", channel.created_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"), False)]

        # Add fields to the embed
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @command(name="source")
    @bot_has_permissions(embed_links=True)
    async def _bot_source(self, ctx):
        """Link to the source code for Enso!"""

        embed = Embed(title=f"<:github:741000905364603010> Source Code | Ensō~Chan {self.bot.version}",
                      description="**Click above me to view my source code!**",
                      url="https://github.com/sgoudham/Enso-Bot",
                      colour=self.bot.admin_colour,
                      timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Developer", value=f"{self.bot.hammyMention} | Hamothy#5619", inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @command(name="vote", aliases=["upvote"])
    async def upvote(self, ctx):
        """Upvote the bot on top.gg!"""

        desc = "Click the link above to upvote me!\nIt would greatly help me out as it allows the bot to be " \
               "noticed more on the website!\nIt's free and takes a maximum of 30 seconds to do. Thanks so much!"
        embed = Embed(title="Upvote me on top.gg!",
                      description=desc,
                      url="https://top.gg/bot/716701699145728094/vote",
                      colour=self.bot.random_colour(),
                      timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Developer", value=f"{self.bot.hammyMention} | Hamothy#5619", inline=False)

        await ctx.send(embed=embed)

    @command(name="about")
    @bot_has_permissions(embed_links=True)
    async def checking_bot_stats(self, ctx):
        """Bot Statistics! (CPU/Mem Usage etc)"""

        stats = Embed(title=f"<:github:741000905364603010> Source Code | Ensō~Chan {self.bot.version}",
                      url="https://github.com/sgoudham/Enso-Bot",
                      colour=self.bot.admin_colour,
                      timestamp=datetime.datetime.utcnow())
        stats.set_thumbnail(url=self.bot.user.avatar_url)
        stats.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        # Grabbing technical statistics of the bot
        proc = Process()
        with proc.oneshot():
            uptime = datetime.timedelta(seconds=time() - proc.create_time())
            mem_total = virtual_memory().total / (1024 ** 2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)

        uptime_hours, uptime_remainder = divmod(uptime.seconds, 3600)
        uptime_minutes, uptime_seconds = divmod(uptime_remainder, 60)
        frmt_uptime = f'{int(uptime_hours):01} Hour(s), {int(uptime_minutes):01} Minute(s), {int(uptime_seconds):01} Second(s)'

        # Grabbing total number of channels across all guilds in which the bot is present in
        channels = map(lambda m: len(m.channels), self.bot.guilds)

        # Setting up fields
        fields = [
            ("Developer", f"{self.bot.hammyMention} | Hamothy#5619", False),

            ("Language | Library",
             f"<:python:747224674319990895> Python {python_version()} | <:discord:747224665553895544> Discord.py {discord_version}",
             False),

            ("<:discord:747224665553895544> Support Server",
             "[Here!](https://discord.com/invite/SZ5nexg)", True),

            ("<:invite:740998357643952139> Invite Link",
             "[Here!](https://top.gg/bot/716701699145728094)", True),

            ("❗ Current Prefix", ctx.prefix, True),

            ("Discord Stats",
             f"Guilds: {len(self.bot.guilds)}"
             f"\nChannels: {sum(list(channels))}"
             f"\nEmojis: {len(self.bot.emojis)}"
             f"\nCommands: {len(self.bot.commands)}"
             f"\nUsers: {len(self.bot.users):,}", True),

            ("Line Count", self.bot.line_count, True),
            ("Uptime", frmt_uptime, False),
            ("Memory Usage", f"{mem_usage:,.2f} / {mem_total:,.2f} MiB ({mem_of_total:.2f}%)", False)]

        # Add fields to the embed
        for name, value, inline in fields:
            stats.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=stats)

    @group(name="avatar", invoke_without_command=True, case_insensitive=True,
           usage="`[member]|greyscale|invert`")
    @bot_has_permissions(embed_links=True)
    async def get_user_avatar(self, ctx, *, member: Optional[Member] = None):
        """
        Displaying Member's Avatar
        Member can be mentioned and their avatar will be displayed
        """

        # Get member mentioned or set to author
        member = ctx.author if not member else member

        # Get the member avatar
        userAvatar = str(member.avatar_url)

        embed = Embed(title=f"{member}'s Avatar",
                      url=userAvatar,
                      colour=self.bot.admin_colour,
                      timestamp=datetime.datetime.utcnow())
        embed.set_image(url=userAvatar)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @get_user_avatar.command(name="greyscale", aliases=["gs"])
    @bot_has_permissions(embed_links=True)
    @cooldown(1, 2, BucketType.user)
    async def greyscale_user_avatar(self, ctx, *, member: Optional[Member] = None):
        """Get the greyscale avatar of the member"""

        # Get member mentioned or set to author
        member = ctx.author if not member else member

        attach = await member.avatar_url.read()
        image = Image.open(io.BytesIO(attach)).convert('LA')

        # Save new grayscale image as bytes
        file = io.BytesIO()
        image.save(file, format='PNG')
        file.seek(0)

        # Send image in an embed
        f = File(file, "image.png")
        embed = Embed(title=f"{member}'s Avatar | Greyscale",
                      colour=self.bot.admin_colour,
                      timestamp=datetime.datetime.utcnow())
        embed.set_image(url="attachment://image.png")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(file=f, embed=embed)

    @get_user_avatar.command(name="invert", aliases=["negative"])
    @bot_has_permissions(embed_links=True)
    @cooldown(1, 2, BucketType.user)
    async def greyscale_user_avatar(self, ctx, *, member: Optional[Member] = None):
        """Get the inverted avatar of the member"""

        # Get member mentioned or set to author
        member = ctx.author if not member else member

        attach = await member.avatar_url.read()
        image = Image.open(io.BytesIO(attach)).convert('RGB')
        inverted = invert(image)

        # Save new inverted image as bytes
        file = io.BytesIO()
        inverted.save(file, format='PNG')
        file.seek(0)

        # Send image in an embed
        f = File(file, "image.png")
        embed = Embed(title=f"{member}'s Avatar | Inverted",
                      colour=self.bot.admin_colour,
                      timestamp=datetime.datetime.utcnow())
        embed.set_image(url="attachment://image.png")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(file=f, embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
