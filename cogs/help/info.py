import datetime
import random
import string
from typing import Optional

from discord import Embed, Member, Colour
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, command

from settings import colour_list

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


class GetInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="userinfo", aliases=["ui"])
    @cooldown(1, 5, BucketType.user)
    async def user_info(self, ctx, target: Optional[Member]):
        """Allow the users to see information about them relating to the guild"""

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
        """Allow the users to see information the guild itself"""

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

        # Define the statuses of the members within the discord
        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

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


def setup(bot):
    bot.add_cog(GetInfo(bot))
