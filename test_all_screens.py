#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive test script for Real Estate Management System
Tests all screens and language switching functionality
"""

import sys
import os
import time
import logging

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import Kivy modules
import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window

# Import app modules
from app.database import DatabaseManager
from app.language_manager import language_manager
from app.font_manager import font_manager
from app.config import config

# Import screens
from app.screens.dashboard import DashboardScreen
from app.screens.owners import OwnersScreen
from app.screens.properties import PropertiesScreen
from app.screens.search import SearchScreen

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestRealEstateApp(App):
    """Test application to verify all screens work correctly"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Real Estate Management System - Test"
        self.test_phase = 0
        self.test_results = []

    def build(self):
        """Build the application"""
        try:
            # Initialize database
            self.db_manager = DatabaseManager()
            self.db_manager.init_database()
            logger.info("Database initialized successfully")

            # Initialize screen manager
            self.screen_manager = ScreenManager()

            # Create and add all screens
            self.dashboard_screen = DashboardScreen(self.db_manager)
            self.owners_screen = OwnersScreen(self.db_manager)
            self.properties_screen = PropertiesScreen(self.db_manager)
            self.search_screen = SearchScreen(self.db_manager)

            self.screen_manager.add_widget(self.dashboard_screen)
            self.screen_manager.add_widget(self.owners_screen)
            self.screen_manager.add_widget(self.properties_screen)
            self.screen_manager.add_widget(self.search_screen)

            # Start with dashboard
            self.screen_manager.current = 'dashboard'

            # Schedule comprehensive tests
            Clock.schedule_once(self.start_tests, 2)

            return self.screen_manager

        except Exception as e:
            logger.error(f"Failed to build app: {e}")
            return None

    def start_tests(self, dt):
        """Start comprehensive testing"""
        logger.info("=== Starting Comprehensive Screen Tests ===")
        self.test_phase = 1
        Clock.schedule_once(self.run_next_test, 1)

    def run_next_test(self, dt):
        """Run the next test phase"""
        try:
            if self.test_phase == 1:
                self.test_dashboard_screen()
            elif self.test_phase == 2:
                self.test_owners_screen()
            elif self.test_phase == 3:
                self.test_properties_screen()
            elif self.test_phase == 4:
                self.test_search_screen()
            elif self.test_phase == 5:
                self.test_language_switching()
            elif self.test_phase == 6:
                self.test_navigation_flow()
            else:
                self.finish_tests()
                return

            self.test_phase += 1
            if self.test_phase <= 6:
                Clock.schedule_once(self.run_next_test, 2)

        except Exception as e:
            logger.error(f"Test phase {self.test_phase} failed: {e}")
            self.test_results.append(f"❌ Phase {self.test_phase}: {e}")
            self.test_phase += 1
            if self.test_phase <= 6:
                Clock.schedule_once(self.run_next_test, 2)

    def test_dashboard_screen(self):
        """Test dashboard screen"""
        logger.info("Testing Dashboard Screen...")
        self.screen_manager.current = 'dashboard'

        # Check if screen loads properly
        current_screen = self.screen_manager.current_screen
        if current_screen.name == 'dashboard':
            self.test_results.append("✅ Dashboard screen loads correctly")
            logger.info("Dashboard screen test passed")
        else:
            self.test_results.append("❌ Dashboard screen failed to load")

    def test_owners_screen(self):
        """Test owners screen"""
        logger.info("Testing Owners Screen...")
        self.screen_manager.current = 'owners'

        # Check if screen loads properly
        current_screen = self.screen_manager.current_screen
        if current_screen.name == 'owners':
            self.test_results.append("✅ Owners screen loads correctly")
            logger.info("Owners screen test passed")
        else:
            self.test_results.append("❌ Owners screen failed to load")

    def test_properties_screen(self):
        """Test properties screen"""
        logger.info("Testing Properties Screen...")
        self.screen_manager.current = 'properties'

        # Check if screen loads properly
        current_screen = self.screen_manager.current_screen
        if current_screen.name == 'properties':
            self.test_results.append("✅ Properties screen loads correctly")
            logger.info("Properties screen test passed")
        else:
            self.test_results.append("❌ Properties screen failed to load")

    def test_search_screen(self):
        """Test search screen"""
        logger.info("Testing Search Screen...")
        self.screen_manager.current = 'search'

        # Check if screen loads properly
        current_screen = self.screen_manager.current_screen
        if current_screen.name == 'search':
            self.test_results.append("✅ Search screen loads correctly")
            logger.info("Search screen test passed")
        else:
            self.test_results.append("❌ Search screen failed to load")

    def test_language_switching(self):
        """Test language switching functionality"""
        logger.info("Testing Language Switching...")

        try:
            # Test switching to English
            original_lang = language_manager.current_language
            language_manager.set_language('en')
            if language_manager.current_language == 'en':
                self.test_results.append("✅ Language switch to English works")
            else:
                self.test_results.append("❌ Language switch to English failed")

            # Test switching to Arabic
            language_manager.set_language('ar')
            if language_manager.current_language == 'ar':
                self.test_results.append("✅ Language switch to Arabic works")
            else:
                self.test_results.append("❌ Language switch to Arabic failed")

            # Test text retrieval
            test_text = language_manager.get_text('dashboard')
            if test_text:
                self.test_results.append("✅ Text retrieval works")
            else:
                self.test_results.append("❌ Text retrieval failed")

            # Restore original language
            language_manager.set_language(original_lang)
            logger.info("Language switching test completed")

        except Exception as e:
            self.test_results.append(f"❌ Language switching error: {e}")

    def test_navigation_flow(self):
        """Test navigation between screens"""
        logger.info("Testing Navigation Flow...")

        try:
            # Test navigation sequence: dashboard -> owners -> properties -> search -> dashboard
            screens = ['dashboard', 'owners', 'properties', 'search', 'dashboard']

            for screen_name in screens:
                self.screen_manager.current = screen_name
                time.sleep(0.1)  # Small delay

                if self.screen_manager.current_screen.name == screen_name:
                    continue
                else:
                    self.test_results.append(f"❌ Navigation to {screen_name} failed")
                    return

            self.test_results.append("✅ Navigation flow works correctly")
            logger.info("Navigation flow test passed")

        except Exception as e:
            self.test_results.append(f"❌ Navigation flow error: {e}")

    def finish_tests(self):
        """Finish testing and display results"""
        logger.info("=== Test Results ===")
        for result in self.test_results:
            logger.info(result)

        # Count passed/failed tests
        passed = len([r for r in self.test_results if r.startswith("✅")])
        failed = len([r for r in self.test_results if r.startswith("❌")])

        logger.info(f"=== Summary: {passed} passed, {failed} failed ===")

        if failed == 0:
            logger.info("🎉 ALL TESTS PASSED! Application is working correctly with pure language separation.")
        else:
            logger.warning(f"⚠️  {failed} tests failed. Check the logs above for details.")

    def goto_dashboard(self):
        """Navigate to dashboard - compatibility method"""
        self.screen_manager.current = 'dashboard'

    def goto_owners(self):
        """Navigate to owners screen"""
        self.screen_manager.current = 'owners'

    def goto_properties(self):
        """Navigate to properties screen"""
        self.screen_manager.current = 'properties'

    def goto_search(self):
        """Navigate to search screen"""
        self.screen_manager.current = 'search'

if __name__ == '__main__':
    try:
        # Set window properties
        Window.size = (1200, 800)

        # Run the test app
        TestRealEstateApp().run()

    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        sys.exit(1)
