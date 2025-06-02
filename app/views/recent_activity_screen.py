#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Recent Activity Screen (Dashboard Item #6)
Implementation according to Project Guideline - View last actions with timestamp, action type, property code
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, ThreeLineListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
from kivy.clock import Clock
import logging
from datetime import datetime
from typing import Dict, Any, List

from app.views.modern_components import (
    DesignTokens, ModernCard, EnhancedStatsCard, ModernButton, ModernSnackbar
)
from app.database import DatabaseManager
from app.language_manager import language_manager
from app.utils import BilingualLabel

logger = logging.getLogger(__name__)


class RecentActivityScreen(MDScreen):
    """Recent Activity Screen - Dashboard Item #6 according to Project Guideline"""

    def __init__(self, db_manager: DatabaseManager, **kwargs):
        super().__init__(**kwargs)
        self.name = 'recent_activity'
        self.db = db_manager
        self.integration_layer = None
        self.activities_data = []

        self.build_ui()
        self.load_activities()

        # Auto-refresh activities every 10 seconds
        Clock.schedule_interval(self.refresh_activities, 10)

    def set_integration_layer(self, integration_layer):
        """Set the integration layer for advanced functionality"""
        self.integration_layer = integration_layer
        logger.info("Integration layer connected to recent activity screen")

    def build_ui(self):
        """Build the recent activity UI according to Project Guideline requirements"""
        # Main container
        main_container = MDBoxLayout(
            orientation='vertical',
            md_bg_color=DesignTokens.COLORS['background']
        )

        # Top App Bar
        app_bar = MDTopAppBar(
            title="Recent Activity",
            md_bg_color=DesignTokens.COLORS['primary'],
            specific_text_color=DesignTokens.COLORS['card'],
            left_action_items=[["arrow-left", lambda x: self.navigate_back()]],
            right_action_items=[
                ["refresh", lambda x: self.refresh_activities()],
                ["export", lambda x: self.export_activities()]
            ]
        )
        main_container.add_widget(app_bar)

        # Scrollable content
        scroll = MDScrollView()
        content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['md'],
            padding=[DesignTokens.SPACING['md'], DesignTokens.SPACING['md']],
            adaptive_height=True
        )

        # Header stats
        self.build_activity_stats(content_layout)

        # Activity filter controls
        self.build_filter_controls(content_layout)

        # Activities list
        self.build_activities_list(content_layout)

        scroll.add_widget(content_layout)
        main_container.add_widget(scroll)
        self.add_widget(main_container)

    def build_activity_stats(self, parent):
        """Build activity statistics cards"""
        stats_container = MDGridLayout(
            cols=3,
            spacing=DesignTokens.SPACING['md'],
            size_hint_y=None,
            height=dp(120),
            adaptive_height=True
        )        # Today's activities
        self.today_activities_card = EnhancedStatsCard(
            title="Today's Activities",
            value="0",
            icon="calendar-today",
            color_scheme='success'
        )
        stats_container.add_widget(self.today_activities_card)

        # Property operations
        self.property_ops_card = EnhancedStatsCard(
            title="Property Operations",
            value="0",
            icon="home-variant",
            color_scheme='primary'
        )
        stats_container.add_widget(self.property_ops_card)

        # Owner operations
        self.owner_ops_card = EnhancedStatsCard(
            title="Owner Operations",
            value="0",
            icon="account-group",
            color_scheme='warning'
        )
        stats_container.add_widget(self.owner_ops_card)

        parent.add_widget(stats_container)

    def build_filter_controls(self, parent):
        """Build filter controls for activities"""
        filter_card = ModernCard(
            padding=DesignTokens.SPACING['md'],
            size_hint_y=None,
            height=dp(80)
        )

        filter_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['md'],
            adaptive_height=True
        )

        # Filter buttons
        filter_buttons = [
            ("All", "view-list", self.filter_all),
            ("Properties", "home", self.filter_properties),
            ("Owners", "account", self.filter_owners),
            ("System", "cog", self.filter_system)
        ]

        for text, icon, callback in filter_buttons:
            btn = ModernButton(
                text=text,
                icon=icon,
                size_hint_x=0.25,
                on_release=callback
            )
            filter_layout.add_widget(btn)

        filter_card.add_widget(filter_layout)
        parent.add_widget(filter_card)

    def build_activities_list(self, parent):
        """Build the activities list according to Project Guideline"""
        # Activities container
        activities_card = ModernCard(
            padding=DesignTokens.SPACING['sm']
        )

        activities_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['sm']
        )

        # Header
        header_label = MDLabel(
            text="Recent Activities",
            font_style="H6",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(40)
        )
        activities_layout.add_widget(header_label)

        # Activities list
        self.activities_list = MDList()
        activities_scroll = MDScrollView(
            size_hint_y=None,
            height=dp(400)
        )
        activities_scroll.add_widget(self.activities_list)
        activities_layout.add_widget(activities_scroll)

        activities_card.add_widget(activities_layout)
        parent.add_widget(activities_card)

    def load_activities(self):
        """Load activities from database according to Project Guideline requirements"""
        try:
            # Get activities from database or integration layer
            if self.integration_layer:
                self.activities_data = self.integration_layer.get_recent_activities()
            else:
                self.activities_data = self.get_activities_from_db()

            self.update_activities_list()
            self.update_activity_stats()

        except Exception as e:
            logger.error(f"Error loading activities: {e}")
            self.show_error("Failed to load activities")

    def get_activities_from_db(self) -> List[Dict]:
        """Get activities from database - Project Guideline format"""
        activities = []

        try:
            # Get recent property operations
            conn = self.db.get_connection()
            cursor = conn.cursor()

            # Recent property additions
            cursor.execute("""
                SELECT Companyco, realstatecode, created_date, 'Property Added' as action_type
                FROM Realstatspecification
                ORDER BY created_date DESC
                LIMIT 20
            """)

            for row in cursor.fetchall():
                activities.append({
                    'timestamp': row[2] or datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'action_type': row[3],
                    'property_code': row[1] or row[0],
                    'description': f"Property {row[1] or row[0]} was added to the system",
                    'category': 'property',
                    'performed_by': 'System User'  # Optional field from guideline
                })

            # Recent owner additions
            cursor.execute("""
                SELECT Ownercode, ownername, created_date, 'Owner Added' as action_type
                FROM Owners
                ORDER BY created_date DESC
                LIMIT 20
            """)

            for row in cursor.fetchall():
                activities.append({
                    'timestamp': row[2] or datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'action_type': row[3],
                    'property_code': row[0],  # Owner code as reference
                    'description': f"Owner {row[1]} ({row[0]}) was added to the system",
                    'category': 'owner',
                    'performed_by': 'System User'
                })

            conn.close()

            # Sort by timestamp
            activities.sort(key=lambda x: x['timestamp'], reverse=True)

            logger.info(f"Loaded {len(activities)} activities from database")
            return activities

        except Exception as e:
            logger.error(f"Error getting activities from database: {e}")
            return []

    def update_activities_list(self):
        """Update the activities list display"""
        self.activities_list.clear_widgets()

        if not self.activities_data:
            # Empty state
            empty_item = ThreeLineListItem(
                text="No activities found",
                secondary_text="No recent activities to display",
                tertiary_text="Start by adding properties or owners"
            )
            self.activities_list.add_widget(empty_item)
            return

        # Add activity items according to Project Guideline format
        for activity in self.activities_data:
            # Create activity item with required fields from guideline
            timestamp = activity.get('timestamp', 'Unknown time')
            action_type = activity.get('action_type', 'Unknown action')
            property_code = activity.get('property_code', 'N/A')
            description = activity.get('description', 'No description')
            performed_by = activity.get('performed_by', 'Unknown user')

            # Icon based on category
            icon_name = self.get_activity_icon(activity.get('category', 'system'))

            activity_item = ThreeLineListItem(
                text=f"{action_type} - {property_code}",
                secondary_text=description,
                tertiary_text=f"{timestamp} | By: {performed_by}",
                on_release=lambda x, activity=activity: self.view_activity_details(activity)
            )

            # Add icon
            icon_widget = IconLeftWidget(
                icon=icon_name,
                theme_icon_color="Custom",
                icon_color=self.get_activity_color(activity.get('category', 'system'))
            )
            activity_item.add_widget(icon_widget)

            # Add action button
            action_widget = IconRightWidget(
                icon="chevron-right",
                on_release=lambda x, activity=activity: self.view_activity_details(activity)
            )
            activity_item.add_widget(action_widget)

            self.activities_list.add_widget(activity_item)

    def get_activity_icon(self, category: str) -> str:
        """Get icon based on activity category"""
        icons = {
            'property': 'home-variant',
            'owner': 'account',
            'system': 'cog',
            'photo': 'camera',
            'search': 'magnify',
            'export': 'download'
        }
        return icons.get(category, 'information')

    def get_activity_color(self, category: str) -> list:
        """Get color based on activity category"""
        colors = {
            'property': DesignTokens.COLORS['primary'],
            'owner': DesignTokens.COLORS['success'],
            'system': DesignTokens.COLORS['info'],
            'photo': DesignTokens.COLORS['warning']
        }
        return colors.get(category, [0.5, 0.5, 0.5, 1])

    def update_activity_stats(self):
        """Update activity statistics"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')

            # Count today's activities
            today_count = sum(1 for activity in self.activities_data
                            if activity.get('timestamp', '').startswith(today))

            # Count property operations
            property_count = sum(1 for activity in self.activities_data
                               if activity.get('category') == 'property')

            # Count owner operations
            owner_count = sum(1 for activity in self.activities_data
                            if activity.get('category') == 'owner')

            # Update cards
            self.today_activities_card.update_value(str(today_count))
            self.property_ops_card.update_value(str(property_count))
            self.owner_ops_card.update_value(str(owner_count))

        except Exception as e:
            logger.error(f"Error updating activity stats: {e}")

    def refresh_activities(self, dt=None):
        """Refresh activities data"""
        self.load_activities()

    def filter_all(self, instance):
        """Show all activities"""
        self.update_activities_list()

    def filter_properties(self, instance):
        """Filter property activities"""
        filtered = [a for a in self.activities_data if a.get('category') == 'property']
        self.show_filtered_activities(filtered)

    def filter_owners(self, instance):
        """Filter owner activities"""
        filtered = [a for a in self.activities_data if a.get('category') == 'owner']
        self.show_filtered_activities(filtered)

    def filter_system(self, instance):
        """Filter system activities"""
        filtered = [a for a in self.activities_data if a.get('category') == 'system']
        self.show_filtered_activities(filtered)

    def show_filtered_activities(self, filtered_activities):
        """Show filtered activities"""
        original_data = self.activities_data
        self.activities_data = filtered_activities
        self.update_activities_list()
        self.activities_data = original_data

    def view_activity_details(self, activity):
        """View detailed information about an activity"""
        try:
            details_text = f"""
