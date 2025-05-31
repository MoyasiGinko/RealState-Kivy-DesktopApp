#!/usr/bin/env python3
"""
Check database structure
"""

import sqlite3

def check_db_structure():
    conn = sqlite3.connect('userdesktop-rs-database.db')

    print("Owners table columns:")
    cursor = conn.execute('PRAGMA table_info(Owners)')
    for row in cursor:
        print(row)

    print("\nRealstatspecification table columns:")
    cursor = conn.execute('PRAGMA table_info(Realstatspecification)')
    for row in cursor:
        print(row)

    conn.close()

if __name__ == "__main__":
    check_db_structure()
