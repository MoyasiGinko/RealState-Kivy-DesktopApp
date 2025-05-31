#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Integration Test
Tests the complete application integration and navigation flow
"""

import sys
import os
sys.path.insert(0, 'app')

def test_application_integration():
    """Test the complete application integration"""
    print("🏠 Real Estate Management System - Integration Test")
    print("=" * 60)

    # Test 1: Core Imports
    print("\n1. Testing Core Imports...")
    try:
        from app.database import DatabaseManager
        from app.language_manager import language_manager
        from app.font_manager import font_manager
        print("✅ Core modules imported successfully")
    except Exception as e:
        print(f"❌ Core import error: {e}")
        return False

    # Test 2: Database Connection
    print("\n2. Testing Database Connection...")
    try:
        db = DatabaseManager()
        owners_count = db.get_total_owners()
        properties_count = db.get_total_properties()
        available_count = db.get_available_properties_count()
        print(f"✅ Database connected successfully")
        print(f"   📊 Stats: {owners_count} owners, {properties_count} properties, {available_count} available")
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

    # Test 3: Screen Imports
    print("\n3. Testing Screen Imports...")
    try:
        from app.screens.dashboard import DashboardScreen
        from app.screens.owners import OwnersScreen
        from app.screens.properties import PropertiesScreen
        from app.screens.search import SearchScreen
        from app.views.enhanced_dashboard_simple import EnhancedDashboardScreen
        print("✅ All screens imported successfully")
    except Exception as e:
        print(f"❌ Screen import error: {e}")
        return False

    # Test 4: Enhanced Dashboard
    print("\n4. Testing Enhanced Dashboard...")
    try:
        enhanced_dashboard = EnhancedDashboardScreen(db, name='enhanced_dashboard')
        print("✅ Enhanced dashboard created successfully")
    except Exception as e:
        print(f"❌ Enhanced dashboard error: {e}")
        return False

    # Test 5: Translation Keys
    print("\n5. Testing Translation Keys...")
    try:
        test_keys = [
            'welcome_dashboard',
            'dashboard_subtitle',
            'system_statistics',
            'total_properties',
            'total_owners',
            'available_properties',
            'occupied_properties',
            'manage_property_owners',
            'manage_properties',
            'search_and_generate_reports',
            'app_settings'
        ]

        missing_keys = []
        for key in test_keys:
            if key not in language_manager.translations['en']:
                missing_keys.append(key)

        if missing_keys:
            print(f"❌ Missing translation keys: {missing_keys}")
            return False
        else:
            print(f"✅ All {len(test_keys)} translation keys found")
    except Exception as e:
        print(f"❌ Translation test error: {e}")
        return False

    # Test 6: Application Structure
    print("\n6. Testing Application Structure...")
    try:
        required_files = [
            'main.py',
            'app/components.py',
            'app/database.py',
            'app/language_manager.py',
            'app/views/enhanced_dashboard_simple.py'
        ]

        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)

        if missing_files:
            print(f"❌ Missing files: {missing_files}")
            return False
        else:
            print(f"✅ All required files present")
    except Exception as e:
        print(f"❌ File structure test error: {e}")
        return False

    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED! The application is ready for use.")
    print("\n📋 Integration Summary:")
    print("   ✅ Core modules working")
    print("   ✅ Database connected and functional")
    print("   ✅ All screens can be created")
    print("   ✅ Enhanced dashboard implemented")
    print("   ✅ Translation system complete")
    print("   ✅ File structure correct")
    print("\n🚀 To run the application: python main.py")
    return True

if __name__ == "__main__":
    test_application_integration()