Activity Details:

Action Type: {activity.get('action_type', 'N/A')}
Property/Reference Code: {activity.get('property_code', 'N/A')}
Timestamp: {activity.get('timestamp', 'N/A')}
Performed By: {activity.get('performed_by', 'N/A')}
Category: {activity.get('category', 'N/A')}

Description:
{activity.get('description', 'No description available')}
            """

            ModernSnackbar.show_info(f"Activity: {activity.get('action_type', 'Unknown')}")

        except Exception as e:
            logger.error(f"Error showing activity details: {e}")

    def export_activities(self):
        """Export activities to file"""
        try:
            if self.integration_layer:
                result = self.integration_layer.export_activities()
                if result:
                    ModernSnackbar.show_success("Activities exported successfully")
                else:
                    ModernSnackbar.show_error("Export failed")
            else:
                ModernSnackbar.show_info("Export functionality not available")

        except Exception as e:
            logger.error(f"Error exporting activities: {e}")
            ModernSnackbar.show_error("Export failed")

    def navigate_back(self):
        """Navigate back to dashboard"""
        try:
            if self.manager:
                self.manager.current = 'enhanced_dashboard'
        except Exception as e:
            logger.error(f"Error navigating back: {e}")

    def show_error(self, message: str):
        """Show error message"""
        ModernSnackbar.show_error(message)

    def get_recent_activities(self) -> List[Dict]:
        """Get recent activities - interface method"""
        return self.activities_data

    def on_enter(self):
        """Called when screen is entered"""
        self.refresh_activities()
