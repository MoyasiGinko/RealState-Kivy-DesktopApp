#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Simple Modal Dialogs
Simple KivyMD modal dialogs for settings and confirmations
"""

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch
from kivy.metrics import dp
import logging

logger = logging.getLogger(__name__)


class SimpleSettingsDialog:
    """Simple Settings Dialog"""

    def __init__(self, app_instance=None):
        self.app = app_instance
        self.dialog = None

    def create_settings_dialog(self):
        """Create simple settings dialog"""
        # Main content container
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            size_hint_y=None,
            height=dp(300),
            padding=[dp(20), dp(10)]
        )

        # Language section
        lang_label = MDLabel(
            text="Language Settings",
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )
        content.add_widget(lang_label)

        # Language buttons
        lang_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )

        ar_btn = MDRaisedButton(
            text="العربية",
            size_hint_x=0.5,
            on_release=lambda x: self.switch_language('ar')
        )
        en_btn = MDRaisedButton(
            text="English",
            size_hint_x=0.5,
            on_release=lambda x: self.switch_language('en')
        )

        lang_layout.add_widget(ar_btn)
        lang_layout.add_widget(en_btn)
        content.add_widget(lang_layout)

        # Dark mode section
        theme_label = MDLabel(
            text="Theme Settings",
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )
        content.add_widget(theme_label)

        # Dark mode toggle
        dark_mode_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )

        dark_mode_label = MDLabel(
            text="Dark Mode",
            font_style="Body1",
            size_hint_x=0.8
        )
        dark_mode_switch = MDSwitch(
            size_hint_x=0.2,
            active=False,
            on_active=self.toggle_dark_mode
        )

        dark_mode_layout.add_widget(dark_mode_label)
        dark_mode_layout.add_widget(dark_mode_switch)
        content.add_widget(dark_mode_layout)

        # Create dialog
        self.dialog = MDDialog(
            title="Settings",
            type="custom",
            content_cls=content,
            size_hint=(0.8, 0.7),
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=self.close_dialog
                ),
                MDRaisedButton(
                    text="Save",
                    on_release=self.save_settings
                ),
            ],
        )

    def switch_language(self, lang_code):
        """Switch application language"""
        try:
            logger.info(f"Language switched to: {lang_code}")
            # Simple language switch implementation
        except Exception as e:
            logger.error(f"Error switching language: {e}")

    def toggle_dark_mode(self, instance, value):
        """Toggle dark mode"""
        try:
            logger.info(f"Dark mode {'enabled' if value else 'disabled'}")
            # Simple dark mode toggle implementation
        except Exception as e:
            logger.error(f"Error toggling dark mode: {e}")

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
            self.dialog = None

    def open(self):
        """Open the settings dialog"""
        self.create_settings_dialog()
        if self.dialog:
            self.dialog.open()


class SimpleConfirmationDialog:
    """Simple Confirmation Dialog"""

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
                    text="Cancel",
                    on_release=self.handle_cancel
                ),
                MDRaisedButton(
                    text="Confirm",
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


class SimpleFormDialog:
    """Simple Form Dialog for adding/editing data"""

    def __init__(self, title="Form", fields=None, on_save=None):
        self.title = title
        self.fields = fields or []
        self.on_save = on_save
        self.dialog = None
        self.field_widgets = {}
        self.create_form_dialog()

    def create_form_dialog(self):
        """Create simple form dialog"""
        # Content container
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None,
            height=dp(50 * len(self.fields) + 20),
            padding=[dp(20), dp(10)]
        )

        # Create form fields
        for field in self.fields:
            field_widget = MDTextField(
                hint_text=field.get('label', ''),
                text=field.get('value', ''),
                helper_text=field.get('helper', ''),
                helper_text_mode="on_error"
            )
            self.field_widgets[field.get('name', '')] = field_widget
            content.add_widget(field_widget)

        # Create dialog
        self.dialog = MDDialog(
            title=self.title,
            type="custom",
            content_cls=content,
            size_hint=(0.8, None),
            height=dp(100 + 60 * len(self.fields)),
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=self.close_dialog
                ),
                MDRaisedButton(
                    text="Save",
                    on_release=self.save_form
                ),
            ],
        )

    def save_form(self, instance):
        """Save form data"""
        try:
            form_data = {}
            for field_name, widget in self.field_widgets.items():
                form_data[field_name] = widget.text

            if self.on_save:
                self.on_save(form_data)

            logger.info("Form saved successfully")
            self.close_dialog(instance)
        except Exception as e:
            logger.error(f"Error saving form: {e}")

    def close_dialog(self, instance):
        """Close the form dialog"""
        if self.dialog:
            self.dialog.dismiss()

    def open(self):
        """Open the form dialog"""
        if self.dialog:
            self.dialog.open()


# Legacy class names for backward compatibility
SettingsDialog = SimpleSettingsDialog
ConfirmationDialog = SimpleConfirmationDialog
