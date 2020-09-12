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


# Help paginator by Rapptz
# Edited by F4stZ4p
# Edited by Hamothy
import asyncio
import datetime
import io
import textwrap
import traceback
from contextlib import redirect_stdout
from typing import Optional

import discord
from discord import Embed, DMChannel
from discord.ext import commands
from discord.ext.commands import Cog, command, has_permissions, guild_only, is_owner


class CannotPaginate(Exception):
    pass


class Pages:
    """Implements a paginator that queries the user for the
    pagination interface.

    Pages are 1-index based, not 0-index based.

    If the user does not reply within 2 minutes then the pagination
    interface exits automatically.

    Parameters
    ------------
    ctx: Context
        The context of the command.
    entries: List[str]
        A list of entries to paginate.
    per_page: int
        How many entries show up per page.
    show_entry_count: bool
        Whether to show an entry count in the footer.

    Attributes
    -----------
    embed: discord.Embed
        The embed object that is being used to send pagination info.
        Feel free to modify this externally. Only the description,
        footer fields, and colour are internally modified.
    permissions: discord.Permissions
        Our permissions for the channel.
    """

    def __init__(self, ctx, *, entries, per_page=8, show_entry_count=True):

        self.bot = ctx.bot
        self.prefix = ctx.prefix
        self.entries = entries
        self.message = ctx.message
        self.channel = ctx.channel
        self.author = ctx.author
        self.per_page = per_page
        pages, left_over = divmod(len(self.entries), self.per_page)
        if left_over:
            pages += 1
        self.maximum_pages = pages
        self.embed = discord.Embed(colour=self.bot.admin_colour,
                                   timestamp=datetime.datetime.utcnow())
        self.paginating = len(entries) > per_page
        self.show_entry_count = show_entry_count
        self.reaction_emojis = [
            ('\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}', self.first_page),
            ('\N{BLACK LEFT-POINTING TRIANGLE}', self.previous_page),
            ('\N{BLACK RIGHT-POINTING TRIANGLE}', self.next_page),
            ('\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}', self.last_page),
            ('\N{INPUT SYMBOL FOR NUMBERS}', self.numbered_page),
            ('\N{BLACK SQUARE FOR STOP}', self.stop_pages),
            ('\N{INFORMATION SOURCE}', self.show_help),
        ]

        if ctx.guild is not None:
            self.permissions = self.channel.permissions_for(ctx.guild.me)
        else:
            self.permissions = self.channel.permissions_for(ctx.bot.user)

        if not self.permissions.embed_links:
            raise CannotPaginate('Bot does not have Embed Links permission')

        if not self.permissions.send_messages:
            raise CannotPaginate('Bot Cannot Send Messages')

        if self.paginating:
            # verify we can actually use the pagination session
            if not self.permissions.add_reactions:
                raise CannotPaginate('Bot does not have Add Reactions permission')

            if not self.permissions.read_message_history:
                raise CannotPaginate('Bot does not have Read Message History permission')

    def get_page(self, page):
        base = (page - 1) * self.per_page
        return self.entries[base:base + self.per_page]

    async def show_page(self, page, *, first=False):
        self.current_page = page
        entries = self.get_page(page)
        p = []
        for index, entry in enumerate(entries, 1 + ((page - 1) * self.per_page)):
            p.append(f'{index}. {entry}')

        if self.maximum_pages > 1:
            if self.show_entry_count:
                text = f'Page {page}/{self.maximum_pages} ({len(self.entries)} entries)'
            else:
                text = f'Page {page}/{self.maximum_pages}'

            self.embed.set_footer(text=text)

        if not self.paginating:
            self.embed.description = '\n'.join(p)
            return await self.channel.send(embed=self.embed)

        if not first:
            self.embed.description = '\n'.join(p)
            await self.message.edit(embed=self.embed)
            return

        p.append('')
        p.append('Confused? React with \N{INFORMATION SOURCE} for more info.')
        self.embed.description = '\n'.join(p)
        self.message = await self.channel.send(embed=self.embed)
        for (reaction, _) in self.reaction_emojis:
            if self.maximum_pages == 2 and reaction in ('\u23ed', '\u23ee'):
                # no |<< or >>| buttons if we only have two pages
                # we can't forbid it if someone ends up using it but remove
                # it from the default set
                continue

            await self.message.add_reaction(reaction)

    async def checked_show_page(self, page):
        if page != 0 and page <= self.maximum_pages:
            await self.show_page(page)

    async def first_page(self):
        """Show First Page"""
        await self.show_page(1)

    async def last_page(self):
        """Show Last Page"""
        await self.show_page(self.maximum_pages)

    async def next_page(self):
        """Show Next Page"""
        await self.checked_show_page(self.current_page + 1)

    async def previous_page(self):
        """Show Previous Page"""
        await self.checked_show_page(self.current_page - 1)

    async def show_current_page(self):
        if self.paginating:
            await self.show_page(self.current_page)

    async def numbered_page(self):
        """Go to Given Page"""
        to_delete = []
        to_delete.append(await self.channel.send('What page do you want to go to?'))

        def message_check(m):
            return m.author == self.author and \
                   self.channel == m.channel and \
                   m.content.isdigit()

        try:
            msg = await self.bot.wait_for('message', check=message_check, timeout=30.0)
        except asyncio.TimeoutError:
            to_delete.append(await self.channel.send('Took too long.'))
            await asyncio.sleep(5)
        else:
            page = int(msg.content)
            to_delete.append(msg)
            if page != 0 and page <= self.maximum_pages:
                await self.show_page(page)
            else:
                to_delete.append(await self.channel.send(f'Invalid page given. ({page}/{self.maximum_pages})'))
                await asyncio.sleep(5)

        try:
            await self.channel.delete_messages(to_delete)
        except Exception:
            pass

    async def show_help(self):
        """shows this message"""
        messages = ['Welcome to the interactive paginator!\n',
                    'This interactively allows you to see pages of text by navigating with '
                    'reactions. They are as follows:\n']

        for (emoji, func) in self.reaction_emojis:
            messages.append(f'{emoji} {func.__doc__}')

        self.embed.description = '\n'.join(messages)
        self.embed.clear_fields()
        self.embed.set_footer(text=f'We were on page {self.current_page} before this message.')
        await self.message.edit(embed=self.embed)

        async def go_back_to_current_page():
            await asyncio.sleep(60.0)
            await self.show_current_page()

        self.bot.loop.create_task(go_back_to_current_page())

    async def stop_pages(self):
        """Deletes Help Message"""
        await self.message.delete()
        self.paginating = False

    def react_check(self, reaction, user):
        if user is None or user.id != self.author.id:
            return False

        if reaction.message.id != self.message.id:
            return False

        for (emoji, func) in self.reaction_emojis:
            if reaction.emoji == emoji:
                self.match = func
                return True
        return False

    async def paginate(self):
        """Actually paginate the entries and run the interactive loop if necessary."""
        first_page = self.show_page(1, first=True)
        if not self.paginating:
            await first_page
        else:
            # allow us to react to reactions right away if we're paginating
            self.bot.loop.create_task(first_page)

        while self.paginating:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=self.react_check, timeout=120.0)
            except asyncio.TimeoutError:
                self.paginating = False
                try:
                    await self.message.clear_reactions()
                except:
                    pass
                finally:
                    break

            try:
                await self.message.remove_reaction(reaction, user)
            except:
                pass  # can't remove it so don't bother doing so

            await self.match()


