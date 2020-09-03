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

import asyncpg
from discord import TextChannel, Embed, NotFound
from discord.ext.commands import Cog, group, bot_has_permissions, has_permissions


def is_url_spoiler(self, text, url):
    spoilers = self.spoilers.findall(text)
    for spoiler in spoilers:
        if url in spoiler:
            return True
    return False


async def send_starboard_and_update_db(self, payload, action):
    """Send the starboard embed and update database/cache"""

    if (starboard := self.bot.get_starboard_channel(payload.guild_id)) and payload.emoji.name == "⭐":
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

        # Making sure the variables are right for each react event
        user = payload.member.id if action == "added" else payload.user_id

        if not message.author.bot and user != message.author.id:
            channel = self.bot.get_channel(starboard)
            msg_id, stars = await self.bot.check_starboard_messages_cache(message.id, payload.guild_id)
            new_stars = stars + 1 if action == "added" else stars - 1

            embed = Embed(title=f"Starred Message | {new_stars} :star:",
                          description=f"{message.content or 'View Attachment'}",
                          colour=message.author.colour,
                          timestamp=datetime.datetime.utcnow())
            embed.set_author(name=message.author, icon_url=message.author.avatar_url)
            embed.set_footer(text=f"ID: {message.id}")
            embed.add_field(name="Original Message",
                            value=f"**Channel:** {message.channel.mention}\n[Jump To Message]({message.jump_url})",
                            inline=False)

            if message.attachments:
                file = message.attachments[0]
                spoiler = file.is_spoiler()
                if not spoiler and file.url.lower().endswith(('png', 'jpeg', 'jpg', 'gif', 'webp')):
                    embed.set_image(url=file.url)
                elif spoiler:
                    embed.add_field(name='Attachment', value=f'||[{file.filename}]({file.url})||', inline=False)
                else:
                    embed.add_field(name='Attachment', value=f'[{file.filename}]({file.url})', inline=False)

            if not stars:
                if new_stars >= self.bot.get_starboard_min_stars(payload.guild_id) and not msg_id:
                    star_message = await channel.send(embed=embed)

                # Setup up pool connection
                pool = self.bot.db
                async with pool.acquire() as conn:

                    # Insert the starboard message in the database
                    try:
                        if new_stars >= self.bot.get_starboard_min_stars(payload.guild_id):
                            update_query = """INSERT INTO starboard_messages (root_message_id, guild_id, star_message_id)
                                              VALUES ($1, $2, $3)"""
                            await conn.execute(update_query, message.id, payload.guild_id, star_message.id)
                        else:
                            update_query = """INSERT INTO starboard_messages (root_message_id, guild_id)
                                                                          VALUES ($1, $2)"""
                            await conn.execute(update_query, message.id, payload.guild_id)

                    # Catch errors
                    except asyncpg.PostgresError as e:
                        print(
                            f"PostGres Error: Starboard_Message Record Could Not Be Inserted For Guild {payload.guild_id}",
                            e)

                    # Update cache
                    else:
                        if new_stars >= self.bot.get_starboard_min_stars(payload.guild_id):
                            self.bot.cache_store_starboard_message(message.id, payload.guild_id, star_message.id)
                        else:
                            self.bot.cache_store_starboard_message(message.id, payload.guild_id, None)

                    # Release connection back to pool
                    finally:
                        await pool.release(conn)

            else:
                if new_stars >= self.bot.get_starboard_min_stars(payload.guild_id) and not msg_id:
                    star_message = await channel.send(embed=embed)
                else:
                    try:
                        star_message = await channel.fetch_message(msg_id)
                        await star_message.edit(embed=embed)
                    except NotFound:
                        pass

                # Setup up pool connection
                pool = self.bot.db
                async with pool.acquire() as conn:

                    # Update the stars that the message has in the database
                    try:
                        if new_stars >= self.bot.get_starboard_min_stars(payload.guild_id):
                            update_query = """UPDATE starboard_messages 
                                              SET stars = $1, star_message_id = $2
                                              WHERE root_message_id = $3 AND guild_id = $4"""
                            await conn.execute(update_query, new_stars, star_message.id, message.id, payload.guild_id)
                        else:
                            update_query = """UPDATE starboard_messages 
                                              SET stars = $1
                                              WHERE root_message_id = $2 AND guild_id = $3"""
                            await conn.execute(update_query, new_stars, message.id, payload.guild_id)

                    # Catch errors
                    except asyncpg.PostgresError as e:
                        print(
                            f"PostGres Error: Starboard_Message Record Could Not Be Updated For Guild {payload.guild_id}",
                            e)

                    # Update cache
                    else:
                        if new_stars >= self.bot.get_starboard_min_stars(payload.guild_id):
                            self.bot.cache_store_starboard_message(message.id, payload.guild_id, star_message.id)
                        self.bot.update_starboard_message(message.id, payload.guild_id, new_stars)

                    # Release connection back to pool
                    finally:
                        await pool.release(conn)


async def get_starboard_from_db(self, ctx, action):
    """Get the starboard record from DB"""

    # Setup up pool connection
    pool = self.bot.db
    async with pool.acquire() as conn:

        # Get the row of the guild from the starboard table
        try:
            select_query = """SELECT * FROM starboard WHERE guild_id = $1"""
            result = await conn.fetchrow(select_query, ctx.guild.id)

        # Catch errors
        except asyncpg.PostgresError as e:
            print("PostGres Error: Starboard Record Could Not Be Retrieved For Starboard Setup", e)

        # Throw error if the guild already exists
        else:
            if action == "setup" and result:
                text = "**Starboard** Already Setup!" \
                       f"\nDo **{ctx.prefix}help starboard** to find out more!"
                await self.bot.generate_embed(ctx, desc=text)
                return None
            elif (action == "update" or action == "delete") and not result:
                text = "**Starboard** Not Setup!" \
                       f"\nDo **{ctx.prefix}help starboard** to find out more!"
                await self.bot.generate_embed(ctx, desc=text)
                return None

        # Release the connection back to the pool
        finally:
            await pool.release(conn)

        return not None


