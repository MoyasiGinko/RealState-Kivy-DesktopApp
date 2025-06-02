#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Activity Controller
Handles activity tracking and recent activity display
"""

from typing import Dict, List
import logging
from datetime import datetime, timedelta

from .base_controller import BaseController

logger = logging.getLogger(__name__)


class ActivityController(BaseController):
    """Controller for managing user activity tracking"""

    def __init__(self, model, view=None):
        super().__init__(model, view)
        self.current_activities = []
        self.filters = {}

    def _setup_view_handlers(self):
        """Setup event handlers for activity view"""
        if self.view:
            # Bind view events to controller methods
            if hasattr(self.view, 'on_refresh_activities'):
                self.view.on_refresh_activities = self.load_recent_activities
            if hasattr(self.view, 'on_filter_activities'):
                self.view.on_filter_activities = self.filter_activities
            if hasattr(self.view, 'on_export_activities'):
                self.view.on_export_activities = self.export_activities
            if hasattr(self.view, 'on_clear_activities'):
                self.view.on_clear_activities = self.clear_activities

    def load_recent_activities(self, limit: int = 50) -> List[Dict]:
        """Load recent activities"""
        try:
            activities = self.model.get_recent_activities(limit)
            self.current_activities = activities
            logger.info(f"Loaded {len(activities)} recent activities")
            return activities
        except Exception as e:
            self.handle_error(f"Failed to load activities: {str(e)}")
            return []

    def get_recent_activities(self, limit: int = 50) -> List[Dict]:
        """Get recent activities (alias for load_recent_activities for compatibility)"""
        return self.load_recent_activities(limit)

    def filter_activities(self, filters: Dict) -> List[Dict]:
        """Filter activities based on criteria"""
        try:
            self.filters = filters
            activities = []

            if filters.get('action_type'):
                activities = self.model.get_activities_by_type(
                    filters['action_type'],
                    filters.get('limit', 50)
                )
            elif filters.get('start_date') and filters.get('end_date'):
                activities = self.model.get_activities_by_date_range(
                    filters['start_date'],
                    filters['end_date']
                )
            else:
                activities = self.model.get_recent_activities(filters.get('limit', 50))

            self.current_activities = activities
            logger.info(f"Found {len(activities)} activities matching filters")
            return activities

        except Exception as e:
            self.handle_error(f"Error filtering activities: {str(e)}")
            return []

    def get_activities_by_type(self, action_type: str, limit: int = 50) -> List[Dict]:
        """Get activities by specific type"""
        try:
            activities = self.model.get_activities_by_type(action_type, limit)
            logger.info(f"Found {len(activities)} activities of type '{action_type}'")
            return activities
        except Exception as e:
            self.handle_error(f"Error getting activities by type: {str(e)}")
            return []

    def get_today_activities(self) -> List[Dict]:
        """Get today's activities"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            activities = self.model.get_activities_by_date_range(today, today)
            logger.info(f"Found {len(activities)} activities for today")
            return activities
        except Exception as e:
            self.handle_error(f"Error getting today's activities: {str(e)}")
            return []

    def get_week_activities(self) -> List[Dict]:
        """Get this week's activities"""
        try:
            today = datetime.now()
            week_ago = today - timedelta(days=7)
            start_date = week_ago.strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')

            activities = self.model.get_activities_by_date_range(start_date, end_date)
            logger.info(f"Found {len(activities)} activities for this week")
            return activities
        except Exception as e:
            self.handle_error(f"Error getting week's activities: {str(e)}")
            return []

    def get_activity_statistics(self) -> Dict:
        """Get activity statistics"""
        try:
            stats = self.model.get_activity_statistics()
            logger.info("Retrieved activity statistics")
            return stats
        except Exception as e:
            self.handle_error(f"Error getting activity statistics: {str(e)}")
            return {}

    def log_activity(self, action_type: str, description: str, details: Dict = None) -> bool:
        """Log a new activity"""
        try:
            success = self.model.log_activity(action_type, description, details)
            if success:
                logger.debug(f"Activity logged: {action_type} - {description}")
                # Refresh the view if available
                if self.view and hasattr(self.view, 'refresh_data'):
                    self.view.refresh_data()
                return True
            else:
                logger.error(f"Failed to log activity: {action_type}")
                return False
        except Exception as e:
            self.handle_error(f"Error logging activity: {str(e)}")
            return False

    def export_activities(self, file_path: str, filters: Dict = None) -> bool:
        """Export activities to file"""
        try:
            if not file_path:
                self.handle_error("Please specify a file path")
                return False

            success = self.model.export_activities(file_path, filters)
            if success:
                self.handle_success(f"Activities exported to {file_path}")
                return True
            else:
                self.handle_error("Failed to export activities")
                return False

        except Exception as e:
            self.handle_error(f"Error exporting activities: {str(e)}")
            return False

    def clear_activities(self) -> bool:
        """Clear all activities"""
        try:
            if self.view and hasattr(self.view, 'confirm_clear'):
                confirmed = self.view.confirm_clear("Are you sure you want to clear all activity history?")
                if not confirmed:
                    return False

            success = self.model.clear_activities()
            if success:
                self.current_activities = []
                self.handle_success("Activity history cleared")
                if self.view:
                    self.view.refresh_data()
                return True
            else:
                self.handle_error("Failed to clear activities")
                return False

        except Exception as e:
            self.handle_error(f"Error clearing activities: {str(e)}")
            return False

    # Helper methods for logging specific activities
    def log_property_action(self, action: str, property_code: str, details: Dict = None) -> bool:
        """Log property-related activities"""
        try:
            if action == 'created':
                return self.model.log_property_created(property_code, details)
            elif action == 'updated':
                return self.model.log_property_updated(property_code, details)
            elif action == 'deleted':
                return self.model.log_property_deleted(property_code, details)
            else:
                return self.log_activity(f'property_{action}', f"Property {property_code} {action}", details)
        except Exception as e:
            logger.error(f"Error logging property action: {e}")
            return False

    def log_owner_action(self, action: str, owner_code: str, owner_name: str, details: Dict = None) -> bool:
        """Log owner-related activities"""
        try:
            if action == 'created':
                return self.model.log_owner_created(owner_code, owner_name, details)
            elif action == 'updated':
                return self.model.log_owner_updated(owner_code, owner_name, details)
            elif action == 'deleted':
                return self.model.log_owner_deleted(owner_code, owner_name, details)
            else:
                return self.log_activity(f'owner_{action}', f"Owner {owner_name} ({owner_code}) {action}", details)
        except Exception as e:
            logger.error(f"Error logging owner action: {e}")
            return False

    def log_photo_action(self, property_code: str, photo_count: int, action: str = 'uploaded', details: Dict = None) -> bool:
        """Log photo-related activities"""
        try:
            if action == 'uploaded':
                return self.model.log_photo_uploaded(property_code, photo_count, details)
            else:
                return self.log_activity(f'photo_{action}', f"{photo_count} photos {action} for property {property_code}", details)
        except Exception as e:
            logger.error(f"Error logging photo action: {e}")
            return False

    def log_export_action(self, export_type: str, record_count: int, file_path: str = None) -> bool:
        """Log export activities"""
        try:
            details = {'file_path': file_path} if file_path else None
            return self.model.log_export_action(export_type, record_count, details)
        except Exception as e:
            logger.error(f"Error logging export action: {e}")
            return False

    def log_backup_action(self, backup_type: str, success: bool, file_path: str = None) -> bool:
        """Log backup activities"""
        try:
            details = {'file_path': file_path} if file_path else None
            return self.model.log_backup_action(backup_type, success, details)
        except Exception as e:
            logger.error(f"Error logging backup action: {e}")
            return False

    def log_settings_change(self, changed_settings: List[str], old_values: Dict = None, new_values: Dict = None) -> bool:
        """Log settings change activities"""
        try:
            details = {}
            if old_values:
                details['old_values'] = old_values
            if new_values:
                details['new_values'] = new_values

            return self.model.log_settings_changed(changed_settings, details)
        except Exception as e:
            logger.error(f"Error logging settings change: {e}")
            return False

    def get_action_types(self) -> List[str]:
        """Get list of available action types for filtering"""
        return [
            'property_created',
            'property_updated',
            'property_deleted',
            'owner_created',
            'owner_updated',
            'owner_deleted',
            'photo_uploaded',
            'export',
            'backup',
            'settings_changed'
        ]

    def on_model_changed(self, event_type: str, data=None):
        """Handle model change notifications"""
        super().on_model_changed(event_type, data)

        if event_type == 'activity_logged':
            logger.debug(f"Activity logged: {data}")
        elif event_type == 'activities_cleared':
            logger.info("Activities cleared")
            self.current_activities = []

    def get_activities(self, **kwargs) -> List[Dict]:
        """Get activities with optional filters"""
        try:
            limit = kwargs.get('limit', 50)
            action_type = kwargs.get('action_type')
            start_date = kwargs.get('start_date')
            end_date = kwargs.get('end_date')

            if action_type:
                activities = self.model.get_activities_by_type(action_type, limit)
            elif start_date and end_date:
                activities = self.model.get_activities_by_date_range(start_date, end_date)
            else:
                activities = self.model.get_recent_activities(limit)

            logger.info(f"Retrieved {len(activities)} activities")
            return activities
        except Exception as e:
            self.handle_error(f"Failed to get activities: {str(e)}")
            return []
