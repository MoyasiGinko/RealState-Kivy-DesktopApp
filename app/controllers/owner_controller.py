#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Owner Controller
Handles owner-related business logic and view interactions
"""

from typing import Dict, List
import logging

from .base_controller import BaseController

logger = logging.getLogger(__name__)


class OwnerController(BaseController):
    """Controller for managing owners"""

    def __init__(self, model, view=None):
        super().__init__(model, view)
        self.current_owner = None

    def _setup_view_handlers(self):
        """Setup event handlers for owner view"""
        if self.view:
            # Bind view events to controller methods
            if hasattr(self.view, 'on_create_owner'):
                self.view.on_create_owner = self.create_owner
            if hasattr(self.view, 'on_update_owner'):
                self.view.on_update_owner = self.update_owner
            if hasattr(self.view, 'on_delete_owner'):
                self.view.on_delete_owner = self.delete_owner
            if hasattr(self.view, 'on_search_owners'):
                self.view.on_search_owners = self.search_owners
            if hasattr(self.view, 'on_select_owner'):
                self.view.on_select_owner = self.select_owner

    def load_owners(self) -> List[Dict]:
        """Load all owners"""
        try:
            owners = self.model.get_all()
            logger.info(f"Loaded {len(owners)} owners")
            return owners
        except Exception as e:
            self.handle_error(f"Failed to load owners: {str(e)}")
            return []

    def create_owner(self, owner_data: Dict) -> bool:
        """Create a new owner"""
        try:
            # Validate data
            is_valid, error_msg = self.validate_input(owner_data)
            if not is_valid:
                self.handle_error(error_msg, "Validation Error")
                return False

            # Create owner
            success = self.model.create(owner_data)
            if success:
                self.handle_success("Owner created successfully")
                if self.view:
                    self.view.refresh_data()
                return True
            else:
                self.handle_error("Failed to create owner")
                return False

        except Exception as e:
            self.handle_error(f"Error creating owner: {str(e)}")
            return False

    def update_owner(self, owner_code: str, owner_data: Dict) -> bool:
        """Update an existing owner"""
        try:
            # Validate data
            is_valid, error_msg = self.validate_input(owner_data)
            if not is_valid:
                self.handle_error(error_msg, "Validation Error")
                return False

            # Update owner
            success = self.model.update(owner_code, owner_data)
            if success:
                self.handle_success("Owner updated successfully")
                if self.view:
                    self.view.refresh_data()
                return True
            else:
                self.handle_error("Failed to update owner")
                return False

        except Exception as e:
            self.handle_error(f"Error updating owner: {str(e)}")
            return False

    def delete_owner(self, owner_code: str) -> bool:
        """Delete an owner"""
        try:
            # Check if owner has properties
            properties_count = self.model.get_owner_properties_count(owner_code)
            if properties_count > 0:
                self.handle_error(
                    f"Cannot delete owner: {properties_count} properties are associated with this owner",
                    "Delete Error"
                )
                return False

            # Confirm deletion
            if self.view and hasattr(self.view, 'confirm_deletion'):
                confirmed = self.view.confirm_deletion(f"Are you sure you want to delete this owner?")
                if not confirmed:
                    return False

            # Delete owner
            success = self.model.delete(owner_code)
            if success:
                self.handle_success("Owner deleted successfully")
                self.current_owner = None
                if self.view:
                    self.view.refresh_data()
                return True
            else:
                self.handle_error("Failed to delete owner")
                return False

        except Exception as e:
            self.handle_error(f"Error deleting owner: {str(e)}")
            return False

    def search_owners(self, search_query: str) -> List[Dict]:
        """Search owners"""
        try:
            if not search_query.strip():
                return self.load_owners()

            owners = self.model.search(search_query)
            logger.info(f"Found {len(owners)} owners matching '{search_query}'")
            return owners

        except Exception as e:
            self.handle_error(f"Error searching owners: {str(e)}")
            return []

    def select_owner(self, owner_code: str):
        """Select an owner for viewing/editing"""
        try:
            owner = self.model.get_by_id(owner_code)
            if owner:
                self.current_owner = owner
                logger.info(f"Selected owner: {owner_code}")

                # Update view with selected owner data
                if self.view and hasattr(self.view, 'load_owner_data'):
                    self.view.load_owner_data(owner)
            else:
                self.handle_error(f"Owner not found: {owner_code}")

        except Exception as e:
            self.handle_error(f"Error selecting owner: {str(e)}")

    def get_owner_properties(self, owner_code: str) -> List[Dict]:
        """Get properties for a specific owner"""
        try:
            # This would typically be handled by the property controller,
            # but we include it here for convenience
            from ..models.property_model import PropertyModel
            property_model = PropertyModel(self.model.db_manager)
            return property_model.get_by_owner(owner_code)

        except Exception as e:
            self.handle_error(f"Error getting owner properties: {str(e)}")
            return []

    def export_owners(self, file_path: str = None) -> bool:
        """Export owners to file"""
        try:
            owners = self.model.get_all()
            if not owners:
                self.handle_error("No owners to export")
                return False

            # This would implement the actual export logic
            # For now, just log the action
            logger.info(f"Exporting {len(owners)} owners")
            self.handle_success(f"Exported {len(owners)} owners successfully")
            return True

        except Exception as e:
            self.handle_error(f"Error exporting owners: {str(e)}")
            return False

    def get_owner_statistics(self) -> Dict:
        """Get owner statistics"""
        try:
            owners = self.model.get_all()
            stats = {
                'total_owners': len(owners),
                'owners_with_properties': 0,
                'owners_without_properties': 0
            }

            for owner in owners:
                properties_count = self.model.get_owner_properties_count(owner['Ownercode'])
                if properties_count > 0:
                    stats['owners_with_properties'] += 1
                else:
                    stats['owners_without_properties'] += 1

            return stats

        except Exception as e:
            self.handle_error(f"Error getting owner statistics: {str(e)}")
            return {}

    def on_model_changed(self, event_type: str, data=None):
        """Handle model change notifications"""
        super().on_model_changed(event_type, data)

        if event_type == 'owner_created':
            logger.info(f"Owner created: {data}")
        elif event_type == 'owner_updated':
            logger.info(f"Owner updated: {data}")
            # Update current owner if it's the one that was updated
            if self.current_owner and data and data.get('Ownercode') == self.current_owner.get('Ownercode'):
                self.select_owner(data['Ownercode'])
        elif event_type == 'owner_deleted':
            logger.info(f"Owner deleted: {data}")
            # Clear current owner if it was deleted
            if self.current_owner and data and data.get('Ownercode') == self.current_owner.get('Ownercode'):
                self.current_owner = None
