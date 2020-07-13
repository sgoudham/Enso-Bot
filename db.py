import sys

import mariadb
from decouple import config

# Get password/host from .env
password = config('DB_PASS')
host = config('DB_HOST')


# Connect to MariaDB Platform
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