class FieldPages(Pages):
    """Similar to Pages except entries should be a list of
    tuples having (key, value) to show as embed fields instead.
    """

    async def show_page(self, page, *, first=False):
        self.current_page = page
        entries = self.get_page(page)

        self.embed.clear_fields()
        self.embed.description = discord.Embed.Empty

        for key, value in entries:
            self.embed.add_field(name=key, value=value, inline=False)

        if self.maximum_pages > 1:
            if self.show_entry_count:
                text = f'Page {page}/{self.maximum_pages} ({len(self.entries)} entries)'
            else:
                text = f'Page {page}/{self.maximum_pages}'

            self.embed.set_footer(text=text)

        if not self.paginating:
            return await self.channel.send(embed=self.embed)

        if not first:
            await self.message.edit(embed=self.embed)
            return

        self.message = await self.channel.send(embed=self.embed)
        for (reaction, _) in self.reaction_emojis:
            if self.maximum_pages == 2 and reaction in ('\u23ed', '\u23ee'):
                # no |<< or >>| buttons if we only have two pages
                # we can't forbid it if someone ends up using it but remove
                # it from the default set
                continue

            await self.message.add_reaction(reaction)


import itertools
import inspect
import re

# ?help
# ?help Cog
# ?help command
#   -> could be a subcommand

_mention = re.compile(r'<@!?([0-9]{1,19})>')


