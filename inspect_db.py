import sqlite3
import os

db_path = 'userdesktop-rs-database.db'

if not os.path.exists(db_path):
    print(f"Database file {db_path} does not exist")
    exit(1)

print(f"Database file exists: {db_path}")
print(f"File size: {os.path.getsize(db_path)} bytes")

try:
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("\nTables in the database:")
    for table in tables:
        print(f"- {table[0]}")

        # Get schema for each table
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        print(f"  Columns in {table[0]}:")
        for column in columns:
            print(f"    - {column[1]} ({column[2]})")

        # Count rows in the table
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"  Rows: {count}")

        # If it's the photos table, get more details
        if table[0].lower() == 'realstatephotos':
            print("\nSample rows from realstatephotos:")
            cursor.execute(f"SELECT * FROM {table[0]} LIMIT 5")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(f"  Row: {row}")
            else:
                print("  No rows found")

    # Close the connection
    conn.close()

except sqlite3.Error as e:
    print(f"SQLite error: {e}")
