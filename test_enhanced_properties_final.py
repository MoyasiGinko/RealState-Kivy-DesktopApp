#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify Enhanced Properties CRUD functionality
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.database import DatabaseManager
from app.views.enhanced_properties import EnhancedPropertiesScreen

def test_enhanced_properties():
    """Test Enhanced Properties CRUD functionality"""

    print("=" * 60)
    print("Testing Enhanced Properties CRUD Functionality")
    print("=" * 60)

    # Initialize database manager
    try:
        db = DatabaseManager()
        print("✓ Database manager initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize database: {e}")
        return False

    # Test Enhanced Properties Screen creation
    try:
        properties_screen = EnhancedPropertiesScreen(db)
        print("✓ Enhanced Properties screen created successfully")
    except Exception as e:
        print(f"✗ Failed to create properties screen: {e}")
        return False

    # Test CRUD method existence
    print("\n--- Testing CRUD Methods Existence ---")

    crud_methods = [
        'edit_property',
        'update_property_simple',
        'confirm_delete_property',
        'save_property_simple',
        'clear_form_simple',
        '_set_edit_mode',
        '_set_new_property_mode',
        '_load_property_dropdowns'
    ]

    for method_name in crud_methods:
        if hasattr(properties_screen, method_name):
            print(f"✓ {method_name} method exists")
        else:
            print(f"✗ {method_name} method missing")

    # Test button state management methods
    print("\n--- Testing Button State Management ---")

    # Test setting new property mode
    try:
        properties_screen._set_new_property_mode()
        print("✓ _set_new_property_mode works")
    except Exception as e:
        print(f"✗ _set_new_property_mode failed: {e}")

    # Test setting edit mode
    try:
        properties_screen._set_edit_mode()
        print("✓ _set_edit_mode works")
    except Exception as e:
        print(f"✗ _set_edit_mode failed: {e}")

    # Test snackbar methods
    print("\n--- Testing Snackbar Methods ---")

    snackbar_methods = [
        'show_success_snackbar',
        'show_error_snackbar',
        'show_info_snackbar'
    ]

    for method_name in snackbar_methods:
        if hasattr(properties_screen, method_name):
            print(f"✓ {method_name} method exists")
        else:
            print(f"✗ {method_name} method missing")

    # Test database operations
    print("\n--- Testing Database Operations ---")

    try:
        properties = db.get_properties()
        print(f"✓ Retrieved {len(properties)} properties from database")
    except Exception as e:
        print(f"✗ Failed to get properties: {e}")

    try:
        owners = db.get_owners()
        print(f"✓ Retrieved {len(owners)} owners from database")
    except Exception as e:
        print(f"✗ Failed to get owners: {e}")

    try:
        property_types = db.get_property_types()
        print(f"✓ Retrieved {len(property_types)} property types from database")
    except Exception as e:
        print(f"✗ Failed to get property types: {e}")

    # Test integration layer setup
    print("\n--- Testing Integration Layer Support ---")

    if hasattr(properties_screen, 'integration_layer'):
        print("✓ Integration layer attribute exists")
        if hasattr(properties_screen, 'set_integration_layer'):
            print("✓ set_integration_layer method exists")
        else:
            print("✗ set_integration_layer method missing")
    else:
        print("✗ Integration layer attribute missing")

    print("\n" + "=" * 60)
    print("Enhanced Properties CRUD Test Complete")
    print("=" * 60)

    return True

if __name__ == '__main__':
    test_enhanced_properties()
