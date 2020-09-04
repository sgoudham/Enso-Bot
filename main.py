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

from bot import Bot

# Initiating Bot Object As Client
client = Bot()


@client.event
async def on_message(message):
    """Make sure bot messages are not tracked"""

    # Ignoring messages that start with 2 ..
    if message.content.startswith("..") or message.author.bot:
        return

    # Processing the message
    await client.process_commands(message)


# Run the bot
client.execute()
