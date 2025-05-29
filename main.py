#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Main Application Entry Point
A comprehensive desktop application for managing real estate properties with bilingual support
Author: Luay Alkawaz
Version: 1.0.0
"""

import os
import sys
import logging
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / 'app'
sys.path.insert(0, str(app_dir))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.widget import Widget

# Import our modules
from config import config
from database import DatabaseManager
from font_manager import font_manager
from language_manager import language_manager
from screens.dashboard import DashboardScreen
from screens.owners import OwnersScreen
from screens.properties import PropertiesScreen
from screens.search import SearchScreen
from components import RTLLabel, BilingualLabel, BilingualButton, LanguageSwitcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Set window properties from config
Window.size = config.window_size
# Ensure minimum size is always > 0
min_width, min_height = config.min_window_size
if min_width <= 0:
    min_width = 800
if min_height <= 0:
    min_height = 600
Window.minimum_width, Window.minimum_height = min_width, min_height


class WelcomeScreen(Screen):
    """Welcome screen with application information and language selection"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'welcome'

        # Main layout with elegant design
        main_layout = BoxLayout(orientation='vertical', padding=[50, 40, 50, 30], spacing=40)

        # Header with logo and title
        header_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(200), spacing=20)

        # Logo centered
        logo_box = BoxLayout(size_hint_y=None, height=dp(120))
        logo = Image(
            source='app-images/alkawaz-logo.jpg',
            size_hint=(None, None),
            size=(dp(120), dp(120)),
            pos_hint={'center_x': 0.5}
        )
        logo_box.add_widget(logo)
        header_layout.add_widget(logo_box)

        # Application title
        title = BilingualLabel(
            translation_key='app_title',
            font_size='42sp',
            bold=True,
            color=config.get_color('primary'),
            halign='center',
            size_hint_y=None,
            height=dp(60)
        )
        header_layout.add_widget(title)
        main_layout.add_widget(header_layout)

        # Language selection section
        lang_section = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120), spacing=15)
        lang_label = BilingualLabel(
            translation_key='switch_language',
            font_size='18sp',
            halign='center',
            color=[0.3, 0.3, 0.3, 1],
            size_hint_y=None,
            height=dp(30)
        )
        lang_section.add_widget(lang_label)

        # Language switcher
        lang_switcher = LanguageSwitcher(size_hint=(None, None), size=(dp(200), dp(50)), pos_hint={'center_x': 0.5})
        lang_section.add_widget(lang_switcher)
        main_layout.add_widget(lang_section)

        # Welcome information
        info_section = BoxLayout(orientation='vertical', spacing=20)

        # Description
        description = BilingualLabel(
            translation_key='app_description',
            font_size='16sp',
            halign='center',
            color=[0.4, 0.4, 0.4, 1],
            size_hint_y=None,
            height=dp(80)
        )
        info_section.add_widget(description)

        # Features list
        features_text = BilingualLabel(
            translation_key='app_features',
            font_size='14sp',
            halign='center',
            color=[0.5, 0.5, 0.5, 1],
            size_hint_y=None,
            height=dp(120)
        )
        info_section.add_widget(features_text)
        main_layout.add_widget(info_section)

        # Enter button
        enter_btn = BilingualButton(
            translation_key='enter_dashboard',
            background_color=config.get_color('primary'),
            font_size='24sp',
            size_hint=(None, None),
            size=(dp(300), dp(60)),
            pos_hint={'center_x': 0.5}
        )
        enter_btn.bind(on_press=self.enter_dashboard)
        main_layout.add_widget(enter_btn)

        # Footer
        footer = BilingualLabel(
            translation_key='app_footer',
            font_size='12sp',
            color=[0.6, 0.6, 0.6, 1],
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        main_layout.add_widget(footer)

        self.add_widget(main_layout)

    def enter_dashboard(self, instance):
        """Navigate to dashboard"""
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'dashboard'


class RealEstateApp(App):
    """Main application class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = config.app_title
        self.db = None
        self.screen_manager = None

    def build(self):
        """Build the application"""
        try:
            # Initialize database
            self.setup_directories()
            self.db = DatabaseManager(config.db_file)
            logger.info("Database initialized successfully")

            # Create screen manager
            self.screen_manager = ScreenManager()

            # Add screens
            self.add_screens()

            # Start with welcome screen
            self.screen_manager.current = 'welcome'

            logger.info("Application started successfully")
            return self.screen_manager

        except Exception as e:
            logger.error(f"Error building application: {e}")
            # Return a simple error screen
            error_layout = BoxLayout(orientation='vertical', padding=20)
            error_label = Label(
                text=f'خطأ في تشغيل التطبيق:\n{str(e)}',
                font_size='18sp',
                color=[1, 0, 0, 1]
            )
            error_layout.add_widget(error_label)
            return error_layout

    def setup_directories(self):
        """Create necessary directories"""
        directories = [
            config.photos_dir,
            config.backup_dir,
            os.path.join(config.photos_dir, 'thumbnails')
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Directory created/verified: {directory}")

    def add_screens(self):
        """Add all screens to the screen manager"""
        try:
            # Welcome screen (entry point)
            welcome_screen = WelcomeScreen()
            self.screen_manager.add_widget(welcome_screen)

            # Dashboard (main hub)
            dashboard_screen = DashboardScreen(db_manager=self.db, name='dashboard')
            self.screen_manager.add_widget(dashboard_screen)

            # Feature screens
            owners_screen = OwnersScreen(db_manager=self.db, name='owners')
            self.screen_manager.add_widget(owners_screen)

            properties_screen = PropertiesScreen(db_manager=self.db, name='properties')
            self.screen_manager.add_widget(properties_screen)

            search_screen = SearchScreen(db_manager=self.db, name='search')
            self.screen_manager.add_widget(search_screen)

            logger.info("All screens added successfully")

        except Exception as e:
            logger.error(f"Error adding screens: {e}")
            raise

    def get_running_app(self):
        """Get the running application instance"""
        return self

    def goto_main_menu(self):
        """Return to welcome screen"""
        if self.screen_manager:
            self.screen_manager.transition = SlideTransition(direction='right')
            self.screen_manager.current = 'welcome'

    def goto_dashboard(self):
        """Navigate to dashboard screen"""
        if self.screen_manager:
            self.screen_manager.transition = SlideTransition(direction='right')
            self.screen_manager.current = 'dashboard'

    def on_stop(self):
        """Called when the application is stopped"""
        logger.info("Application stopped")
        if self.db:
            self.db.close_connection()


def main():
    """Main entry point"""
    try:
        # Check if Kivy is available
        try:
            import kivy
            logger.info(f"Kivy version: {kivy.__version__}")
        except ImportError:
            print("Error: Kivy is not installed. Please run: pip install kivy")
            return 1

        # Create and run the application
        app = RealEstateApp()
        app.run()
        return 0

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
