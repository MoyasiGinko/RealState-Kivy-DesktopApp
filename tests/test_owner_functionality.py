#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
End-to-end test for the owner functionality in the application.
Tests both the owner code generation and adding owners to the database.
"""

import sys
import traceback
# Add the app directory to Python path
sys.path.insert(0, './app')

from database import DatabaseManager

def test_owner_functionality():
    """Test the entire owner functionality"""

    try:
        db = DatabaseManager()

        print("========== Testing Owner Functionality ==========")

        # Step 1: Generate multiple owner codes and verify they're all unique
        print("\n----- Step 1: Testing owner code generation -----")
        codes = set()
        for i in range(10):
            code = db.generate_owner_code()
            print(f"Generated code {i+1}: {code}")

            # Verify the code
            if len(code) != 4:
                print(f"ERROR: Code '{code}' is not 4 characters in length!")

            if not code.isalnum():
                print(f"ERROR: Code '{code}' contains non-alphanumeric characters!")

            # Add to set to check for duplicates
            codes.add(code)

        # Verify that all codes are unique
        if len(codes) != 10:
            print(f"ERROR: Generated {10-len(codes)} duplicate codes!")
        else:
            print("All codes are unique!")

        # Step 2: Add several owners to the database
        print("\n----- Step 2: Testing adding owners -----")
        test_owners = [
            {"name": "John Smith", "phone": "555-111-2222", "note": "Test owner 1"},
            {"name": "Jane Doe", "phone": "555-333-4444", "note": "Test owner 2"},
            {"name": "Alice Johnson", "phone": "555-555-6666", "note": "Test owner 3"}
        ]

        added_codes = []
        for i, owner in enumerate(test_owners):
            code = db.add_owner(owner["name"], owner["phone"], owner["note"])
            print(f"Added owner {i+1}: {owner['name']} with code: {code}")

            if not code or len(code) != 4:
                print(f"ERROR: Invalid owner code returned: '{code}'")

            added_codes.append(code)

        # Step 3: Retrieve all owners and verify our test owners are in the database
        print("\n----- Step 3: Testing retrieving owners -----")
        all_owners = db.get_owners()
        print(f"Retrieved {len(all_owners)} owners from database")

        # Check if all our test owners are in the database
        found_count = 0
        for code in added_codes:
            found = False
            for owner in all_owners:
                if owner[0] == code:
                    print(f"Found owner: {owner}")
                    found = True
                    found_count += 1
                    break

            if not found:
                print(f"ERROR: Owner with code '{code}' not found in database!")

        if found_count == len(test_owners):
            print("All test owners were successfully found in the database!")
        else:
            print(f"ERROR: Only found {found_count} out of {len(test_owners)} test owners in the database!")

        print("\n========== Owner Functionality Test Complete ==========")

    except Exception as e:
        print(f"ERROR: An exception occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_owner_functionality()
