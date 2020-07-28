import asyncio

import aiomysql
from decouple import config

# Get password/host from .env
password = config('DB_PASS')
host = config('DB_HOST')


# Setting up connection using pool/aiomysql
async def connection(loop):
    pool = await aiomysql.create_pool(
        host=host,
        port=3306,
        user="hamothy",
        password=password,
        db='enso',
        loop=loop)

    return pool


# Make sure the connection is setup before the bot is ready
loop = asyncio.get_event_loop()
loop.run_until_complete(connection(loop))
