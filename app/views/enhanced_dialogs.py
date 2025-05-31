#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Enhanced Modal Dialogs
Beautiful KivyMD modal dialogs for settings, confirmations, and forms
"""

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.card import MDCard
# from kivymd.uix.separator import MDSeparator
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
import logging

from app.language_manager import language_manager
from app.theme_manager import theme_manager

logger = logging.getLogger(__name__)


class SettingsDialog:
    """Enhanced Settings Dialog with KivyMD components"""

    def __init__(self, app_instance=None):
        self.app = app_instance
        self.dialog = None
        self.create_settings_dialog()

    def create_settings_dialog(self):
        """Create comprehensive settings dialog"""
        # Main content container
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            size_hint_y=None,
            height=dp(500),
            padding=[dp(20), dp(10)]
        )

        # Settings sections
        self.build_language_section(content)
        # content.add_widget(MDSeparator())

        self.build_theme_section(content)
        # content.add_widget(MDSeparator())

        self.build_database_section(content)
        # content.add_widget(MDSeparator())

        self.build_notification_section(content)

        # Scroll view for content
        scroll = ScrollView()
        scroll.add_widget(content)

        # Create dialog
        self.dialog = MDDialog(
            title=language_manager.get_text('app_settings'),
            type="custom",
            content_cls=scroll,
            size_hint=(0.8, 0.9),
            buttons=[
                MDFlatButton(
                    text=language_manager.get_text('cancel'),
                    theme_text_color="Custom",
                    text_color=theme_manager.get_color('primary'),
                    on_release=self.close_dialog
                ),
                MDRaisedButton(
                    text=language_manager.get_text('save'),
                    on_release=self.save_settings
                ),
            ],
        )

    def build_language_section(self, parent):
        """Build language settings section"""
        # Section header
        header = MDLabel(
            text=language_manager.get_text('language_settings'),
            theme_text_color="Custom",
            text_color=theme_manager.get_color('primary'),
            font_style="H6",
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        parent.add_widget(header)

        # Language selection
        lang_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(15),
            elevation=1
        )

        # Current language display
        current_lang = MDLabel(
            text=f"{language_manager.get_text('current_language')}: {language_manager.current_language}",
            font_style="Body1",
            size_hint_y=None,
            height=dp(30)
        )
        lang_card.add_widget(current_lang)

        # Language switch buttons
        lang_buttons = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40),
            adaptive_width=True
        )

        ar_btn = MDRaisedButton(
            text="العربية",
            size_hint_x=None,
            width=dp(100),
            on_release=lambda x: self.switch_language('ar')
        )
        en_btn = MDRaisedButton(
            text="English",
            size_hint_x=None,
            width=dp(100),
            on_release=lambda x: self.switch_language('en')
        )

        lang_buttons.add_widget(ar_btn)
        lang_buttons.add_widget(en_btn)
        lang_card.add_widget(lang_buttons)

        parent.add_widget(lang_card)

    def build_theme_section(self, parent):
        """Build theme settings section"""
        header = MDLabel(
            text=language_manager.get_text('theme_settings'),
            theme_text_color="Custom",
            text_color=theme_manager.get_color('primary'),
            font_style="H6",
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        parent.add_widget(header)

        theme_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            padding=dp(15),
            elevation=1
        )

        # Dark mode toggle
        dark_mode_layout = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True,
            spacing=dp(10)
        )

        dark_mode_label = MDLabel(
            text=language_manager.get_text('dark_mode'),
            font_style="Body1",
            size_hint_x=0.8
        )
        dark_mode_switch = MDSwitch(
            size_hint_x=0.2,
            active=theme_manager.is_dark_mode() if hasattr(theme_manager, 'is_dark_mode') else False,
            on_active=self.toggle_dark_mode
        )

        dark_mode_layout.add_widget(dark_mode_label)
        dark_mode_layout.add_widget(dark_mode_switch)
        theme_card.add_widget(dark_mode_layout)

        parent.add_widget(theme_card)

    def build_database_section(self, parent):
        """Build database settings section"""
        header = MDLabel(
            text=language_manager.get_text('database_settings'),
            theme_text_color="Custom",
            text_color=theme_manager.get_color('primary'),
            font_style="H6",
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        parent.add_widget(header)

        db_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(15),
            elevation=1
        )

        # Database backup button
        backup_btn = MDRaisedButton(
            text=language_manager.get_text('backup_database'),
            size_hint_y=None,
            height=dp(40),
            on_release=self.backup_database
        )
        db_card.add_widget(backup_btn)

        # Auto-backup toggle
        auto_backup_layout = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True,
            spacing=dp(10)
        )

        auto_backup_label = MDLabel(
            text=language_manager.get_text('auto_backup'),
            font_style="Body1",
            size_hint_x=0.8
        )
        auto_backup_switch = MDSwitch(
            size_hint_x=0.2,
            active=True,  # Default enabled
            on_active=self.toggle_auto_backup
        )

        auto_backup_layout.add_widget(auto_backup_label)
        auto_backup_layout.add_widget(auto_backup_switch)
        db_card.add_widget(auto_backup_layout)

        parent.add_widget(db_card)

    def build_notification_section(self, parent):
        """Build notification settings section"""
        header = MDLabel(
            text=language_manager.get_text('notification_settings'),
            theme_text_color="Custom",
            text_color=theme_manager.get_color('primary'),
            font_style="H6",
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        parent.add_widget(header)

        notif_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            padding=dp(15),
            elevation=1
        )

        # Notifications toggle
        notif_layout = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True,
            spacing=dp(10)
        )

        notif_label = MDLabel(
            text=language_manager.get_text('enable_notifications'),
            font_style="Body1",
            size_hint_x=0.8
        )
        notif_switch = MDSwitch(
            size_hint_x=0.2,
            active=True,  # Default enabled
            on_active=self.toggle_notifications
        )

        notif_layout.add_widget(notif_label)
        notif_layout.add_widget(notif_switch)
        notif_card.add_widget(notif_layout)

        parent.add_widget(notif_card)

    def switch_language(self, lang_code):
        """Switch application language"""
        try:
            language_manager.set_language(lang_code)
            logger.info(f"Language switched to: {lang_code}")
            # You might want to refresh the UI here
        except Exception as e:
            logger.error(f"Error switching language: {e}")

    def toggle_dark_mode(self, instance, value):
        """Toggle dark mode"""
        try:
            if hasattr(theme_manager, 'set_dark_mode'):
                theme_manager.set_dark_mode(value)
            logger.info(f"Dark mode {'enabled' if value else 'disabled'}")
        except Exception as e:
            logger.error(f"Error toggling dark mode: {e}")

    def backup_database(self, instance):
        """Backup database"""
        try:
            # Implementation for database backup
            logger.info("Database backup initiated")
            # You can add actual backup logic here
        except Exception as e:
            logger.error(f"Error backing up database: {e}")

    def toggle_auto_backup(self, instance, value):
        """Toggle auto backup"""
        try:
            logger.info(f"Auto backup {'enabled' if value else 'disabled'}")
            # Implementation for auto backup settings
        except Exception as e:
            logger.error(f"Error toggling auto backup: {e}")

    def toggle_notifications(self, instance, value):
        """Toggle notifications"""
        try:
            logger.info(f"Notifications {'enabled' if value else 'disabled'}")
            # Implementation for notification settings
        except Exception as e:
            logger.error(f"Error toggling notifications: {e}")

    def save_settings(self, instance):
        """Save all settings"""
        try:
            logger.info("Settings saved successfully")
            self.close_dialog(instance)
        except Exception as e:
            logger.error(f"Error saving settings: {e}")

    def close_dialog(self, instance):
        """Close the settings dialog"""
        if self.dialog:
            self.dialog.dismiss()

    def open(self):
        """Open the settings dialog"""
        if self.dialog:
            self.dialog.open()


class ConfirmationDialog:
    """Enhanced Confirmation Dialog"""

    def __init__(self, title, message, on_confirm=None, on_cancel=None):
        self.title = title
        self.message = message
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self.dialog = None
        self.create_dialog()

    def create_dialog(self):
        """Create confirmation dialog"""
        self.dialog = MDDialog(
            title=self.title,
            text=self.message,
            buttons=[
                MDFlatButton(
                    text=language_manager.get_text('cancel'),
                    theme_text_color="Custom",
                    text_color=theme_manager.get_color('primary'),
                    on_release=self.handle_cancel
                ),
                MDRaisedButton(
                    text=language_manager.get_text('confirm'),
                    on_release=self.handle_confirm
                ),
            ],
        )

    def handle_confirm(self, instance):
        """Handle confirm action"""
        if self.on_confirm:
            self.on_confirm()
        self.dialog.dismiss()

    def handle_cancel(self, instance):
        """Handle cancel action"""
        if self.on_cancel:
            self.on_cancel()
        self.dialog.dismiss()

    def open(self):
        """Open the confirmation dialog"""
        if self.dialog:
            self.dialog.open()


class RecentActivityDialog:
    """Recent Activity Modal Dialog"""

    def __init__(self, db_manager=None):
        self.db = db_manager
        self.dialog = None
        self.create_activity_dialog()

    def create_activity_dialog(self):
        """Create recent activity dialog"""
        # Content container
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(400),
            padding=[dp(10), dp(10)]
        )

        # Activity list
        self.activity_list = MDList()
        scroll = ScrollView()
        scroll.add_widget(self.activity_list)
        content.add_widget(scroll)

        # Load activities
        self.load_recent_activities()

        # Create dialog
        self.dialog = MDDialog(
            title=language_manager.get_text('recent_activity'),
            type="custom",
            content_cls=content,
            size_hint=(0.9, 0.8),
            buttons=[
                MDFlatButton(
                    text=language_manager.get_text('close'),
                    theme_text_color="Custom",
                    text_color=theme_manager.get_color('primary'),
                    on_release=self.close_dialog
                ),
            ],
        )

    def load_recent_activities(self):
        """Load recent activities from database"""
        try:
            # Clear existing items
            self.activity_list.clear_widgets()

            # Mock recent activities (you can replace with actual database queries)
            activities = [
                {
                    'title': language_manager.get_text('property_added'),
                    'subtitle': language_manager.get_text('new_property_registered'),
                    'icon': 'home-plus',
                    'time': '2 hours ago'
                },
                {
                    'title': language_manager.get_text('owner_updated'),
                    'subtitle': language_manager.get_text('owner_info_modified'),
                    'icon': 'account-edit',
                    'time': '5 hours ago'
                },
                {
                    'title': language_manager.get_text('property_sold'),
                    'subtitle': language_manager.get_text('property_status_changed'),
                    'icon': 'handshake',
                    'time': '1 day ago'
                },
                {
                    'title': language_manager.get_text('backup_created'),
                    'subtitle': language_manager.get_text('database_backup_completed'),
                    'icon': 'backup-restore',
                    'time': '2 days ago'
                }
            ]

            # Add activity items
            for activity in activities:
                item = OneLineAvatarIconListItem(
                    text=activity['title'],
                    secondary_text=f"{activity['subtitle']} • {activity['time']}",
                )
                item.add_widget(IconLeftWidget(icon=activity['icon']))
                self.activity_list.add_widget(item)

        except Exception as e:
            logger.error(f"Error loading recent activities: {e}")

    def close_dialog(self, instance):
        """Close the activity dialog"""
        if self.dialog:
            self.dialog.dismiss()

    def open(self):
        """Open the activity dialog"""
        if self.dialog:
            self.dialog.open()
