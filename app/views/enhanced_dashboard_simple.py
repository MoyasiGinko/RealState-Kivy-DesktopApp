#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Enhanced Dashboard (Simple Compatible Version)
Beautiful, responsive dashboard using standard Kivy components with enhanced features
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle, RoundedRectangle
import logging

from app.components import BilingualLabel, BilingualButton, NavigationHeader
from app.language_manager import language_manager

logger = logging.getLogger(__name__)


class EnhancedDashboardScreen(Screen):
    """Enhanced Dashboard with Material Design-inspired layout using standard Kivy components"""

    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.stats_data = {}
        self.build_ui()
        Clock.schedule_once(self.load_dashboard_data, 0.5)

    def build_ui(self):
        """Build the complete dashboard UI"""
        main_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=[dp(20), dp(10)])

        # Add gradient background
        with main_layout.canvas.before:
            Color(0.95, 0.95, 0.97, 1)  # Light background
            self.background_rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self._update_background, pos=self._update_background)        # Navigation Header
        header = NavigationHeader(
            screen_title_key='welcome_dashboard',
            size_hint_y=None,
            height=dp(60)
        )
        main_layout.add_widget(header)

        # Welcome Section
        welcome_section = self.build_welcome_section()
        main_layout.add_widget(welcome_section)

        # Stats Section
        stats_section = self.build_stats_section()
        main_layout.add_widget(stats_section)

        # Quick Actions Section
        actions_section = self.build_actions_section()
        main_layout.add_widget(actions_section)

        self.add_widget(main_layout)

    def _update_background(self, instance, value):
        """Update background rectangle"""
        self.background_rect.size = instance.size
        self.background_rect.pos = instance.pos

    def build_welcome_section(self):
        """Build welcome section with subtitle"""
        section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=[dp(20), dp(10)],
            spacing=dp(10)
        )

        # Welcome title
        welcome_title = BilingualLabel(
            translation_key='welcome_dashboard',
            font_size='32sp',
            bold=True,
            halign='center',
            color=[0.2, 0.3, 0.5, 1],
            size_hint_y=None,
            height=dp(50)
        )
        section.add_widget(welcome_title)

        # Subtitle
        subtitle = BilingualLabel(
            translation_key='dashboard_subtitle',
            font_size='16sp',
            halign='center',
            color=[0.4, 0.5, 0.6, 1],
            size_hint_y=None,
            height=dp(40)
        )
        section.add_widget(subtitle)

        return section

    def build_stats_section(self):
        """Build statistics section with cards"""
        section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(200),
            padding=[dp(10), 0],
            spacing=dp(10)
        )

        # Section title
        title = BilingualLabel(
            translation_key='system_statistics',
            font_size='20sp',
            bold=True,
            halign='center',
            size_hint_y=None,
            height=dp(40)
        )
        section.add_widget(title)

        # Stats grid
        stats_grid = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(150)
        )

        # Create stat cards
        self.total_properties_card = self.create_stat_card('total_properties', '0')
        self.total_owners_card = self.create_stat_card('total_owners', '0')
        self.available_properties_card = self.create_stat_card('available_properties', '0')
        self.occupied_properties_card = self.create_stat_card('occupied_properties', '0')

        stats_grid.add_widget(self.total_properties_card)
        stats_grid.add_widget(self.total_owners_card)
        stats_grid.add_widget(self.available_properties_card)
        stats_grid.add_widget(self.occupied_properties_card)

        section.add_widget(stats_grid)
        return section

    def create_stat_card(self, title_key, value):
        """Create a statistics card"""
        card = BoxLayout(
            orientation='vertical',
            padding=[dp(15), dp(10)],
            spacing=dp(5)
        )

        # Add card background
        with card.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.card_rect = RoundedRectangle(
                size=card.size,
                pos=card.pos,
                radius=[dp(8)]
            )
        card.bind(size=lambda instance, value: setattr(self.card_rect, 'size', instance.size))
        card.bind(pos=lambda instance, value: setattr(self.card_rect, 'pos', instance.pos))

        # Value label
        value_label = Label(
            text=value,
            font_size='24sp',
            bold=True,
            color=[0.2, 0.6, 1, 1],  # Blue color
            halign='center',
            size_hint_y=None,
            height=dp(40)
        )
        card.add_widget(value_label)

        # Title label
        title_label = BilingualLabel(
            translation_key=title_key,
            font_size='14sp',
            halign='center',
            color=[0.4, 0.5, 0.6, 1],
            size_hint_y=None,
            height=dp(30)
        )
        card.add_widget(title_label)

        # Store reference to value label for updates
        card.value_label = value_label
        return card

    def build_actions_section(self):
        """Build quick actions section"""
        section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(280),
            padding=[dp(10), 0],
            spacing=dp(10)
        )

        # Section title
        title = BilingualLabel(
            translation_key='quick_actions',
            font_size='20sp',
            bold=True,
            halign='center',
            size_hint_y=None,
            height=dp(40)
        )
        section.add_widget(title)

        # Actions grid
        actions_grid = GridLayout(
            cols=2,
            spacing=dp(15),
            size_hint_y=None,
            height=dp(230)
        )

        # Create action buttons
        actions = [
            ('manage_property_owners', 'owners', self.goto_owners),
            ('manage_properties', 'properties', self.goto_properties),
            ('search_and_generate_reports', 'search', self.goto_search),
            ('app_settings', 'settings', self.show_settings)
        ]

        for title_key, icon, callback in actions:
            action_card = self.create_action_card(title_key, callback)
            actions_grid.add_widget(action_card)

        section.add_widget(actions_grid)
        return section

    def create_action_card(self, title_key, callback):
        """Create an action card with button"""
        card = BoxLayout(
            orientation='vertical',
            padding=[dp(10), dp(15)],
            spacing=dp(10)
        )

        # Add card background with subtle elevation
        with card.canvas.before:
            Color(1, 1, 1, 1)  # White background
            card_rect = RoundedRectangle(
                size=card.size,
                pos=card.pos,
                radius=[dp(12)]
            )
        card.bind(size=lambda instance, value: setattr(card_rect, 'size', instance.size))
        card.bind(pos=lambda instance, value: setattr(card_rect, 'pos', instance.pos))

        # Action button
        action_btn = BilingualButton(
            translation_key=title_key,
            background_color=[0.2, 0.6, 1, 1],
            font_size='16sp',
            size_hint_y=None,
            height=dp(80)
        )
        action_btn.bind(on_press=lambda x: callback())

        card.add_widget(action_btn)

        return card

    def load_dashboard_data(self, dt=None):
        """Load dashboard data asynchronously"""
        if not self.db:
            return

        try:
            # Get statistics
            properties_count = self.db.get_total_properties()
            owners_count = self.db.get_total_owners()
            available_count = self.db.get_available_properties_count()
            occupied_count = properties_count - available_count

            # Update stat cards
            self.total_properties_card.value_label.text = str(properties_count)
            self.total_owners_card.value_label.text = str(owners_count)
            self.available_properties_card.value_label.text = str(available_count)
            self.occupied_properties_card.value_label.text = str(occupied_count)

            logger.info("Dashboard data loaded successfully")

        except Exception as e:
            logger.error(f"Error loading dashboard data: {e}")

    def goto_owners(self):
        """Navigate to owners screen"""
        try:
            self.manager.current = 'owners'
        except Exception as e:
            logger.error(f"Error navigating to owners: {e}")

    def goto_properties(self):
        """Navigate to properties screen"""
        try:
            self.manager.current = 'properties'
        except Exception as e:
            logger.error(f"Error navigating to properties: {e}")

    def goto_search(self):
        """Navigate to search screen"""
        try:
            self.manager.current = 'search'
        except Exception as e:
            logger.error(f"Error navigating to search: {e}")

    def show_settings(self):
        """Show settings dialog"""
        try:
            # For now, just log that settings was requested
            logger.info("Settings requested - feature coming soon")
        except Exception as e:
            logger.error(f"Error showing settings: {e}")

    def on_language_changed(self):
        """Called when language changes"""
        pass
