#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Enhanced Modern Dashboard Screen
"""

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.animation import Animation
import os
import logging

from app.components import (RTLLabel, CustomActionButton as ActionButton, StatsCard,
                           BilingualLabel, TranslatableButton, LanguageSwitcher,
                           NavigationHeader, ResponsiveCard, BilingualButton, SettingsDialog)
from app.config import config
from app.database import DatabaseManager
from app.font_manager import font_manager
from app.language_manager import language_manager
from app.config import config

logger = logging.getLogger(__name__)


class ActivitySidebar(BoxLayout):
    """Modern activity sidebar that slides in from the right"""

    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.db = db_manager
        self.orientation = 'vertical'
        self.size_hint_x = None
        self.width = dp(400)
        self.pos_hint = {'right': 1, 'top': 1}
        self.padding = [20, 20, 20, 20]
        self.spacing = dp(15)

        # Add background
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 0.98)  # Light background with transparency
            self.bg_rect = RoundedRectangle(radius=[15, 0, 0, 15])
            self.bind(size=self._update_bg, pos=self._update_bg)

        self.build_sidebar()

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def build_sidebar(self):
        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=10)

        title = BilingualLabel(
            translation_key='recent_activity',
            font_size='20sp',
            bold=True,
            color=[0.2, 0.2, 0.2, 1],
            size_hint_x=0.8
        )
        header.add_widget(title)

        # Close button
        close_btn = Button(
            text='×',
            font_size='24sp',
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            background_color=[1, 0.3, 0.3, 1]
        )
        close_btn.bind(on_press=self.close_sidebar)
        header.add_widget(close_btn)

        self.add_widget(header)

        # Activities container with scroll
        scroll = ScrollView()
        self.activities_container = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None
        )
        self.activities_container.bind(minimum_height=self.activities_container.setter('height'))
        scroll.add_widget(self.activities_container)
        self.add_widget(scroll)

        # Load activities
        self.load_activities()

    def load_activities(self):
        """Load recent activities"""
        try:
            self.activities_container.clear_widgets()

            # Get recent properties
            recent_properties = self.db.get_recent_properties()

            if not recent_properties:
                no_activity = BilingualLabel(
                    translation_key='no_recent_activity',
                    font_size='14sp',
                    color=[0.5, 0.5, 0.5, 1],
                    halign='center',
                    size_hint_y=None,
                    height=dp(60)
                )
                self.activities_container.add_widget(no_activity)
                return

            # Show all recent properties
            for prop in recent_properties:
                activity_item = self.create_activity_item(prop)
                self.activities_container.add_widget(activity_item)

        except Exception as e:
            logger.error(f"Error loading activities: {e}")

    def create_activity_item(self, property_data):
        """Create activity item"""
        item_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint_y=None,
            height=dp(80),
            padding=[10, 10]
        )

        # Add background
        with item_layout.canvas.before:
            Color(1, 1, 1, 0.8)
            bg = RoundedRectangle(radius=[8])
            item_layout.bg = bg
            item_layout.bind(size=lambda *args: setattr(bg, 'size', item_layout.size),
                           pos=lambda *args: setattr(bg, 'pos', item_layout.pos))

        # Property info
        info_text = f"{language_manager.get_text('property')}: {property_data.get('Property-address', language_manager.get_text('not_specified'))}"
        info_label = RTLLabel(
            text=info_text,
            font_size='12sp',
            size_hint_y=None,
            height=dp(40)
        )
        item_layout.add_widget(info_label)

        # Action button
        view_btn = BilingualButton(
            translation_key='view_details',
            size_hint_y=None,
            height=dp(30),
            background_color=[0.2, 0.6, 1, 1]
        )
        view_btn.bind(on_press=lambda x: self.view_property(property_data))
        item_layout.add_widget(view_btn)

        return item_layout

    def view_property(self, property_data):
        """Navigate to property details"""
        # Close sidebar and navigate
        self.close_sidebar()
        self.parent.parent.navigate_to('properties')

    def close_sidebar(self, *args):
        """Close the sidebar with animation"""
        anim = Animation(x=self.parent.width, duration=0.3)
        anim.bind(on_complete=lambda *args: self.parent.remove_widget(self))
        anim.start(self)


class ModernStatCard(BoxLayout):
    """Enhanced statistics card with modern design"""

    def __init__(self, title_key, value, color, icon_source=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = [20, 20]
        self.size_hint_y = None
        self.height = dp(120)

        # Add modern background with gradient effect
        with self.canvas.before:
            Color(*color, 0.1)
            self.bg_rect = RoundedRectangle(radius=[12])
            self.bind(size=self._update_bg, pos=self._update_bg)

            # Add border
            Color(*color, 0.3)
            self.border = Line(rounded_rectangle=[0, 0, 0, 0, 12], width=2)
            self.bind(size=self._update_border, pos=self._update_border)

        # Icon and value section
        top_section = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=0.6)

        # Icon if provided
        if icon_source and os.path.exists(icon_source):
            icon = Image(
                source=icon_source,
                size_hint=(None, None),
                size=(dp(40), dp(40))
            )
            top_section.add_widget(icon)

        # Value
        value_label = RTLLabel(
            text=str(value),
            font_size='32sp',
            color=color,
            bold=True,
            halign='center'
        )
        top_section.add_widget(value_label)

        self.add_widget(top_section)

        # Title
        title = BilingualLabel(
            translation_key=title_key,
            font_size='14sp',
            color=color,
            bold=True,
            halign='center',
            size_hint_y=0.4
        )
        self.add_widget(title)

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def _update_border(self, *args):
        self.border.rounded_rectangle = [*self.pos, *self.size, 12]


class QuickActionCard(BoxLayout):
    """Modern quick action card with icon and enhanced design"""

    def __init__(self, title_key, icon_source, color, callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(15)
        self.padding = [20, 20]
        self.size_hint_y = None
        self.height = dp(140)

        # Add modern background with hover effect
        with self.canvas.before:
            Color(*color, 0.1)
            self.bg_rect = RoundedRectangle(radius=[15])
            self.bind(size=self._update_bg, pos=self._update_bg)

            # Add subtle border
            Color(*color, 0.4)
            self.border = Line(rounded_rectangle=[0, 0, 0, 0, 15], width=2)
            self.bind(size=self._update_border, pos=self._update_border)

        # Icon section
        icon_container = BoxLayout(size_hint_y=0.6, padding=[0, 10])
        if os.path.exists(icon_source):
            icon = Image(
                source=icon_source,
                size_hint=(None, None),
                size=(dp(60), dp(60)),
                pos_hint={'center_x': 0.5}
            )
            icon_container.add_widget(icon)
        self.add_widget(icon_container)

        # Title section
        title = BilingualLabel(
            translation_key=title_key,
            font_size='16sp',
            color=color,
            bold=True,
            halign='center',
            size_hint_y=0.4
        )
        self.add_widget(title)

        # Make it clickable
        self.bind(on_touch_down=self._on_touch)
        self.callback = callback

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def _update_border(self, *args):
        self.border.rounded_rectangle = [*self.pos, *self.size, 15]

    def _on_touch(self, instance, touch):
        if self.collide_point(*touch.pos):
            self.callback()
            return True
        return False


class DashboardScreen(Screen):
    """Enhanced Modern Dashboard Screen with Hero Section and Responsive Design"""

    def __init__(self, db_manager: DatabaseManager, **kwargs):
        super().__init__(**kwargs)
        self.name = 'dashboard'
        self.db = db_manager
        self.sidebar = None

        self.build_modern_ui()

        # Auto-refresh stats every 30 seconds
        Clock.schedule_interval(self.refresh_stats, 30)

    def build_modern_ui(self):
        """Build the enhanced modern dashboard UI"""
        # Main scrollable container
        main_scroll = ScrollView()
        main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(25),
            padding=[25, 20, 25, 25],
            size_hint_y=None
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))

        # Hero Header Section
        self.build_hero_header(main_layout)

        # Statistics Hero Section
        self.build_statistics_hero(main_layout)

        # Quick Actions Section
        self.build_quick_actions(main_layout)

        main_scroll.add_widget(main_layout)
        self.add_widget(main_scroll)        # Load initial data
        Clock.schedule_once(self.load_dashboard_data, 0.1)

    def build_hero_header(self, main_layout):
        """Build the hero header section"""
        header_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(80),
            spacing=20,
            padding=[0, 10]
        )

        # Add gradient background
        with header_layout.canvas.before:
            Color(0.1, 0.3, 0.6, 1)  # Blue gradient
            self.header_bg = RoundedRectangle(radius=[15])
            header_layout.bind(
                size=lambda *args: setattr(self.header_bg, 'size', header_layout.size),
                pos=lambda *args: setattr(self.header_bg, 'pos', header_layout.pos)
            )

        # Back to welcome button
        back_btn = BilingualButton(
            translation_key='back_to_menu',
            background_color=[0.9, 0.9, 0.9, 1],
            color=[0.2, 0.2, 0.2, 1],
            size_hint=(None, None),
            size=(dp(160), dp(45))
        )
        back_btn.bind(on_press=self.go_to_welcome)
        header_layout.add_widget(back_btn)

        # Dashboard title with modern styling
        title = BilingualLabel(
            translation_key='dashboard',
            font_size='28sp',
            bold=True,
            color=[1, 1, 1, 1],
            halign='center'
        )
        header_layout.add_widget(title)

        # Language and controls
        controls_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            size=(dp(200), dp(60)),
            spacing=dp(10)
        )

        # Language switcher
        lang_switcher = LanguageSwitcher(
            size_hint=(None, None),
            size=(dp(180), dp(40))
        )
        controls_layout.add_widget(lang_switcher)

        header_layout.add_widget(controls_layout)
        main_layout.add_widget(header_layout)

    def build_statistics_hero(self, main_layout):
        """Build the enhanced statistics hero section"""
        stats_section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(200),
            spacing=dp(15),
            padding=[10, 15]
        )

        # Add modern background
        with stats_section.canvas.before:
            Color(0.98, 0.98, 0.98, 1)
            self.stats_bg = RoundedRectangle(radius=[12])
            stats_section.bind(
                size=lambda *args: setattr(self.stats_bg, 'size', stats_section.size),
                pos=lambda *args: setattr(self.stats_bg, 'pos', stats_section.pos)
            )

        # Section header with recent activity button
        header_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=10
        )

        section_title = BilingualLabel(
            translation_key='system_statistics',
            font_size='22sp',
            bold=True,
            color=[0.2, 0.2, 0.2, 1],
            size_hint_x=0.7
        )
        header_row.add_widget(section_title)

        # Recent Activity Button (replaces the old section)
        activity_btn = BilingualButton(
            translation_key='recent_activity',
            background_color=[0.2, 0.6, 1, 1],
            size_hint=(None, None),
            size=(dp(180), dp(40))
        )
        activity_btn.bind(on_press=self.show_activity_sidebar)
        header_row.add_widget(activity_btn)

        stats_section.add_widget(header_row)

        # Statistics cards container
        self.stats_container = GridLayout(
            cols=4,
            spacing=dp(15),
            size_hint_y=None,
            height=dp(135),
            padding=[10, 0]
        )
        stats_section.add_widget(self.stats_container)

        main_layout.add_widget(stats_section)

    def build_quick_actions(self, main_layout):
        """Build the quick actions section with medium-sized responsive cards"""
        actions_section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(220),
            spacing=dp(15),
            padding=[10, 15]
        )

        # Add background

        # Section title
        title = BilingualLabel(
            translation_key='quick_actions',
            font_size='22sp',
            bold=True,
            color=[0.2, 0.5, 0.9, 1],  # Light blue color
            size_hint_y=None,
            height=dp(40),
            halign='center'
        )
        actions_section.add_widget(title)

        # Actions grid with 2x2 layout
        actions_grid = GridLayout(
            cols=2,
            spacing=dp(20),
            size_hint_y=None,
            height=dp(160),
            padding=[20, 0]
        )

        # Define action cards with icons
        actions_data = [
            ('owners_management', 'app-images/insert.jpg', [0.2, 0.7, 0.3, 1], lambda: self.navigate_to('owners')),
            ('properties_management', 'app-images/save.jpg', [0.8, 0.4, 0.1, 1], lambda: self.navigate_to('properties')),
            ('search_reports', 'app-images/browse.jpg', [0.6, 0.2, 0.8, 1], lambda: self.navigate_to('search')),
            ('settings', 'app-images/update.jpg', [0.1, 0.5, 0.8, 1], self.show_settings)
        ]

        for title_key, icon_source, color, callback in actions_data:
            action_card = QuickActionCard(title_key, icon_source, color, callback)
            actions_grid.add_widget(action_card)

        actions_section.add_widget(actions_grid)
        main_layout.add_widget(actions_section)

    def show_activity_sidebar(self, instance):
        """Show the activity sidebar"""
        if self.sidebar:
            return  # Already showing

        # Create sidebar
        self.sidebar = ActivitySidebar(self.db)

        # Position sidebar off-screen initially
        self.sidebar.x = self.width

        # Add to parent (main screen)
        self.add_widget(self.sidebar)

        # Animate in
        anim = Animation(x=self.width - self.sidebar.width, duration=0.3)
        anim.start(self.sidebar)

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

    def refresh_stats(self, dt=None):
        """Load and display enhanced statistics"""
        try:
            # Clear existing stats
            self.stats_container.clear_widgets()

            # Get statistics from database
            total_owners = self.db.get_total_owners()
            total_properties = self.db.get_total_properties()
            available_properties = self.db.get_available_properties_count()
            occupied_properties = total_properties - available_properties

            # Create modern stats cards
            stats_data = [
                ('total_owners', str(total_owners), [0.2, 0.6, 0.9, 1], 'app-images/insert.jpg'),
                ('total_properties', str(total_properties), [0.1, 0.7, 0.4, 1], 'app-images/save.jpg'),
                ('available_properties', str(available_properties), [0.9, 0.6, 0.1, 1], 'app-images/browse.jpg'),
                ('occupied_properties', str(occupied_properties), [0.8, 0.3, 0.3, 1], 'app-images/update.jpg')
            ]

            for title_key, value, color, icon_source in stats_data:
                card = ModernStatCard(title_key, value, color, icon_source)
                self.stats_container.add_widget(card)

        except Exception as e:
            logger.error(f"Error loading dashboard statistics: {e}")

    def show_settings(self, instance=None):
        """Show settings dialog"""
        try:
            settings_dialog = SettingsDialog()
            settings_dialog.open()
        except Exception as e:
            logger.error(f"Error showing settings: {e}")

    def on_enter(self, *args):
        """Called when screen is entered - refresh data"""
        self.refresh_stats()

    def on_leave(self, *args):
        """Called when leaving screen - cleanup"""
        if self.sidebar:
            self.remove_widget(self.sidebar)
            self.sidebar = None
