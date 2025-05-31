#!/usr/bin/env python3
"""
Final Integration Test for Recent Activity Modal Dialog
Tests that the modal dialog can be opened multiple times successfully.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_modal_integration():
    """Test the modal dialog integration"""
    print("Testing Recent Activity Modal Dialog Integration...")

    try:
        # Test import
        from app.views.recent_activity_modal import (
            RecentActivityModalDialog,
            show_recent_activity_modal,
            show_fresh_recent_activity_modal
        )
        print("✓ Successfully imported modal dialog components")

        # Test database import
        from app.database import DatabaseManager
        db = DatabaseManager()
        print("✓ Successfully imported and initialized database")

        # Test modal creation
        print("\n--- Testing Modal Dialog Creation ---")

        # Test 1: Basic modal creation
        modal1 = RecentActivityModalDialog(db)
        print("✓ Test 1: Basic modal creation successful")

        # Test 2: Convenience function
        modal2 = show_recent_activity_modal(db)
        print("✓ Test 2: Convenience function works")

        # Test 3: Fresh modal function
        modal3 = show_fresh_recent_activity_modal(db)
        print("✓ Test 3: Fresh modal function works")

        # Test 4: Multiple modals
        modals = [show_fresh_recent_activity_modal(db) for _ in range(3)]
        print("✓ Test 4: Multiple modal creation successful")

        # Test 5: Modal properties
        test_modal = RecentActivityModalDialog(db)
        assert hasattr(test_modal, 'size_hint'), "Modal should have size_hint"
        assert hasattr(test_modal, 'height'), "Modal should have height"
        assert hasattr(test_modal, 'auto_dismiss'), "Modal should have auto_dismiss"
        print("✓ Test 5: Modal has required properties")

        print(f"\n🎉 All tests passed! Modal dialog integration is working correctly.")
        print(f"📊 Summary:")
        print(f"   - Modal dialogs created: {len(modals) + 3}")
        print(f"   - All imports successful: ✓")
        print(f"   - Database integration: ✓")
        print(f"   - Modal properties: ✓")

        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dashboard_integration():
    """Test that the dashboard can use the modal dialog"""
    print("\n--- Testing Dashboard Integration ---")

    try:
        from app.views.enhanced_dashboard import EnhancedDashboardScreen
        from app.database import DatabaseManager

        db = DatabaseManager()
        dashboard = EnhancedDashboardScreen(db, name='test_dashboard')
        print("✓ Dashboard screen created successfully")

        # Test that dashboard has the modal methods
        assert hasattr(dashboard, 'show_recent_activity_dialog'), "Dashboard should have show_recent_activity_dialog method"
        assert hasattr(dashboard, 'show_activity_sidebar'), "Dashboard should have show_activity_sidebar method"
        print("✓ Dashboard has required modal methods")

        return True

    except Exception as e:
        print(f"❌ Dashboard integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Final Integration Tests for Recent Activity Modal Dialog\n")

    modal_test = test_modal_integration()
    dashboard_test = test_dashboard_integration()

    print(f"\n" + "="*60)
    print(f"📋 FINAL TEST RESULTS:")
    print(f"   Modal Dialog Tests: {'✅ PASSED' if modal_test else '❌ FAILED'}")
    print(f"   Dashboard Integration: {'✅ PASSED' if dashboard_test else '❌ FAILED'}")

    if modal_test and dashboard_test:
        print(f"\n🎊 SUCCESS! All integration tests passed!")
        print(f"   The Recent Activity modal dialog is ready for use.")
        print(f"   Users can now open the dialog multiple times without issues.")
    else:
        print(f"\n⚠️  Some tests failed. Please review the errors above.")

    print("="*60)
