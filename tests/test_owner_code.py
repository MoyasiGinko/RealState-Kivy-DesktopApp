#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test the owner code generation functionality.
Ensures that owner codes are:
1. Always 4 characters in length
2. Unique
3. Only contain alphanumeric characters
"""

import sys
# Add the app directory to Python path
sys.path.insert(0, './app')

from database import DatabaseManager

def test_owner_code_generation():
    """Test that owner codes are correctly generated"""

    db = DatabaseManager()

    print("Testing owner code generation...")
    print("Generating 20 codes to verify uniqueness and format...")

    # Generate a set of codes to verify uniqueness
    codes = set()
    for i in range(20):
        code = db.generate_owner_code()
        print(f"Code {i+1}: {code}")

        # Verify the code length
        if len(code) != 4:
            print(f"ERROR: Code '{code}' is not 4 characters in length!")

        # Verify the code only contains alphanumeric characters
        if not code.isalnum():
            print(f"ERROR: Code '{code}' contains non-alphanumeric characters!")

        # Verify the code is uppercase
        if not code.isupper() and not code.isdigit():
            print(f"ERROR: Code '{code}' is not all uppercase!")

        # Add to set to check for duplicates
        codes.add(code)

    # Verify that all codes are unique
    if len(codes) != 20:
        print(f"ERROR: Generated {20-len(codes)} duplicate codes!")
    else:
        print("All codes are unique!")

    print("Owner code generation test complete!")

if __name__ == "__main__":
    test_owner_code_generation()