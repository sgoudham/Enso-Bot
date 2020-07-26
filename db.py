import asyncio
import sys

import aiomysql
import mariadb
from decouple import config

# Get password/host from .env
password = config('DB_PASS')
host = config('DB_HOST')


# Setting up connection using pool/aiomysql
async def connection2(loop):
    pool = await aiomysql.create_pool(
        host=host,
        port=3306,
        user="hamothy",
        password=password,
        db='enso',
        loop=loop)

    return pool


loop = asyncio.get_event_loop()
loop.run_until_complete(connection2(loop))


# Connect to MariaDB Platform and database Enso
def connection():
    try:
        conn = mariadb.connect(
            user="hamothy",
            password=password,
            host=host,
            port=3306,
            database="enso"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Returning connection string
    return conn