def cleanup_prefix(bot, prefix):
    m = _mention.match(prefix)
    if m:
        user = bot.get_user(int(m.group(1)))
        if user:
            return f'@{user.name} '
    return prefix


async def _can_run(cmd, ctx):
    try:
        return await cmd.can_run(ctx)
    except:
        return False


def _command_signature(cmd):
    # this is modified from discord.py source
    # which I wrote myself lmao

    result = [cmd.qualified_name]
    if cmd.usage:
        result.append(cmd.usage)
        return ' '.join(result)

    params = cmd.clean_params
    if not params:
        return ' '.join(result)

    for name, param in params.items():
        if param.default is not param.empty:
            # We don't want None or '' to trigger the [name=value] case and instead it should
            # do [name] since [name=None] or [name=] are not exactly useful for the user.
            should_print = param.default if isinstance(param.default, str) else param.default is not None
            if should_print:
                result.append(f'[{name}={param.default!r}]')
            else:
                result.append(f'`[{name}]`')
        elif param.kind == param.VAR_POSITIONAL:
            result.append(f'`[{name}...]`')
        else:
            result.append(f'`<{name}>`')

    return ' '.join(result)


class HelpPaginator(Pages):
    def __init__(self, ctx, entries, *, per_page=10):
        super().__init__(ctx, entries=entries, per_page=per_page)
        self.reaction_emojis.append(('\N{WHITE QUESTION MARK ORNAMENT}', self.show_bot_help))
        self.total = len(entries)

    @classmethod
    async def from_cog(cls, ctx, cog):
        cog_name = cog.__class__.__name__

        if ctx.guild is None:
            icon = ctx.author.avatar_url
        else:
            icon = ctx.guild.icon_url

        # get the commands
        entries = sorted(Cog.get_commands(cog), key=lambda c: c.name)

        # remove the ones we can't run
        entries = [cmd for cmd in entries if not cmd.hidden]

        self = cls(ctx, entries)
        self.title = f'(っ◔◡◔)っ {cog_name} (っ◔◡◔)っ'
        self.embed.set_thumbnail(url=icon)
        self.description = inspect.getdoc(cog)
        self.prefix = cleanup_prefix(ctx.bot, ctx.prefix)

        return self

    @classmethod
    async def from_command(cls, ctx, command):
        try:
            entries = sorted(command.commands, key=lambda c: c.name)
        except AttributeError:
            entries = []
        else:
            entries = [cmd for cmd in entries if not cmd.hidden]

        self = cls(ctx, entries)
        if not isinstance(command, discord.ext.commands.Group):
            if command.aliases:
                aliases = " | ".join(command.aliases)
                if command.usage:
                    self.title = f"{command.qualified_name} | {aliases} {command.signature}"
                elif command.signature:
                    self.title = f"{command.qualified_name} | {aliases} `{command.signature}`"
                else:
                    self.title = f"{command.qualified_name} | {aliases}"
            else:
                if command.usage:
                    self.title = f"{command.qualified_name} | {command.signature}"
                elif command.signature:
                    self.title = f"{command.qualified_name} `{command.signature}`"
                else:
                    self.title = f"{command.qualified_name}"

        else:
            if command.aliases:
                aliases = " | ".join(command.aliases)
                self.title = f"{command.name} | {aliases}"
            else:
                self.title = command.name

        if command.description:
            self.description = f'{command.description}\n\n{command.help}'
        else:
            self.description = command.help or 'No help given.'

        self.prefix = cleanup_prefix(ctx.bot, ctx.prefix)
        return self

    @classmethod
    async def from_bot(cls, ctx):
        def key(c):
            return c.cog_name or '\u200bMisc'

        entries = sorted(ctx.bot.commands, key=key)
        nested_pages = []
        per_page = 8

        # 0: (cog, desc, commands) (max len == 9)
        # 1: (cog, desc, commands) (max len == 9)
        # ...

        for cog, commands in itertools.groupby(entries, key=key):
            plausible = [cmd for cmd in commands if not cmd.hidden]
            if len(plausible) == 0:
                continue

            description = ctx.bot.get_cog(cog)
            if description is None:
                description = discord.Embed.Empty
            else:
                description = inspect.getdoc(description) or discord.Embed.Empty

            nested_pages.extend(
                (cog, description, plausible[i:i + per_page]) for i in range(0, len(plausible), per_page))

        if ctx.guild is None:
            icon = ctx.author.avatar_url
        else:
            icon = ctx.guild.icon_url

        self = cls(ctx, nested_pages, per_page=1)  # this forces the pagination session
        self.prefix = cleanup_prefix(ctx.bot, ctx.prefix)
        self.embed.set_thumbnail(url=icon)

        # swap the get_page implementation with one that supports our style of pagination
        self.get_page = self.get_bot_page
        self._is_bot = True

        # replace the actual total
        self.total = sum(len(o) for _, _, o in nested_pages)
        return self

    def get_bot_page(self, page):
        cog, description, commands = self.entries[page - 1]
        self.title = f'{cog} Commands'
        self.description = description
        return commands

    async def show_page(self, page, *, first=False):
        self.current_page = page
        entries = self.get_page(page)

        self.embed.clear_fields()
        self.embed.description = self.description
        self.embed.title = self.title

        self.embed.set_footer(text=f'"{self.prefix}help command | module" For More Information!')

        signature = _command_signature

        for entry in entries:
            self.embed.add_field(name=signature(entry), value=entry.short_doc or "No help given", inline=False)

        if self.maximum_pages:
            self.embed.set_author(name=f'Page {page}/{self.maximum_pages} ({self.total} commands)')

        if not self.paginating:
            return await self.channel.send(embed=self.embed)

        if not first:
            await self.message.edit(embed=self.embed)
            return

        self.message = await self.channel.send(embed=self.embed)
        for (reaction, _) in self.reaction_emojis:
            if self.maximum_pages == 2 and reaction in ('\u23ed', '\u23ee'):
                # no |<< or >>| buttons if we only have two pages
                # we can't forbid it if someone ends up using it but remove
                # it from the default set
                continue

            await self.message.add_reaction(reaction)

    async def show_help(self):
        """Shows This Message"""

        self.embed.title = 'Paginator help'
        self.embed.description = 'Hello! Welcome to the help page.'

        messages = [f'{emoji} {func.__doc__}' for emoji, func in self.reaction_emojis]
        self.embed.clear_fields()
        self.embed.add_field(name='What are these reactions for?', value='\n'.join(messages), inline=False)

        self.embed.set_footer(text=f'We were on page {self.current_page} before this message.')
        await self.message.edit(embed=self.embed)

        async def go_back_to_current_page():
            await asyncio.sleep(30.0)
            await self.show_current_page()

        self.bot.loop.create_task(go_back_to_current_page())

    async def show_bot_help(self):
        """Information On The Bot"""

        self.embed.title = 'Using Ensō~Chan'
        self.embed.description = 'Hiya! This is the Help Page!'
        self.embed.clear_fields()

        entries = (
            ('`<argument>`', 'This means the argument is **required**.'),
            ('`[argument]`', 'This means the argument is **optional**.'),
            ('`[A|B]`', 'This means the it can be **either A or B**.'),
            ('`[argument...]`', 'This means you can have multiple arguments.\n' \
                                'Now that you know the basics, it should be noted that...\n' \
                                '**You do not type in the brackets!**')
        )

        self.embed.add_field(name='How do I use Ensō~Chan', value='Reading the signature is pretty straightforward')

        for name, value in entries:
            self.embed.add_field(name=name, value=value, inline=False)

        self.embed.set_footer(text=f'We were on page {self.current_page} before this message.')
        await self.message.edit(embed=self.embed)

        async def go_back_to_current_page():
            await asyncio.sleep(30.0)
            await self.show_current_page()

        self.bot.loop.create_task(go_back_to_current_page())


