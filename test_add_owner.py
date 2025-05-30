#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test adding an owner with the generated owner code.
"""

import sys
import traceback
# Add the app directory to Python path
sys.path.insert(0, './app')

from database import DatabaseManager

def test_add_owner():
    """Test adding an owner with the generated owner code"""

    try:
        db = DatabaseManager()

        print("Testing adding an owner with the generated owner code...")        # Generate a unique owner code
        owner_code = db.generate_owner_code()
        print(f"Generated owner code: {owner_code}")

        # Add an owner with the generated code
        test_name = "Test Owner"
        test_phone = "555-123-4567"
        test_note = "Test note for the owner"

        # Now add the owner (this will internally generate another code)
        result_code = db.add_owner(test_name, test_phone, test_note)
        print(f"Added owner with code: {result_code}")

        # Compare the codes - they should be different since add_owner generates its own code
        print(f"Generated code: {owner_code}, Used code: {result_code}")
        print(f"Codes are {'different' if owner_code != result_code else 'the same'} as expected")

        # Verify the code is 4 characters long
        if len(result_code) != 4:
            print(f"ERROR: Added owner code '{result_code}' is not 4 characters in length!")

        # Get all owners and check if our new owner is in the list
        owners = db.get_owners()
        found = False
        for owner in owners:
            if owner[0] == result_code:
                found = True
                print(f"Found owner in database: {owner}")
                break

        if not found:
            print(f"ERROR: Added owner with code '{result_code}' not found in database!")
        else:
            print("Owner successfully added to the database!")

        print("Add owner test complete!")
    except Exception as e:
        print(f"ERROR: An exception occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_add_owner()

if __name__ == "__main__":
    test_add_owner()
