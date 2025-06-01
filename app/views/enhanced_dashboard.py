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
from app.utils import BilingualLabel, LanguageSwitcher
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

        self.build_modern_ui()        # Schedule data loading
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

        # Scrollable content with improved spacing
        scroll = MDScrollView()
        content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['xl'],  # Increased spacing between sections
            padding=[DesignTokens.SPACING['lg'], DesignTokens.SPACING['md'], DesignTokens.SPACING['lg'], DesignTokens.SPACING['md']],
            adaptive_height=True
        )

        # Welcome section
        self.build_welcome_section(content_layout)

        # Statistics section
        self.build_stats_section(content_layout)        # Quick actions section
        self.build_quick_actions_section(content_layout)

        scroll.add_widget(content_layout)
        main_container.add_widget(scroll)


        self.add_widget(main_container)

    def build_app_bar(self, parent):
        """Build modern app bar with actions"""
        app_bar = MDTopAppBar(
            title="Real Estate Dashboard",
            md_bg_color=DesignTokens.COLORS['primary'],
            specific_text_color=DesignTokens.COLORS['card'],
            left_action_items=[["home", lambda x: self.navigate_to_welcome()]],
            right_action_items=[
                ["refresh", lambda x: self.refresh_stats()],
                ["cog", lambda x: self.show_settings()]
                # Removed the profile button (["account-circle", ...])
            ]
        )
        parent.add_widget(app_bar)


    def build_welcome_section(self, parent):
        """Build welcome hero section with improved spacing and responsiveness"""
        # Outer container for spacing below the card
        outer_container = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(200),  # Increased height for better fit
            padding=[0, 0, 0, DesignTokens.SPACING['md']],
            spacing=DesignTokens.SPACING['sm'],
            adaptive_height=False
        )

        welcome_card = ModernCard(
            md_bg_color=DesignTokens.COLORS['primary'],
            size_hint_y=None,
            height=dp(180),  # Increased height for better content fitting
            radius=DesignTokens.RADIUS['lg'],
            padding=[0, 0, 0, 0]
        )

        welcome_content = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['xl'],
            padding=[
                DesignTokens.SPACING['xl'],
                DesignTokens.SPACING['lg'],
                DesignTokens.SPACING['xl'],
                DesignTokens.SPACING['lg']
            ],
            adaptive_height=True
        )

        # Welcome text container with proper sizing and responsiveness
        text_layout = MDBoxLayout(
            orientation='vertical',
            size_hint_x=0.7,
            spacing=DesignTokens.SPACING['md'],
            adaptive_height=True
        )

        welcome_title = MDLabel(
            text=language_manager.get_text('welcome_dashboard'),
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['card'],
            font_style="H4",
            bold=True,
            size_hint_y=None,
            height=dp(44),
            text_size=(None, None),
            halign="left",
            valign="top"
        )
        text_layout.add_widget(welcome_title)

        welcome_subtitle = MDLabel(
            text=language_manager.get_text('dashboard_subtitle'),
            theme_text_color="Custom",
            text_color=(DesignTokens.COLORS['card'][0], DesignTokens.COLORS['card'][1], DesignTokens.COLORS['card'][2], 0.85),
            font_style="Body1",
            size_hint_y=None,
            height=dp(56),
            text_size=(dp(320), None),
            halign="left",
            valign="top"
        )
        text_layout.add_widget(welcome_subtitle)

        welcome_content.add_widget(text_layout)

        # Language switcher container with vertical centering
        lang_container = MDBoxLayout(
            orientation='vertical',
            size_hint_x=0.3,
            adaptive_height=True,
            spacing=DesignTokens.SPACING['md'],
            padding=[0, dp(18), 0, 0]
        )

        lang_switcher = LanguageSwitcher(
            size_hint=(None, None),
            size=(dp(140), dp(48)),
            pos_hint={'center_x': 0.5}
        )
        lang_container.add_widget(lang_switcher)

        welcome_content.add_widget(lang_container)
        welcome_card.add_widget(welcome_content)
        outer_container.add_widget(welcome_card)

        # Add extra spacing below the card for visual separation
        outer_container.add_widget(
            MDLabel(size_hint_y=None, height=DesignTokens.SPACING['md'])
        )

        parent.add_widget(outer_container)

    def build_stats_section(self, parent):
        """Build enhanced statistics section"""
        # Section container with proper spacing
        stats_container = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(300),  # Increased height for better stats display
            spacing=DesignTokens.SPACING['md']
        )

        # Section header
        stats_header = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),  # Increased header height
            spacing=DesignTokens.SPACING['sm'],
            padding=[0, DesignTokens.SPACING['sm']]
        )

        stats_title = MDLabel(
            text=language_manager.get_text('system_statistics'),
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_primary'],
            font_style="H5",
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )
        stats_header.add_widget(stats_title)

        refresh_btn = MDIconButton(
            icon="refresh",
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['primary'],
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            on_release=lambda x: self.refresh_stats()
        )
        stats_header.add_widget(refresh_btn)

        stats_container.add_widget(stats_header)

        # Stats grid with improved sizing
        self.stats_grid = MDGridLayout(
            cols=2,  # Responsive: 2 cols on mobile, 4 on desktop
            spacing=DesignTokens.SPACING['lg'],
            size_hint_y=None,            height=dp(240),  # Increased height for better card display
            padding=[DesignTokens.SPACING['sm'], 0]
        )

        stats_container.add_widget(self.stats_grid)
        parent.add_widget(stats_container)

    def build_quick_actions_section(self, parent):
        """Build quick actions navigation section"""
        # Section container with proper spacing
        actions_container = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=DesignTokens.SPACING['md'],
            adaptive_height=True
        )

        # Section header with improved styling
        actions_header = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=DesignTokens.SPACING['sm'],
            padding=[0, DesignTokens.SPACING['sm']]
        )

        actions_title = MDLabel(
            text=language_manager.get_text('quick_actions'),
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_primary'],
            font_style="H5",
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )
        actions_header.add_widget(actions_title)
        actions_container.add_widget(actions_header)        # Actions grid with improved layout
        actions_grid = MDGridLayout(
            cols=1,  # Stack vertically for better mobile experience
            spacing=DesignTokens.SPACING['lg'],  # Increased spacing between cards
            size_hint_y=None,
            adaptive_height=True,
            padding=[DesignTokens.SPACING['sm'], 0]
        )

        # Navigation cards
        navigation_items = [
            {
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
                'action': lambda: self.navigate_to('enhanced_search'),                'color_scheme': 'warning'
            },            {
                'title': language_manager.get_text('settings'),
                'subtitle': language_manager.get_text('app_settings'),
                'icon': 'cog',
                'action': self.show_settings,
                'color_scheme': 'secondary'
            },
            {
                'title': language_manager.get_text('recent_activity'),
                'subtitle': language_manager.get_text('view_recent_activity'),
                'icon': 'history',
                'action': self.show_recent_activity,
                'color_scheme': 'info'
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
                height=dp(90)  # Increased height for better visual balance
            )
            actions_grid.add_widget(nav_card)

        actions_container.add_widget(actions_grid)
        parent.add_widget(actions_container)

    def build_fab(self, parent):
        """Build floating action button with improved positioning"""
        fab = MDFloatingActionButton(
            icon="plus",
            md_bg_color=DesignTokens.COLORS['secondary'],
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['card'],
            pos_hint={'center_x': 0.85, 'center_y': 0.12},  # Better positioning
            size_hint=(None, None),
            size=(dp(56), dp(56)),  # Standard FAB size
            elevation=6,
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
            },            {
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
                height=dp(110)  # Increased height for better visual balance
            )

            stat_card.opacity = 0
            self.stats_grid.add_widget(stat_card)

            # Animate each card with staggered timing
            Clock.schedule_once(
                lambda dt, card=stat_card: Animation(opacity=1, duration=0.3).start(card),
                len(self.stats_grid.children) * 0.1
            )

    def refresh_stats(self, dt=None):
        """Refresh statistics"""
        self.load_dashboard_data()

    def navigate_to(self, screen_name):
        """Navigate to specific screen"""
        if hasattr(self, 'manager') and self.manager:
            self.manager.current = screen_name

    def navigate_to_welcome(self, instance=None):
        """Navigate to welcome/home screen"""
        if hasattr(self, 'manager') and self.manager:
            # Navigate to the welcome screen
            self.manager.current = 'welcome'

    def scroll_to_top(self):
        """Scroll the dashboard to the top to show welcome section"""
        try:
            # Find the scroll view in the widget tree
            for widget in self.walk():
                if isinstance(widget, MDScrollView):
                    widget.scroll_y = 1  # Scroll to top
                    break
        except Exception as e:
            logger.error(f"Error scrolling to top: {e}")

    def show_navigation_drawer(self):
        """Show navigation drawer"""        # Implementation for navigation drawer
        pass

    def show_settings(self, instance=None):
        """Show settings dialog"""
        from app.views.enhanced_dialogs import SettingsDialog
        dialog = SettingsDialog(self)
        dialog.open()

    def show_recent_activity(self, instance=None):
        """Show recent activity modal dialog"""
        try:
            from app.views.recent_activity_modal import show_fresh_recent_activity_modal
            # Use the new modal dialog component that ensures proper modal behavior
            dialog = show_fresh_recent_activity_modal(self.db)
            if dialog:
                logger.info("Recent Activity modal dialog opened successfully")
            else:
                logger.error("Failed to open Recent Activity modal dialog")
        except Exception as e:
            logger.error(f"Error opening Recent Activity modal dialog: {e}")

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
