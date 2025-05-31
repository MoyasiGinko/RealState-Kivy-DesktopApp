#!/usr/bin/env python3
"""
Comprehensive test for Recent Activity Modal Close Button
Tests the close button in a real Kivy app context
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kivy.logger import Logger
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout

class TestModalApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.modal_dialog = None

    def build(self):
        # Create a simple screen with a button to open the modal
        screen = MDScreen()
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=20,
            padding=50,
            adaptive_height=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        open_button = MDRaisedButton(
            text="Open Recent Activity Modal",
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5},
            on_release=self.open_modal
        )
        layout.add_widget(open_button)

        close_test_button = MDRaisedButton(
            text="Test Close Function",
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5},
            on_release=self.test_close_function
        )
        layout.add_widget(close_test_button)

        screen.add_widget(layout)
        return screen

    def open_modal(self, instance):
        """Open the recent activity modal"""
        try:
            from app.views.recent_activity_modal import RecentActivityModalDialog
            from app.database import DatabaseManager

            print("Creating modal dialog...")

            # Create database manager
            db = DatabaseManager()

            # Create modal dialog
            self.modal_dialog = RecentActivityModalDialog(db)

            # Open the dialog
            self.modal_dialog.open()
            print("Modal dialog opened successfully")

        except Exception as e:
            print(f"Error opening modal: {e}")
            import traceback
            traceback.print_exc()

    def test_close_function(self, instance):
        """Test the close function directly"""
        if self.modal_dialog and self.modal_dialog.dialog:
            print("Testing close function...")
            try:
                self.modal_dialog._close_dialog(None)
                print("Close function executed successfully")
            except Exception as e:
                print(f"Error in close function: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("No modal dialog is open to close")

if __name__ == "__main__":
    print("🔍 Starting Modal Close Button Test App\n")
    print("Instructions:")
    print("1. Click 'Open Recent Activity Modal' to open the dialog")
    print("2. Try clicking the 'Close' button in the dialog")
    print("3. If that doesn't work, click 'Test Close Function' to test directly")
    print("4. Close this app when done testing\n")

    TestModalApp().run()
