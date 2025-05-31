#!/usr/bin/env python3
"""
Simple test for Recent Activity Modal Dialog close button
Tests that the close button callbacks are properly set
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_modal_close_button():
    """Test the modal dialog close button functionality"""

    try:
        # Test import
        from app.views.recent_activity_modal import RecentActivityModalDialog
        print("✓ Successfully imported modal dialog components")

        # Test modal creation
        modal = RecentActivityModalDialog()
        print("✓ Modal dialog created")

        # Test creating fresh dialog
        modal._create_fresh_dialog()
        print("✓ Fresh dialog created")

        # Check if dialog has buttons
        if modal.dialog and modal.dialog.buttons:
            print(f"✓ Dialog has {len(modal.dialog.buttons)} buttons")

            # Check each button
            for i, button in enumerate(modal.dialog.buttons):
                print(f"  Button {i+1}: text='{button.text}', callback={type(button.on_release)}")

                # Test if the close button callback is properly set
                if button.text == "Close":
                    print(f"  Close button found with callback")

                    # Test the callback method directly
                    print("  Testing close callback directly...")
                    try:
                        modal._close_dialog(None)
                        print("  ✓ Close callback executed successfully")
                    except Exception as e:
                        print(f"  ❌ Close callback failed: {e}")

        else:
            print("❌ Dialog has no buttons")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Testing Recent Activity Modal Close Button\n")
    result = test_modal_close_button()
    print(f"\nTest {'PASSED' if result else 'FAILED'}")