def send_feedback(self, message, author):
    """Preparing Embed to send to the support server"""

    embed = Embed(title="Feedback!",
                  colour=self.bot.admin_colour,
                  timestamp=datetime.datetime.utcnow())

    embed.set_thumbnail(url=author.avatar_url)
    embed.set_footer(text=f"Send By {author}")

    fields = [("Member", f"{author.mention} | {author}", False),
              ("Message", message.content, False)]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    return embed


def message_sent_confirmation(self):
    """Preparing Embed to be sent to the user after the message has been received successfully"""

    ConfirmationEmbed = Embed(title="Thank you for your feedback!",
                              description=f"**Message relayed to {self.bot.hammyMention}**",
                              colour=self.bot.admin_colour,
                              timestamp=datetime.datetime.utcnow())
    ConfirmationEmbed.set_footer(text=f"Thanks Once Again! ~ Hammy")

    return ConfirmationEmbed


def error_handling(self, author):
    """Preparing embed to send if the message is not suitable"""

    ErrorHandlingEmbed = Embed(
        title="Uh Oh! Please make sure the message is below **1024** characters!",
        colour=self.bot.admin_colour,
        timestamp=datetime.datetime.utcnow())

    ErrorHandlingEmbed.set_footer(text=f"Sent To {author}")

    return ErrorHandlingEmbed


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


