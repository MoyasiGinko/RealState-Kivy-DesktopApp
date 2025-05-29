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
            'primary_color': '0.2, 0.4, 0.8, 1',
            'success_color': '0.2, 0.7, 0.3, 1',
            'warning_color': '0.8, 0.5, 0.2, 1',
            'error_color': '0.7, 0.3, 0.2, 1'
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
        """Get color as list of floats"""
        color_str = self.get('ui', f'{color_name}_color', '0.2, 0.4, 0.8, 1')
        try:
            return [float(x.strip()) for x in color_str.split(',')]
        except:
            return [0.2, 0.4, 0.8, 1]

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


# Global configuration instance
config = Config()
