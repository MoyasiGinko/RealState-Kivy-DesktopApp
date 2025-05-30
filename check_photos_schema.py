import sqlite3
import os

db_path = 'userdesktop-rs-database.db'

try:
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if realstatephotos table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='realstatephotos'")
    if cursor.fetchone():
        print("realstatephotos table exists")

        # Get schema for realstatephotos
        cursor.execute("PRAGMA table_info(realstatephotos)")
        columns = cursor.fetchall()
        print("Columns in realstatephotos table:")
        for column in columns:
            print(f"  - {column[1]} ({column[2]})")

        # Get a sample row
        cursor.execute("SELECT * FROM realstatephotos LIMIT 1")
        row = cursor.fetchone()
        if row:
            print("\nSample row:")
            for i, column in enumerate(columns):
                print(f"  {column[1]}: {row[i]}")
        else:
            print("\nNo data in realstatephotos table")
    else:
        print("realstatephotos table does not exist")

    # Close the connection
    conn.close()

except sqlite3.Error as e:
    print(f"SQLite error: {e}")
