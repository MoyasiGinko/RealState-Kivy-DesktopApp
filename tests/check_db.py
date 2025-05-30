import sqlite3

# Connect to the database
conn = sqlite3.connect('userdesktop-rs-database.db')
cursor = conn.cursor()

# Get list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(f"- {table[0]}")

    # Get columns for each table
    cursor.execute(f"PRAGMA table_info({table[0]})")
    columns = cursor.fetchall()
    print(f"  Columns in {table[0]}:")
    for column in columns:
        print(f"    - {column[1]} ({column[2]})")
    print()

# Close the connection
conn.close()
