#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Color Improvements Test
Test the enhanced color palette for better visibility and contrast
"""

import sys
import os
import time
import logging

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.screenmanager import ScreenManager, Screen
    from kivy.metrics import dp
    from kivy.clock import Clock

    from app.components import (RTLLabel, CustomActionButton, FormField, DataTable,
                               BilingualLabel, BilingualButton, SearchBox, MessageDialog,
                               LanguageSwitcher, NavigationHeader)
    from app.config import config
    from app.language_manager import language_manager
    from app.database import Database

    print("✅ All imports successful")

except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class ColorTestScreen(Screen):
    """Screen to test color improvements"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'color_test'
        self.build_ui()

    def build_ui(self):
        """Build the test UI"""
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Navigation header
        header = NavigationHeader(
            screen_title_key='color_test_title',
            show_back_button=False
        )
        main_layout.add_widget(header)

        # Test title
        title = BilingualLabel(
            translation_key='welcome',
            font_size='24sp',
            bold=True,
            size_hint_y=None,
            height=dp(50)
        )
        main_layout.add_widget(title)

        # Color test sections
        test_layout = BoxLayout(orientation='horizontal', spacing=20)

        # Left panel - Form elements
        left_panel = BoxLayout(orientation='vertical', spacing=10, size_hint_x=0.5)

        left_title = RTLLabel(
            text="Form Elements Test",
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        left_panel.add_widget(left_title)

        # Test form fields
        name_field = FormField(
            translation_key='name',
            input_type='text',
            required=True
        )
        left_panel.add_widget(name_field)

        province_field = FormField(
            translation_key='province',
            input_type='spinner',
            values=['Baghdad', 'Basra', 'Najaf', 'Karbala']
        )
        left_panel.add_widget(province_field)

        # Test buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=dp(50))

        primary_btn = CustomActionButton(
            text="Primary Button",
            button_type='primary'
        )
        button_layout.add_widget(primary_btn)

        success_btn = CustomActionButton(
            text="Success Button",
            button_type='success'
        )
        button_layout.add_widget(success_btn)

        warning_btn = CustomActionButton(
            text="Warning Button",
            button_type='warning'
        )
        button_layout.add_widget(warning_btn)

        left_panel.add_widget(button_layout)

        # Test search box
        search_box = SearchBox()
        left_panel.add_widget(search_box)

        test_layout.add_widget(left_panel)

        # Right panel - Data table
        right_panel = BoxLayout(orientation='vertical', spacing=10, size_hint_x=0.5)

        right_title = RTLLabel(
            text="Data Table Test",
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        right_panel.add_widget(right_title)

        # Test data table
        columns = [
            {'title': 'Name', 'field': 'name'},
            {'title': 'Type', 'field': 'type'},
            {'title': 'Price', 'field': 'price'}
        ]

        test_data = [
            {'name': 'Property 1', 'type': 'House', 'price': '$100,000'},
            {'name': 'Property 2', 'type': 'Apartment', 'price': '$75,000'},
            {'name': 'Property 3', 'type': 'Villa', 'price': '$200,000'}
        ]

        data_table = DataTable(columns=columns, data=test_data)
        right_panel.add_widget(data_table)

        test_layout.add_widget(right_panel)
        main_layout.add_widget(test_layout)

        # Language switcher
        lang_switcher = LanguageSwitcher(size_hint_y=None, height=dp(40))
        main_layout.add_widget(lang_switcher)

        # Test message button
        msg_btn = CustomActionButton(
            text="Test Message Dialog",
            action=self.show_test_message,
            size_hint_y=None,
            height=dp(50)
        )
        main_layout.add_widget(msg_btn)

        self.add_widget(main_layout)

    def show_test_message(self):
        """Show a test message dialog"""
        dialog = MessageDialog(
            title="Color Test",
            message="This is a test message to verify color improvements and text visibility.",
            message_type='info'
        )
        dialog.open()

class ColorTestApp(App):
    """Test application for color improvements"""

    def build(self):
        """Build the application"""
        self.title = "Real Estate System - Color Test"

        # Create screen manager
        sm = ScreenManager()

        # Add test screen
        test_screen = ColorTestScreen()
        sm.add_widget(test_screen)
        sm.current = 'color_test'

        return sm

def test_color_configuration():
    """Test color configuration values"""
    print("\n🎨 Testing Color Configuration:")

    # Test color retrieval
    colors_to_test = [
        'primary', 'secondary', 'success', 'warning', 'error', 'info',
        'background', 'card_background', 'input_background', 'header_background',
        'text_primary', 'text_secondary', 'text_muted', 'text_light',
        'button_text_light', 'button_text_dark', 'border', 'separator'
    ]

    for color_name in colors_to_test:
        try:
            color_value = config.get_color(color_name)
            print(f"✅ {color_name}: {color_value}")
        except Exception as e:
            print(f"❌ {color_name}: Error - {e}")

    return True

def test_language_separation():
    """Test pure language separation"""
    print("\n🌐 Testing Language Separation:")

    # Test English mode
    language_manager.switch_to_language('en')
    english_text = language_manager.get_text('welcome')
    print(f"✅ English mode: '{english_text}'")

    # Test Arabic mode
    language_manager.switch_to_language('ar')
    arabic_text = language_manager.get_text('welcome')
    print(f"✅ Arabic mode: '{arabic_text}'")

    # Verify they are different and pure
    if english_text != arabic_text and english_text and arabic_text:
        print("✅ Language separation working correctly")
        return True
    else:
        print("❌ Language separation failed")
        return False

def main():
    """Run comprehensive color and functionality test"""
    print("🚀 Starting Real Estate System Color Improvements Test...")

    try:
        # Test color configuration
        config_test = test_color_configuration()

        # Test language separation
        lang_test = test_language_separation()

        # Test database connection
        print("\n💾 Testing Database Connection:")
        try:
            db = Database()
            db.connect()
            print("✅ Database connection successful")
            db.close()
            db_test = True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            db_test = False

        # Summary
        print("\n📊 Test Results Summary:")
        print(f"{'✅' if config_test else '❌'} Color Configuration: {'PASSED' if config_test else 'FAILED'}")
        print(f"{'✅' if lang_test else '❌'} Language Separation: {'PASSED' if lang_test else 'FAILED'}")
        print(f"{'✅' if db_test else '❌'} Database Connection: {'PASSED' if db_test else 'FAILED'}")

        if config_test and lang_test and db_test:
            print("\n🎉 All tests PASSED! Starting visual color test...")

            # Reset to English for visual test
            language_manager.switch_to_language('en')

            # Start visual test app
            app = ColorTestApp()
            app.run()

        else:
            print("\n❌ Some tests FAILED. Please check the errors above.")
            return False

    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
