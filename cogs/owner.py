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

import asyncio
import inspect
import io
import textwrap
import traceback
from contextlib import redirect_stdout
from typing import Optional

import asyncpg
from discord import Member
from discord.ext.commands import Cog, command, is_owner


def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    # remove `foo`
    return content.strip('` \n')


def paginate(text: str):
    """Simple generator that paginates text."""
    last = 0
    pages = []
    for curr in range(0, len(text)):
        if curr % 1980 == 0:
            pages.append(text[last:curr])
            last = curr
            appd_index = curr
    if appd_index != len(text) - 1:
        pages.append(text[last:curr])
    return list(filter(lambda a: a != '', pages))


def get_syntax_error(e):
    if e.text is None:
        return f'```py\n{e.__class__.__name__}: {e}\n```'
    return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'


class Owner(Cog):
    """Commands for Ensō server"""

    def __init__(self, bot):
        self.bot = bot

    @command(name="dm", hidden=True)
    @is_owner()
    async def dm(self, ctx, member: Member, *, text):
        """DM users"""

        # Delete the message sent instantly
        await ctx.message.delete()
        # Send the message typed the mentioned user
        await member.send(text)

    @command(name="leave", hidden=True)
    @is_owner()
    async def leave(self, ctx):
        """Leaves the guild"""

        await self.bot.generate_embed(ctx, desc="**Leaving the guild... Bye Bye uvu**")
        await ctx.guild.leave()

    @command(name="forceprefix", hidden=True)
    @is_owner()
    async def override_prefix(self, ctx, new: Optional[str] = None):
        """Override the prefix in any given guild (Owner only)"""

        # As long as a new prefix has been given and is less than 5 characters
        if new and len(new) <= 5:
            # Store the new prefix in the dictionary and update the database
            await self.bot.storage_prefix_for_guild(ctx, new)

        # Making sure that errors are handled if prefix is above 5 characters
        elif new and len(new) > 5:
            await self.bot.generate_embed(ctx, desc="The guild prefix must be less than or equal to **5** characters!")

        # if no prefix was provided
        elif not new:
            # Grab the current prefix for the guild within the cached dictionary
            prefix = self.bot.get_prefix_for_guild(ctx.guild.id)
            await self.bot.generate_embed(ctx, desc=f"**The current guild prefix is `{prefix}`**")

    @command(name="restart", hidden=True)
    @is_owner()
    async def restart(self, ctx):
        """Restart the bot"""

        # Close the database connection
        try:
            await asyncio.wait_for(self.bot.db.close(), timeout=1.0)

        # Catch errors
        except asyncio.TimeoutError:
            await self.bot.generate_embed(ctx, desc="**Database Connection Timed Out!")

        # Shutdown the bot
        else:
            await self.bot.generate_embed(ctx, desc="**Success Senpai!"
                                                    "\nMy Reboot Had No Problems** <a:ThumbsUp:737832825469796382>")
            await self.bot.logout()

    @command(name="reloadusers", hidden=True)
    @is_owner()
    async def reload_db(self, ctx):
        """Reloads the database by inserting/updating all the records"""

        # Store every single record into an array
        records = [(ctx.guild.id, member.id) for member in ctx.guild.members]

        # Setup up pool connection
        pool = self.bot.db
        async with pool.acquire() as conn:

            # Define the insert statement that will insert the user's information
            try:
                insert_query = """INSERT INTO members (guild_id, member_id) VALUES ($1, $2)
                            ON CONFLICT (guild_id, member_id) DO NOTHING"""
                await conn.executemany(insert_query, records)

            # Catch errors
            except asyncpg.PostgresError as e:
                print(f"PostGres Error: Member(s) were not be able to be added to Guild", e)

            # Print success
            else:
                print(f"Record(s) Inserted Into Members")

    @command(name="cache", hidden=True)
    @is_owner()
    async def set_cache(self, ctx, size: Optional[int]):
        """Allow me to dynamically set the cache max size"""

        # Change the size of the cache
        if size:
            try:
                self.bot.member_cache.change_array_size(size)

            # Catch errors
            except Exception as e:
                print(e)

            # Let me that it's successful
            else:
                await self.bot.generate_embed(ctx, desc=f"Cache Now Storing To **{size}** Records")

        # Display the length of the current queue and cache and the max length of the cache
        else:
            max_cache_len, cache_len, queue_len = self.bot.member_cache.get_size()
            await self.bot.generate_embed(ctx, desc=f"Current Records Stored Within Cache: **{cache_len}**"
                                                    f"\nCurrent Queue Length: **{queue_len}**"
                                                    f"\nMax Size Of Cache: **{max_cache_len}**")

    @command(name="eval", hidden=True)
    @is_owner()
    async def _eval(self, ctx, *, body):
        """
        Evaluates python code
        Gracefully yoinked from (https://github.com/fourjr/eval-bot)"""

        env = {
            'ctx': ctx,
            'bot': self.bot,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'source': inspect.getsource
        }

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()
        err = out = None

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            return await ctx.message.add_reaction('\u2049')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    try:
                        out = await ctx.send(f'```py\n{value}\n```')
                    except:
                        paginated_text = paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f'```py\n{page}\n```')
                                break
                            await ctx.send(f'```py\n{page}\n```')
            else:
                try:
                    out = await ctx.send(f'```py\n{value}{ret}\n```')
                except:
                    paginated_text = paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')

        if out:
            await ctx.message.add_reaction('\u2705')  # tick
        elif err:
            await ctx.message.add_reaction('\u2049')  # x
        else:
            await ctx.message.add_reaction('\u2705')


def setup(bot):
    bot.add_cog(Owner(bot))
