import sqlite3

# Connect to the database
conn = sqlite3.connect('userdesktop-rs-database.db')
cursor = conn.cursor()

# Get the actual schema of the realstatephotos table
cursor.execute("PRAGMA table_info(realstatephotos)")
columns = cursor.fetchall()
print("Columns in realstatephotos table:")
for column in columns:
    print(f"  {column[1]} ({column[2]})")

# Get a sample row to see the actual data
cursor.execute("SELECT * FROM realstatephotos LIMIT 1")
row = cursor.fetchone()
if row:
    print("\nSample row:")
    for i, column in enumerate(columns):
        print(f"  {column[1]}: {row[i]}")
else:
    print("\nNo data in realstatephotos table")

# Close the connection
conn.close()
