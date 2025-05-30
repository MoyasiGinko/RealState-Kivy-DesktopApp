#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test real estate code generation uniqueness
"""

import sys
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / 'app'
sys.path.insert(0, str(app_dir))

from database import DatabaseManager

def test_realstate_code_uniqueness():
    """Test real estate code uniqueness"""
    db = DatabaseManager()

    # Generate a large number of codes to test uniqueness
    codes = set()
    for i in range(100):
        code = db.generate_realstate_code()
        print(f"Generated code {i+1}: {code}")

        # Verify format: 8 characters (4-character company code + 4-digit random number)
        assert len(code) == 8, f"Code length should be 8, got {len(code)}"

        # Verify first character is a letter
        assert code[0].isalpha(), f"First character should be a letter, got {code[0]}"

        # Verify next 3 characters are digits
        assert code[1:4].isdigit(), f"Characters 2-4 should be digits, got {code[1:4]}"

        # Verify last 4 characters are digits
        assert code[4:].isdigit(), f"Last 4 characters should be digits, got {code[4:]}"

        # Check uniqueness
        assert code not in codes, f"Duplicate code generated: {code}"
        codes.add(code)

    print(f"Successfully generated {len(codes)} unique real estate codes")
    print("All codes passed validation")

if __name__ == "__main__":
    test_realstate_code_uniqueness()
