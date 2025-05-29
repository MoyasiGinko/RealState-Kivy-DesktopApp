#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Main Dashboard Screen
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.clock import Clock
import os
import logging

from app.components import (RTLLabel, CustomActionButton as ActionButton, StatsCard)
from app.database import DatabaseManager
from app.font_manager import font_manager

logger = logging.getLogger(__name__)


class DashboardScreen(Screen):
    """Main dashboard screen"""

    def __init__(self, db_manager: DatabaseManager, **kwargs):
        super().__init__(**kwargs)
        self.name = 'dashboard'
        self.db = db_manager

        self.build_ui()

        # Auto-refresh stats every 30 seconds
        Clock.schedule_interval(self.refresh_stats, 30)

    def build_ui(self):
        """Build the dashboard UI"""
        main_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))

        # Header
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80))

        # Logo
        try:
            logo = Image(
                source='app-images/alkawaz-logo.jpg',
                size_hint_x=0.2,
                fit_mode="contain"
            )
            header_layout.add_widget(logo)
        except:
            pass

        # Title
        title_layout = BoxLayout(orientation='vertical', size_hint_x=0.6)
        title_layout.add_widget(RTLLabel(
            text='نظام إدارة العقارات',
            font_size='28sp',
            bold=True
        ))
        title_layout.add_widget(RTLLabel(
            text='Real Estate Management System',
            font_size='16sp'
        ))
        header_layout.add_widget(title_layout)

        # Company info
        try:
            company_logo = Image(
                source='app-images/tbci.jpg',
                size_hint_x=0.2,
                fit_mode="contain"
            )
            header_layout.add_widget(company_logo)
        except:
            pass

        main_layout.add_widget(header_layout)

        # Statistics section
        stats_layout = BoxLayout(orientation='vertical', spacing=dp(10))
        stats_layout.add_widget(RTLLabel(
            text='إحصائيات النظام',
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(40)
        ))

        # Stats cards
        self.stats_container = GridLayout(
            cols=4,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(120)
        )
        stats_layout.add_widget(self.stats_container)

        main_layout.add_widget(stats_layout)

        # Quick actions section
        actions_layout = BoxLayout(orientation='vertical', spacing=dp(10))
        actions_layout.add_widget(RTLLabel(
            text='الإجراءات السريعة',
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(40)
        ))

        # Action buttons grid
        actions_grid = GridLayout(
            cols=3,
            spacing=dp(20),
            size_hint_y=None,
            height=dp(200)
        )

        # Create action buttons
        action_buttons = [
            {
                'text': 'إدارة الملاك',
                'icon': 'app-images/insert.jpg',
                'screen': 'owners',
                'color': [0.2, 0.7, 0.3, 1]
            },
            {
                'text': 'إدارة العقارات',
                'icon': 'app-images/update.jpg',
                'screen': 'properties',
                'color': [0.2, 0.4, 0.8, 1]
            },
            {
                'text': 'البحث والتقارير',
                'icon': 'app-images/browse.jpg',
                'screen': 'search',
                'color': [0.8, 0.5, 0.2, 1]
            }
        ]

        for btn_info in action_buttons:
            btn_layout = BoxLayout(orientation='vertical', spacing=dp(10))

            # Icon
            try:
                icon = Image(
                    source=btn_info['icon'],
                    size_hint_y=0.7,
                    fit_mode="contain"
                )
                btn_layout.add_widget(icon)
            except:
                pass

            # Button
            action_btn = ActionButton(
                text=btn_info['text'],
                action=lambda screen=btn_info['screen']: self.navigate_to_screen(screen),
                button_type='primary',
                size_hint_y=0.3
            )
            action_btn.background_color = btn_info['color']
            btn_layout.add_widget(action_btn)

            actions_grid.add_widget(btn_layout)

        actions_layout.add_widget(actions_grid)
        main_layout.add_widget(actions_layout)

        # Recent activity section
        recent_layout = BoxLayout(orientation='vertical', spacing=dp(10))
        recent_layout.add_widget(RTLLabel(
            text='النشاط الأخير',
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(40)
        ))

        # Recent properties scroll view
        self.recent_scroll = ScrollView()
        self.recent_container = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint_y=None
        )
        self.recent_container.bind(minimum_height=self.recent_container.setter('height'))
        self.recent_scroll.add_widget(self.recent_container)
        recent_layout.add_widget(self.recent_scroll)

        main_layout.add_widget(recent_layout)

        # Footer
        footer = RTLLabel(
            text='تطوير: لؤي القواز - Real Estate Management System v1.0.0',
            font_size='12sp',
            size_hint_y=None,
            height=dp(30)
        )
        main_layout.add_widget(footer)

        self.add_widget(main_layout)

        # Load initial data
        self.refresh_stats()
        self.load_recent_properties()

    def refresh_stats(self, *args):
        """Refresh statistics display"""
        try:
            stats = self.db.get_statistics()

            # Clear existing stats
            self.stats_container.clear_widgets()

            # Create stats cards
            stats_data = [
                {
                    'title': 'إجمالي الملاك',
                    'value': str(stats.get('total_owners', 0)),
                    'color': [0.2, 0.7, 0.3, 1]
                },
                {
                    'title': 'إجمالي العقارات',
                    'value': str(stats.get('total_properties', 0)),
                    'color': [0.2, 0.4, 0.8, 1]
                },
                {
                    'title': 'عقارات للبيع',
                    'value': str(self.count_by_offer_type(stats, '03001')),
                    'color': [0.8, 0.5, 0.2, 1]
                },
                {
                    'title': 'عقارات للإيجار',
                    'value': str(self.count_by_offer_type(stats, '03002')),
                    'color': [0.7, 0.3, 0.7, 1]
                }
            ]

            for stat in stats_data:
                card = StatsCard(**stat)
                self.stats_container.add_widget(card)

        except Exception as e:
            logger.error(f"Error refreshing stats: {e}")

    def count_by_offer_type(self, stats: dict, offer_code: str) -> int:
        """Count properties by offer type"""
        properties_by_offer = stats.get('properties_by_offer', [])
        for code, name, count in properties_by_offer:
            if code == offer_code:
                return count
        return 0

    def load_recent_properties(self):
        """Load recent properties"""
        try:
            # Get recent properties (limit to 5)
            properties = self.db.get_properties()[:5]

            self.recent_container.clear_widgets()

            if not properties:
                no_data = RTLLabel(
                    text='لا توجد عقارات مسجلة',
                    size_hint_y=None,
                    height=dp(40)
                )
                self.recent_container.add_widget(no_data)
                return

            for prop in properties:
                # Create property card
                prop_layout = BoxLayout(
                    orientation='horizontal',
                    spacing=dp(10),
                    size_hint_y=None,
                    height=dp(60),
                    padding=dp(10)
                )

                # Property info
                info_layout = BoxLayout(orientation='vertical', size_hint_x=0.8)

                # Property name/address
                name_label = RTLLabel(
                    text=prop.get('Property-address', 'عقار بدون عنوان')[:50],
                    font_size='14sp',
                    bold=True
                )
                info_layout.add_widget(name_label)

                # Property details
                details = f"المالك: {prop.get('ownername', 'غير محدد')} | "
                details += f"المساحة: {prop.get('Property-area', 0)} م²"

                details_label = RTLLabel(
                    text=details,
                    font_size='12sp'
                )
                info_layout.add_widget(details_label)

                prop_layout.add_widget(info_layout)

                # View button
                view_btn = ActionButton(
                    text='عرض',
                    size_hint_x=0.2,
                    action=lambda p=prop: self.view_property(p)
                )
                prop_layout.add_widget(view_btn)

                self.recent_container.add_widget(prop_layout)

        except Exception as e:
            logger.error(f"Error loading recent properties: {e}")

    def navigate_to_screen(self, screen_name: str):
        """Navigate to specified screen"""
        try:
            self.manager.current = screen_name
        except Exception as e:
            logger.error(f"Error navigating to screen {screen_name}: {e}")

    def view_property(self, property_data: dict):
        """View property details"""
        try:
            # Store property data for the properties screen
            if hasattr(self.manager, 'get_screen'):
                props_screen = self.manager.get_screen('properties')
                if hasattr(props_screen, 'load_property_data'):
                    props_screen.load_property_data(property_data)

            self.navigate_to_screen('properties')
        except Exception as e:
            logger.error(f"Error viewing property: {e}")

    def on_enter(self, *args):
        """Called when screen is entered"""
        # Refresh data when entering screen
        self.refresh_stats()
        self.load_recent_properties()
