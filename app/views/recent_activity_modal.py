#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Recent Activity Modal Dialog
Completely independent modal dialog component for displaying recent activities
This ensures it always shows as a popup modal, never as a sidebar
"""

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class RecentActivityModalDialog:
    """
    Completely Independent Recent Activity Modal Dialog Component
    Designed to always show as a popup modal dialog, never as a sidebar
    """

    def __init__(self, db_manager=None):
        """
        Initialize the Recent Activity Modal Dialog

        Args:
            db_manager: Database manager instance (optional)
        """
        self.db = db_manager
        self.dialog = None

    def _create_fresh_dialog(self):
        """Create a completely fresh dialog instance"""

        # Create main content container with specific sizing to ensure modal behavior
        main_content = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(500),  # Fixed height to ensure modal appearance
            padding=[dp(20), dp(20), dp(20), dp(10)],
            spacing=dp(15)
        )

        # Header section
        header_label = MDLabel(
            text="Recent System Activities",
            font_style="H6",
            size_hint_y=None,
            height=dp(40),
            halign="center"
        )
        main_content.add_widget(header_label)

        # Activity content card to ensure proper containment
        activity_card = MDCard(
            size_hint_y=None,
            height=dp(400),
            elevation=2,
            padding=dp(10),
            radius=[10, 10, 10, 10]
        )

        # Activity list container
        activity_container = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(380)
        )

        # Scrollable activity list
        scroll_view = MDScrollView()
        activity_list = MDList()

        # Populate with activities
        self._load_activities_into_list(activity_list)

        scroll_view.add_widget(activity_list)
        activity_container.add_widget(scroll_view)
        activity_card.add_widget(activity_container)
        main_content.add_widget(activity_card)

        # Create the modal dialog with specific parameters to ensure modal behavior
        self.dialog = MDDialog(
            title="Recent Activity",
            type="custom",
            content_cls=main_content,
            size_hint=(0.85, None),  # Fixed width, auto height
            height=dp(600),  # Explicit height
            auto_dismiss=True,  # Allow dismissing by clicking outside
            buttons=[
                MDFlatButton(
                    text="Refresh",
                    on_release=self._refresh_activities
                ),
                MDRaisedButton(
                    text="Close",
                    on_release=self._close_dialog
                ),
            ],
        )

        logger.info("Fresh Recent Activity modal dialog created")

    def _load_activities_into_list(self, activity_list):
        """Load activities into the list widget"""
        try:
            activities = self._get_activities_data()

            if not activities:
                # Show empty state
                empty_item = OneLineListItem(
                    text="No recent activities found"
                )
                activity_list.add_widget(empty_item)
                return

            # Add activity items
            for activity in activities:
                if isinstance(activity, dict):
                    # Rich activity data
                    item = TwoLineListItem(
                        text=activity.get('title', 'Unknown Activity'),
                        secondary_text=activity.get('description', 'No description available')
                    )
                else:
                    # Simple string activity
                    item = OneLineListItem(text=str(activity))

                activity_list.add_widget(item)

        except Exception as e:
            logger.error(f"Error loading activities into list: {e}")
            error_item = OneLineListItem(text="Error loading activities - please try again")
            activity_list.add_widget(error_item)

    def _get_activities_data(self):
        """Get activities data from database or sample data"""
        try:
            if self.db:
                return self._get_activities_from_database()
            else:
                return self._get_sample_activities_data()
        except Exception as e:
            logger.error(f"Error getting activities data: {e}")
            return self._get_sample_activities_data()

    def _get_activities_from_database(self):
        """Get real activities from database"""
        try:
            # Placeholder for real database implementation
            # Replace this with actual database queries based on your schema

            # Example implementation:
            # cursor = self.db.get_cursor()
            # cursor.execute("""
            #     SELECT activity_type, description, created_at
            #     FROM system_activities
            #     ORDER BY created_at DESC
            #     LIMIT 15
            # """)
            # activities = []
            # for row in cursor.fetchall():
            #     activities.append({
            #         'title': row['activity_type'],
            #         'description': f"{row['description']} - {row['created_at']}"
            #     })
            # return activities

            # For now, return sample data
            return self._get_sample_activities_data()

        except Exception as e:
            logger.error(f"Database error while fetching activities: {e}")
            return self._get_sample_activities_data()

    def _get_sample_activities_data(self):
        """Get sample activities data for demonstration"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        return [
            {
                'title': 'Property Added',
                'description': f'New villa added to Downtown area - {current_time}'
            },
            {
                'title': 'Owner Profile Updated',
                'description': f'John Smith\'s contact information modified - {current_time}'
            },
            {
                'title': 'Property Sale Completed',
                'description': f'Apartment on Main Street sold successfully - {current_time}'
            },
            {
                'title': 'System Backup',
                'description': f'Database backup completed successfully - {current_time}'
            },
            {
                'title': 'New User Registration',
                'description': f'New agent registered in the system - {current_time}'
            },
            {
                'title': 'Photos Uploaded',
                'description': f'Property photos uploaded for listing #456 - {current_time}'
            },
            {
                'title': 'Report Generated',
                'description': f'Monthly sales report generated - {current_time}'
            },
            {
                'title': 'Settings Updated',
                'description': f'System preferences modified - {current_time}'
            },
            {
                'title': 'Inquiry Received',
                'description': f'New property inquiry from potential buyer - {current_time}'
            },
            {
                'title': 'Payment Recorded',
                'description': f'Commission payment recorded for property #789 - {current_time}'
            }
        ]

    def _refresh_activities(self, instance):
        """Refresh the activities in the dialog"""
        try:
            if self.dialog and self.dialog.content_cls:
                # Find the activity list and refresh it
                logger.info("Refreshing activities...")
                # For simplicity, close and reopen the dialog
                self._close_dialog(instance)
                self.open()
        except Exception as e:
            logger.error(f"Error refreshing activities: {e}")

    def _close_dialog(self, instance):
        """Close the modal dialog"""
        try:
            if self.dialog:
                self.dialog.dismiss()
                logger.info("Recent Activity modal dialog closed")
        except Exception as e:
            logger.error(f"Error closing Recent Activity modal dialog: {e}")
        finally:
            # Always ensure dialog reference is cleared
            self.dialog = None

    def open(self):
        """Open the Recent Activity modal dialog"""
        try:
            # Ensure any existing dialog is closed first
            if self.dialog:
                self.dialog.dismiss()
                self.dialog = None

            # Create fresh dialog instance
            self._create_fresh_dialog()

            # Open the dialog
            if self.dialog:
                self.dialog.open()
                logger.info("Recent Activity modal dialog opened successfully")
            else:
                logger.error("Failed to create dialog instance")

        except Exception as e:
            logger.error(f"Error opening Recent Activity modal dialog: {e}")

    def close(self):
        """Programmatically close the dialog"""
        self._close_dialog(None)

    def is_open(self):
        """Check if the dialog is currently open"""
        return self.dialog is not None


# Standalone function to show the modal dialog
def show_recent_activity_modal(db_manager=None):
    """
    Standalone function to show Recent Activity as a modal dialog

    Args:
        db_manager: Database manager instance (optional)

    Returns:
        RecentActivityModalDialog: The dialog instance
    """
    try:
        dialog = RecentActivityModalDialog(db_manager)
        dialog.open()
        return dialog
    except Exception as e:
        logger.error(f"Error showing recent activity modal: {e}")
        return None


# Alternative function that guarantees fresh instance every time
def show_fresh_recent_activity_modal(db_manager=None):
    """
    Alternative function that creates a completely fresh modal dialog every time

    Args:
        db_manager: Database manager instance (optional)

    Returns:
        RecentActivityModalDialog: The fresh dialog instance
    """
    try:
        # Always create a new instance
        dialog = RecentActivityModalDialog(db_manager)
        dialog.open()
        logger.info("Fresh Recent Activity modal dialog created and opened")
        return dialog
    except Exception as e:
        logger.error(f"Error creating fresh recent activity modal: {e}")
        return None
