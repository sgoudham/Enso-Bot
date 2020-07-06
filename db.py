import sys

import mariadb
from decouple import config

password = config('DB_PASS')


def connection():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="u67_i1Lq7r8fQ2",
            password=password,
            host="216.155.135.248",
            port=3306,
            database="s67_Enso"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    return conn


"""if conn:
print("Connected to MySQL Server version ")
cursor = conn.cursor()
cursor.execute("SELECT * FROM LOGS;")
record = cursor.fetchone()
print("You're connected to database: ", record)
"""
# if conn:
"""cursor.close()
conn.close()"""
# print("MySQL connection is closed")
