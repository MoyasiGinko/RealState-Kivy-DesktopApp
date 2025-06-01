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

# Set Kivy configuration before importing other Kivy modules
from kivy.config import Config

# Import our config first
from app.config import config

# Set minimum window size using our config
Config.set('graphics', 'minimum_width', str(max(100, config.min_width)))
Config.set('graphics', 'minimum_height', str(max(100, config.min_height)))
Config.set('graphics', 'width', str(config.window_width))
Config.set('graphics', 'height', str(config.window_height))

# Now import other kivy modules
from kivy.app import App
from kivymd.app import MDApp
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
from app.database import DatabaseManager
from app.font_manager import font_manager
from app.language_manager import language_manager
from app.views.enhanced_search import EnhancedSearchScreen
from app.utils import RTLLabel, BilingualLabel, BilingualButton, LanguageSwitcher
from app.controllers.app_controller import AppController

# Import enhanced components
from app.views.enhanced_dashboard import EnhancedDashboardScreen
from app.views.enhanced_owners import EnhancedOwnersScreen
from app.views.enhanced_properties import EnhancedPropertiesScreen

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


class WelcomeScreen(Screen):
    """Modern welcome screen with elegant animation and design"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'welcome'

        # Main layout with modern gradient background
        main_layout = BoxLayout(orientation='vertical', padding=[60, 50, 60, 40], spacing=50)

        # Add gradient background
        with main_layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.05, 0.1, 0.2, 1)  # Dark blue gradient start
            Rectangle(size=(2000, 2000), pos=(0, 0))

        # Hero section with logo and title
        hero_section = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(280), spacing=30)

        # Logo with glow effect
        logo_container = BoxLayout(size_hint_y=None, height=dp(150), padding=[0, 20])
        logo = Image(
            source='app-images/alkawaz-logo.jpg',
            size_hint=(None, None),
            size=(dp(150), dp(150)),
            pos_hint={'center_x': 0.5}
        )
        logo_container.add_widget(logo)
        hero_section.add_widget(logo_container)

        # Main title with enhanced styling
        title = BilingualLabel(
            translation_key='app_title',
            font_size='48sp',
            bold=True,
            color=[1, 1, 1, 1],  # White text
            halign='center',
            size_hint_y=None,
            height=dp(70)
        )
        hero_section.add_widget(title)

        # Subtitle
        subtitle = BilingualLabel(
            translation_key='app_subtitle',
            font_size='20sp',
            color=[0.8, 0.9, 1, 1],  # Light blue
            halign='center',
            size_hint_y=None,
            height=dp(40)
        )
        hero_section.add_widget(subtitle)

        main_layout.add_widget(hero_section)

        # Features section with cards
        features_section = BoxLayout(orientation='vertical', spacing=25)

        # Language selection with modern design
        lang_section = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(100), spacing=15)
        lang_label = BilingualLabel(
            translation_key='select_language',
            font_size='18sp',
            halign='center',
            color=[0.9, 0.9, 0.9, 1],
            size_hint_y=None,
            height=dp(30)
        )
        lang_section.add_widget(lang_label)

        # Enhanced language switcher
        lang_switcher = LanguageSwitcher(
            size_hint=(None, None),
            size=(dp(250), dp(50)),
            pos_hint={'center_x': 0.5}
        )
        lang_section.add_widget(lang_switcher)
        features_section.add_widget(lang_section)

        # Description with better typography
        description = BilingualLabel(
            translation_key='app_description',
            font_size='16sp',
            halign='center',
            color=[0.7, 0.8, 0.9, 1],
            size_hint_y=None,
            height=dp(80)
        )
        features_section.add_widget(description)

        main_layout.add_widget(features_section)

        # Action section with animated enter button
        action_section = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120), spacing=20)

        # Enhanced enter button with gradient effect
        enter_btn = BilingualButton(
            translation_key='enter_dashboard',
            background_color=[0.2, 0.6, 1, 1],  # Blue gradient
            font_size='28sp',
            size_hint=(None, None),
            size=(dp(350), dp(70)),
            pos_hint={'center_x': 0.5}
        )
        enter_btn.bind(on_press=self.enter_dashboard)
        action_section.add_widget(enter_btn)

        # Footer with version info
        footer = BilingualLabel(
            translation_key='app_footer',
            font_size='12sp',
            color=[0.5, 0.6, 0.7, 1],
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        action_section.add_widget(footer)

        main_layout.add_widget(action_section)

        self.add_widget(main_layout)

        # Add entrance animation
        self.animate_entrance()

    def animate_entrance(self):
        """Add subtle entrance animation"""
        from kivy.animation import Animation
        # Fade in effect
        self.opacity = 0
        anim = Animation(opacity=1, duration=1.5)
        anim.start(self)

    def enter_dashboard(self, instance):
        """Navigate to enhanced dashboard with smooth transition"""
        self.manager.transition = SlideTransition(direction='left', duration=0.4)
        self.manager.current = 'enhanced_dashboard'


class RealEstateApp(MDApp):
    """Main application class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = config.app_title
        self.db = None
        self.screen_manager = None
        self.app_controller = None

    def build(self):
        """Build the application"""
        try:
            # Initialize database
            self.setup_directories()
            self.db = DatabaseManager(config.db_file)
            logger.info("Database initialized successfully")

            # Initialize MVC architecture
            self.app_controller = AppController(self.db)

            # Create screen manager
            self.screen_manager = ScreenManager()
            self.app_controller.set_screen_manager(self.screen_manager)

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

            # Enhanced Dashboard (main hub) - Use enhanced version as primary
            enhanced_dashboard = EnhancedDashboardScreen(self.db, name='enhanced_dashboard')
            self.screen_manager.add_widget(enhanced_dashboard)            # Feature screens - controllers will be set up when navigating
            enhanced_owners = EnhancedOwnersScreen(self.db, name='enhanced_owners')
            self.screen_manager.add_widget(enhanced_owners)

            # Enhanced properties screen with modern components
            enhanced_properties_screen = EnhancedPropertiesScreen(self.db, name='enhanced_properties')
            self.screen_manager.add_widget(enhanced_properties_screen)

            search_screen = EnhancedSearchScreen(self.db, name='enhanced_search')
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
        """Navigate to enhanced dashboard screen"""
        if self.screen_manager:
            self.screen_manager.transition = SlideTransition(direction='right')
            self.screen_manager.current = 'enhanced_dashboard'

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
