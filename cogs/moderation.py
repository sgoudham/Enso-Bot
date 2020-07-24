from discord import Member
from discord.ext import commands
from discord.ext.commands import command, guild_only, has_guild_permissions


class Moderation(commands.Cog):
    """Moderation Commands! (Kick/Ban/Mute etc)"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @command()
    @guild_only()
    @has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: Member, *, reason=None):
        """Kick Members from Server"""

        # Check if reason has been given
        if reason:
            reason = reason
        # Set default reason to None
        else:
            reason = "No Reason Given"

        await ctx.guild.kick(user=member, reason=reason)

        await ctx.send(f"{ctx.author.name} **kicked** {member.name}"
                       f"\n**Reason:** '{reason}'")

    @command()
    @guild_only()
    @has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: Member, *, reason=None):
        """Ban Members from Server"""

        # Check if reason has been given
        if reason:
            reason = reason
        # Set default reason to None
        else:
            reason = "No Reason Given"

        await ctx.guild.ban(user=member, reason=reason)

        await ctx.send(f"{ctx.author.name} **banned** {member.name}"
                       f"\n**Reason:** '{reason}'")

    @command()
    @guild_only()
    @has_guild_permissions(ban_members=True)
    async def unban(self, ctx, member: int, *, reason=None):
        """Unban Member from Server"""

        # Check if reason has been given
        if reason:
            reason = reason
        # Set default reason to None
        else:
            reason = "No Reason Given"

        member = await self.bot.fetch_user(member)
        await ctx.guild.unban(member, reason=reason)

        await ctx.send(f"{ctx.author.name} **unbanned** {member.name}"
                       f"\n**Reason:** '{reason}'")

    @command()
    @guild_only()
    @has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = None):
        """Purge Messages from Channel"""
        if not amount:
            amount = 100

        if amount > 100:
            await ctx.send("Sorry! You can only purge up to **100** messages at a time!")
        elif amount <= 100:
            channel = ctx.message.channel
            messages = []

            async for message in channel.history(limit=amount):
                messages.append(message)

            await channel.delete_messages(messages)
            msg = await ctx.send(f"{ctx.author.mention} {amount} messages deleted!")


def setup(bot):
    bot.add_cog(Moderation(bot))
