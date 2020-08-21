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
from discord.ext.commands import is_owner

from bot import Bot

# Initiating Bot Object As Client
client = Bot()
client.create_connection()


@client.command()
@is_owner()
async def test(ctx):
    # Alt Account
    testing1 = await client.check_cache(556665878662348811, 621621615930638336)
    print(client.member_cache.cache)

    # My Account on the same guild as Alt
    testing3 = await client.check_cache(154840866496839680, 621621615930638336)
    print(client.member_cache.cache)

    # Me in another guild
    testing4 = await client.check_cache(154840866496839680, 663651584399507476)
    print(client.member_cache.cache)


# Run the bot
client.execute()
