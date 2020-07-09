import sys

import mariadb
from decouple import config

password = config('DB_PASS')


def connection():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="root@%",
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
