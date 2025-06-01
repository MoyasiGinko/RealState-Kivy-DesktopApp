#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Base View
Base class for all views with common functionality
"""

from abc import ABC, abstractmethod
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
import logging

from ..utils import ConfirmDialog, MessageDialog, BilingualLabel, BilingualButton
from ..language_manager import language_manager

logger = logging.getLogger(__name__)


class BaseView(Screen, ABC):
    """Base view class with common functionality"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = None
        self._initialized = False

    def set_controller(self, controller):
        """Set the controller for this view"""
        self.controller = controller
        if controller:
            controller.view = self

    def initialize_data(self):
        """Initialize view data - called when screen becomes active"""
        if not self._initialized:
            self._setup_ui()
            self._initialized = True
        self.refresh_data()

    @abstractmethod
    def _setup_ui(self):
        """Setup the user interface - implement in subclasses"""
        pass

    @abstractmethod
    def refresh_data(self):
        """Refresh view data - implement in subclasses"""
        pass

    def show_error(self, message: str, title: str = "Error"):
        """Show error message to user"""
        try:
            dialog = MessageDialog(
                title=title,
                message=message,
                message_type='error'
            )
            dialog.open()
        except Exception as e:
            logger.error(f"Error showing error dialog: {e}")
            # Fallback to simple popup
            self._show_simple_popup(title, message)

    def show_success(self, message: str, title: str = "Success"):
        """Show success message to user"""
        try:
            dialog = MessageDialog(
                title=title,
                message=message,
                message_type='success'
            )
            dialog.open()
        except Exception as e:
            logger.error(f"Error showing success dialog: {e}")
            # Fallback to simple popup
            self._show_simple_popup(title, message)

    def show_info(self, message: str, title: str = "Information"):
        """Show info message to user"""
        try:
            dialog = MessageDialog(
                title=title,
                message=message,
                message_type='info'
            )
            dialog.open()
        except Exception as e:
            logger.error(f"Error showing info dialog: {e}")
            # Fallback to simple popup
            self._show_simple_popup(title, message)

    def confirm_deletion(self, message: str = None) -> bool:
        """Show confirmation dialog for deletion"""
        try:
            if not message:
                message = language_manager.get_text('confirm_delete')

            result = [False]  # Use list to allow modification in nested function

            def on_confirm(instance):
                result[0] = True
                popup.dismiss()

            def on_cancel(instance):
                result[0] = False
                popup.dismiss()

            popup = ConfirmDialog(
                title=language_manager.get_text('confirm'),
                message=message,
                confirm_callback=on_confirm,
                cancel_callback=on_cancel
            )
            popup.open()

            # Note: This is a simplified version. In a real implementation,
            # you'd need to handle this asynchronously
            return result[0]

        except Exception as e:
            logger.error(f"Error showing confirmation dialog: {e}")
            return False

    def _show_simple_popup(self, title: str, message: str):
        """Fallback simple popup"""
        try:
            content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))

            label = BilingualLabel(
                text_en=message,
                text_ar=message,
                text_size=(None, None),
                halign='center'
            )
            content.add_widget(label)

            close_btn = BilingualButton(
                translation_key='close',
                size_hint_y=None,
                height=dp(40)
            )
            content.add_widget(close_btn)

            popup = Popup(
                title=title,
                content=content,
                size_hint=(0.8, 0.4),
                auto_dismiss=True
            )

            close_btn.bind(on_press=popup.dismiss)
            popup.open()

        except Exception as e:
            logger.error(f"Error showing simple popup: {e}")

    def navigate_to(self, screen_name: str):
        """Navigate to another screen"""
        try:
            if self.manager:
                self.manager.current = screen_name
        except Exception as e:
            logger.error(f"Error navigating to {screen_name}: {e}")

    def get_form_data(self, form_container) -> dict:
        """Extract data from form fields"""
        data = {}
        try:
            for child in form_container.children:
                if hasattr(child, 'get_value') and hasattr(child, 'translation_key'):
                    key = child.translation_key or getattr(child, 'field_name', None)
                    if key:
                        data[key] = child.get_value()
        except Exception as e:
            logger.error(f"Error extracting form data: {e}")
        return data

    def clear_form(self, form_container):
        """Clear all form fields"""
        try:
            for child in form_container.children:
                if hasattr(child, 'clear'):
                    child.clear()
        except Exception as e:
            logger.error(f"Error clearing form: {e}")

    def populate_form(self, form_container, data: dict):
        """Populate form fields with data"""
        try:
            for child in form_container.children:
                if hasattr(child, 'set_value') and hasattr(child, 'translation_key'):
                    key = child.translation_key or getattr(child, 'field_name', None)
                    if key and key in data:
                        child.set_value(data[key])
        except Exception as e:
            logger.error(f"Error populating form: {e}")

    def on_enter(self):
        """Called when screen is entered"""
        super().on_enter()
        self.initialize_data()

    def on_leave(self):
        """Called when screen is left"""
        super().on_leave()
        # Cleanup if needed


class BasePopupView(Popup, ABC):
    """Base class for popup views"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = None
        self._initialized = False

    def set_controller(self, controller):
        """Set the controller for this popup"""
        self.controller = controller

    def initialize(self):
        """Initialize popup - called when opened"""
        if not self._initialized:
            self._setup_ui()
            self._initialized = True
        self._load_data()

    @abstractmethod
    def _setup_ui(self):
        """Setup the user interface - implement in subclasses"""
        pass

    @abstractmethod
    def _load_data(self):
        """Load data for popup - implement in subclasses"""
        pass

    def show_error(self, message: str, title: str = "Error"):
        """Show error message"""
        logger.error(message)
        # Could show a nested popup or update popup content

    def show_success(self, message: str, title: str = "Success"):
        """Show success message"""
        logger.info(message)
        # Could show a nested popup or update popup content
