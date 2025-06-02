#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Settings Model
Handles application settings and configuration
"""

from typing import Dict, Any, Optional, List
import logging
import json
import os

from .base_model import BaseModel

logger = logging.getLogger(__name__)


class SettingsModel(BaseModel):
    """Model for managing application settings"""

    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.settings_file = "app_settings.json"
        self.default_settings = {
            'company_code': 'DEFAULT',
            'photo_save_path': 'property_photos',
            'backup_directory': 'backups',
            'auto_backup_enabled': True,
            'backup_frequency': 'daily',
            'theme': 'light',
            'language': 'en',
            'currency': 'USD',
            'decimal_places': 2,
            'date_format': 'dd/mm/yyyy',
            'recent_files_limit': 10,
            'auto_save': True,
            'auto_save_interval': 300,  # seconds
            'enable_notifications': True,
            'enable_sound': True,
            'window_maximized': False,
            'window_width': 1200,
            'window_height': 800,
            'last_backup_date': None
        }

    def get_all_settings(self) -> Dict[str, Any]:
        """Get all application settings"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)

                # Merge with defaults to ensure all keys exist
                merged_settings = self.default_settings.copy()
                merged_settings.update(settings)
                return merged_settings
            else:
                # Return default settings if file doesn't exist
                return self.default_settings.copy()

        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            return self.default_settings.copy()

    def get_setting(self, key: str) -> Any:
        """Get a specific setting value"""
        try:
            settings = self.get_all_settings()
            return settings.get(key, self.default_settings.get(key))
        except Exception as e:
            logger.error(f"Error getting setting {key}: {e}")
            return self.default_settings.get(key)

    def update_setting(self, key: str, value: Any) -> bool:
        """Update a specific setting"""
        try:
            settings = self.get_all_settings()
            settings[key] = value
            return self.save_settings(settings)
        except Exception as e:
            logger.error(f"Error updating setting {key}: {e}")
            return False

    def update_settings(self, settings_dict: Dict[str, Any]) -> bool:
        """Update multiple settings"""
        try:
            current_settings = self.get_all_settings()
            current_settings.update(settings_dict)
            return self.save_settings(current_settings)
        except Exception as e:
            logger.error(f"Error updating settings: {e}")
            return False

    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            logger.info("Settings saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            return False

    def reset_to_defaults(self) -> bool:
        """Reset all settings to default values"""
        try:
            return self.save_settings(self.default_settings.copy())
        except Exception as e:
            logger.error(f"Error resetting settings: {e}")
            return False

    def export_settings(self, file_path: str) -> bool:
        """Export settings to a file"""
        try:
            settings = self.get_all_settings()
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            logger.info(f"Settings exported to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting settings: {e}")
            return False

    def import_settings(self, file_path: str) -> bool:
        """Import settings from a file"""
        try:
            if not os.path.exists(file_path):
                logger.error(f"Settings file not found: {file_path}")
                return False

            with open(file_path, 'r', encoding='utf-8') as f:
                imported_settings = json.load(f)

            # Validate imported settings
            if not isinstance(imported_settings, dict):
                logger.error("Invalid settings file format")
                return False

            # Only import valid settings keys
            valid_settings = {}
            for key, value in imported_settings.items():
                if key in self.default_settings:
                    valid_settings[key] = value

            return self.update_settings(valid_settings)

        except Exception as e:
            logger.error(f"Error importing settings: {e}")
            return False

    def create_backup_directory(self) -> bool:
        """Create backup directory if it doesn't exist"""
        try:
            backup_dir = self.get_setting('backup_directory')
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir, exist_ok=True)
                logger.info(f"Created backup directory: {backup_dir}")
            return True
        except Exception as e:
            logger.error(f"Error creating backup directory: {e}")
            return False

    def create_photo_directory(self) -> bool:
        """Create photo directory if it doesn't exist"""
        try:
            photo_dir = self.get_setting('photo_save_path')
            if not os.path.exists(photo_dir):
                os.makedirs(photo_dir, exist_ok=True)
                logger.info(f"Created photo directory: {photo_dir}")
            return True
        except Exception as e:
            logger.error(f"Error creating photo directory: {e}")
            return False

    def validate_settings(self, settings: Dict[str, Any]) -> tuple[bool, str]:
        """Validate settings values"""
        try:
            # Validate company code
            if 'company_code' in settings:
                if not settings['company_code'] or len(settings['company_code'].strip()) == 0:
                    return False, "Company code cannot be empty"

            # Validate directories
            for dir_key in ['photo_save_path', 'backup_directory']:
                if dir_key in settings:
                    if not settings[dir_key] or len(settings[dir_key].strip()) == 0:
                        return False, f"{dir_key} cannot be empty"

            # Validate numeric values
            numeric_settings = ['decimal_places', 'recent_files_limit', 'auto_save_interval',
                              'window_width', 'window_height']
            for key in numeric_settings:
                if key in settings:
                    try:
                        int(settings[key])
                    except (ValueError, TypeError):
                        return False, f"{key} must be a valid number"

            # Validate boolean values
            boolean_settings = ['auto_backup_enabled', 'auto_save', 'enable_notifications',
                              'enable_sound', 'window_maximized']
            for key in boolean_settings:
                if key in settings:
                    if not isinstance(settings[key], bool):
                        return False, f"{key} must be true or false"

            return True, ""

        except Exception as e:
            logger.error(f"Error validating settings: {e}")
            return False, f"Validation error: {str(e)}"

    # Implementation of abstract methods from BaseModel
    def get_all(self) -> List[Dict]:
        """Get all settings as a list (for compatibility with BaseModel interface)"""
        settings = self.get_all_settings()
        return [{'key': key, 'value': value} for key, value in settings.items()]

    def get_by_id(self, record_id: str) -> Optional[Dict]:
        """Get setting by key (for compatibility with BaseModel interface)"""
        value = self.get_setting(record_id)
        if value is not None:
            return {'key': record_id, 'value': value}
        return None

    def create(self, data: Dict) -> bool:
        """Create/update a setting (for compatibility with BaseModel interface)"""
        if 'key' in data and 'value' in data:
            return self.update_setting(data['key'], data['value'])
        return False

    def update(self, record_id: str, data: Dict) -> bool:
        """Update a setting (for compatibility with BaseModel interface)"""
        if 'value' in data:
            return self.update_setting(record_id, data['value'])
        return False

    def delete(self, record_id: str) -> bool:
        """Delete a setting (reset to default for compatibility with BaseModel interface)"""
        if record_id in self.default_settings:
            return self.update_setting(record_id, self.default_settings[record_id])
        return False