# Set up the Cog
class Help(Cog):
    """Help Commands!"""

    def __init__(self, bot):
        self.bot = bot

    @command(name='help', usage="`[command|cog]`")
    async def _help(self, ctx, *, cmd: Optional[str] = None):
        """Shows help about a command or the bot"""

        try:
            if cmd is None:
                p = await HelpPaginator.from_bot(ctx)
            else:
                entity = ctx.bot.get_cog(cmd) or ctx.bot.get_command(cmd)

                if entity is None:
                    clean = cmd.replace('@', '@\u200b')
                    return await self.bot.generate_embed(ctx, desc=f"Command or Category **{clean}** Not Found.")
                elif isinstance(entity, commands.Command):
                    p = await HelpPaginator.from_command(ctx, entity)
                else:
                    p = await HelpPaginator.from_cog(ctx, entity)

            await p.paginate()
        except Exception as ex:
            await ctx.send(f"**{ex}**")

    @command(name="forceprefix", hidden=True)
    @guild_only()
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

    @command(name="prefix")
    @guild_only()
    @has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new: Optional[str] = None):
        """View/Change Guild Prefix"""

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

    @command(name="support")
    async def support(self, ctx):
        """Joining Support Server And Sending Feedback"""

        embed = Embed(title="Support Server!",
                      description=f"Do **{ctx.prefix}feedback** to send me feedback about the bot and/or report any issues "
                                  f"that you are having!",
                      url="https://discord.gg/SZ5nexg",
                      colour=self.bot.admin_colour,
                      timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        fields = [("Developer", f"{self.bot.hammyMention} | Hamothy#5619", False),
                  ("Data Collection",
                   "\nData Stored:" +
                   "\n- User ID" +
                   "\n- Guild ID" +
                   "\n\n If you wish to delete this data being stored about you. Follow steps outlined below:" +
                   "\n\n1) **Enable Developer Mode**" +
                   "\n2) Note down your **User ID** and the **Guild ID** (You must have left this guild or are planning to leave)" +
                   f"\n3) Join support server and notify me or use **{ctx.prefix}feedback** to notify me", False)]

        # Add fields to the embed
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @command(name="feedback")
    async def feedback(self, ctx):
        """Sending Feedback to Support Server"""

        # Get the #feedback channel within the support server
        channel = self.bot.get_channel(self.bot.enso_feedback_ID)

        embed = Embed(title="Provide Feedback!",
                      description=f"Hiya! Please respond to this message with the feedback you want to provide!"
                                  f"\n(You have **5 minutes** to respond. Make sure it is a **single message** and under **1024** characters!)",
                      url="https://discord.gg/SZ5nexg",
                      colour=self.bot.admin_colour,
                      timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        helper = await ctx.author.send(embed=embed)

        def check(m):
            """Ensure that the feedback received is from the author's DMs"""
            return m.author == ctx.author and isinstance(m.channel, DMChannel)

        try:
            # Wait for feedback from author
            msg = await ctx.bot.wait_for('message', check=check, timeout=300.0)

            # Make sure sure that the message is below 1024 characters
            while len(msg.content) > 1024 and check(msg):
                await ctx.author.send(embed=error_handling(self, ctx.author))

                # Wait for feedback again
                msg = await ctx.bot.wait_for('message', check=check, timeout=300.0)

            # Once message is below 1024 characters
            # Send confirmation message to author to let them know feedback has been sent
            # Send the feedback entered from the author into support server
            if len(msg.content) < 1024 and check(msg):
                await ctx.author.send(embed=message_sent_confirmation(self))

                await channel.send(embed=send_feedback(self, msg, ctx.author))

        # Edit current embed to show error that the feedback timed out
        except asyncio.TimeoutError:

            embed = Embed(title="(｡T ω T｡) You waited too long",
                          description=f"Do **{ctx.prefix}feedback** to try again!",
                          colour=self.bot.admin_colour,
                          timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"Sent To {ctx.author}", icon_url=ctx.author.avatar_url)

            # Send out an error message if the user waited too long
            await helper.edit(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
