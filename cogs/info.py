import datetime
import random
import string
from asyncio.subprocess import Process
from platform import python_version
from time import time

from discord import Colour
from discord import Embed
from discord import __version__ as discord_version
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from discord.ext.commands import command
from psutil import Process, virtual_memory

from settings import colour_list, enso_embedmod_colours

# Using forzenset
# Permissions to filter through
Perms = frozenset(
    {
        "create instant invite",
        "add reactions",
        "view audit log",
        "priority speaker",
        "stream",
        "read messages",
        "send messages",
        "send tts messages",
        "embed links",
        "attach links",
        "read message history",
        "external emojis",
        "view guild insights",
        "connect",
        "speak",
        "use voice activation",
        "change nickname"
    }
)


# Method to detect which permissions to filter out
def DetectPermissions(message, fset):
    # Split the message individual permissions
    message = message.split(",")

    # Filter the permission out if it's in the frozenset
    filtered = filter(lambda perm: perm not in fset, message)
    return ", ".join(filtered)


class Info(commands.Cog):
    """(User/Server/Bot etc) Information!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Printing out that Cog is ready on startup"""
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @command(name="userinfo", aliases=["ui"])
    @cooldown(1, 5, BucketType.user)
    async def user_info(self, ctx, target=None):
        """User Information! (Created At/Joined/Roles etc)"""

        # If a target has been specified, set them as the user
        if target:
            target = target
        # If no target has been specified, choose the author
        else:
            target = ctx.author

        # Get the member avatar
        userAvatar = target.avatar_url

        # Store all the roles that the user has
        # (Skipping the first element as it's always going to be @everyone)
        roles = f"{' '.join(map(str, (role.mention for role in target.roles[1:])))}"

        # Returns the permissions that the user has within the guild
        filtered = filter(lambda x: x[1], target.guild_permissions)
        # Replace all "_" with " " in each item and join them together
        permission = ",".join(map(lambda x: x[0].replace("_", " "), filtered))

        # Capitalise every word in the array and filter out the permissions that are defined within the frozenset
        permissions = string.capwords("".join(map(str, DetectPermissions(permission, Perms))))

        # Set up the embed to display everything about the user
        embed = Embed(
            title=f"**User Information**",
            colour=Colour(int(random.choice(colour_list))),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=userAvatar)
        embed.set_footer(text=f"ID: {target.id}", icon_url='{}'.format(userAvatar))

        # Define fields to be added into the embed
        embed_fields = [("Name", str(target.mention), True),
                        ("Tag", target.name, True),
                        ("Discrim", "#" + target.discriminator, True),
                        ("Registered", target.created_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"), True),
                        ("Joined", target.joined_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"), True),
                        ("Top Role", target.top_role.mention, False),
                        ("Roles", roles, False),
                        ("Key Permissions", permissions, False),
                        ("Status", str(target.status).title(), True),
                        ("Boosting Server", bool(target.premium_since), True),
                        ("Bot", target.bot, True)]

        # Add fields to the embed
        for name, value, inline in embed_fields:
            embed.add_field(name=name, value=value, inline=inline)

        # Send the embed to the channel that the command was triggered in
        await ctx.send(embed=embed)

    @command(name="serverinfo", aliases=["guildinfo"])
    @cooldown(1, 5, BucketType.user)
    async def server_info(self, ctx):
        """Guild Information! (Owner/Roles/Emojis etc)"""

        # Define guild icon and id
        guild_icon = ctx.guild.icon_url
        guild_id = ctx.guild.id

        # Check if the amount of roles is above 20
        if len(ctx.guild.roles) > 20:
            # Display the first 20 roles with a length specified telling the user how many roles were not shown
            length = len(ctx.guild.roles) - 20

            # Store the first 20 roles in a string called "roles"
            # (Skipping the first element as it's always going to be @everyone)
            role_string = f"{' **>** '.join(map(str, (role.mention for role in ctx.guild.roles[1:20])))} and **{length}** more"

        else:
            # Display all the roles in the server as it is less than 20
            role_string = f"{' **>** '.join(map(str, (role.mention for role in ctx.guild.roles[1:])))}"

        # Check if the list of emojis returned are greater than 20
        if len(ctx.guild.emojis) > 20:
            # Display the first 20 emojis with a length specified telling the user how many emojis were not shown
            length = len(ctx.guild.emojis) - 20
            # Store the first 20 emojis in a string
            emojis = f"{' '.join(map(str, ctx.guild.emojis[:20]))} and **{length}** more..."
        else:
            # Display all the emojis in the server as it is less than 20
            emojis = " ".join(map(str, ctx.guild.emojis))

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
                      colour=Colour(int(random.choice(colour_list))),
                      timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=guild_icon)
        embed.set_footer(text=f"ID: {guild_id}", icon_url='{}'.format(guild_icon))

        # Get the list of banned users from the server
        bans = len(await ctx.guild.bans())
        # Get the list of invites created for the server
        invites = len(await ctx.guild.invites())

        # Define fields to be added into the embed
        fields = [("Owner", ctx.guild.owner, True),
                  ("Created", ctx.guild.created_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"), False),
                  ("Region", str(ctx.guild.region).capitalize(), False),
                  ("Statuses", f"🟢 {statuses[0]} \n🟠 {statuses[1]} \n🔴 {statuses[2]} \n⚪ {statuses[3]}", False),

                  (f"Members ({len(ctx.guild.members)})",
                   f"\nHumans: {len(list(filter(lambda m: not m.bot, ctx.guild.members)))}" +
                   f"\nBots: {len(list(filter(lambda m: m.bot, ctx.guild.members)))}" +
                   f"\nBanned: {bans}", True),

                  (f"Channels ({len(ctx.guild.channels)})",
                   f"\nText: {len(ctx.guild.text_channels)}" +
                   f"\nVoice: {len(ctx.guild.voice_channels)}", True),

                  ("Misc", f"Categories: {len(ctx.guild.categories)}" +
                   f"\nInvites: {invites}", True),

                  (f"Roles ({len(ctx.guild.roles)})", role_string, True),
                  (f"Emojis ({len(ctx.guild.emojis)})", emojis, False)]

        # Add fields to the embed
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        # Send the embed to the channel that the command was triggered in
        await ctx.send(embed=embed)

    @command(name="channelinfo", aliases=["chinfo"])
    @cooldown(1, 5, BucketType.user)
    async def channel_info(self, ctx):
        """Channel Statistics! (Category/Created At etc)"""

        # Get the channel that the user is in
        channel = ctx.channel

        # Set up Embed
        embed = Embed(title=f"Statistics For {channel.name}",
                      description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'N/A'}",
                      timestamp=datetime.datetime.utcnow(),
                      colur=Colour(int(random.choice(colour_list))))
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text=f"ID: {channel.id}")

        # Setting up fields
        fields = [
            ("Guild", ctx.guild.name, True),
            ("Creation At", channel.created_at.strftime("%a, %b %d, %Y\n%I:%M:%S %p"), True),
            ("Topic", f"{channel.topic if channel.topic else 'No Topic'}", True),
            ("Permissions Synced?", channel.permissions_synced, True),
            ("Position", channel.position, True),
            ("NSFW?", channel.is_nsfw(), True)
        ]

        # Add fields to the embed
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @command(name="stats")
    @cooldown(1, 5, BucketType.user)
    async def checking_bot_stats(self, ctx):
        """Bot Statistics! (CPU/Mem Usage etc)"""

        stats = Embed(title="Bot Stats",
                      colour=enso_embedmod_colours,
                      timestamp=datetime.datetime.utcnow())
        stats.set_thumbnail(url=ctx.guild.icon_url)

        # Grabbing technical statistics of the bot
        proc = Process()
        with proc.oneshot():
            uptime = datetime.timedelta(seconds=time() - proc.create_time())
            mem_total = virtual_memory().total / (1024 ** 2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)

        uptime_hours, uptime_remainder = divmod(uptime.seconds, 3600)
        uptime_minutes, uptime_seconds = divmod(uptime_remainder, 60)
        frmt_uptime = '{:01} Hours, {:01} Minutes, {:01} Seconds'.format(int(uptime_hours), int(uptime_minutes),
                                                                         int(uptime_seconds))

        # Setting up fields
        fields = [
            ("Developer", "Hamothy#5619", True),
            ("Bot Version", "1.7.2", False),
            ("Language | Library", f"Python {python_version()} | Discord.py {discord_version}", False),
            ("Uptime", frmt_uptime, False),
            ("Memory Usage", f"{mem_usage:,.2f} / {mem_total:,.2f} MiB ({mem_of_total:.2f}%)", False),
            ("Guilds", f"{len(self.bot.guilds)}", True),
            ("Users", f"{len(self.bot.users):,}", True)
        ]

        # Add fields to the embed
        for name, value, inline in fields:
            stats.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=stats)


def setup(bot):
    bot.add_cog(Info(bot))
