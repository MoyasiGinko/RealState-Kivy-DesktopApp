#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Main Dashboard Screen
"""

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
import os
import logging

from app.components import (RTLLabel, CustomActionButton as ActionButton, StatsCard,
                           BilingualLabel, TranslatableButton, LanguageSwitcher,
                           NavigationHeader, ResponsiveCard, BilingualButton)
from app.config import config
from app.database import DatabaseManager
from app.font_manager import font_manager
from app.language_manager import language_manager
from app.config import config

logger = logging.getLogger(__name__)


class DashboardScreen(Screen):
    """Main dashboard screen - Central hub for all application features"""

    def __init__(self, db_manager: DatabaseManager, **kwargs):
        super().__init__(**kwargs)
        self.name = 'dashboard'
        self.db = db_manager

        self.build_ui()

        # Auto-refresh stats every 30 seconds
        Clock.schedule_interval(self.refresh_stats, 30)

    def build_ui(self):
        """Build the modern, responsive dashboard UI"""
        # Main layout with proper spacing
        main_layout = BoxLayout(orientation='vertical', spacing=dp(20), padding=[20, 15, 20, 20])

        # Header with navigation
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=20)

        # Back to welcome button
        back_btn = BilingualButton(
            translation_key='back_to_menu',
            button_type='secondary',
            size_hint=(None, None),
            size=(dp(150), dp(40))
        )
        back_btn.bind(on_press=self.go_to_welcome)
        header_layout.add_widget(back_btn)

        # Dashboard title
        title_style = config.get_label_style('title')
        title = BilingualLabel(
            translation_key='dashboard',
            font_size=title_style['font_size'],
            bold=True,
            color=title_style['color'],
            halign='center'
        )
        header_layout.add_widget(title)

        # Theme and language controls
        controls_layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(150), dp(85)), spacing=dp(5))

        # Theme selector
        from app.components import ThemeSelector
        theme_selector = ThemeSelector(size_hint=(None, None), size=(dp(150), dp(40)))
        controls_layout.add_widget(theme_selector)

        # Language switcher
        lang_switcher = LanguageSwitcher(size_hint=(None, None), size=(dp(150), dp(40)))
        controls_layout.add_widget(lang_switcher)

        header_layout.add_widget(controls_layout)

        main_layout.add_widget(header_layout)

        # Statistics section
        stats_section = ResponsiveCard(title='system_statistics')
        self.stats_container = BoxLayout(orientation='horizontal', spacing=dp(20), padding=[20, 20])
        stats_section.add_widget(self.stats_container)
        main_layout.add_widget(stats_section)

        # Quick actions section
        actions_section = ResponsiveCard(title='quick_actions')
        actions_grid = GridLayout(cols=2, spacing=dp(20), padding=[20, 20], size_hint_y=None)
        actions_grid.bind(minimum_height=actions_grid.setter('height'))

        # Action buttons with consistent styling
        button_style = {
            'font_size': '18sp',
            'size_hint_y': None,
            'height': dp(80),
            'bold': True
        }

        # Owners Management
        owners_btn = BilingualButton(
            translation_key='owners_management',
            button_type='success',
            **button_style
        )
        owners_btn.bind(on_press=lambda x: self.navigate_to('owners'))
        actions_grid.add_widget(owners_btn)

        # Properties Management
        properties_btn = BilingualButton(
            translation_key='properties_management',
            button_type='warning',
            **button_style
        )
        properties_btn.bind(on_press=lambda x: self.navigate_to('properties'))
        actions_grid.add_widget(properties_btn)

        # Search & Reports
        search_btn = BilingualButton(
            translation_key='search_reports',
            button_type='danger',
            **button_style
        )
        search_btn.bind(on_press=lambda x: self.navigate_to('search'))
        actions_grid.add_widget(search_btn)

        # System Settings (placeholder)
        settings_btn = BilingualButton(
            translation_key='settings',
            button_type='info',
            **button_style
        )
        settings_btn.bind(on_press=self.show_settings)
        actions_grid.add_widget(settings_btn)

        actions_section.add_widget(actions_grid)
        main_layout.add_widget(actions_section)

        # Recent activity section
        recent_section = ResponsiveCard(title='recent_activity')
        self.recent_container = BoxLayout(orientation='vertical', spacing=dp(10), padding=[20, 20])
        recent_section.add_widget(self.recent_container)
        main_layout.add_widget(recent_section)

        self.add_widget(main_layout)

        # Load initial data
        Clock.schedule_once(self.load_dashboard_data, 0.1)

    def navigate_to(self, screen_name):
        """Navigate to a specific screen"""
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = screen_name

    def go_to_welcome(self, instance):
        """Navigate back to welcome screen"""
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'welcome'

    def load_dashboard_data(self, dt):
        """Load dashboard data asynchronously"""
        Clock.schedule_once(lambda dt: self.refresh_stats(), 0)
        Clock.schedule_once(lambda dt: self.load_recent_activities(), 0.1)

    def refresh_stats(self, dt=None):
        """Load and display statistics"""
        try:
            # Clear existing stats
            self.stats_container.clear_widgets()

            # Get statistics from database
            total_owners = self.db.get_total_owners()
            total_properties = self.db.get_total_properties()
            available_properties = self.db.get_available_properties_count()

            # Create stats cards
            stats_data = [
                ('total_owners', str(total_owners), config.get_color('primary_color')),
                ('total_properties', str(total_properties), config.get_color('success_color')),
                ('available_properties', str(available_properties), config.get_color('warning_color')),
                ('database_status', language_manager.get_text('active'), config.get_color('info_color'))
            ]

            for title_key, value, color in stats_data:
                card = self.create_stat_card(title_key, value, color)
                self.stats_container.add_widget(card)

        except Exception as e:
            logger.error(f"Error loading dashboard statistics: {e}")
            # Show error message
            error_style = config.get_label_style('normal')
            error_label = BilingualLabel(
                translation_key='error_loading_data',
                font_size=error_style['font_size'],
                color=config.get_color('error_color')
            )
            self.stats_container.add_widget(error_label)

    def create_stat_card(self, title_key: str, value: str, color: list):
        """Create a modern statistics card"""
        card_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint_x=0.25,
            padding=dp(15)
        )

        # Add background with canvas
        with card_layout.canvas.before:
            Color(*color, 0.1)  # Light background
            bg_rect = RoundedRectangle(radius=[10])
            card_layout.bg_rect = bg_rect
            card_layout.bind(
                size=lambda *args: setattr(bg_rect, 'size', card_layout.size),
                pos=lambda *args: setattr(bg_rect, 'pos', card_layout.pos)
            )

        # Title
        title = BilingualLabel(
            translation_key=title_key,
            font_size='14sp',
            color=color,
            bold=True,
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        card_layout.add_widget(title)

        # Value
        value_label = RTLLabel(
            text=value,
            font_size='24sp',
            color=color,
            bold=True,
            halign='center',
            size_hint_y=None,
            height=dp(40)
        )
        card_layout.add_widget(value_label)

        return card_layout

    def load_recent_activities(self, dt=None):
        """Load recent activities"""
        try:
            # Clear existing activities
            self.recent_container.clear_widgets()

            # Get recent properties
            recent_properties = self.db.get_recent_properties()

            if not recent_properties:
                no_activity = BilingualLabel(
                    translation_key='no_recent_activity',
                    font_size='14sp',
                    color=config.get_color('text_muted'),
                    halign='center',
                    size_hint_y=None,
                    height=dp(40)
                )
                self.recent_container.add_widget(no_activity)
                return

            # Show recent properties (limit to 3)
            for prop in recent_properties[:3]:
                activity_item = self.create_activity_item(prop)
                self.recent_container.add_widget(activity_item)

        except Exception as e:
            logger.error(f"Error loading recent activities: {e}")

    def create_activity_item(self, property_data: dict):
        """Create an activity item widget"""
        item_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50),
            padding=[10, 5]
        )

        # Property info
        info_text = f"{language_manager.get_text('property')}: {property_data.get('Property-address', language_manager.get_text('not_specified'))[:30]}..."
        info_label = RTLLabel(
            text=info_text,
            font_size='12sp',
            size_hint_x=0.8
        )
        item_layout.add_widget(info_label)

        # View button
        view_btn = BilingualButton(
            translation_key='view',
            size_hint_x=0.2,
            size_hint_y=None,
            height=dp(30),
            background_color=config.get_color('secondary')
        )
        view_btn.bind(on_press=lambda x: self.view_property(property_data))
        item_layout.add_widget(view_btn)

        return item_layout

    def view_property(self, property_data: dict):
        """Navigate to property details"""
        try:
            # Navigate to properties screen
            self.navigate_to('properties')
        except Exception as e:
            logger.error(f"Error viewing property: {e}")

    def show_settings(self, instance):
        """Show settings dialog"""
        from app.components import MessageDialog
        dialog = MessageDialog(
            title=language_manager.get_text('settings'),
            message=language_manager.get_text('feature_coming_soon'),
            message_type='info'
        )
        dialog.open()

    def on_enter(self, *args):
        """Called when screen is entered - refresh data"""
        self.refresh_stats()
        self.load_recent_activities()
