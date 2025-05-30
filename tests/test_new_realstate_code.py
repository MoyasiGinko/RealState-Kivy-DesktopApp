#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the new real estate code generation format
Verifies both full code and company prefix uniqueness
"""

import sys
from pathlib import Path
import re

# Add the app directory to Python path
app_dir = Path(__file__).parent / 'app'
sys.path.insert(0, str(app_dir))

from database import DatabaseManager

def test_realstate_code_generation():
    """Test the new real estate code generation format"""
    db = DatabaseManager()

    # Generate 50 real estate codes to check format and uniqueness
    codes = []
    company_prefixes = []

    print("Testing real estate code generation with both code and company prefix uniqueness...")

    for i in range(50):
        code = db.generate_realstate_code()
        company_prefix = code[:4]
        random_part = code[4:]

        print(f"Generated code {i+1}: {code} (Prefix: {company_prefix}, Random: {random_part})")

        # Verify format: 8 characters total
        assert len(code) == 8, f"Code length should be 8, got {len(code)}"

        # Verify first character is an alphabet letter
        assert code[0].isalpha(), f"First character should be an alphabet letter, got {code[0]}"

        # Verify characters 2-4 are digits (positions 1-3 in zero-based indexing)
        assert code[1:4].isdigit(), f"Characters 2-4 should be digits, got {code[1:4]}"

        # Verify the company prefix format (1 letter + 3 digits)
        assert re.match(r'^[A-Z]\d{3}$', company_prefix), f"Company prefix should be 1 letter + 3 digits, got {company_prefix}"

        # Verify last 4 characters are digits
        assert random_part.isdigit(), f"Random part should be digits, got {random_part}"

        # Check uniqueness of the full code
        assert code not in codes, f"Duplicate code generated: {code}"
        codes.append(code)

        # Check uniqueness of the company prefix
        assert company_prefix not in company_prefixes, f"Duplicate company prefix generated: {company_prefix}"
        company_prefixes.append(company_prefix)

    print(f"Successfully generated {len(codes)} unique real estate codes")
    print(f"All {len(company_prefixes)} company prefixes are unique")
    print("All validation checks passed successfully!")

if __name__ == "__main__":
    test_realstate_code_generation()
    test_realstate_code_generation()
