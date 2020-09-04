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
from discord import Embed


class Starboard:
    def __init__(self, bot):
        self.bot = bot

    async def send_starboard_message(self, payload, new_stars, msg_id, channel, message, embed):
        """Send the message to the starboard for the first time"""

        # When the message stars is larger than the minimum, send to the starboard and store in database/cache
        if new_stars >= self.bot.get_starboard_min_stars(payload.guild_id) and not msg_id:
            star_message = await channel.send(embed=embed)

            # Only insert the record into database when it doesn't exist in cache
            if not self.bot.check_root_message_id(message.id, payload.guild_id):
                # Setup up pool connection
                pool = self.bot.db
                async with pool.acquire() as conn:

                    # Insert the starboard message in the database
                    try:
                        insert = """INSERT INTO starboard_messages (root_message_id, guild_id, star_message_id)
                                              VALUES ($1, $2, $3)"""
                        await conn.execute(insert, message.id, payload.guild_id, star_message.id)

                    # Catch errors
                    except asyncpg.PostgresError as e:
                        print(
                            f"PostGres Error: Starboard_Message Record Could Not Be Inserted For Guild {payload.guild_id}",
                            e)

                    # Update cache
                    else:
                        self.bot.cache_store_starboard_message(message.id, payload.guild_id, star_message.id)
            else:
                # Setup up pool connection
                pool = self.bot.db
                async with pool.acquire() as conn:

                    # Update the stars that the message has in the database and then store the message id's
                    try:
                        update = """UPDATE starboard_messages SET stars = $1, star_message_id = $2 WHERE root_message_id = $3 AND guild_id = $4"""
                        await conn.execute(update, new_stars, star_message.id, message.id, payload.guild_id)

                    # Catch errors
                    except asyncpg.PostgresError as e:
                        print(
                            f"PostGres Error: Starboard_Message Record Could Not Be Updated For Guild {payload.guild_id}",
                            e)

                    # Update cache
                    else:
                        self.bot.update_starboard_message_id(message.id, payload.guild_id, star_message.id)
                        self.bot.update_starboard_message_stars(message.id, payload.guild_id, new_stars)

        # Store the message into the database so the reactions can be tracked
        else:
            # Only insert into the database when the message doesn't exist in cache
            if not self.bot.check_root_message_id(message.id, payload.guild_id):
                # Setup up pool connection
                pool = self.bot.db
                async with pool.acquire() as conn:

                    # Insert the starboard message in the database
                    try:
                        insert = """INSERT INTO starboard_messages (root_message_id, guild_id) VALUES ($1, $2)"""
                        await conn.execute(insert, message.id, payload.guild_id)

                    # Catch errors
                    except asyncpg.PostgresError as e:
                        print(
                            f"PostGres Error: Starboard_Message Record Could Not Be Inserted For Guild {payload.guild_id}",
                            e)

                    # Update cache
                    else:
                        self.bot.cache_store_starboard_message(message.id, payload.guild_id, None)

            # When the message is already in the database/cache, update the amount of reactions
            else:
                # Setup up pool connection
                pool = self.bot.db
                async with pool.acquire() as conn:

                    # Update the stars that the message has in the database and then store the message id's
                    try:
                        update = """UPDATE starboard_messages SET stars = $1 WHERE root_message_id = $2 AND guild_id = $3"""
                        await conn.execute(update, new_stars, message.id, payload.guild_id)

                    # Catch errors
                    except asyncpg.PostgresError as e:
                        print(
                            f"PostGres Error: Starboard_Message Record Could Not Be Updated For Guild {payload.guild_id}",
                            e)

                    # Update cache
                    else:
                        self.bot.update_starboard_message_stars(message.id, payload.guild_id, new_stars)

    async def edit_starboard_message(self, payload, new_stars, msg_id, channel, message, embed):
        """Edit the message which is already on the starboard"""

        min_stars = self.bot.get_starboard_min_stars(payload.guild_id)

        # When the message has finally reached the minimum amount of stars, send the message to the starboard
        if new_stars >= min_stars and not msg_id:
            star_message = await channel.send(embed=embed)

            # Setup up pool connection
            pool = self.bot.db
            async with pool.acquire() as conn:

                # Update the stars that the message has in the database and then store the message id's
                try:
                    update = """UPDATE starboard_messages SET stars = $1, star_message_id = $2
                                      WHERE root_message_id = $3 AND guild_id = $4"""
                    await conn.execute(update, new_stars, star_message.id, message.id, payload.guild_id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(f"PostGres Error: Starboard_Message Record Could Not Be Updated For Guild {payload.guild_id}",
                          e)

                # Update cache
                else:
                    self.bot.cache_store_starboard_message(message.id, payload.guild_id, star_message.id)
                    self.bot.update_starboard_message_stars(message.id, payload.guild_id, new_stars)

        elif new_stars < min_stars and msg_id:
            star_message = await channel.fetch_message(msg_id)
            await star_message.delete()

            # Setup up pool connection
            pool = self.bot.db
            async with pool.acquire() as conn:

                # Update the stars that the message has in the database and set the star message id to None
                try:
                    update = """UPDATE starboard_messages 
                                                  SET stars = $1, star_message_id = NULL
                                                  WHERE root_message_id = $2 AND guild_id = $3"""
                    await conn.execute(update, new_stars, message.id, payload.guild_id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(
                        f"PostGres Error: Starboard_Message Record Could Not Be Updated For Guild {payload.guild_id}",
                        e)

                # Update cache
                else:
                    self.bot.del_starboard_star_message_id(message.id, payload.guild_id)
                    self.bot.update_starboard_message_stars(message.id, payload.guild_id, new_stars)

        # When the message already exists on the starboard but doesn't have enough reactions anymore
        elif msg_id:
            star_message = await channel.fetch_message(msg_id)
            await star_message.edit(embed=embed)

            # Setup up pool connection
            pool = self.bot.db
            async with pool.acquire() as conn:

                # Update the stars that the message has in the database and set the star message id to None
                try:
                    update = """UPDATE starboard_messages 
                                      SET stars = $1
                                      WHERE root_message_id = $2 AND guild_id = $3"""
                    await conn.execute(update, new_stars, message.id, payload.guild_id)

                # Catch errors
                except asyncpg.PostgresError as e:
                    print(
                        f"PostGres Error: Starboard_Message Record Could Not Be Updated For Guild {payload.guild_id}",
                        e)

                # Update cache
                else:
                    self.bot.update_starboard_message_id(message.id, payload.guild_id, star_message.id)
                    self.bot.update_starboard_message_stars(message.id, payload.guild_id, new_stars)

        elif not msg_id:
            self.bot.update_starboard_message_stars(message.id, payload.guild_id, new_stars)

    async def send_starboard_and_update_db(self, payload, action):
        """Send the starboard embed and update database/cache"""

        if (starboard := self.bot.get_starboard_channel(payload.guild_id)) and payload.emoji.name == "⭐":
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

            if not message.author.bot and payload.user_id != message.author.id:
                channel = self.bot.get_channel(starboard)
                msg_id, stars = await self.bot.check_starboard_messages_cache(message.id, payload.guild_id)
                new_stars = stars + 1 if action == "added" else stars - 1

                embed = Embed(title=f"Starred Message | {new_stars} :star:",
                              description=f"{message.content or 'View Attachment'}",
                              colour=message.author.colour,
                              timestamp=datetime.datetime.utcnow())
                embed.set_author(name=message.author, icon_url=message.author.avatar_url)
                embed.set_footer(text=f"ID: {message.id}")
                embed.add_field(name="Original",
                                value=f"**Channel:** {message.channel.mention}\n[Jump To Message]({message.jump_url})",
                                inline=False)

                # Send spoiler attachments as links
                if message.attachments:
                    file = message.attachments[0]
                    spoiler = file.is_spoiler()
                    if not spoiler and file.url.endswith(('png', 'jpeg', 'jpg', 'gif', 'webp')):
                        embed.set_image(url=file.url)
                    elif spoiler:
                        embed.add_field(name='Attachment', value=f'||[{file.filename}]({file.url})||', inline=False)
                    else:
                        embed.add_field(name='Attachment', value=f'[{file.filename}]({file.url})', inline=False)

                # When the message has no previous stars, send a new starboard message or update the amount of stars it has
                if not stars:
                    await self.send_starboard_message(payload, new_stars, msg_id, channel, message, embed)

                # When the message has stars already from the cache/database. Delete or edit the message
                else:
                    await self.edit_starboard_message(payload, new_stars, msg_id, channel, message, embed)
