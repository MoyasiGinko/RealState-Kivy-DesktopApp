#!/usr/bin/env python3
"""
Quick test to check database schema
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from database import DatabaseManager

def check_schema():
    """Check database table schemas"""
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()

        print("=== Database Schema Check ===")

        # Check Realstatspecification table
        print("\n--- Realstatspecification table ---")
        cursor.execute("PRAGMA table_info(Realstatspecification)")
        columns = cursor.fetchall()
        for col in columns:
            print(f"Column: {col[1]}, Type: {col[2]}")

        # Check realstatephotos table
        print("\n--- realstatephotos table ---")
        cursor.execute("PRAGMA table_info(realstatephotos)")
        columns = cursor.fetchall()
        if columns:
            for col in columns:
                print(f"Column: {col[1]}, Type: {col[2]}")
        else:
            print("Table does not exist or has no columns")

        conn.close()

    except Exception as e:
        print(f"Error checking schema: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_schema()
