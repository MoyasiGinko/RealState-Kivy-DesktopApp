import sqlite3
import os

def inspect_database(db_path):
    print(f"Inspecting database: {db_path}")

    if not os.path.exists(db_path):
        print(f"Database file does not exist: {db_path}")
        return

    print(f"Database file size: {os.path.getsize(db_path)} bytes")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get list of all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        print(f"\nFound {len(tables)} tables:")
        for table in tables:
            table_name = table[0]
            print(f"\n=== Table: {table_name} ===")

            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print("Columns:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")

            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]
            print(f"Row count: {row_count}")

            # Get sample data (first 2 rows)
            if row_count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
                rows = cursor.fetchall()
                print("Sample data:")
                for row in rows:
                    print(f"  {row}")

        conn.close()
        print("\nDatabase inspection complete")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

# Run the inspection
inspect_database('userdesktop-rs-database.db')
