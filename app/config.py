#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Configuration Module
Handles application configuration and settings
"""

import configparser
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class Config:
    """Application configuration manager"""

    def __init__(self, config_file: str = "config.ini"):
        """Initialize configuration"""
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                self.config.read(self.config_file, encoding='utf-8')
                logger.info(f"Configuration loaded from {self.config_file}")
            else:
                self.create_default_config()
                logger.info("Default configuration created")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self.create_default_config()

    def create_default_config(self):
        """Create default configuration file"""
        self.config['database'] = {
            'db_file': 'userdesktop-rs-database.db',
            'backup_dir': 'backups',
            'photos_dir': 'property_photos'
        }

        self.config['application'] = {
            'title': 'نظام إدارة العقارات - Real Estate Management System',
            'version': '1.0.0',
            'author': 'Luay Alkawaz',
            'window_width': '1200',
            'window_height': '800',
            'min_width': '1000',
            'min_height': '700'
        }

        self.config['ui'] = {
            'font_size_large': '24',
            'font_size_medium': '18',
            'font_size_small': '14',
            # Theme is now managed by theme_manager
            'current_theme': 'light',  # Default theme
        }

        self.config['fonts'] = {
            'arabic_font': 'fonts/NotoSansArabic-Regular.ttf',
            'arabic_bold_font': 'fonts/NotoSansArabic-Bold.ttf',
            'default_font': 'Roboto',
            'fallback_font': 'DejaVuSans'
        }

        self.save_config()

    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
            logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")

    def get(self, section: str, key: str, fallback: Any = None) -> str:
        """Get configuration value"""
        try:
            return self.config.get(section, key, fallback=fallback)
        except Exception:
            return fallback

    def getint(self, section: str, key: str, fallback: int = 0) -> int:
        """Get integer configuration value"""
        try:
            return self.config.getint(section, key, fallback=fallback)
        except Exception:
            return fallback

    def getfloat(self, section: str, key: str, fallback: float = 0.0) -> float:
        """Get float configuration value"""
        try:
            return self.config.getfloat(section, key, fallback=fallback)
        except Exception:
            return fallback

    def getboolean(self, section: str, key: str, fallback: bool = False) -> bool:
        """Get boolean configuration value"""
        try:
            return self.config.getboolean(section, key, fallback=fallback)
        except Exception:
            return fallback

    def set(self, section: str, key: str, value: str):
        """Set configuration value"""
        try:
            if not self.config.has_section(section):
                self.config.add_section(section)
            self.config.set(section, key, str(value))
            self.save_config()
        except Exception as e:
            logger.error(f"Error setting configuration: {e}")

    # Convenience methods for common settings
    @property
    def db_file(self) -> str:
        """Get database file path"""
        return self.get('database', 'db_file', 'userdesktop-rs-database.db')

    @property
    def photos_dir(self) -> str:
        """Get photos directory"""
        return self.get('database', 'photos_dir', 'property_photos')

    @property
    def backup_dir(self) -> str:
        """Get backup directory"""
        return self.get('database', 'backup_dir', 'backups')

    @property
    def app_title(self) -> str:
        """Get application title"""
        return self.get('application', 'title', 'Real Estate Management System')

    @property
    def window_size(self) -> tuple:
        """Get window size"""
        width = self.getint('application', 'window_width', 1200)
        height = self.getint('application', 'window_height', 800)
        return (width, height)

    @property
    def min_window_size(self) -> tuple:
        """Get minimum window size"""
        width = self.getint('application', 'min_width', 1000)
        height = self.getint('application', 'min_height', 700)
        return (width, height)

    def get_color(self, color_name: str) -> list:
        """Get color as list of floats from theme manager"""
        # Import here to avoid circular import
        from app.theme_manager import theme_manager
        return theme_manager.get_color(color_name)

    def get_font_name(self, font_type: str = 'default') -> str:
        """Get font name based on type"""
        font_map = {
            'arabic': self.get('fonts', 'arabic_font', 'fonts/NotoSansArabic-Regular.ttf'),
            'arabic_bold': self.get('fonts', 'arabic_bold_font', 'fonts/NotoSansArabic-Bold.ttf'),
            'default': self.get('fonts', 'default_font', 'Roboto'),
            'fallback': self.get('fonts', 'fallback_font', 'DejaVuSans')
        }
        return font_map.get(font_type, font_map['default'])

    def has_arabic_text(self, text: str) -> bool:
        """Check if text contains Arabic characters"""
        if not text:
            return False
        arabic_range = range(0x0600, 0x06FF)  # Arabic Unicode range
        return any(ord(char) in arabic_range for char in text)

    def set_theme(self, theme_name: str):
        """Set the current theme"""
        from app.theme_manager import theme_manager, ThemeType
        try:
            # Convert string to ThemeType enum
            theme_type = ThemeType(theme_name.lower())
            theme_manager.set_theme(theme_type)
            self.set('ui', 'current_theme', theme_name.lower())
        except ValueError:
            logger.error(f"Invalid theme name: {theme_name}")

    def get_theme(self) -> str:
        """Get current theme name"""
        return self.get('ui', 'current_theme', 'light')

    def get_button_style(self, button_type: str = 'primary') -> Dict[str, Any]:
        """Get button style from theme manager"""
        from app.theme_manager import theme_manager
        return theme_manager.get_button_style(button_type)

    def get_input_style(self) -> Dict[str, Any]:
        """Get input style from theme manager"""
        from app.theme_manager import theme_manager
        return theme_manager.get_input_style()

    def get_label_style(self, label_type: str = 'normal') -> Dict[str, Any]:
        """Get label style from theme manager"""
        from app.theme_manager import theme_manager
        return theme_manager.get_label_style(label_type)

    def get_card_style(self) -> Dict[str, Any]:
        """Get card style from theme manager"""
        from app.theme_manager import theme_manager
        return theme_manager.get_card_style()

    def get_table_style(self) -> Dict[str, Any]:
        """Get table style from theme manager"""
        from app.theme_manager import theme_manager
        return theme_manager.get_table_style()


# Global configuration instance
config = Config()
