#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Main Controller
Central controller that orchestrates all system components
"""

from typing import Dict, List, Optional
import logging
import os

from .property_controller import PropertyController
from .owner_controller import OwnerController
from .settings_controller import SettingsController
from .activity_controller import ActivityController
from .backup_controller import BackupController
from .report_controller import ReportController

logger = logging.getLogger(__name__)


class MainController:
    """Main controller that coordinates all system components"""

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.controllers = {}
        self._initialize_controllers()
        self._setup_system()

    def _initialize_controllers(self):
        """Initialize all sub-controllers"""
        try:            # Import models
            from ..models.property_model import PropertyModel
            from ..models.owner_model import OwnerModel
            from ..models.settings_model import SettingsModel
            from ..models.activity_model import ActivityModel

            # Create models
            self.property_model = PropertyModel(self.db_manager)
            self.owner_model = OwnerModel(self.db_manager)
            self.settings_model = SettingsModel(self.db_manager)
            self.activity_model = ActivityModel(self.db_manager)            # Create controllers
            self.controllers['property'] = PropertyController(self.property_model)
            self.controllers['owner'] = OwnerController(self.owner_model)
            self.controllers['settings'] = SettingsController(self.settings_model)
            self.controllers['activity'] = ActivityController(self.activity_model)
            self.controllers['backup'] = BackupController(self.db_manager)
            self.controllers['report'] = ReportController(self.property_model, self.owner_model)

            logger.info("All controllers initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing controllers: {e}")
            raise

    def _setup_system(self):
        """Setup system-wide configurations"""
        try:
            # Load system settings
            self.settings = self.controllers['settings'].load_settings()

            # Setup logging level from settings
            log_level = self.settings.get('logging_level', 'INFO')
            logging.getLogger().setLevel(getattr(logging, log_level))

            # Create necessary directories
            self._ensure_directories()

            # Log system startup
            self.log_activity("system_startup", {"timestamp": "now"})

            logger.info("System setup completed successfully")

        except Exception as e:
            logger.error(f"Error setting up system: {e}")

    def _ensure_directories(self):
        """Ensure all necessary directories exist"""
        directories = [
            'backups',
            'reports',
            'exports',
            'logs',
            'temp'
        ]

        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logger.info(f"Created directory: {directory}")

    # Property Management Methods
    def get_all_properties(self) -> List[Dict]:
        """Get all properties"""
        try:
            properties = self.controllers['property'].load_properties()
            self.log_activity("properties_loaded", {"count": len(properties)})
            return properties
        except Exception as e:
            logger.error(f"Error getting all properties: {e}")
            return []

    def create_property(self, property_data: Dict) -> bool:
        """Create a new property"""
        try:
            success = self.controllers['property'].create_property(property_data)
            if success:
                self.log_activity("property_created", {
                    "property_code": property_data.get('realstatecode', 'unknown')
                })
            return success
        except Exception as e:
            logger.error(f"Error creating property: {e}")
            return False

    def update_property(self, company_code: str, property_data: Dict) -> bool:
        """Update an existing property"""
        try:
            success = self.controllers['property'].update_property(company_code, property_data)
            if success:
                self.log_activity("property_updated", {
                    "company_code": company_code
                })
            return success
        except Exception as e:
            logger.error(f"Error updating property: {e}")
            return False

    def delete_property(self, company_code: str) -> bool:
        """Delete a property"""
        try:
            success = self.controllers['property'].delete_property(company_code)
            if success:
                self.log_activity("property_deleted", {
                    "company_code": company_code
                })
            return success
        except Exception as e:
            logger.error(f"Error deleting property: {e}")
            return False

    def search_properties(self, criteria: Dict) -> List[Dict]:
        """Search properties with advanced criteria"""
        try:
            properties = self.controllers['property'].advanced_search(criteria)
            self.log_activity("properties_searched", {
                "criteria": criteria,
                "results_count": len(properties)
            })
            return properties
        except Exception as e:
            logger.error(f"Error searching properties: {e}")
            return []

    # Owner Management Methods
    def get_all_owners(self) -> List[Dict]:
        """Get all owners"""
        try:
            owners = self.controllers['owner'].load_owners()
            self.log_activity("owners_loaded", {"count": len(owners)})
            return owners
        except Exception as e:
            logger.error(f"Error getting all owners: {e}")
            return []

    def create_owner(self, owner_data: Dict) -> bool:
        """Create a new owner"""
        try:
            success = self.controllers['owner'].create_owner(owner_data)
            if success:
                self.log_activity("owner_created", {
                    "owner_name": owner_data.get('ownername', 'unknown')
                })
            return success
        except Exception as e:
            logger.error(f"Error creating owner: {e}")
            return False

    def update_owner(self, owner_code: str, owner_data: Dict) -> bool:
        """Update an existing owner"""
        try:
            success = self.controllers['owner'].update_owner(owner_code, owner_data)
            if success:
                self.log_activity("owner_updated", {
                    "owner_code": owner_code
                })
            return success
        except Exception as e:
            logger.error(f"Error updating owner: {e}")
            return False

    def delete_owner(self, owner_code: str) -> bool:
        """Delete an owner"""
        try:
            success = self.controllers['owner'].delete_owner(owner_code)
            if success:
                self.log_activity("owner_deleted", {
                    "owner_code": owner_code
                })
            return success
        except Exception as e:
            logger.error(f"Error deleting owner: {e}")
            return False

    # Reference Data Methods
    def get_property_types(self) -> List[tuple]:
        """Get property types for dropdowns"""
        return self.controllers['property'].get_property_types()

    def get_build_types(self) -> List[tuple]:
        """Get build types for dropdowns"""
        return self.controllers['property'].get_build_types()

    def get_offer_types(self) -> List[tuple]:
        """Get offer types for dropdowns"""
        return self.controllers['property'].get_offer_types()

    def get_provinces(self) -> List[tuple]:
        """Get provinces for dropdowns"""
        return self.controllers['property'].get_provinces()

    # Report Generation Methods
    def generate_property_summary_report(self, filters: Dict = None) -> Optional[str]:
        """Generate property summary report"""
        try:
            report_path = self.controllers['report'].generate_property_summary_report(filters)
            if report_path:
                self.log_activity("report_generated", {
                    "type": "property_summary",
                    "filters": filters,
                    "file": report_path
                })
            return report_path
        except Exception as e:
            logger.error(f"Error generating property summary report: {e}")
            return None

    def generate_owner_properties_report(self, owner_code: str = None) -> Optional[str]:
        """Generate owner properties report"""
        try:
            report_path = self.controllers['report'].generate_owner_properties_report(owner_code)
            if report_path:
                self.log_activity("report_generated", {
                    "type": "owner_properties",
                    "owner_code": owner_code,
                    "file": report_path
                })
            return report_path
        except Exception as e:
            logger.error(f"Error generating owner properties report: {e}")
            return None

    def generate_market_analysis_report(self) -> Optional[str]:
        """Generate market analysis report"""
        try:
            report_path = self.controllers['report'].generate_market_analysis_report()
            if report_path:
                self.log_activity("report_generated", {
                    "type": "market_analysis",
                    "file": report_path
                })
            return report_path
        except Exception as e:
            logger.error(f"Error generating market analysis report: {e}")
            return None

    def export_properties_to_csv(self, properties: List[Dict], filename: str = None) -> Optional[str]:
        """Export properties to CSV"""
        try:
            csv_path = self.controllers['report'].export_report_to_csv(properties, filename)
            if csv_path:
                self.log_activity("data_exported", {
                    "format": "csv",
                    "count": len(properties),
                    "file": csv_path
                })
            return csv_path
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            return None

    # Backup and Data Management Methods
    def create_full_backup(self) -> Optional[str]:
        """Create full database backup"""
        try:
            backup_path = self.controllers['backup'].create_full_backup()
            if backup_path:
                self.log_activity("backup_created", {
                    "type": "full_backup",
                    "file": backup_path
                })
            return backup_path
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return None

    def restore_from_backup(self, backup_path: str) -> bool:
        """Restore database from backup"""
        try:
            success = self.controllers['backup'].restore_from_backup(backup_path)
            if success:
                self.log_activity("backup_restored", {
                    "source": backup_path
                })
            return success
        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            return False

    def list_backups(self) -> List[Dict]:
        """List available backups"""
        return self.controllers['backup'].list_backups()

    def cleanup_old_backups(self, keep_count: int = 10) -> int:
        """Clean up old backups"""
        try:
            deleted_count = self.controllers['backup'].cleanup_old_backups(keep_count)
            if deleted_count > 0:
                self.log_activity("backups_cleaned", {
                    "deleted_count": deleted_count,
                    "kept_count": keep_count
                })
            return deleted_count
        except Exception as e:
            logger.error(f"Error cleaning backups: {e}")
            return 0

    # Settings Management Methods
    def get_settings(self) -> Dict:
        """Get current settings"""
        return self.controllers['settings'].load_settings()

    def update_settings(self, settings_data: Dict) -> bool:
        """Update system settings"""
        try:
            success = self.controllers['settings'].update_settings(settings_data)
            if success:
                self.log_activity("settings_updated", {
                    "updated_keys": list(settings_data.keys())
                })
                # Reload settings
                self.settings = self.controllers['settings'].load_settings()
            return success
        except Exception as e:
            logger.error(f"Error updating settings: {e}")
            return False

    def reset_settings(self) -> bool:
        """Reset settings to defaults"""
        try:
            success = self.controllers['settings'].reset_to_defaults()
            if success:
                self.log_activity("settings_reset", {})
                self.settings = self.controllers['settings'].load_settings()
            return success
        except Exception as e:
            logger.error(f"Error resetting settings: {e}")
            return False

    # Activity and Logging Methods
    def log_activity(self, activity_type: str, data: Dict):
        """Log system activity"""
        try:
            self.controllers['activity'].log_activity(activity_type, data)
        except Exception as e:
            logger.error(f"Error logging activity: {e}")

    def get_recent_activities(self, limit: int = 50) -> List[Dict]:
        """Get recent system activities"""
        try:
            return self.controllers['activity'].get_recent_activities(limit)
        except Exception as e:
            logger.error(f"Error getting recent activities: {e}")
            return []

    def get_activity_statistics(self) -> Dict:
        """Get activity statistics"""
        try:
            return self.controllers['activity'].get_statistics()
        except Exception as e:
            logger.error(f"Error getting activity statistics: {e}")
            return {}

    # System Status and Health Methods
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        try:
            status = {
                'database_connected': self._check_database_connection(),
                'total_properties': len(self.get_all_properties()),
                'total_owners': len(self.get_all_owners()),
                'recent_activities': len(self.get_recent_activities(10)),
                'available_backups': len(self.list_backups()),
                'settings_loaded': bool(self.settings),
                'system_health': 'healthy'
            }

            # Check for any issues
            if not status['database_connected']:
                status['system_health'] = 'database_error'
            elif status['total_properties'] == 0 and status['total_owners'] == 0:
                status['system_health'] = 'no_data'

            return status

        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {
                'system_health': 'error',
                'error_message': str(e)
            }

    def _check_database_connection(self) -> bool:
        """Check if database connection is working"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Database connection check failed: {e}")
            return False

    # Utility Methods
    def get_controller(self, controller_name: str):
        """Get specific controller instance"""
        return self.controllers.get(controller_name)

    def shutdown(self):
        """Graceful system shutdown"""
        try:
            self.log_activity("system_shutdown", {"timestamp": "now"})

            # Close database connections
            if hasattr(self.db_manager, 'close_connection'):
                self.db_manager.close_connection()

            logger.info("System shutdown completed")

        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.shutdown()
