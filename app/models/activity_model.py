#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Activity Model
Handles tracking of user activities and recent actions
"""

from typing import Dict, List, Optional
import logging
import json
import os
from datetime import datetime

from .base_model import BaseModel

logger = logging.getLogger(__name__)


class ActivityModel(BaseModel):
    """Model for managing user activity tracking"""

    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.activity_file = "activity_log.json"
        self.max_activities = 100  # Maximum number of activities to keep

    def log_activity(self, action_type: str, description: str, details: Dict = None) -> bool:
        """Log a new activity"""
        try:
            activity = {
                'timestamp': datetime.now().isoformat(),
                'action_type': action_type,
                'description': description,
                'details': details or {},
                'user': 'System'  # Could be extended to track actual users
            }

            activities = self._load_activities()
            activities.insert(0, activity)  # Add to beginning of list

            # Keep only the most recent activities
            if len(activities) > self.max_activities:
                activities = activities[:self.max_activities]

            return self._save_activities(activities)

        except Exception as e:
            logger.error(f"Error logging activity: {e}")
            return False

    def get_recent_activities(self, limit: int = 50) -> List[Dict]:
        """Get recent activities"""
        try:
            activities = self._load_activities()
            return activities[:limit]
        except Exception as e:
            logger.error(f"Error getting recent activities: {e}")
            return []

    def get_activities_by_type(self, action_type: str, limit: int = 50) -> List[Dict]:
        """Get activities by type"""
        try:
            activities = self._load_activities()
            filtered = [a for a in activities if a.get('action_type') == action_type]
            return filtered[:limit]
        except Exception as e:
            logger.error(f"Error getting activities by type: {e}")
            return []

    def get_activities_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Get activities within a date range"""
        try:
            activities = self._load_activities()
            filtered = []

            for activity in activities:
                activity_date = activity.get('timestamp', '')[:10]  # Get YYYY-MM-DD part
                if start_date <= activity_date <= end_date:
                    filtered.append(activity)

            return filtered
        except Exception as e:
            logger.error(f"Error getting activities by date range: {e}")
            return []

    def clear_activities(self) -> bool:
        """Clear all activities"""
        try:
            return self._save_activities([])
        except Exception as e:
            logger.error(f"Error clearing activities: {e}")
            return False

    def export_activities(self, file_path: str, filters: Dict = None) -> bool:
        """Export activities to a file"""
        try:
            if filters:
                # Apply filters
                activities = self._load_activities()
                if filters.get('action_type'):
                    activities = [a for a in activities if a.get('action_type') == filters['action_type']]
                if filters.get('start_date') and filters.get('end_date'):
                    activities = self.get_activities_by_date_range(filters['start_date'], filters['end_date'])
            else:
                activities = self._load_activities()

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(activities, f, indent=4, ensure_ascii=False)

            logger.info(f"Activities exported to {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error exporting activities: {e}")
            return False

    def get_activity_statistics(self) -> Dict:
        """Get activity statistics"""
        try:
            activities = self._load_activities()

            # Count by action type
            type_counts = {}
            today_count = 0
            week_count = 0

            today = datetime.now().date()
            week_ago = datetime.now().date().replace(day=today.day-7) if today.day > 7 else today.replace(month=today.month-1, day=30)

            for activity in activities:
                # Count by type
                action_type = activity.get('action_type', 'unknown')
                type_counts[action_type] = type_counts.get(action_type, 0) + 1

                # Count by date
                try:
                    activity_date = datetime.fromisoformat(activity.get('timestamp', '')).date()
                    if activity_date == today:
                        today_count += 1
                    if activity_date >= week_ago:
                        week_count += 1
                except:
                    pass

            return {
                'total_activities': len(activities),
                'today_activities': today_count,
                'week_activities': week_count,
                'by_type': type_counts,
                'most_common': max(type_counts.items(), key=lambda x: x[1]) if type_counts else ('none', 0)
            }

        except Exception as e:
            logger.error(f"Error getting activity statistics: {e}")
            return {}

    def _load_activities(self) -> List[Dict]:
        """Load activities from file"""
        try:
            if os.path.exists(self.activity_file):
                with open(self.activity_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading activities: {e}")
            return []

    def _save_activities(self, activities: List[Dict]) -> bool:
        """Save activities to file"""
        try:
            with open(self.activity_file, 'w', encoding='utf-8') as f:
                json.dump(activities, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Error saving activities: {e}")
            return False

    # Activity logging helper methods for common actions
    def log_property_created(self, property_code: str, details: Dict = None) -> bool:
        """Log property creation activity"""
        return self.log_activity(
            'property_created',
            f"Property {property_code} created",
            details
        )

    def log_property_updated(self, property_code: str, details: Dict = None) -> bool:
        """Log property update activity"""
        return self.log_activity(
            'property_updated',
            f"Property {property_code} updated",
            details
        )

    def log_property_deleted(self, property_code: str, details: Dict = None) -> bool:
        """Log property deletion activity"""
        return self.log_activity(
            'property_deleted',
            f"Property {property_code} deleted",
            details
        )

    def log_owner_created(self, owner_code: str, owner_name: str, details: Dict = None) -> bool:
        """Log owner creation activity"""
        return self.log_activity(
            'owner_created',
            f"Owner {owner_name} ({owner_code}) created",
            details
        )

    def log_owner_updated(self, owner_code: str, owner_name: str, details: Dict = None) -> bool:
        """Log owner update activity"""
        return self.log_activity(
            'owner_updated',
            f"Owner {owner_name} ({owner_code}) updated",
            details
        )

    def log_owner_deleted(self, owner_code: str, owner_name: str, details: Dict = None) -> bool:
        """Log owner deletion activity"""
        return self.log_activity(
            'owner_deleted',
            f"Owner {owner_name} ({owner_code}) deleted",
            details
        )

    def log_photo_uploaded(self, property_code: str, photo_count: int, details: Dict = None) -> bool:
        """Log photo upload activity"""
        return self.log_activity(
            'photo_uploaded',
            f"{photo_count} photos uploaded for property {property_code}",
            details
        )

    def log_export_action(self, export_type: str, record_count: int, details: Dict = None) -> bool:
        """Log export activity"""
        return self.log_activity(
            'export',
            f"Exported {record_count} {export_type} records",
            details
        )

    def log_backup_action(self, backup_type: str, success: bool, details: Dict = None) -> bool:
        """Log backup activity"""
        status = "successful" if success else "failed"
        return self.log_activity(
            'backup',
            f"Database backup ({backup_type}) {status}",
            details
        )

    # Abstract methods implementation (required by BaseModel)
    def get_all(self) -> List[Dict]:
        """Get all activities"""
        return self.get_recent_activities(self.max_activities)

    def get_by_id(self, record_id: str) -> Optional[Dict]:
        """Get activity by ID (timestamp)"""
        try:
            activities = self._load_activities()
            for activity in activities:
                if activity.get('timestamp') == record_id:
                    return activity
            return None
        except Exception as e:
            logger.error(f"Error getting activity by ID: {e}")
            return None

    def create(self, data: Dict) -> bool:
        """Create new activity (alias for log_activity)"""
        return self.log_activity(
            data.get('action_type', 'unknown'),
            data.get('description', ''),
            data.get('details')
        )

    def update(self, record_id: str, data: Dict) -> bool:
        """Update activity (not typically done, but required by interface)"""
        # Activities are typically immutable, but for interface compliance
        return False

    def delete(self, record_id: str) -> bool:
        """Delete specific activity by timestamp"""
        try:
            activities = self._load_activities()
            original_count = len(activities)
            activities = [a for a in activities if a.get('timestamp') != record_id]
            if len(activities) < original_count:
                return self._save_activities(activities)
            return False
        except Exception as e:
            logger.error(f"Error deleting activity: {e}")
            return False
