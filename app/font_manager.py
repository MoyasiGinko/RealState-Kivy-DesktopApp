#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Font Management
Handles font loading and Arabic text support
"""

import os
import platform
import logging
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path

logger = logging.getLogger(__name__)


class FontManager:
    """Manages font loading and Arabic text support"""

    def __init__(self):
        self.system_fonts = self._get_system_fonts()
        self.arabic_font_loaded = False
        self.setup_fonts()

    def _get_system_fonts(self) -> dict:
        """Get available system fonts based on platform"""
        system = platform.system().lower()

        fonts = {
            'arabic': None,
            'arabic_bold': None,
            'default': None
        }

        if system == 'windows':
            # Windows system fonts
            windows_fonts = [
                'C:/Windows/Fonts/tahoma.ttf',
                'C:/Windows/Fonts/tahomabd.ttf',
                'C:/Windows/Fonts/arial.ttf',
                'C:/Windows/Fonts/arialbd.ttf',
                'C:/Windows/Fonts/calibri.ttf',
                'C:/Windows/Fonts/calibrib.ttf'
            ]

            for font_path in windows_fonts:
                if os.path.exists(font_path):
                    if 'tahoma' in font_path.lower():
                        if 'bd' in font_path.lower():
                            fonts['arabic_bold'] = font_path
                        else:
                            fonts['arabic'] = font_path
                    elif fonts['default'] is None:
                        fonts['default'] = font_path

        elif system == 'linux':
            # Linux system fonts
            linux_paths = [
                '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
                '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
            ]

            for font_path in linux_paths:
                if os.path.exists(font_path):
                    if 'Bold' in font_path:
                        fonts['arabic_bold'] = font_path
                    else:
                        fonts['arabic'] = font_path
                        fonts['default'] = font_path

        elif system == 'darwin':  # macOS
            # macOS system fonts
            macos_paths = [
                '/System/Library/Fonts/Helvetica.ttc',
                '/System/Library/Fonts/Arial.ttf',
                '/Library/Fonts/Arial.ttf'
            ]

            for font_path in macos_paths:
                if os.path.exists(font_path):
                    fonts['arabic'] = font_path
                    fonts['default'] = font_path
                    break

        return fonts

    def setup_fonts(self):
        """Setup and register fonts with Kivy"""
        try:
            # Register Arabic font if available
            arabic_font = self.system_fonts.get('arabic')
            if arabic_font and os.path.exists(arabic_font):
                LabelBase.register(
                    name='Arabic',
                    fn_regular=arabic_font,
                    fn_bold=self.system_fonts.get('arabic_bold', arabic_font)
                )
                self.arabic_font_loaded = True
                logger.info(f"Arabic font registered: {arabic_font}")
            else:
                # Fallback to default system font
                default_font = self.system_fonts.get('default')
                if default_font and os.path.exists(default_font):
                    LabelBase.register(
                        name='Arabic',
                        fn_regular=default_font
                    )
                    logger.warning(f"Using fallback font for Arabic: {default_font}")
                else:
                    logger.warning("No suitable font found for Arabic text")

        except Exception as e:
            logger.error(f"Error setting up fonts: {e}")

    def get_font_name(self, text: str = "", bold: bool = False) -> str:
        """Get appropriate font name for given text"""
        if self.has_arabic_text(text) or not text:
            return 'Arabic'
        return 'Roboto' if not bold else 'Roboto'

    def has_arabic_text(self, text: str) -> bool:
        """Check if text contains Arabic characters"""
        if not text:
            return True  # Default to Arabic font for empty text

        # Arabic Unicode ranges
        arabic_ranges = [
            (0x0600, 0x06FF),  # Arabic
            (0x0750, 0x077F),  # Arabic Supplement
            (0x08A0, 0x08FF),  # Arabic Extended-A
            (0xFB50, 0xFDFF),  # Arabic Presentation Forms-A
            (0xFE70, 0xFEFF),  # Arabic Presentation Forms-B
        ]

        for char in text:
            char_code = ord(char)
            for start, end in arabic_ranges:
                if start <= char_code <= end:
                    return True
        return False


# Global font manager instance
font_manager = FontManager()
