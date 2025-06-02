#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Modern UI Components with KivyMD
Material Design components for a beautiful, modern interface
"""

from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton, MDFloatingActionButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationDrawerItem
from kivymd.uix.list import MDList, OneLineListItem, ThreeLineListItem, OneLineIconListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.chip import MDChip
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.selectioncontrol import MDSwitch, MDCheckbox
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.imagelist import MDSmartTile
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.bottomsheet import MDBottomSheet
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp, sp
from kivy.uix.widget import Widget
from typing import Callable, List, Dict, Optional, Any
import logging
import os

from app.font_manager import font_manager
from app.language_manager import language_manager

logger = logging.getLogger(__name__)


# Design tokens and color scheme
class DesignTokens:
    """Modern design tokens for consistent UI"""

    # Color Palette - Professional Real Estate Theme
    COLORS = {
        'primary': (0.13, 0.39, 0.65, 1),          # Professional Blue #2163A5
        'primary_light': (0.20, 0.58, 0.88, 1),   # Light Blue #3394E0
        'primary_dark': (0.08, 0.26, 0.43, 1),    # Dark Blue #15426E
        'secondary': (0.96, 0.76, 0.24, 1),       # Gold Accent #F5C23D
        'success': (0.20, 0.70, 0.35, 1),         # Green #33B359
        'warning': (1.0, 0.69, 0.26, 1),          # Orange #FFB042
        'error': (0.86, 0.27, 0.31, 1),           # Red #DC454F
        'surface': (0.98, 0.98, 0.98, 1),         # Light Gray #FAFAFA
        'background': (0.95, 0.95, 0.95, 1),      # Background Gray #F3F3F3
        'card': (1.0, 1.0, 1.0, 1),               # White Cards
        'text_primary': (0.13, 0.13, 0.13, 1),    # Dark Text #212121
        'text_secondary': (0.46, 0.46, 0.46, 1),  # Gray Text #757575
        'text_hint': (0.62, 0.62, 0.62, 1),       # Hint Text #9E9E9E
        'info': (0.25, 0.47, 0.75, 1),         # Info Blue #4080C0
        'divider': (0.88, 0.88, 0.88, 1),         # Divider #E0E0E0

    }

    # Elevation & Shadows
    ELEVATIONS = {
        'card': 2,
        'button': 1,
        'modal': 8,
        'nav_drawer': 16,
        'low': 1,
        'medium': 4,
        'high': 8,
    }

    # Spacing
    SPACING = {
        'xs': dp(4),
        'sm': dp(8),
        'md': dp(16),
        'lg': dp(24),
        'xl': dp(32),
        'extra_small': dp(4),  # Alias for 'xs'
        'small': dp(8),  # Alias for 'sm'
        'medium': dp(16),  # Alias for 'md'
        'large': dp(24),  # Alias for 'lg'
        'extra_large': dp(32),  # Alias for 'xl'
    }

    # Border Radius
    RADIUS = {
        'sm': [dp(4), dp(4), dp(4), dp(4)],
        'md': [dp(8), dp(8), dp(8), dp(8)],
        'lg': [dp(12), dp(12), dp(12), dp(12)],
        'xl': [dp(16), dp(16), dp(16), dp(16)],
        'small': [dp(4), dp(4), dp(4), dp(4)],  # Alias for 'sm'
        'medium': [dp(8), dp(8), dp(8), dp(8)],  # Alias for 'md'
        'large': [dp(12), dp(12), dp(12), dp(12)],  # Alias for 'lg'
        'extra_large': [dp(16), dp(16), dp(16), dp(16)],  # Alias for 'xl'
    }


# Enhanced Modern Card with design tokens
class ModernCard(MDCard):
    """Enhanced Material Design card with consistent design tokens"""

    def __init__(self, variant='default', title=None, **kwargs):
        # Remove title from kwargs as MDCard doesn't support it
        kwargs.pop('title', None)

        # Apply design tokens based on variant
        if variant == 'stats':
            kwargs.setdefault('md_bg_color', DesignTokens.COLORS['surface'])
            kwargs.setdefault('elevation', DesignTokens.ELEVATIONS['card'])
        elif variant == 'form':
            kwargs.setdefault('md_bg_color', DesignTokens.COLORS['card'])
            kwargs.setdefault('elevation', DesignTokens.ELEVATIONS['card'] + 1)
        else:
            kwargs.setdefault('md_bg_color', DesignTokens.COLORS['card'])
            kwargs.setdefault('elevation', DesignTokens.ELEVATIONS['card'])

        kwargs.setdefault('radius', DesignTokens.RADIUS['lg'])
        kwargs.setdefault('padding', DesignTokens.SPACING['md'])
        kwargs.setdefault('spacing', DesignTokens.SPACING['sm'])
        kwargs.setdefault('orientation', 'vertical')
        kwargs.setdefault('adaptive_height', True)

        super().__init__(**kwargs)


class StatsCard(ModernCard):
    """Statistics card with icon, title, and value"""

    def __init__(self, title: str, value: str, icon: str = "information",
                 color: tuple = None, **kwargs):
        super().__init__(**kwargs)

        if color is None:
            color = (0.2, 0.6, 1, 1)  # Default blue

        # Header with icon and title
        header = MDBoxLayout(
            adaptive_height=True,
            spacing=dp(8),
            md_bg_color=(0, 0, 0, 0)  # Transparent
        )

        # Icon
        icon_widget = MDIconButton(
            icon=icon,
            theme_icon_color="Custom",
            icon_color=color,
            icon_size=dp(32)
        )
        header.add_widget(icon_widget)

        # Title and value
        text_layout = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            md_bg_color=(0, 0, 0, 0)
        )

        title_label = MDLabel(
            text=title,
            theme_text_color="Secondary",
            font_style="Body1",
            adaptive_height=True
        )
        text_layout.add_widget(title_label)

        value_label = MDLabel(
            text=str(value),
            theme_text_color="Primary",
            font_style="H4",
            adaptive_height=True
        )
        text_layout.add_widget(value_label)

        header.add_widget(text_layout)
        self.add_widget(header)


class ModernTextField(MDTextField):
    """Enhanced text field with RTL support and validation"""

    def __init__(self, translation_key: str = None, required: bool = False,
                 input_type: str = 'text', **kwargs):

        self.translation_key = translation_key
        self.required = required
        self.input_type = input_type

        # Set label text
        if translation_key:
            kwargs['hint_text'] = language_manager.get_text(translation_key)

        # Set Material Design properties
        kwargs.setdefault('mode', 'line')
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(56))

        # Handle RTL text
        if language_manager.current_language == 'ar':
            kwargs.setdefault('text_direction', 'rtl')

        super().__init__(**kwargs)

        # Add required indicator
        if required:
            self.hint_text += " *"

        # Setup validation
        self.bind(text=self._validate_input)

        # Register for language changes
        language_manager.add_observer(self)

    def _validate_input(self, instance, text):
        """Validate input based on type and requirements"""
        if self.required and not text.strip():
            self.error = True
            self.helper_text = language_manager.get_text('field_required')
        elif self.input_type == 'email' and text and '@' not in text:
            self.error = True
            self.helper_text = language_manager.get_text('invalid_email')
        elif self.input_type == 'number' and text:
            try:
                float(text)
                self.error = False
                self.helper_text = ""
            except ValueError:
                self.error = True
                self.helper_text = language_manager.get_text('invalid_number')
        else:
            self.error = False
            self.helper_text = ""

    def get_value(self) -> str:
        """Get field value"""
        return self.text

    def set_value(self, value: str):
        """Set field value"""
        self.text = str(value) if value else ''

    def clear(self):
        """Clear field"""
        self.text = ''
        self.error = False
        self.helper_text = ""

    def on_language_changed(self):
        """Update when language changes"""
        if self.translation_key:
            hint_text = language_manager.get_text(self.translation_key)
            if self.required:
                hint_text += " *"
            self.hint_text = hint_text


class ModernButton(MDRaisedButton):
    """Enhanced Material Design button with translation support"""

    def __init__(self, translation_key: str = None, button_type: str = 'primary',
                 icon: str = None, **kwargs):

        self.translation_key = translation_key
        self.button_type = button_type

        # Set text
        if translation_key:
            kwargs['text'] = language_manager.get_text(translation_key)

        # Set icon
        if icon:
            kwargs['icon'] = icon

        # Set Material Design properties based on type
        if button_type == 'primary':
            kwargs.setdefault('md_bg_color', (0.2, 0.6, 1, 1))  # Blue
        elif button_type == 'secondary':
            kwargs.setdefault('md_bg_color', (0.5, 0.5, 0.5, 1))  # Gray
        elif button_type == 'success':
            kwargs.setdefault('md_bg_color', (0.2, 0.8, 0.2, 1))  # Green
        elif button_type == 'danger':
            kwargs.setdefault('md_bg_color', (0.8, 0.2, 0.2, 1))  # Red

        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(48))
        kwargs.setdefault('elevation', 2)

        super().__init__(**kwargs)

        # Register for language changes
        if translation_key:
            language_manager.add_observer(self)

    def on_language_changed(self):
        """Update when language changes"""
        if self.translation_key:
            self.text = language_manager.get_text(self.translation_key)


class ModernDataTable(MDCard):
    """Enhanced data table with Material Design styling"""

    def __init__(self, columns: List[Dict], rows_data: List[List] = None, **kwargs):
        super().__init__(**kwargs)

        self.columns = columns
        self.rows_data = rows_data or []

        # Create data table
        self.data_table = MDDataTable(
            column_data=[(col['text'], dp(col.get('width', 100))) for col in columns],
            row_data=self.rows_data,
            elevation=0,
            rows_num=10,
            use_pagination=True
        )

        self.add_widget(self.data_table)

    def update_data(self, rows_data: List[List]):
        """Update table data"""
        self.rows_data = rows_data
        self.data_table.row_data = rows_data

    def add_row(self, row_data: List):
        """Add a new row"""
        self.rows_data.append(row_data)
        self.data_table.row_data = self.rows_data

    def remove_row(self, index: int):
        """Remove a row by index"""
        if 0 <= index < len(self.rows_data):
            self.rows_data.pop(index)
            self.data_table.row_data = self.rows_data


class PropertyCard(ModernCard):
    """Card for displaying property information"""

    def __init__(self, property_data: Dict, on_click: Callable = None, **kwargs):
        super().__init__(**kwargs)

        self.property_data = property_data
        self.on_click = on_click

        # Property image
        if property_data.get('photos'):
            photo_path = property_data['photos'].split(';')[0]
            try:
                image_tile = MDSmartTile(
                    source=photo_path,
                    size_hint_y=None,
                    height=dp(200),
                    radius=[15, 15, 0, 0],
                    box_radius=[0, 0, 0, 0]
                )
                self.add_widget(image_tile)
            except:
                pass  # Skip if image not found

        # Property details
        details_layout = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            spacing=dp(8),
            padding=dp(16)
        )

        # Location (title)
        location_label = MDLabel(
            text=property_data.get('location', 'Unknown Location'),
            theme_text_color="Primary",
            font_style="H6",
            adaptive_height=True
        )
        details_layout.add_widget(location_label)

        # Property type and area
        type_area_label = MDLabel(
            text=f"{property_data.get('propertytype', '')} • {property_data.get('area', '')} m²",
            theme_text_color="Secondary",
            font_style="Body2",
            adaptive_height=True
        )
        details_layout.add_widget(type_area_label)

        # Price
        if property_data.get('price'):
            price_label = MDLabel(
                text=f"${property_data['price']:,}",
                theme_text_color="Primary",
                font_style="H6",
                adaptive_height=True            )
            details_layout.add_widget(price_label)

        # Status chip
        if property_data.get('status'):
            status_chip = MDChip(
                type="filter",
                size_hint_x=None,
                width=dp(100)
            )
            status_chip.add_widget(MDLabel(
                text=property_data['status'],
                halign="center",
                adaptive_size=True
            ))
            details_layout.add_widget(status_chip)

        self.add_widget(details_layout)

        # Handle clicks
        if on_click:
            self.bind(on_release=lambda x: on_click(property_data))


class OwnerCard(ModernCard):
    """Card for displaying owner information"""

    def __init__(self, owner_data: Dict, on_click: Callable = None, **kwargs):
        super().__init__(**kwargs)

        self.owner_data = owner_data
        self.on_click = on_click

        # Owner details
        details_layout = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            spacing=dp(8)
        )

        # Owner name
        name_label = MDLabel(
            text=owner_data.get('ownername', 'Unknown Owner'),
            theme_text_color="Primary",
            font_style="H6",
            adaptive_height=True
        )
        details_layout.add_widget(name_label)

        # Phone number
        if owner_data.get('ownerphone'):
            phone_label = MDLabel(
                text=owner_data['ownerphone'],
                theme_text_color="Secondary",
                font_style="Body2",
                adaptive_height=True
            )
            details_layout.add_widget(phone_label)

        # Notes
        if owner_data.get('Note'):
            notes_label = MDLabel(
                text=owner_data['Note'][:100] + "..." if len(owner_data['Note']) > 100 else owner_data['Note'],
                theme_text_color="Secondary",
                font_style="Caption",
                adaptive_height=True
            )
            details_layout.add_widget(notes_label)

        self.add_widget(details_layout)

        # Handle clicks
        if on_click:
            self.bind(on_release=lambda x: on_click(owner_data))


class ModernDialog(MDDialog):
    """Enhanced dialog with Material Design styling"""

    def __init__(self, title: str, content_text: str = None,
                 dialog_type: str = 'info', buttons: List = None, **kwargs):

        # Set default properties
        kwargs.setdefault('size_hint', (0.8, None))
        kwargs.setdefault('height', dp(300))

        # Create buttons if not provided
        if buttons is None:
            buttons = [
                MDFlatButton(
                    text=language_manager.get_text('close'),
                    on_release=self.dismiss
                )
            ]

        super().__init__(
            title=title,
            text=content_text,
            buttons=buttons,
            **kwargs
        )


class ModernSnackbar:
    """Enhanced snackbar for notifications"""

    @staticmethod
    def show_message(text: str, duration: float = 3):
        """Show a snackbar message"""
        from kivymd.uix.label import MDLabel

        snackbar = Snackbar(
            duration=duration,
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=(1 - 20/100)  # 20dp margins
        )
        snackbar.add_widget(
            MDLabel(
                text=text,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )
        )
        snackbar.open()

    @staticmethod
    def show_success(text: str):
        """Show success message"""
        ModernSnackbar.show_message(f"✓ {text}")

    @staticmethod
    def show_error(text: str):
        """Show error message"""
        ModernSnackbar.show_message(f"✗ {text}")

    @staticmethod
    def show_info(text: str):
        """Show info message"""
        ModernSnackbar.show_message(f"ℹ {text}")


class NavigationDrawer(MDNavigationDrawer):
    """Modern navigation drawer for the app"""

    def __init__(self, **kwargs):
        kwargs.setdefault('radius', (0, 16, 16, 0))
        kwargs.setdefault('width', dp(280))
        kwargs.setdefault('elevation', 16)

        super().__init__(**kwargs)

        # Navigation items
        nav_items = [
            {'icon': 'view-dashboard', 'text': 'dashboard', 'screen': 'dashboard'},
            {'icon': 'account-group', 'text': 'owners', 'screen': 'owners'},
            {'icon': 'home-city', 'text': 'properties', 'screen': 'properties'},
            {'icon': 'magnify', 'text': 'search', 'screen': 'search'},
        ]

        for item in nav_items:
            nav_item = MDNavigationDrawerItem(
                icon=item['icon'],
                text=language_manager.get_text(item['text']),
                on_release=lambda x, screen=item['screen']: self.navigate_to_screen(screen)
            )
            self.add_widget(nav_item)

    def navigate_to_screen(self, screen_name: str):
        """Navigate to a screen and close drawer"""
        # This will be connected to the main app controller
        self.parent.current = screen_name
        self.set_state("close")


class ModernTopBar(MDTopAppBar):
    """Modern top app bar with navigation and actions"""

    def __init__(self, title: str = None, **kwargs):
        kwargs.setdefault('elevation', 4)
        kwargs.setdefault('md_bg_color', (0.2, 0.6, 1, 1))  # Blue

        if title:
            kwargs['title'] = title

        # Default actions
        kwargs.setdefault('right_action_items', [
            ["dots-vertical", lambda x: self.show_menu()]
        ])

        # Navigation icon
        kwargs.setdefault('left_action_items', [
            ["menu", lambda x: self.toggle_nav_drawer()]
        ])

        super().__init__(**kwargs)

    def toggle_nav_drawer(self):
        """Toggle navigation drawer"""
        # This will be implemented by the screen
        pass

    def show_menu(self):
        """Show options menu"""
        # This will be implemented by the screen
        pass


class LoadingSpinner(MDBoxLayout):
    """Loading indicator with spinner and text"""

    def __init__(self, text: str = None, **kwargs):
        kwargs.setdefault('orientation', 'vertical')
        kwargs.setdefault('adaptive_height', True)
        kwargs.setdefault('spacing', dp(16))
        kwargs.setdefault('pos_hint', {'center_x': 0.5, 'center_y': 0.5})

        super().__init__(**kwargs)

        # Spinner
        spinner = MDSpinner(
            size_hint=(None, None),
            size=(dp(48), dp(48)),
            pos_hint={'center_x': 0.5}
        )
        self.add_widget(spinner)

        # Loading text
        if text:
            loading_label = MDLabel(
                text=text,
                theme_text_color="Secondary",
                font_style="Body1",
                halign="center",
                adaptive_height=True
            )
            self.add_widget(loading_label)


class EmptyState(MDBoxLayout):
    """Empty state widget with icon and message"""

    def __init__(self, icon: str = "inbox-outline", message: str = None,
                 action_text: str = None, action_callback: Callable = None, **kwargs):
        kwargs.setdefault('orientation', 'vertical')
        kwargs.setdefault('adaptive_height', True)
        kwargs.setdefault('spacing', dp(24))
        kwargs.setdefault('pos_hint', {'center_x': 0.5, 'center_y': 0.5})

        super().__init__(**kwargs)

        # Icon
        icon_widget = MDIconButton(
            icon=icon,
            theme_icon_color="Secondary",
            icon_size=dp(64),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(icon_widget)

        # Message
        if message:
            message_label = MDLabel(
                text=message,
                theme_text_color="Secondary",
                font_style="H6",
                halign="center",
                adaptive_height=True
            )
            self.add_widget(message_label)

        # Action button
        if action_text and action_callback:
            action_button = MDRaisedButton(
                text=action_text,
                size_hint=(None, None),
                size=(dp(200), dp(48)),
                pos_hint={'center_x': 0.5},
                on_release=action_callback
            )
            self.add_widget(action_button)


class EnhancedStatsCard(ModernCard):
    """Enhanced statistics card with modern design and animations"""

    def __init__(self, title: str, value: str, icon: str = "information",
                 color_scheme: str = 'primary', trend: str = None, **kwargs):
        kwargs['variant'] = 'stats'
        super().__init__(**kwargs)

        # Color schemes
        color_schemes = {
            'primary': DesignTokens.COLORS['primary'],
            'success': DesignTokens.COLORS['success'],
            'warning': DesignTokens.COLORS['warning'],
            'error': DesignTokens.COLORS['error'],
            'secondary': DesignTokens.COLORS['secondary']
        }

        main_color = color_schemes.get(color_scheme, DesignTokens.COLORS['primary'])

        # Main container
        container = MDBoxLayout(
            adaptive_height=True,
            spacing=DesignTokens.SPACING['sm'],
            md_bg_color=(0, 0, 0, 0)
        )        # Icon container with background
        icon_container = MDBoxLayout(
            size_hint=(None, None),
            size=(dp(48), dp(48)),
            md_bg_color=(main_color[0], main_color[1], main_color[2], 0.1),  # Light background
            radius=[dp(8)],
            adaptive_height=True
        )

        icon_widget = MDIconButton(
            icon=icon,
            theme_icon_color="Custom",
            icon_color=main_color,
            icon_size=dp(24),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        icon_container.add_widget(icon_widget)
        container.add_widget(icon_container)

        # Content
        content_layout = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            md_bg_color=(0, 0, 0, 0)
        )

        # Title
        title_label = MDLabel(
            text=title,
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_secondary'],
            font_style="Caption",
            adaptive_height=True
        )
        content_layout.add_widget(title_label)

        # Value with trend
        value_container = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True,
            spacing=DesignTokens.SPACING['xs']
        )

        value_label = MDLabel(
            text=str(value),
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_primary'],
            font_style="H5",
            adaptive_height=True,
            bold=True
        )
        value_container.add_widget(value_label)

        # Trend indicator
        if trend:
            trend_icon = "trending-up" if trend == "up" else "trending-down"
            trend_color = DesignTokens.COLORS['success'] if trend == "up" else DesignTokens.COLORS['error']

            trend_widget = MDIconButton(
                icon=trend_icon,
                theme_icon_color="Custom",
                icon_color=trend_color,
                icon_size=dp(20)
            )
            value_container.add_widget(trend_widget)

        content_layout.add_widget(value_container)
        container.add_widget(content_layout)

        self.add_widget(container)


class ModernNavigationCard(ModernCard):
    """Navigation card with hover effects and modern styling"""

    def __init__(self, title: str, subtitle: str, icon: str,
                 action: Callable = None, color_scheme: str = 'primary', **kwargs):
        # Remove custom properties that MDCard doesn't support
        kwargs.pop('title', None)
        kwargs.pop('subtitle', None)
        kwargs.pop('icon', None)
        kwargs.pop('action', None)
        kwargs.pop('color_scheme', None)

        super().__init__(**kwargs)

        color_schemes = {
            'primary': DesignTokens.COLORS['primary'],
            'success': DesignTokens.COLORS['success'],
            'warning': DesignTokens.COLORS['warning'],
            'error': DesignTokens.COLORS['error'],
            'secondary': DesignTokens.COLORS['secondary']
        }

        main_color = color_schemes.get(color_scheme, DesignTokens.COLORS['primary'])

        # Make it clickable
        self.on_release = action if action else lambda: None

        # Content container
        content = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True,
            spacing=DesignTokens.SPACING['md'],
            md_bg_color=(0, 0, 0, 0)
        )        # Icon with gradient background
        icon_bg = MDBoxLayout(
            size_hint=(None, None),
            size=(dp(64), dp(64)),
            md_bg_color=(main_color[0], main_color[1], main_color[2], 0.1),
            radius=DesignTokens.RADIUS['lg']
        )

        icon_widget = MDIconButton(
            icon=icon,
            theme_icon_color="Custom",
            icon_color=main_color,
            icon_size=dp(32),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        icon_bg.add_widget(icon_widget)
        content.add_widget(icon_bg)

        # Text content
        text_layout = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            md_bg_color=(0, 0, 0, 0)
        )

        title_label = MDLabel(
            text=title,
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_primary'],
            font_style="H6",
            adaptive_height=True,
            bold=True
        )
        text_layout.add_widget(title_label)

        subtitle_label = MDLabel(
            text=subtitle,
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_secondary'],
            font_style="Body2",
            adaptive_height=True
        )
        text_layout.add_widget(subtitle_label)

        content.add_widget(text_layout)

        # Arrow indicator
        arrow = MDIconButton(
            icon="chevron-right",
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['text_hint'],
            icon_size=dp(24)
        )
        content.add_widget(arrow)

        self.add_widget(content)


class ModernImageViewer(MDCard):
    """Modern image viewer with preview capabilities"""

    def __init__(self, image_path: str = None, **kwargs):
        super().__init__(**kwargs)

        # Container for image
        image_container = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            spacing=DesignTokens.SPACING['sm']
        )

        if image_path and os.path.exists(image_path):
            # Image display
            image_tile = MDSmartTile(
                source=image_path,
                size_hint_y=None,
                height=dp(300),
                radius=DesignTokens.RADIUS['md']
            )
            image_container.add_widget(image_tile)
        else:
            # Placeholder for no image
            placeholder = MDBoxLayout(
                size_hint_y=None,
                height=dp(200),
                md_bg_color=DesignTokens.COLORS['surface'],
                radius=DesignTokens.RADIUS['md']
            )

            placeholder_icon = MDIconButton(
                icon="image-outline",
                theme_icon_color="Custom",
                icon_color=DesignTokens.COLORS['text_hint'],
                icon_size=dp(64),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            placeholder.add_widget(placeholder_icon)
            image_container.add_widget(placeholder)

        self.add_widget(image_container)


class ModernFilterChip(MDChip):
    """Modern filter chip for property filtering"""

    def __init__(self, text: str, filter_key: str, filter_value: Any,
                 on_filter: Callable = None, **kwargs):
        kwargs.setdefault('type', 'filter')
        kwargs.setdefault('check', False)
        super().__init__(**kwargs)

        self.text = text
        self.filter_key = filter_key
        self.filter_value = filter_value
        self.on_filter = on_filter

        # Style the chip
        self.md_bg_color = DesignTokens.COLORS['surface']
        self.text_color = DesignTokens.COLORS['text_primary']

        self.bind(active=self._on_chip_active)

    def _on_chip_active(self, instance, active):
        """Handle chip activation"""
        if self.on_filter:
            self.on_filter(self.filter_key, self.filter_value, active)


class ModernProgressCard(ModernCard):
    """Card with progress indicator for operations"""

    def __init__(self, title: str, progress: float = 0, **kwargs):
        super().__init__(**kwargs)

        self.title = title
        self.progress_value = progress

        # Title
        title_label = MDLabel(
            text=title,
            theme_text_color="Primary",
            font_style="H6",
            adaptive_height=True
        )
        self.add_widget(title_label)        # Progress bar
        self.progress_bar = MDProgressBar(
            value=progress,
            md_bg_color=DesignTokens.COLORS['primary']
        )
        self.add_widget(self.progress_bar)

        # Progress text
        self.progress_label = MDLabel(
            text=f"{progress:.0f}%",
            theme_text_color="Secondary",
            font_style="Body2",
            adaptive_height=True
        )
        self.add_widget(self.progress_label)

    def set_progress(self, value: float):
        """Update progress value and label."""
        self.progress_value = value
        self.progress_bar.value = value
        self.progress_label.text = f"{value:.0f}%"


class ModernSearchBar(MDCard):
    """Modern search bar with filters and actions"""

    def __init__(self, placeholder="Search...", on_search=None, filters=None, **kwargs):
        super().__init__(**kwargs)
        self.elevation = DesignTokens.ELEVATIONS['low']
        self.radius = DesignTokens.RADIUS['medium']
        self.size_hint_y = None
        self.height = dp(56)
        self.padding = dp(8)

        layout = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True,
            spacing=dp(8)
        )

        # Search icon
        search_icon = MDIconButton(
            icon="magnify",
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['text_secondary']
        )
        layout.add_widget(search_icon)

        # Search field
        self.search_field = MDTextField(
            hint_text=placeholder,
            size_hint_y=None,
            height=dp(40),
            mode="fill"
        )
        if on_search:
            self.search_field.bind(on_text_validate=on_search)
        layout.add_widget(self.search_field)

        # Filter button
        if filters:
            filter_button = MDIconButton(
                icon="filter-variant",
                theme_icon_color="Custom",
                icon_color=DesignTokens.COLORS['primary']
            )
            layout.add_widget(filter_button)

        self.add_widget(layout)

    def get_text(self):
        """Get search text"""
        return self.search_field.text

    def clear(self):
        """Clear search text"""
        self.search_field.text = ""


class ModernActionBar(MDCard):
    """Modern action bar with customizable actions"""

    def __init__(self, actions=None, **kwargs):
        super().__init__(**kwargs)
        self.elevation = DesignTokens.ELEVATIONS['medium']
        self.radius = DesignTokens.RADIUS['medium']
        self.size_hint_y = None
        self.height = dp(72)
        self.padding = dp(16)

        layout = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True,
            spacing=dp(16)
        )

        if actions:
            for action in actions:
                if action.get('type') == 'raised':
                    button = MDRaisedButton(
                        text=action.get('text', ''),
                        md_bg_color=action.get('color', DesignTokens.COLORS['primary']),
                        on_release=action.get('callback')
                    )
                elif action.get('type') == 'flat':
                    button = MDFlatButton(
                        text=action.get('text', ''),
                        theme_text_color="Custom",
                        text_color=action.get('color', DesignTokens.COLORS['primary']),
                        on_release=action.get('callback')
                    )
                elif action.get('type') == 'icon':
                    button = MDIconButton(
                        icon=action.get('icon', 'plus'),
                        theme_icon_color="Custom",
                        icon_color=action.get('color', DesignTokens.COLORS['primary']),
                        on_release=action.get('callback')
                    )
                else:
                    continue

                layout.add_widget(button)

        self.add_widget(layout)


class ModernListItem(MDCard):
    """Modern list item with customizable content"""

    def __init__(self, title=None, subtitle=None, icon=None, trailing_icon=None,
                 on_tap=None, **kwargs):
        # Remove any invalid properties that MDCard doesn't support
        kwargs.pop("title", None)
        kwargs.pop("subtitle", None)
        kwargs.pop("icon", None)
        kwargs.pop("trailing_icon", None)
        kwargs.pop("on_tap", None)

        # Pop custom keys from kwargs if present (for **dict usage)
        if title is None:
            title = kwargs.pop("title", "")
        if subtitle is None:
            subtitle = kwargs.pop("subtitle", "")
        if icon is None:
            icon = kwargs.pop("icon", None)
        if trailing_icon is None:
            trailing_icon = kwargs.pop("trailing_icon", None)
        if on_tap is None:
            on_tap = kwargs.pop("on_tap", None)
        super().__init__(**kwargs)
        self.elevation = DesignTokens.ELEVATIONS['low']
        self.radius = DesignTokens.RADIUS['small']
        self.size_hint_y = None
        self.height = dp(72)
        self.padding = dp(16)
        self.ripple_behavior = True

        if on_tap:
            self.bind(on_release=on_tap)

        layout = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True,
            spacing=dp(16)
        )

        # Leading icon
        if icon:
            icon_widget = MDIconButton(
                icon=icon,
                theme_icon_color="Custom",
                icon_color=DesignTokens.COLORS['primary']
            )
            layout.add_widget(icon_widget)

        # Content
        content_layout = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True
        )

        title_label = MDLabel(
            text=title,
            theme_text_color="Primary",
            font_style="Subtitle1",
            adaptive_height=True
        )
        content_layout.add_widget(title_label)

        if subtitle:
            subtitle_label = MDLabel(
                text=subtitle,
                theme_text_color="Secondary",
                font_style="Body2",
                adaptive_height=True
            )
            content_layout.add_widget(subtitle_label)

        layout.add_widget(content_layout)

        # Trailing icon
        if trailing_icon:
            trailing_widget = MDIconButton(
                icon=trailing_icon,
                theme_icon_color="Custom",
                icon_color=DesignTokens.COLORS['text_secondary']
            )
            layout.add_widget(trailing_widget)

        self.add_widget(layout)


class ModernGridView(MDGridLayout):
    """Modern grid view for displaying cards in a grid"""

    def __init__(self, cols=2, spacing=None, **kwargs):
        # Remove scroll-related kwargs since we're now a GridLayout
        scroll_kwargs = ['do_scroll_x', 'do_scroll_y', 'scroll_type', 'bar_width', 'bar_color']
        for key in scroll_kwargs:
            kwargs.pop(key, None)

        super().__init__(**kwargs)

        if spacing is None:
            spacing = DesignTokens.SPACING['medium']

        self.cols = cols
        self.adaptive_height = True
        self.spacing = spacing
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))

    def add_item(self, widget):
        """Add item to grid"""
        self.add_widget(widget)

    def clear_items(self):
        """Clear all items from grid"""
        self.clear_widgets()

    def set_cols(self, cols):
        """Set number of columns"""
        self.cols = cols


class ModernFormCard(MDCard):
    """Modern form card with grouped form fields"""

    def __init__(self, title="", fields=None, **kwargs):
        super().__init__(**kwargs)
        self.elevation = DesignTokens.ELEVATIONS['medium']
        self.radius = DesignTokens.RADIUS['large']
        self.padding = DesignTokens.SPACING['large']
        self.adaptive_height = True

        self.form_fields = {}

        layout = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            spacing=DesignTokens.SPACING['medium']
        )

        # Title
        if title:
            title_label = MDLabel(
                text=title,
                theme_text_color="Primary",
                font_style="H6",
                adaptive_height=True
            )
            layout.add_widget(title_label)

        # Form fields
        if fields:
            for field in fields:
                field_widget = self._create_field(field)
                if field_widget:
                    layout.add_widget(field_widget)

        self.add_widget(layout)

    def _create_field(self, field_config):
        """Create form field based on configuration"""
        field_type = field_config.get('type', 'text')
        field_name = field_config.get('name', '')

        if field_type == 'text':
            field = ModernTextField(
                hint_text=field_config.get('hint', ''),
                required=field_config.get('required', False)
            )
        elif field_type == 'dropdown':
            # Create dropdown field
            field = MDTextField(
                hint_text=field_config.get('hint', ''),
                readonly=True
            )
            # Add dropdown menu logic here if needed
        elif field_type == 'switch':
            field = MDBoxLayout(
                orientation='horizontal',
                adaptive_height=True,
                spacing=dp(16)
            )
            label = MDLabel(
                text=field_config.get('label', ''),
                theme_text_color="Primary",
                adaptive_height=True
            )
            switch = MDSwitch()
            field.add_widget(label)
            field.add_widget(switch)
            self.form_fields[field_name] = switch
            return field
        else:
            return None

        self.form_fields[field_name] = field
        return field

    def get_field_value(self, field_name):
        """Get value of a form field"""
        field = self.form_fields.get(field_name)
        if field:
            if hasattr(field, 'text'):
                return field.text
            elif hasattr(field, 'active'):
                return field.active
        return None

    def set_field_value(self, field_name, value):
        """Set value of a form field"""
        field = self.form_fields.get(field_name)
        if field:
            if hasattr(field, 'text'):
                field.text = str(value)
            elif hasattr(field, 'active'):
                field.active = bool(value)

    def validate_form(self):
        """Validate all form fields"""
        errors = []
        for name, field in self.form_fields.items():
            if hasattr(field, 'required') and field.required:
                if not field.text.strip():
                    errors.append(f"{name} is required")
        return errors


# Export all components for easy importing
__all__ = [
    'DesignTokens',
    'ModernCard',
    'StatsCard',
    'ModernTextField',
    'ModernButton',
    'ModernDataTable',
    'PropertyCard',
    'OwnerCard',
    'ModernDialog',
    'ModernSnackbar',
    'NavigationDrawer',
    'LoadingSpinner',
    'EmptyState',
    'EnhancedStatsCard',
    'ModernNavigationCard',
    'ModernImageViewer',
    'ModernFilterChip',
    'ModernProgressCard',
    'ModernSearchBar',
    'ModernActionBar',
    'ModernListItem',
    'ModernGridView',
    'ModernFormCard'
]
