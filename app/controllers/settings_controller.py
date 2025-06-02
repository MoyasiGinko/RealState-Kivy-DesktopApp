#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Settings Controller
Handles settings-related business logic and view interactions
"""

from typing import Dict, Any
import logging
import os

from .base_controller import BaseController

logger = logging.getLogger(__name__)


class SettingsController(BaseController):
    """Controller for managing application settings"""

    def __init__(self, model, view=None):
        super().__init__(model, view)
        self.current_settings = {}

    def _setup_view_handlers(self):
        """Setup event handlers for settings view"""
        if self.view:
            # Bind view events to controller methods
            if hasattr(self.view, 'on_save_settings'):
                self.view.on_save_settings = self.save_settings
            if hasattr(self.view, 'on_reset_settings'):
                self.view.on_reset_settings = self.reset_settings
            if hasattr(self.view, 'on_export_settings'):
                self.view.on_export_settings = self.export_settings
            if hasattr(self.view, 'on_import_settings'):
                self.view.on_import_settings = self.import_settings

    def get_settings(self) -> Dict[str, Any]:
        """Get all current settings (alias for load_settings)"""
        return self.load_settings()

    def load_settings(self) -> Dict[str, Any]:
        """Load all application settings"""
        try:
            settings = self.model.get_all_settings()
            self.current_settings = settings
            logger.info("Settings loaded successfully")
            return settings
        except Exception as e:
            self.handle_error(f"Failed to load settings: {str(e)}")
            return {}

    def get_setting(self, key: str) -> Any:
        """Get a specific setting value"""
        try:
            value = self.model.get_setting(key)
            logger.debug(f"Retrieved setting {key}: {value}")
            return value
        except Exception as e:
            self.handle_error(f"Failed to get setting {key}: {str(e)}")
            return None

    def update_setting(self, key: str, value: Any) -> bool:
        """Update a specific setting"""
        try:
            # Validate the setting update
            test_settings = {key: value}
            is_valid, error_msg = self.model.validate_settings(test_settings)
            if not is_valid:
                self.handle_error(error_msg, "Validation Error")
                return False

            success = self.model.update_setting(key, value)
            if success:
                self.current_settings[key] = value
                self.handle_success(f"Setting '{key}' updated successfully")

                # Handle special settings that require action
                self._handle_special_settings(key, value)

                if self.view:
                    self.view.refresh_data()
                return True
            else:
                self.handle_error(f"Failed to update setting '{key}'")
                return False

        except Exception as e:
            self.handle_error(f"Error updating setting {key}: {str(e)}")
            return False

    def save_settings(self, settings_dict: Dict[str, Any]) -> bool:
        """Save multiple settings"""
        try:
            # Validate all settings
            is_valid, error_msg = self.model.validate_settings(settings_dict)
            if not is_valid:
                self.handle_error(error_msg, "Validation Error")
                return False

            success = self.model.update_settings(settings_dict)
            if success:
                self.current_settings.update(settings_dict)
                self.handle_success("Settings saved successfully")

                # Handle special settings that require action
                for key, value in settings_dict.items():
                    self._handle_special_settings(key, value)

                if self.view:
                    self.view.refresh_data()
                return True
            else:
                self.handle_error("Failed to save settings")
                return False

        except Exception as e:
            self.handle_error(f"Error saving settings: {str(e)}")
            return False

    def reset_settings(self) -> bool:
        """Reset all settings to default values"""
        try:
            if self.view and hasattr(self.view, 'confirm_reset'):
                confirmed = self.view.confirm_reset("Are you sure you want to reset all settings to default values?")
                if not confirmed:
                    return False

            success = self.model.reset_to_defaults()
            if success:
                self.current_settings = self.model.get_all_settings()
                self.handle_success("Settings reset to default values")
                if self.view:
                    self.view.refresh_data()
                return True
            else:
                self.handle_error("Failed to reset settings")
                return False

        except Exception as e:
            self.handle_error(f"Error resetting settings: {str(e)}")
            return False

    def export_settings(self, file_path: str) -> bool:
        """Export settings to a file"""
        try:
            if not file_path:
                self.handle_error("Please specify a file path")
                return False

            success = self.model.export_settings(file_path)
            if success:
                self.handle_success(f"Settings exported to {file_path}")
                return True
            else:
                self.handle_error("Failed to export settings")
                return False

        except Exception as e:
            self.handle_error(f"Error exporting settings: {str(e)}")
            return False

    def import_settings(self, file_path: str) -> bool:
        """Import settings from a file"""
        try:
            if not file_path or not os.path.exists(file_path):
                self.handle_error("Please specify a valid file path")
                return False

            if self.view and hasattr(self.view, 'confirm_import'):
                confirmed = self.view.confirm_import("Importing settings will overwrite current settings. Continue?")
                if not confirmed:
                    return False

            success = self.model.import_settings(file_path)
            if success:
                self.current_settings = self.model.get_all_settings()
                self.handle_success(f"Settings imported from {file_path}")
                if self.view:
                    self.view.refresh_data()
                return True
            else:
                self.handle_error("Failed to import settings")
                return False

        except Exception as e:
            self.handle_error(f"Error importing settings: {str(e)}")
            return False

    def create_directories(self) -> bool:
        """Create necessary directories based on settings"""
        try:
            # Create backup directory
            backup_success = self.model.create_backup_directory()

            # Create photo directory
            photo_success = self.model.create_photo_directory()

            if backup_success and photo_success:
                self.handle_success("Directories created successfully")
                return True
            else:
                self.handle_error("Failed to create some directories")
                return False

        except Exception as e:
            self.handle_error(f"Error creating directories: {str(e)}")
            return False

    def get_theme_settings(self) -> Dict[str, Any]:
        """Get theme-related settings"""
        try:
            settings = self.current_settings or self.load_settings()
            theme_settings = {
                'theme': settings.get('theme', 'light'),
                'window_maximized': settings.get('window_maximized', False),
                'window_width': settings.get('window_width', 1200),
                'window_height': settings.get('window_height', 800)
            }
            return theme_settings
        except Exception as e:
            self.handle_error(f"Error getting theme settings: {str(e)}")
            return {}

    def get_backup_settings(self) -> Dict[str, Any]:
        """Get backup-related settings"""
        try:
            settings = self.current_settings or self.load_settings()
            backup_settings = {
                'auto_backup_enabled': settings.get('auto_backup_enabled', True),
                'backup_frequency': settings.get('backup_frequency', 'daily'),
                'backup_directory': settings.get('backup_directory', 'backups'),
                'last_backup_date': settings.get('last_backup_date', None)
            }
            return backup_settings
        except Exception as e:
            self.handle_error(f"Error getting backup settings: {str(e)}")
            return {}

    def update_last_backup_date(self, date_str: str) -> bool:
        """Update the last backup date"""
        return self.update_setting('last_backup_date', date_str)

    def _handle_special_settings(self, key: str, value: Any):
        """Handle settings that require special actions"""
        try:
            if key == 'photo_save_path':
                # Create photo directory if it doesn't exist
                self.model.create_photo_directory()

            elif key == 'backup_directory':
                # Create backup directory if it doesn't exist
                self.model.create_backup_directory()

            elif key == 'theme':
                # Apply theme changes (would be handled by the view)
                logger.info(f"Theme changed to: {value}")

            elif key == 'language':
                # Handle language change (would reload UI text)
                logger.info(f"Language changed to: {value}")

        except Exception as e:
            logger.error(f"Error handling special setting {key}: {e}")

    def validate_input(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """Validate settings input data"""
        return self.model.validate_settings(data)

    def on_model_changed(self, event_type: str, data=None):
        """Handle model change notifications"""
        super().on_model_changed(event_type, data)

        if event_type == 'settings_updated':
            logger.info(f"Settings updated: {data}")
        elif event_type == 'settings_reset':
            logger.info("Settings reset to defaults")
