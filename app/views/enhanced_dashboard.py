#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Enhanced Modern Dashboard
Beautiful, responsive dashboard with Material Design components
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDFloatingActionButton, MDIconButton
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.animation import Animation
import logging

from app.views.modern_components import (
    DesignTokens, EnhancedStatsCard, ModernNavigationCard,
    ModernCard, ModernTextField, ModernButton
)
from app.components import BilingualLabel, LanguageSwitcher
from app.language_manager import language_manager
from app.database import DatabaseManager

logger = logging.getLogger(__name__)


class EnhancedDashboardScreen(MDScreen):
    """Enhanced Material Design Dashboard with animations and modern layout"""

    def __init__(self, db_manager: DatabaseManager = None, **kwargs):
        super().__init__(**kwargs)
        self.name = 'enhanced_dashboard'
        self.db = db_manager
        self.stats_data = {}

        self.build_modern_ui()

        # Schedule data loading
        Clock.schedule_once(self.load_dashboard_data, 0.5)

        # Auto-refresh stats every 30 seconds
        Clock.schedule_interval(self.refresh_stats, 30)

    def build_modern_ui(self):
        """Build enhanced modern UI with Material Design"""
        # Main container
        main_container = MDBoxLayout(
            orientation='vertical',
            md_bg_color=DesignTokens.COLORS['background']
        )

        # Top App Bar
        self.build_app_bar(main_container)

        # Scrollable content
        scroll = MDScrollView()
        content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['lg'],
            padding=[DesignTokens.SPACING['md'], DesignTokens.SPACING['sm']],
            adaptive_height=True
        )

        # Welcome section
        self.build_welcome_section(content_layout)

        # Statistics section
        self.build_stats_section(content_layout)

        # Quick actions section
        self.build_quick_actions_section(content_layout)

        # Recent activity section
        self.build_recent_activity_section(content_layout)

        scroll.add_widget(content_layout)
        main_container.add_widget(scroll)

        # Floating Action Button
        self.build_fab(main_container)

        self.add_widget(main_container)

    def build_app_bar(self, parent):
        """Build modern app bar with actions"""
        app_bar = MDTopAppBar(
            title="Real Estate Dashboard",
            md_bg_color=DesignTokens.COLORS['primary'],
            specific_text_color=DesignTokens.COLORS['card'],
            left_action_items=[["menu", lambda x: self.show_navigation_drawer()]],
            right_action_items=[
                ["refresh", lambda x: self.refresh_stats()],
                ["cog", lambda x: self.show_settings()],
                ["account-circle", lambda x: self.show_profile()]
            ]
        )
        parent.add_widget(app_bar)

    def build_welcome_section(self, parent):
        """Build welcome hero section"""
        welcome_card = ModernCard(
            md_bg_color=DesignTokens.COLORS['primary'],
            size_hint_y=None,
            height=dp(140)
        )

        welcome_content = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['md']
        )

        # Welcome text
        text_layout = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True
        )

        welcome_title = MDLabel(
            text=language_manager.get_text('welcome_dashboard'),
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['card'],
            font_style="H4",
            bold=True,
            adaptive_height=True
        )
        text_layout.add_widget(welcome_title)

        welcome_subtitle = MDLabel(
            text=language_manager.get_text('dashboard_subtitle'),
            theme_text_color="Custom",
            text_color=(DesignTokens.COLORS['card'][0], DesignTokens.COLORS['card'][1], DesignTokens.COLORS['card'][2], 0.8),
            font_style="Body1",
            adaptive_height=True
        )
        text_layout.add_widget(welcome_subtitle)

        welcome_content.add_widget(text_layout)

        # Language switcher
        lang_switcher = LanguageSwitcher(
            size_hint=(None, None),
            size=(dp(120), dp(40))
        )
        welcome_content.add_widget(lang_switcher)

        welcome_card.add_widget(welcome_content)
        parent.add_widget(welcome_card)

    def build_stats_section(self, parent):
        """Build enhanced statistics section"""
        # Section header
        stats_header = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=DesignTokens.SPACING['sm']
        )

        stats_title = MDLabel(
            text=language_manager.get_text('system_statistics'),
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_primary'],
            font_style="H5",
            bold=True,
            adaptive_height=True
        )
        stats_header.add_widget(stats_title)

        refresh_btn = MDIconButton(
            icon="refresh",
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['primary'],
            on_release=lambda x: self.refresh_stats()
        )

        stats_header.add_widget(refresh_btn)

        parent.add_widget(stats_header)

        # Stats grid
        self.stats_grid = MDGridLayout(
            cols=2,  # Responsive: 2 cols on mobile, 4 on desktop
            spacing=DesignTokens.SPACING['md'],
            size_hint_y=None,
            height=dp(200),
            adaptive_height=True
        )
        parent.add_widget(self.stats_grid)

    def build_quick_actions_section(self, parent):
        """Build quick actions navigation section"""
        # Section header
        actions_title = MDLabel(
            text=language_manager.get_text('quick_actions'),
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_primary'],
            font_style="H5",
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        parent.add_widget(actions_title)

        # Actions grid
        actions_grid = MDGridLayout(
            cols=1,  # Stack vertically for better mobile experience
            spacing=DesignTokens.SPACING['md'],
            adaptive_height=True
        )

        # Navigation cards
        navigation_items = [            {
                'title': language_manager.get_text('owners_management'),
                'subtitle': language_manager.get_text('manage_property_owners'),
                'icon': 'account-group',
                'action': lambda: self.navigate_to('enhanced_owners'),
                'color_scheme': 'primary'
            },
            {
                'title': language_manager.get_text('properties_management'),
                'subtitle': language_manager.get_text('manage_properties'),
                'icon': 'home-city',
                'action': lambda: self.navigate_to('enhanced_properties'),
                'color_scheme': 'success'
            },
            {
                'title': language_manager.get_text('search_reports'),
                'subtitle': language_manager.get_text('search_and_generate_reports'),
                'icon': 'file-chart',
                'action': lambda: self.navigate_to('enhanced_search'),
                'color_scheme': 'warning'
            },
            {
                'title': language_manager.get_text('settings'),
                'subtitle': language_manager.get_text('app_settings'),
                'icon': 'cog',
                'action': self.show_settings,
                'color_scheme': 'secondary'
            }
        ]

        for item in navigation_items:
            nav_card = ModernNavigationCard(
                title=item['title'],
                subtitle=item['subtitle'],
                icon=item['icon'],
                action=item['action'],
                color_scheme=item['color_scheme'],
                size_hint_y=None,
                height=dp(80)
            )
            actions_grid.add_widget(nav_card)

        parent.add_widget(actions_grid)

    def build_recent_activity_section(self, parent):
        """Build recent activity section"""
        activity_title = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )

        title_label = MDLabel(
            text=language_manager.get_text('recent_activity'),
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_primary'],
            font_style="H5",
            bold=True
        )
        activity_title.add_widget(title_label)

        # View all button
        view_all_btn = MDIconButton(
            icon="arrow-right",
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['secondary'],
            on_release=self.show_recent_activity_dialog
        )
        activity_title.add_widget(view_all_btn)

        parent.add_widget(activity_title)

        # Activity card with actual data
        self.activity_card = ModernCard(
            size_hint_y=None,
            height=dp(200)
        )

        self.activity_content = MDBoxLayout(
            orientation='vertical',
            padding=dp(15),
            spacing=dp(10)
        )

        self.load_recent_activities()
        self.activity_card.add_widget(self.activity_content)
        parent.add_widget(self.activity_card)

    def load_recent_activities(self):
        """Load and display recent activities"""
        self.activity_content.clear_widgets()

        try:
            # Get recent activities from database
            activities = self.get_recent_activities()

            if not activities:
                no_activity = MDLabel(
                    text=language_manager.get_text('no_recent_activity'),
                    theme_text_color="Custom",
                    text_color=DesignTokens.COLORS['text_secondary'],
                    font_style="Body1",
                    halign="center",
                    valign="center"
                )
                self.activity_content.add_widget(no_activity)
            else:
                for activity in activities[:3]:  # Show only last 3 activities
                    activity_item = self.create_activity_item(activity)
                    self.activity_content.add_widget(activity_item)

        except Exception as e:
            logger.error(f"Error loading recent activities: {e}")
            error_label = MDLabel(
                text=language_manager.get_text('error_loading_activities'),
                theme_text_color="Custom",
                text_color=DesignTokens.COLORS['error'],
                font_style="Body1",
                halign="center"
            )
            self.activity_content.add_widget(error_label)

    def get_recent_activities(self):
        """Get recent activities from database"""
        if not self.db:
            return []

        try:
            # Sample activities - you can expand this based on your database schema
            activities = []            # Get recent owners
            recent_owners = self.db.get_recent_owners(limit=2)
            for owner in recent_owners:
                # Make sure to access the correct indices based on the query
                # Owners table: Ownercode, ownername, ownerphone, Note
                owner_name = owner[1] if len(owner) > 1 else "Unknown"
                owner_phone = owner[2] if len(owner) > 2 else "No phone"

                activities.append({
                    'type': 'owner_added',
                    'title': f"New owner: {owner_name}",
                    'subtitle': f"Phone: {owner_phone}",
                    'time': '2 hours ago',  # You can calculate this from created_at if available
                    'icon': 'account-plus'
                })            # Get recent properties
            recent_properties = self.db.get_recent_properties(limit=2)
            for prop in recent_properties:
                # The properties are returned as dictionaries
                prop_address = prop.get('Property-address', 'Unknown address')
                prop_type = prop.get('Rstatetcode', 'Unknown type')

                activities.append({
                    'type': 'property_added',
                    'title': f"New property: {prop_address}",
                    'subtitle': f"Type: {prop_type}",
                    'time': '5 hours ago',
                    'icon': 'home-plus'
                })

            return activities

        except Exception as e:
            logger.error(f"Error getting recent activities: {e}")
            return []

    def create_activity_item(self, activity):
        """Create an activity item widget"""
        item_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(15),
            padding=[0, dp(5)]
        )        # Icon
        icon = MDIconButton(
            icon=activity['icon'],
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['secondary'],
            size_hint_x=None,
            width=dp(30),
            font_size=dp(24)
        )
        item_layout.add_widget(icon)# Content
        content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(2)
        )

        title = MDLabel(
            text=activity['title'],
            font_style="Subtitle2",
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_primary'],
            size_hint_y=None,
            height=dp(20)
        )
        content_layout.add_widget(title)

        subtitle = MDLabel(
            text=activity['subtitle'],
            font_style="Caption",
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_secondary'],
            size_hint_y=None,
            height=dp(16)
        )
        content_layout.add_widget(subtitle)

        item_layout.add_widget(content_layout)

        # Time
        time_label = MDLabel(
            text=activity['time'],
            font_style="Caption",
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_secondary'],
            size_hint_x=None,
            width=dp(80),
            halign="right"
        )
        item_layout.add_widget(time_label)

        return item_layout

    def build_fab(self, parent):
        """Build floating action button"""
        fab = MDFloatingActionButton(
            icon="plus",
            md_bg_color=DesignTokens.COLORS['secondary'],
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['text_primary'],
            pos_hint={'center_x': 0.9, 'center_y': 0.1},
            on_release=self.show_quick_add_menu
        )
        parent.add_widget(fab)

    def load_dashboard_data(self, dt=None):
        """Load dashboard data asynchronously"""
        if not self.db:
            return

        try:
            # Load statistics
            self.stats_data = {
                'total_owners': self.db.get_total_owners(),
                'total_properties': self.db.get_total_properties(),
                'available_properties': self.db.get_available_properties_count(),
                'occupied_properties': 0  # Calculate this
            }

            self.stats_data['occupied_properties'] = (
                self.stats_data['total_properties'] -
                self.stats_data['available_properties']
            )

            self.update_stats_display()

        except Exception as e:
            logger.error(f"Error loading dashboard data: {e}")

    def update_stats_display(self):
        """Update statistics display with animations"""
        self.stats_grid.clear_widgets()

        stats_config = [
            {
                'title': language_manager.get_text('total_owners'),
                'value': str(self.stats_data.get('total_owners', 0)),
                'icon': 'account-group',
                'color_scheme': 'primary',
                'trend': 'up'
            },
            {
                'title': language_manager.get_text('total_properties'),
                'value': str(self.stats_data.get('total_properties', 0)),
                'icon': 'home-city',
                'color_scheme': 'success',
                'trend': 'up'
            },
            {
                'title': language_manager.get_text('available_properties'),
                'value': str(self.stats_data.get('available_properties', 0)),
                'icon': 'home-outline',
                'color_scheme': 'warning'
            },
            {
                'title': language_manager.get_text('occupied_properties'),
                'value': str(self.stats_data.get('occupied_properties', 0)),
                'icon': 'home',
                'color_scheme': 'error'
            }
        ]

        for config in stats_config:
          stat_card = EnhancedStatsCard(
              title=config['title'],
              value=config['value'],
              icon=config['icon'],
              color_scheme=config['color_scheme'],
              trend=config.get('trend'),
              size_hint_y=None,
              height=dp(100)
          )
          stat_card.opacity = 0
          self.stats_grid.add_widget(stat_card)
          anim = Animation(opacity=1, duration=0.3)
          anim.start(stat_card)

        # Animate in
        anim = Animation(opacity=1, duration=0.3)
        anim.start(stat_card)

    def refresh_stats(self, dt=None):
        """Refresh statistics"""
        self.load_dashboard_data()

    def navigate_to(self, screen_name):
        """Navigate to specific screen"""
        if hasattr(self, 'manager') and self.manager:
            self.manager.current = screen_name

    def show_navigation_drawer(self):
        """Show navigation drawer"""
        # Implementation for navigation drawer
        pass

    def show_settings(self, instance=None):
        """Show settings dialog"""
        from app.views.enhanced_dialogs import SettingsDialog
        dialog = SettingsDialog(self)
        dialog.open()

    def show_recent_activity_dialog(self, instance=None):
        """Show recent activity dialog"""
        from app.views.enhanced_dialogs import RecentActivityDialog
        dialog = RecentActivityDialog(self.db)
        dialog.open()

    def show_profile(self):
        """Show user profile"""
        # Implementation for profile
        pass

    def show_quick_add_menu(self, instance):
        """Show quick add menu"""
        # Implementation for quick add menu
        pass

    def on_enter(self, *args):
        """Called when screen is entered"""
        self.refresh_stats()

    def on_leave(self, *args):
        """Called when leaving screen"""
        pass
