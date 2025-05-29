#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Theme Manager
Centralized theme and color management for the entire application
"""

from typing import Dict, List, Any, Optional
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class ThemeType(Enum):
    """Available theme types"""
    LIGHT = "light"
    DARK = "dark"
    BLUE = "blue"
    GREEN = "green"
    ORANGE = "orange"
    PURPLE = "purple"
    PROFESSIONAL = "professional"
    MODERN = "modern"


class ThemeManager:
    """Centralized theme and color management system"""

    def __init__(self):
        """Initialize theme manager with default theme"""
        self.current_theme = ThemeType.LIGHT
        self.custom_colors = {}
        self.observers = []

        # Initialize all theme definitions
        self._init_themes()

    def _init_themes(self):
        """Initialize all available themes"""
        self.themes = {
            ThemeType.LIGHT: self._get_light_theme(),
            ThemeType.DARK: self._get_dark_theme(),
            ThemeType.BLUE: self._get_blue_theme(),
            ThemeType.GREEN: self._get_green_theme(),
            ThemeType.ORANGE: self._get_orange_theme(),
            ThemeType.PURPLE: self._get_purple_theme(),
            ThemeType.PROFESSIONAL: self._get_professional_theme(),
            ThemeType.MODERN: self._get_modern_theme(),
        }

    def _get_light_theme(self) -> Dict[str, Any]:
        """Light theme configuration"""
        return {
            # Primary Brand Colors
            'primary_color': [0.15, 0.35, 0.7, 1],      # Deep blue
            'secondary_color': [0.25, 0.25, 0.25, 1],   # Dark gray
            'accent_color': [0.9, 0.6, 0.2, 1],         # Orange accent

            # Status Colors
            'success_color': [0.15, 0.6, 0.25, 1],      # Green
            'warning_color': [0.9, 0.6, 0.1, 1],        # Amber
            'error_color': [0.8, 0.2, 0.2, 1],          # Red
            'info_color': [0.2, 0.5, 0.8, 1],           # Blue

            # Background Colors
            'background_color': [0.98, 0.98, 0.98, 1],  # Very light gray
            'card_background_color': [1, 1, 1, 1],      # Pure white
            'input_background_color': [0.95, 0.95, 0.95, 1],  # Light gray
            'header_background_color': [0.2, 0.3, 0.5, 1],    # Dark blue
            'sidebar_background_color': [0.94, 0.94, 0.94, 1], # Light sidebar

            # Text Colors
            'text_primary_color': [0.1, 0.1, 0.1, 1],   # Almost black
            'text_secondary_color': [0.3, 0.3, 0.3, 1], # Dark gray
            'text_muted_color': [0.5, 0.5, 0.5, 1],     # Medium gray
            'text_light_color': [0.9, 0.9, 0.9, 1],     # Light for dark backgrounds
            'text_on_primary_color': [1, 1, 1, 1],      # White text on primary

            # Border and Separator Colors
            'border_color': [0.8, 0.8, 0.8, 1],         # Light border
            'separator_color': [0.9, 0.9, 0.9, 1],      # Very light separator
            'divider_color': [0.85, 0.85, 0.85, 1],     # Divider line

            # Button Colors
            'button_text_light': [1, 1, 1, 1],          # White text for dark buttons
            'button_text_dark': [0.1, 0.1, 0.1, 1],     # Dark text for light buttons
            'button_hover_color': [0.1, 0.25, 0.6, 1],  # Button hover state
            'button_pressed_color': [0.05, 0.2, 0.5, 1], # Button pressed state

            # Special Purpose Colors
            'disabled_color': [0.7, 0.7, 0.7, 1],       # Disabled elements
            'hover_color': [0.95, 0.95, 0.95, 1],       # Hover state
            'selected_color': [0.85, 0.9, 1, 1],        # Selected state
            'focus_color': [0.2, 0.4, 0.8, 0.3],        # Focus outline

            # Shadow and Effects
            'shadow_color': [0, 0, 0, 0.1],              # Drop shadow
            'overlay_color': [0, 0, 0, 0.5],             # Modal overlay

            # Table and Data Colors
            'table_header_bg': [0.2, 0.3, 0.5, 1],      # Table header background
            'table_row_even': [1, 1, 1, 1],             # Even table rows
            'table_row_odd': [0.98, 0.98, 0.98, 1],     # Odd table rows
            'table_row_hover': [0.9, 0.95, 1, 1],       # Table row hover

            # Font Sizes
            'font_size_tiny': 10,
            'font_size_small': 12,
            'font_size_normal': 14,
            'font_size_medium': 16,
            'font_size_large': 18,
            'font_size_xlarge': 20,
            'font_size_title': 24,
            'font_size_header': 28,

            # Spacing and Layout
            'spacing_tiny': 2,
            'spacing_small': 5,
            'spacing_normal': 10,
            'spacing_medium': 15,
            'spacing_large': 20,
            'spacing_xlarge': 30,

            # Border Radius
            'border_radius_small': 3,
            'border_radius_normal': 5,
            'border_radius_medium': 8,
            'border_radius_large': 12,

            # Component Heights
            'button_height': 40,
            'input_height': 35,
            'header_height': 60,
            'toolbar_height': 45,
            'footer_height': 30,
        }

    def _get_dark_theme(self) -> Dict[str, Any]:
        """Dark theme configuration"""
        return {
            # Primary Brand Colors
            'primary_color': [0.2, 0.4, 0.8, 1],        # Bright blue
            'secondary_color': [0.7, 0.7, 0.7, 1],      # Light gray
            'accent_color': [1, 0.7, 0.3, 1],           # Orange accent

            # Status Colors
            'success_color': [0.2, 0.8, 0.3, 1],        # Bright green
            'warning_color': [1, 0.8, 0.2, 1],          # Bright amber
            'error_color': [1, 0.3, 0.3, 1],            # Bright red
            'info_color': [0.3, 0.6, 1, 1],             # Bright blue

            # Background Colors
            'background_color': [0.15, 0.15, 0.15, 1],  # Dark gray
            'card_background_color': [0.2, 0.2, 0.2, 1], # Darker gray
            'input_background_color': [0.25, 0.25, 0.25, 1], # Input background
            'header_background_color': [0.1, 0.1, 0.1, 1],   # Very dark
            'sidebar_background_color': [0.18, 0.18, 0.18, 1], # Dark sidebar

            # Text Colors
            'text_primary_color': [0.9, 0.9, 0.9, 1],   # Light text
            'text_secondary_color': [0.7, 0.7, 0.7, 1], # Medium light text
            'text_muted_color': [0.5, 0.5, 0.5, 1],     # Muted text
            'text_light_color': [1, 1, 1, 1],           # Pure white
            'text_on_primary_color': [1, 1, 1, 1],      # White text on primary

            # Border and Separator Colors
            'border_color': [0.4, 0.4, 0.4, 1],         # Dark border
            'separator_color': [0.3, 0.3, 0.3, 1],      # Dark separator
            'divider_color': [0.35, 0.35, 0.35, 1],     # Divider line

            # Button Colors
            'button_text_light': [1, 1, 1, 1],          # White text
            'button_text_dark': [0.1, 0.1, 0.1, 1],     # Dark text
            'button_hover_color': [0.3, 0.5, 0.9, 1],   # Button hover
            'button_pressed_color': [0.15, 0.35, 0.7, 1], # Button pressed

            # Special Purpose Colors
            'disabled_color': [0.4, 0.4, 0.4, 1],       # Disabled elements
            'hover_color': [0.25, 0.25, 0.25, 1],       # Hover state
            'selected_color': [0.3, 0.4, 0.6, 1],       # Selected state
            'focus_color': [0.2, 0.4, 0.8, 0.5],        # Focus outline

            # Shadow and Effects
            'shadow_color': [0, 0, 0, 0.3],              # Stronger shadow
            'overlay_color': [0, 0, 0, 0.7],             # Darker overlay

            # Table and Data Colors
            'table_header_bg': [0.1, 0.1, 0.1, 1],      # Dark table header
            'table_row_even': [0.2, 0.2, 0.2, 1],       # Even rows
            'table_row_odd': [0.18, 0.18, 0.18, 1],     # Odd rows
            'table_row_hover': [0.3, 0.3, 0.4, 1],      # Row hover

            # Inherit font sizes and other properties from light theme
            **{k: v for k, v in self._get_light_theme().items()
               if k.startswith(('font_size_', 'spacing_', 'border_radius_', 'button_height', 'input_height', 'header_height', 'toolbar_height', 'footer_height'))}
        }

    def _get_blue_theme(self) -> Dict[str, Any]:
        """Blue professional theme"""
        base = self._get_light_theme()
        base.update({
            'primary_color': [0.1, 0.3, 0.6, 1],        # Deep blue
            'secondary_color': [0.2, 0.4, 0.7, 1],      # Medium blue
            'accent_color': [0.3, 0.6, 0.9, 1],         # Light blue
            'header_background_color': [0.05, 0.2, 0.4, 1], # Dark blue header
            'card_background_color': [0.98, 0.99, 1, 1], # Slight blue tint
            'selected_color': [0.8, 0.9, 1, 1],         # Blue selection
        })
        return base

    def _get_green_theme(self) -> Dict[str, Any]:
        """Green nature theme"""
        base = self._get_light_theme()
        base.update({
            'primary_color': [0.1, 0.6, 0.2, 1],        # Forest green
            'secondary_color': [0.2, 0.7, 0.3, 1],      # Medium green
            'accent_color': [0.4, 0.8, 0.4, 1],         # Light green
            'header_background_color': [0.05, 0.4, 0.1, 1], # Dark green header
            'card_background_color': [0.98, 1, 0.98, 1], # Slight green tint
            'selected_color': [0.8, 1, 0.8, 1],         # Green selection
        })
        return base

    def _get_orange_theme(self) -> Dict[str, Any]:
        """Orange warm theme"""
        base = self._get_light_theme()
        base.update({
            'primary_color': [0.8, 0.4, 0.1, 1],        # Deep orange
            'secondary_color': [0.9, 0.5, 0.2, 1],      # Medium orange
            'accent_color': [1, 0.7, 0.3, 1],           # Light orange
            'header_background_color': [0.6, 0.3, 0.05, 1], # Dark orange header
            'card_background_color': [1, 0.99, 0.98, 1], # Slight orange tint
            'selected_color': [1, 0.9, 0.8, 1],         # Orange selection
        })
        return base

    def _get_purple_theme(self) -> Dict[str, Any]:
        """Purple elegant theme"""
        base = self._get_light_theme()
        base.update({
            'primary_color': [0.4, 0.1, 0.6, 1],        # Deep purple
            'secondary_color': [0.5, 0.2, 0.7, 1],      # Medium purple
            'accent_color': [0.7, 0.4, 0.9, 1],         # Light purple
            'header_background_color': [0.3, 0.05, 0.4, 1], # Dark purple header
            'card_background_color': [1, 0.98, 1, 1],   # Slight purple tint
            'selected_color': [0.9, 0.8, 1, 1],         # Purple selection
        })
        return base

    def _get_professional_theme(self) -> Dict[str, Any]:
        """Professional corporate theme"""
        base = self._get_light_theme()
        base.update({
            'primary_color': [0.2, 0.2, 0.3, 1],        # Dark slate
            'secondary_color': [0.3, 0.3, 0.4, 1],      # Medium slate
            'accent_color': [0.5, 0.6, 0.7, 1],         # Light slate
            'header_background_color': [0.1, 0.1, 0.2, 1], # Very dark slate
            'card_background_color': [0.99, 0.99, 0.99, 1], # Off-white
            'selected_color': [0.9, 0.9, 0.95, 1],      # Slate selection
            'text_primary_color': [0.15, 0.15, 0.2, 1], # Dark slate text
        })
        return base

    def _get_modern_theme(self) -> Dict[str, Any]:
        """Modern minimalist theme"""
        base = self._get_light_theme()
        base.update({
            'primary_color': [0, 0, 0, 1],               # Pure black
            'secondary_color': [0.2, 0.2, 0.2, 1],      # Dark gray
            'accent_color': [0.9, 0.9, 0.9, 1],         # Light gray
            'header_background_color': [0.05, 0.05, 0.05, 1], # Almost black
            'card_background_color': [1, 1, 1, 1],      # Pure white
            'selected_color': [0.95, 0.95, 0.95, 1],    # Light gray selection
            'border_color': [0.9, 0.9, 0.9, 1],         # Very light border
        })
        return base

    def set_theme(self, theme_type: ThemeType):
        """Set the current theme"""
        if theme_type in self.themes:
            self.current_theme = theme_type
            self._notify_observers()
            logger.info(f"Theme changed to: {theme_type.value}")
        else:
            logger.error(f"Unknown theme type: {theme_type}")

    def get_color(self, color_name: str) -> List[float]:
        """Get color value by name"""
        theme = self.themes[self.current_theme]

        # Check custom colors first
        if color_name in self.custom_colors:
            return self.custom_colors[color_name]

        # Then check current theme
        if color_name in theme:
            return theme[color_name]

        # Fallback to light theme
        fallback_theme = self.themes[ThemeType.LIGHT]
        if color_name in fallback_theme:
            return fallback_theme[color_name]

        # Default fallback
        logger.warning(f"Color '{color_name}' not found, using default")
        return [0.5, 0.5, 0.5, 1]  # Gray fallback

    def get_theme_property(self, property_name: str) -> Any:
        """Get any theme property by name"""
        theme = self.themes[self.current_theme]
        return theme.get(property_name, None)

    def set_custom_color(self, color_name: str, color_value: List[float]):
        """Set a custom color that overrides theme colors"""
        self.custom_colors[color_name] = color_value
        self._notify_observers()

    def get_all_colors(self) -> Dict[str, List[float]]:
        """Get all colors for the current theme"""
        theme = self.themes[self.current_theme].copy()
        theme.update(self.custom_colors)
        return {k: v for k, v in theme.items() if k.endswith('_color')}

    def get_available_themes(self) -> List[ThemeType]:
        """Get list of available themes"""
        return list(self.themes.keys())

    def get_current_theme_name(self) -> str:
        """Get current theme name"""
        return self.current_theme.value

    def reset_custom_colors(self):
        """Reset all custom colors"""
        self.custom_colors.clear()
        self._notify_observers()

    def add_observer(self, observer):
        """Add theme change observer"""
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        """Remove theme change observer"""
        if observer in self.observers:
            self.observers.remove(observer)

    def _notify_observers(self):
        """Notify all observers of theme change"""
        for observer in self.observers:
            if hasattr(observer, 'on_theme_changed'):
                try:
                    observer.on_theme_changed()
                except Exception as e:
                    logger.error(f"Error notifying theme observer: {e}")

    # Button Style Configurations
    def get_button_style(self, button_type: str = 'primary') -> Dict[str, Any]:
        """Get complete button style configuration"""
        styles = {
            'primary': {
                'background_color': self.get_color('primary_color'),
                'color': self.get_color('button_text_light'),
                'font_size': f"{self.get_theme_property('font_size_normal')}sp",
                'height': self.get_theme_property('button_height'),
            },
            'secondary': {
                'background_color': self.get_color('secondary_color'),
                'color': self.get_color('button_text_light'),
                'font_size': f"{self.get_theme_property('font_size_normal')}sp",
                'height': self.get_theme_property('button_height'),
            },
            'success': {
                'background_color': self.get_color('success_color'),
                'color': self.get_color('button_text_light'),
                'font_size': f"{self.get_theme_property('font_size_normal')}sp",
                'height': self.get_theme_property('button_height'),
            },
            'warning': {
                'background_color': self.get_color('warning_color'),
                'color': self.get_color('button_text_light'),
                'font_size': f"{self.get_theme_property('font_size_normal')}sp",
                'height': self.get_theme_property('button_height'),
            },
            'danger': {
                'background_color': self.get_color('error_color'),
                'color': self.get_color('button_text_light'),
                'font_size': f"{self.get_theme_property('font_size_normal')}sp",
                'height': self.get_theme_property('button_height'),
            },
            'info': {
                'background_color': self.get_color('info_color'),
                'color': self.get_color('button_text_light'),
                'font_size': f"{self.get_theme_property('font_size_normal')}sp",
                'height': self.get_theme_property('button_height'),
            },
            'light': {
                'background_color': self.get_color('card_background_color'),
                'color': self.get_color('text_primary_color'),
                'font_size': f"{self.get_theme_property('font_size_normal')}sp",
                'height': self.get_theme_property('button_height'),
            },
            'dark': {
                'background_color': self.get_color('text_primary_color'),
                'color': self.get_color('card_background_color'),
                'font_size': f"{self.get_theme_property('font_size_normal')}sp",
                'height': self.get_theme_property('button_height'),
            },
        }
        return styles.get(button_type, styles['primary'])

    def get_input_style(self) -> Dict[str, Any]:
        """Get input field style configuration"""
        return {
            'background_color': self.get_color('input_background_color'),
            'foreground_color': self.get_color('text_primary_color'),
            'font_size': f"{self.get_theme_property('font_size_normal')}sp",
            'height': self.get_theme_property('input_height'),
        }

    def get_label_style(self, label_type: str = 'normal') -> Dict[str, Any]:
        """Get label style configuration"""
        styles = {
            'normal': {
                'color': self.get_color('text_primary_color'),
                'font_size': f"{self.get_theme_property('font_size_normal')}sp",
            },
            'title': {
                'color': self.get_color('text_primary_color'),
                'font_size': f"{self.get_theme_property('font_size_title')}sp",
            },
            'header': {
                'color': self.get_color('text_primary_color'),
                'font_size': f"{self.get_theme_property('font_size_header')}sp",
            },
            'secondary': {
                'color': self.get_color('text_secondary_color'),
                'font_size': f"{self.get_theme_property('font_size_normal')}sp",
            },
            'muted': {
                'color': self.get_color('text_muted_color'),
                'font_size': f"{self.get_theme_property('font_size_small')}sp",
            },
            'light': {
                'color': self.get_color('text_light_color'),
                'font_size': f"{self.get_theme_property('font_size_normal')}sp",
            },
        }
        return styles.get(label_type, styles['normal'])

    def get_card_style(self) -> Dict[str, Any]:
        """Get card/container style configuration"""
        return {
            'background_color': self.get_color('card_background_color'),
            'border_color': self.get_color('border_color'),
            'spacing': self.get_theme_property('spacing_normal'),
            'padding': [
                self.get_theme_property('spacing_medium'),
                self.get_theme_property('spacing_normal'),
                self.get_theme_property('spacing_medium'),
                self.get_theme_property('spacing_normal')
            ],
        }

    def get_table_style(self) -> Dict[str, Any]:
        """Get table style configuration"""
        return {
            'header_background': self.get_color('table_header_bg'),
            'header_text_color': self.get_color('text_light_color'),
            'row_even_color': self.get_color('table_row_even'),
            'row_odd_color': self.get_color('table_row_odd'),
            'row_hover_color': self.get_color('table_row_hover'),
            'border_color': self.get_color('border_color'),
            'text_color': self.get_color('text_primary_color'),
        }


# Global theme manager instance
theme_manager = ThemeManager()
