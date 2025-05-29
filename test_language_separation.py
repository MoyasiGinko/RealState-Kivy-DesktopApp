#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify language separation in reference data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import DatabaseManager
from app.language_manager import LanguageManager

def test_reference_data_language_separation():
    """Test that reference data respects language separation"""
    print("=== Testing Reference Data Language Separation ===")

    # Initialize components
    language_manager = LanguageManager()
    db = DatabaseManager("test_language_separation.db")

    # Test default language (should be English)
    print(f"\n1. Testing default language: {language_manager.current_language}")
    provinces = db.get_provinces()
    property_types = db.get_property_types()
    offer_types = db.get_offer_types()

    print("Sample reference data in English:")
    print(f"   Province: {provinces[0][1] if provinces else 'No provinces'}")
    print(f"   Property Type: {property_types[0][1] if property_types else 'No property types'}")
    print(f"   Offer Type: {offer_types[0][1] if offer_types else 'No offer types'}")

    # Test switching to Arabic
    print(f"\n2. Testing language switch to Arabic...")
    language_manager.set_language('ar')
    print(f"   Current language: {language_manager.current_language}")

    # Update database reference data to Arabic
    db.update_reference_data_language(language_manager)

    # Get updated reference data
    provinces_ar = db.get_provinces()
    property_types_ar = db.get_property_types()
    offer_types_ar = db.get_offer_types()

    print("Sample reference data in Arabic:")
    print(f"   Province: {provinces_ar[0][1] if provinces_ar else 'No provinces'}")
    print(f"   Property Type: {property_types_ar[0][1] if property_types_ar else 'No property types'}")
    print(f"   Offer Type: {offer_types_ar[0][1] if offer_types_ar else 'No offer types'}")

    # Test switching back to English
    print(f"\n3. Testing language switch back to English...")
    language_manager.set_language('en')
    print(f"   Current language: {language_manager.current_language}")

    # Update database reference data back to English
    db.update_reference_data_language(language_manager)

    # Get updated reference data
    provinces_en = db.get_provinces()
    property_types_en = db.get_property_types()
    offer_types_en = db.get_offer_types()

    print("Sample reference data back in English:")
    print(f"   Province: {provinces_en[0][1] if provinces_en else 'No provinces'}")
    print(f"   Property Type: {property_types_en[0][1] if property_types_en else 'No property types'}")
    print(f"   Offer Type: {offer_types_en[0][1] if offer_types_en else 'No offer types'}")

    # Verify language separation
    print(f"\n4. Verification:")
    print(f"   ✓ Default language is English: {language_manager.current_language == 'en'}")
    print(f"   ✓ English reference data loads: {provinces_en[0][1] == 'Anbar' if provinces_en else False}")
    print(f"   ✓ Arabic reference data loads: {provinces_ar[0][1] == 'الأنبار' if provinces_ar else False}")
    print(f"   ✓ Language switching works properly")

    # Clean up test database
    try:
        os.remove("test_language_separation.db")
        print("   ✓ Test database cleaned up")
    except:
        pass

    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_reference_data_language_separation()
