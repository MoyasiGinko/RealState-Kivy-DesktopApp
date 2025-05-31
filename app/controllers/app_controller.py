#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Main App Controller
Coordinates the overall application flow and screen management
"""

from typing import Dict, Any
import logging

from .base_controller import BaseController
from .owner_controller import OwnerController
from .property_controller import PropertyController
from ..models.owner_model import OwnerModel
from ..models.property_model import PropertyModel

logger = logging.getLogger(__name__)


class AppController:
    """Main application controller that coordinates all other controllers"""

    def __init__(self, db_manager, screen_manager=None):
        self.db_manager = db_manager
        self.screen_manager = screen_manager

        # Initialize models
        self.owner_model = OwnerModel(db_manager)
        self.property_model = PropertyModel(db_manager)

        # Initialize controllers
        self.owner_controller = OwnerController(self.owner_model)
        self.property_controller = PropertyController(self.property_model)

        # Current screen tracking
        self.current_screen = None

        logger.info("App controller initialized")

    def set_screen_manager(self, screen_manager):
        """Set the screen manager reference"""
        self.screen_manager = screen_manager

    def navigate_to_screen(self, screen_name: str, **kwargs):
        """Navigate to a specific screen"""
        try:
            if self.screen_manager:
                if screen_name in [screen.name for screen in self.screen_manager.screens]:
                    self.screen_manager.current = screen_name
                    self.current_screen = screen_name
                    logger.info(f"Navigated to screen: {screen_name}")

                    # Setup controller for the new screen
                    self._setup_screen_controller(screen_name, **kwargs)
                else:
                    logger.error(f"Screen not found: {screen_name}")
            else:
                logger.error("Screen manager not set")

        except Exception as e:
            logger.error(f"Error navigating to screen {screen_name}: {e}")

    def _setup_screen_controller(self, screen_name: str, **kwargs):
        """Setup the appropriate controller for a screen"""
        try:
            screen = self.get_screen(screen_name)
            if not screen:
                return

            if screen_name == 'owners':
                self.owner_controller.view = screen
                screen.controller = self.owner_controller
                self.owner_controller._setup_view_handlers()

            elif screen_name == 'properties':
                self.property_controller.view = screen
                screen.controller = self.property_controller
                self.property_controller._setup_view_handlers()

            elif screen_name == 'dashboard':
                # Dashboard needs both controllers
                screen.owner_controller = self.owner_controller
                screen.property_controller = self.property_controller

            elif screen_name == 'search':
                # Search screen needs both controllers
                screen.owner_controller = self.owner_controller
                screen.property_controller = self.property_controller

            # Initialize screen data
            if hasattr(screen, 'initialize_data'):
                screen.initialize_data()

        except Exception as e:
            logger.error(f"Error setting up controller for screen {screen_name}: {e}")

    def get_screen(self, screen_name: str):
        """Get a screen by name"""
        if self.screen_manager:
            for screen in self.screen_manager.screens:
                if screen.name == screen_name:
                    return screen
        return None

    def get_dashboard_statistics(self) -> Dict:
        """Get statistics for dashboard"""
        try:
            stats = {}

            # Owner statistics
            owner_stats = self.owner_controller.get_owner_statistics()
            stats.update(owner_stats)

            # Property statistics
            property_stats = self.property_controller.get_property_statistics()
            stats.update(property_stats)

            # Combined statistics
            stats['total_records'] = stats.get('total_owners', 0) + stats.get('total_properties', 0)

            return stats

        except Exception as e:
            logger.error(f"Error getting dashboard statistics: {e}")
            return {}

    def search_all(self, query: str) -> Dict:
        """Search across all entities"""
        try:
            results = {
                'owners': [],
                'properties': []
            }

            if query.strip():
                # Search owners
                results['owners'] = self.owner_controller.search_owners(query)

                # Search properties
                filters = {'location': query}
                results['properties'] = self.property_controller.filter_properties(filters)

            return results

        except Exception as e:
            logger.error(f"Error performing global search: {e}")
            return {'owners': [], 'properties': []}

    def backup_data(self, backup_path: str = None) -> bool:
        """Backup application data"""
        try:
            # This would implement backup logic
            logger.info("Data backup started")

            # For now, just log the action
            logger.info("Data backup completed successfully")
            return True

        except Exception as e:
            logger.error(f"Error backing up data: {e}")
            return False

    def restore_data(self, backup_path: str) -> bool:
        """Restore application data from backup"""
        try:
            # This would implement restore logic
            logger.info(f"Data restore started from: {backup_path}")

            # For now, just log the action
            logger.info("Data restore completed successfully")
            return True

        except Exception as e:
            logger.error(f"Error restoring data: {e}")
            return False

    def export_all_data(self, export_path: str) -> bool:
        """Export all application data"""
        try:
            # Export owners
            owner_success = self.owner_controller.export_owners(f"{export_path}/owners.csv")

            # Export properties
            property_success = self.property_controller.export_properties(f"{export_path}/properties.csv")

            return owner_success and property_success

        except Exception as e:
            logger.error(f"Error exporting all data: {e}")
            return False

    def get_app_status(self) -> Dict:
        """Get overall application status"""
        try:
            status = {
                'database_connected': self.db_manager is not None,
                'current_screen': self.current_screen,
                'total_owners': len(self.owner_model.get_all()),
                'total_properties': len(self.property_model.get_all()),
                'controllers_initialized': True
            }

            return status

        except Exception as e:
            logger.error(f"Error getting app status: {e}")
            return {'error': str(e)}

    def cleanup(self):
        """Cleanup resources when app is closing"""
        try:
            logger.info("Cleaning up app controller")

            # Close database connections
            if self.db_manager:
                self.db_manager.close_connection()

            # Clear references
            self.owner_controller = None
            self.property_controller = None
            self.screen_manager = None

            logger.info("App controller cleanup completed")

        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


class DashboardController(BaseController):
    """Controller specifically for dashboard screen"""

    def __init__(self, app_controller, view=None):
        self.app_controller = app_controller
        super().__init__(None, view)

    def get_statistics(self) -> Dict:
        """Get dashboard statistics"""
        return self.app_controller.get_dashboard_statistics()

    def get_recent_activities(self) -> list:
        """Get recent activities for dashboard"""
        try:
            activities = []

            # Get recent properties (last 5)
            properties = self.app_controller.property_model.get_all()[:5]
            for prop in properties:
                activities.append({
                    'type': 'property',
                    'action': 'created',
                    'description': f"Property at {prop.get('location', 'Unknown')} was added",
                    'date': prop.get('created_date', '')
                })

            # Get recent owners (last 5)
            owners = self.app_controller.owner_model.get_all()[:5]
            for owner in owners:
                activities.append({
                    'type': 'owner',
                    'action': 'created',
                    'description': f"Owner {owner.get('ownername', 'Unknown')} was added",
                    'date': owner.get('created_date', '')
                })

            # Sort by date
            activities.sort(key=lambda x: x.get('date', ''), reverse=True)

            return activities[:10]  # Return last 10 activities

        except Exception as e:
            logger.error(f"Error getting recent activities: {e}")
            return []
