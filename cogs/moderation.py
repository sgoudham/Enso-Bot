import datetime
from datetime import timedelta

from discord import Member
from discord.ext import commands
from discord.ext.commands import command, guild_only, has_guild_permissions, bot_has_guild_permissions


class Moderation(commands.Cog):
    """Moderation Commands! (Kick/Ban/Mute etc)"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @command(name="kick", aliases=["Kick"])
    @guild_only()
    @has_guild_permissions(kick_members=True)
    @bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: Member, *, reason=None):
        """Kick Members from Server"""

        # Check if reason has been given
        if reason:
            reason = reason
        # Set default reason to None
        else:
            reason = "No Reason Given"

        # Kick the user and then give confirmation to the channel
        await ctx.guild.kick(user=member, reason=reason)
        await ctx.send(f"{ctx.author.name} **kicked** {member.name}"
                       f"\n**Reason:** '{reason}'")

    @command(name="ban", aliases=["Ban"])
    @guild_only()
    @has_guild_permissions(ban_members=True)
    @bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: Member, *, reason=None):
        """Ban Members from Server"""

        # Check if reason has been given
        if reason:
            reason = reason
        # Set default reason to None
        else:
            reason = "No Reason Given"

        # Ban the user and send confirmation to the channel
        await ctx.guild.ban(user=member, reason=reason)
        await ctx.send(f"{ctx.author.name} **banned** {member.name}"
                       f"\n**Reason:** '{reason}'")

    @command(name="unban", aliases=["Unban"])
    @guild_only()
    @has_guild_permissions(ban_members=True)
    @bot_has_guild_permissions(ban_members=True)
    async def unban(self, ctx, member: int, *, reason=None):
        """Unban Member from Server"""

        # Check if reason has been given
        if reason:
            reason = reason
        # Set default reason to None
        else:
            reason = "No Reason Given"

        # Get the member and unban them
        member = await self.bot.fetch_user(member)
        await ctx.guild.unban(member, reason=reason)

        # Confirm that the user has been unbanned
        await ctx.send(f"{ctx.author.name} **unbanned** {member.name}"
                       f"\n**Reason:** '{reason}'")

    @command(name="purge", aliases=["Purge"])
    @guild_only()
    @has_guild_permissions(manage_messages=True)
    @bot_has_guild_permissions(manage_messages=True, read_message_history=True)
    async def purge(self, ctx, amount: int = None):
        """Purge Messages from Channel"""

        if amount:
            if 0 < amount <= 100:
                with ctx.channel.typing():
                    await ctx.message.delete()
                    deleted = await ctx.channel.purge(limit=amount + 1,
                                                      after=datetime.datetime.utcnow() - timedelta(days=14))

                    await ctx.send(f"Deleted **{(len(deleted) - 1):,}** messages.", delete_after=5)

            # Send error if
            else:
                await ctx.send("The amount provided is not between **0** and **100**")
        else:
            await ctx.send("**You must specify an amount!**")


def setup(bot):
    bot.add_cog(Moderation(bot))
