import sys

import mariadb
from decouple import config

password = config('DB_PASS')


def connection():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="hamothy",
            password=password,
            host="173.208.202.20",
            port=3306,
            database="enso"
        )
        if conn:
            print("working")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    return conn


connection()