# Set up the cog
class Starboard(Cog):
    """Starboard feature!"""

    def __init__(self, bot):
        self.bot = bot

    @group(name="starboard", case_insensitive=True, usage="`<setup|update|delete>`")
    @bot_has_permissions(embed_links=True)
    @has_permissions(manage_guild=True)
    async def starboard(self, ctx):
        """
        Starboard! Let the community star messages!
        """

    @starboard.command(name="stars")
    @bot_has_permissions(embed_links=True)
    async def sb_min_stars(self, ctx, stars: int):
        """Update the minimum amount of stars needed for the message to appear on the starboard"""

        if await get_starboard_from_db(self, ctx, "update") and stars > 0:
            # Setup up pool connection
            pool = self.bot.db
            async with pool.acquire() as conn:

                # Update the starboard min_stars in the database
                try:
                    update_query = """UPDATE starboard SET min_stars = $1 WHERE guild_id = $2"""
                    await conn.execute(update_query, stars, ctx.guild.id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(f"PostGres Error: Starboard Record Could Not Be Updated For Guild {ctx.guild.id}", e)

                # Send confirmation that the channel has been updated
                else:
                    star_channel = self.bot.get_starboard_channel(ctx.guild.id)
                    channel = self.bot.get_channel(star_channel)
                    text = "**Minimum Stars Updated!**" \
                           f"\nMessages will now need {stars} :star: to appear in {channel.mention}"
                    await self.bot.generate_embed(ctx, desc=text)

                    # Update cache
                    self.bot.update_starboard_min_stars(ctx.guild.id, stars)

                # Release connection back to pool
                finally:
                    await pool.release(conn)

        elif stars <= 0:
            await self.bot.generate_embed(ctx, desc="Minimum Stars Must Be Over or Equal to 1!")

    @starboard.command(name="setup")
    @bot_has_permissions(embed_links=True)
    async def sb_setup(self, ctx, starboard_channel: TextChannel):
        """
        Setup Starboard
        First Argument: Input Channel(Mention or ID) where starred messages will be sent
        """

        if await get_starboard_from_db(self, ctx, "setup"):
            # Setup up pool connection
            pool = self.bot.db
            async with pool.acquire() as conn:

                # Insert the information about the starboard into database
                try:
                    insert_query = """INSERT INTO starboard (guild_id, channel_id) VALUES ($1, $2)"""
                    await conn.execute(insert_query, ctx.guild.id, starboard_channel.id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(f"PostGres Error: Starboard Record Could Not Be Inserted For Guild {ctx.guild.id}", e)

                # Send confirmation message
                else:
                    text = "**Starboard** is successfully set up!" \
                           f"\nRefer to **{ctx.prefix}help modmail** for more information"
                    await self.bot.generate_embed(ctx, desc=text)

                    # Store into cache
                    self.bot.cache_store_starboard(ctx.guild.id, starboard_channel.id, 1)

                # Release connection back into pool
                finally:
                    await pool.release(conn)

    @starboard.command(name="update")
    @bot_has_permissions(embed_links=True)
    async def sb_update(self, ctx, starboard_channel: TextChannel):
        """
        Update the channel that the starred messages are sent to
        You can Mention or use the Channel ID
        """

        if await get_starboard_from_db(self, ctx, "update"):
            # Setup up pool connection
            pool = self.bot.db
            async with pool.acquire() as conn:

                # Update the starboard channel in the database
                try:
                    update_query = """UPDATE starboard SET channel_id = $1 WHERE guild_id = $2"""
                    await conn.execute(update_query, starboard_channel.id, ctx.guild.id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(f"PostGres Error: Starboard Record Could Not Be Updated For Guild {ctx.guild.id}", e)

                # Send confirmation that the channel has been updated
                else:
                    text = "**Channel Updated**" \
                           f"\nNew Starred Messages will be sent to {starboard_channel.mention}"
                    await self.bot.generate_embed(ctx, desc=text)

                    # Update cache
                    self.bot.update_starboard_channel(ctx.guild.id, starboard_channel.id)

                # Release connection back to pool
                finally:
                    await pool.release(conn)

    @starboard.command(name="delete")
    @bot_has_permissions(embed_links=True)
    async def sb_delete(self, ctx):
        """Delete the starboard from the guild"""

        if await get_starboard_from_db(self, ctx, "delete"):
            # Setup up pool connection
            pool = self.bot.db
            async with pool.acquire() as conn:

                # Remove the starboard record from the database
                try:
                    delete_query = """DELETE FROM starboard WHERE guild_id = $1"""
                    await conn.execute(delete_query, ctx.guild.id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(f"PostGres Error: Starboard Record Could Not Be Deleted for Guild {ctx.guild.id}", e)

                # Sending confirmation message that the starboard has been deleted
                else:
                    text = "**Starboard** successfully deleted!" \
                           f"\nDo **{ctx.prefix}help starboard** to find out more!"
                    await self.bot.generate_embed(ctx, desc=text)

                    # Delete from cache
                    self.bot.delete_starboard(ctx.guild.id)

                # Release connection back to pool
                finally:
                    await pool.release(conn)

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Removing reaction when a star is removed from the message"""

        await send_starboard_and_update_db(self, payload, action="removed")

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Listening for star reactions for any guilds that have starboard enabled"""

        await send_starboard_and_update_db(self, payload, action="added")


def setup(bot):
    bot.add_cog(Starboard(bot))
