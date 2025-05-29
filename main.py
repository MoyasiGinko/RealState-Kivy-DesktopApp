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

# Import our modules
from config import config
from database import DatabaseManager
from font_manager import font_manager
from screens.dashboard import DashboardScreen
from screens.owners import OwnersScreen
from screens.properties import PropertiesScreen
from screens.search import SearchScreen
from components import RTLLabel

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
Window.minimum_width, Window.minimum_height = config.min_window_size


class MainMenuScreen(Screen):
    """Main menu screen with navigation buttons"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'menu'

        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Title
        title = RTLLabel(
            text=config.app_title,
            font_size='32sp',
            size_hint_y=None,
            height='80dp',
            color=config.get_color('primary')
        )
        main_layout.add_widget(title)

        # Menu buttons layout
        buttons_layout = GridLayout(cols=2, spacing=20, size_hint_y=None, height='400dp')

        # Dashboard button
        dashboard_btn = Button(
            text='لوحة التحكم\nDashboard',
            font_size='18sp',
            background_color=config.get_color('primary'),
            font_name=font_manager.get_font_name('لوحة التحكم\nDashboard')
        )
        dashboard_btn.bind(on_press=lambda x: self.goto_screen('dashboard'))
        buttons_layout.add_widget(dashboard_btn)

        # Owners button
        owners_btn = Button(
            text='إدارة الملاك\nOwners Management',
            font_size='18sp',
            background_color=config.get_color('success'),
            font_name=font_manager.get_font_name('إدارة الملاك\nOwners Management')
        )
        owners_btn.bind(on_press=lambda x: self.goto_screen('owners'))
        buttons_layout.add_widget(owners_btn)

        # Properties button
        properties_btn = Button(
            text='إدارة العقارات\nProperties Management',
            font_size='18sp',
            background_color=config.get_color('warning'),
            font_name=font_manager.get_font_name('إدارة العقارات\nProperties Management')
        )
        properties_btn.bind(on_press=lambda x: self.goto_screen('properties'))
        buttons_layout.add_widget(properties_btn)

        # Search/Reports button
        search_btn = Button(
            text='البحث والتقارير\nSearch & Reports',
            font_size='18sp',
            background_color=config.get_color('error'),
            font_name=font_manager.get_font_name('البحث والتقارير\nSearch & Reports')
        )
        search_btn.bind(on_press=lambda x: self.goto_screen('search'))
        buttons_layout.add_widget(search_btn)

        main_layout.add_widget(buttons_layout)

        # Footer
        footer = RTLLabel(
            text=f'نسخة {config.get("application", "version", "1.0.0")} - تطوير {config.get("application", "author", "Luay Alkawaz")}',
            font_size='14sp',
            size_hint_y=None,
            height='40dp',
            color=[0.5, 0.5, 0.5, 1]
        )
        main_layout.add_widget(footer)

        self.add_widget(main_layout)

    def goto_screen(self, screen_name):
        """Navigate to specified screen"""
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = screen_name


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

            # Start with main menu
            self.screen_manager.current = 'menu'

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
            # Main menu
            menu_screen = MainMenuScreen()
            self.screen_manager.add_widget(menu_screen)

            # Dashboard
            dashboard_screen = DashboardScreen(db_manager=self.db, name='dashboard')
            self.screen_manager.add_widget(dashboard_screen)

            # Owners management
            owners_screen = OwnersScreen(db_manager=self.db, name='owners')
            self.screen_manager.add_widget(owners_screen)

            # Properties management
            properties_screen = PropertiesScreen(db_manager=self.db, name='properties')
            self.screen_manager.add_widget(properties_screen)

            # Search and reports
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
        """Return to main menu"""
        if self.screen_manager:
            self.screen_manager.transition = SlideTransition(direction='right')
            self.screen_manager.current = 'menu'

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
