# Ensō~Chan - A Multi Purpose Discord Bot That Has Everything Your Server Needs!
# Copyright (C) 2020  Goudham Suresh

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
import string

from discord import Forbidden, Embed
from discord.ext import commands
from discord.ext.commands import Cog


async def send_error(ctx, perms, embed):
    """
    Sending error message to the user
    Only send error message if the channel permissions allow it
    """

    if perms.send_messages and perms.embed_links:
        await ctx.send(embed=embed)
    else:
        print("Error: Error Handling Message Could Not Be Sent")


async def on_bot_forbidden(ctx, perms, args2):
    """Handles Missing Bot Permissions Errors"""

    # Convert list into string of the missing permissions
    missing_perms = string.capwords(", ".join(args2.missing_perms).replace("_", " "))

    embed = Embed(description=f"❌ I Need **{missing_perms}** Permission(s) to Execute This Command! ❌",
                  colour=ctx.bot.admin_colour)

    await send_error(ctx, perms, embed)


async def on_command_forbidden(ctx, perms):
    """Handles Forbidden Error"""

    embed = Embed(description="**❌ I Don't Have Permissions To Execute This Command ❌**",
                  colour=ctx.bot.admin_colour)

    await send_error(ctx, perms, embed)


async def on_command_bad_argument(ctx, perms):
    """Handles Bad Argument Errors (Argument can't be read properly)"""

    embed = Embed(description="**❌ Uh oh! Couldn't find anyone to mention! Try again! ❌**",
                  colour=ctx.bot.admin_colour)

    await send_error(ctx, perms, embed)


async def on_command_not_found(ctx, perms):
    """Handles the command not found error"""

    embed = Embed(description=f"Command Not Found! ❌ Please use **{ctx.prefix}help** to see all commands",
                  colour=ctx.bot.admin_colour)

    await send_error(ctx, perms, embed)


async def on_command_cooldown(ctx, perms, error):
    """Handles Cooldown Errors"""

    embed = Embed(description=f"That command is on cooldown. Try again in **{error.retry_after:,.2f}** seconds",
                  colour=ctx.bot.admin_colour)

    await send_error(ctx, perms, embed)


async def on_command_permission(ctx, perms, args2):
    """Handles User Missing Permissions Errors"""

    # Convert list into string of the missing permissions
    missing_perms = string.capwords(", ".join(args2.missing_perms).replace("_", " "))

    embed = Embed(description=f"❌ Uh oh! You Need **{missing_perms}** Permission(s) To Execute This Command! ❌",
                  colour=ctx.bot.admin_colour)

    await send_error(ctx, perms, embed)


async def on_command_missing_argument(ctx, perms):
    """Handles the missing argument error"""

    embed = Embed(description="Required Argument(s) Missing!"
                              f"\nUse **{ctx.prefix}help** to find how to use **{ctx.command}**",
                  colour=ctx.bot.admin_colour)

    await send_error(ctx, perms, embed)


async def on_not_owner(ctx, perms):
    """Handles the error when the user is not the owner and tries to invoke owner only command"""

    embed = Embed(description="**❌ Owner Only Command ❌**",
                  colour=ctx.bot.admin_colour)

    await send_error(ctx, perms, embed)


class Errors(Cog):
    """Moderation Commands! (Kick/Ban/Mute etc)"""

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx, args2):
        """Event to detect and handle errors"""

        # Get permissions for the bot within
        perms = ctx.guild.me.permissions_in(ctx.message.channel)

        # if the user did not specify an user
        if isinstance(args2, commands.MissingRequiredArgument):
            await on_command_missing_argument(ctx, perms)
        # if the user has spammed a command and invoked a cooldown
        elif isinstance(args2, commands.CommandOnCooldown):
            await on_command_cooldown(ctx, perms, args2)
        # if the user tries to access a command that isn't available
        elif isinstance(args2, commands.CommandNotFound):
            await on_command_not_found(ctx, perms)
        # if the user provides an argument that isn't recognised
        elif isinstance(args2, commands.BadArgument):
            await on_command_bad_argument(ctx, perms)
        # if the user does not the correct permissions to call a command
        elif isinstance(args2, commands.MissingPermissions):
            await on_command_permission(ctx, perms, args2)
        # if the bot is missing permissions needed
        elif isinstance(args2, commands.BotMissingPermissions):
            await on_bot_forbidden(ctx, perms, args2)
        # if the bot is forbidden from performing the command
        elif isinstance(args2, Forbidden):
            await on_command_forbidden(ctx, perms)
        # if the user tries to invoke a command that is only for the owner
        elif isinstance(args2, commands.NotOwner):
            await on_not_owner(ctx, perms)


def setup(bot):
    bot.add_cog(Errors(bot))
