#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for real estate code generation
"""

import sys
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / 'app'
sys.path.insert(0, str(app_dir))

from database import DatabaseManager

def test_realstate_code_generation():
    """Test real estate code generation"""
    db = DatabaseManager()

    # Generate 10 real estate codes to check format and uniqueness
    codes = []
    for _ in range(10):
        code = db.generate_realstate_code()
        print(f"Generated code: {code}")

        # Verify format: 8 characters (4-character company code + 4-digit random number)
        assert len(code) == 8, f"Code length should be 8, got {len(code)}"

        # Verify first 4 characters are the company code (typically "ALKZ")
        company_part = code[:4]
        assert company_part.isalpha(), f"Company part should be letters, got {company_part}"

        # Verify last 4 characters are digits
        random_part = code[4:]
        assert random_part.isdigit(), f"Random part should be digits, got {random_part}"

        # Check uniqueness in our sample
        assert code not in codes, f"Duplicate code generated: {code}"
        codes.append(code)

    print(f"Successfully generated {len(codes)} unique real estate codes")
    print("All codes passed validation")

if __name__ == "__main__":
    test_realstate_code_generation()
