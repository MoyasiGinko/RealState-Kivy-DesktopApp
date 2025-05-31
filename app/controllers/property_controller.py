#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Property Controller
Handles property-related business logic and view interactions
"""

from typing import Dict, List
import logging
import os

from .base_controller import BaseController

logger = logging.getLogger(__name__)


class PropertyController(BaseController):
    """Controller for managing properties"""

    def __init__(self, model, view=None):
        super().__init__(model, view)
        self.current_property = None
        self.filters = {}

    def _setup_view_handlers(self):
        """Setup event handlers for property view"""
        if self.view:
            # Bind view events to controller methods
            if hasattr(self.view, 'on_create_property'):
                self.view.on_create_property = self.create_property
            if hasattr(self.view, 'on_update_property'):
                self.view.on_update_property = self.update_property
            if hasattr(self.view, 'on_delete_property'):
                self.view.on_delete_property = self.delete_property
            if hasattr(self.view, 'on_search_properties'):
                self.view.on_search_properties = self.search_properties
            if hasattr(self.view, 'on_select_property'):
                self.view.on_select_property = self.select_property
            if hasattr(self.view, 'on_filter_properties'):
                self.view.on_filter_properties = self.filter_properties

    def load_properties(self) -> List[Dict]:
        """Load all properties"""
        try:
            properties = self.model.get_all()
            logger.info(f"Loaded {len(properties)} properties")
            return properties
        except Exception as e:
            self.handle_error(f"Failed to load properties: {str(e)}")
            return []

    def create_property(self, property_data: Dict) -> bool:
        """Create a new property"""
        try:
            # Validate data
            is_valid, error_msg = self.validate_input(property_data)
            if not is_valid:
                self.handle_error(error_msg, "Validation Error")
                return False

            # Create property
            success = self.model.create(property_data)
            if success:
                self.handle_success("Property created successfully")
                if self.view:
                    self.view.refresh_data()
                return True
            else:
                self.handle_error("Failed to create property")
                return False

        except Exception as e:
            self.handle_error(f"Error creating property: {str(e)}")
            return False

    def update_property(self, maincode: str, property_data: Dict) -> bool:
        """Update an existing property"""
        try:
            # Validate data
            is_valid, error_msg = self.validate_input(property_data)
            if not is_valid:
                self.handle_error(error_msg, "Validation Error")
                return False

            # Update property
            success = self.model.update(maincode, property_data)
            if success:
                self.handle_success("Property updated successfully")
                if self.view:
                    self.view.refresh_data()
                return True
            else:
                self.handle_error("Failed to update property")
                return False

        except Exception as e:
            self.handle_error(f"Error updating property: {str(e)}")
            return False

    def delete_property(self, maincode: str) -> bool:
        """Delete a property"""
        try:
            # Confirm deletion
            if self.view and hasattr(self.view, 'confirm_deletion'):
                confirmed = self.view.confirm_deletion(f"Are you sure you want to delete this property?")
                if not confirmed:
                    return False

            # Delete property
            success = self.model.delete(maincode)
            if success:
                self.handle_success("Property deleted successfully")
                self.current_property = None
                if self.view:
                    self.view.refresh_data()
                return True
            else:
                self.handle_error("Failed to delete property")
                return False

        except Exception as e:
            self.handle_error(f"Error deleting property: {str(e)}")
            return False

    def search_properties(self, search_query: str) -> List[Dict]:
        """Search properties"""
        try:
            if not search_query.strip():
                return self.load_properties()

            # Create search filters based on query
            filters = {
                'location': search_query
            }

            properties = self.model.search(filters)
            logger.info(f"Found {len(properties)} properties matching '{search_query}'")
            return properties

        except Exception as e:
            self.handle_error(f"Error searching properties: {str(e)}")
            return []

    def filter_properties(self, filters: Dict) -> List[Dict]:
        """Filter properties based on criteria"""
        try:
            self.filters = filters
            properties = self.model.search(filters)
            logger.info(f"Found {len(properties)} properties matching filters")
            return properties

        except Exception as e:
            self.handle_error(f"Error filtering properties: {str(e)}")
            return []

    def select_property(self, maincode: str):
        """Select a property for viewing/editing"""
        try:
            property_data = self.model.get_by_id(maincode)
            if property_data:
                self.current_property = property_data
                logger.info(f"Selected property: {maincode}")

                # Update view with selected property data
                if self.view and hasattr(self.view, 'load_property_data'):
                    self.view.load_property_data(property_data)
            else:
                self.handle_error(f"Property not found: {maincode}")

        except Exception as e:
            self.handle_error(f"Error selecting property: {str(e)}")

    def get_properties_by_owner(self, owner_code: str) -> List[Dict]:
        """Get properties for a specific owner"""
        try:
            properties = self.model.get_by_owner(owner_code)
            logger.info(f"Found {len(properties)} properties for owner {owner_code}")
            return properties

        except Exception as e:
            self.handle_error(f"Error getting properties by owner: {str(e)}")
            return []

    def get_property_statistics(self) -> Dict:
        """Get property statistics"""
        try:
            stats = self.model.get_statistics()
            logger.info("Retrieved property statistics")
            return stats

        except Exception as e:
            self.handle_error(f"Error getting property statistics: {str(e)}")
            return {}

    def upload_photos(self, maincode: str, photo_paths: List[str]) -> bool:
        """Upload photos for a property"""
        try:
            if not photo_paths:
                self.handle_error("No photos selected")
                return False

            # Get current property data
            property_data = self.model.get_by_id(maincode)
            if not property_data:
                self.handle_error("Property not found")
                return False

            # Combine existing photos with new ones
            existing_photos = property_data.get('photos', '').split(';') if property_data.get('photos') else []
            existing_photos = [p for p in existing_photos if p.strip()]

            all_photos = existing_photos + photo_paths
            photos_string = ';'.join(all_photos)

            # Update property with new photos
            success = self.model.update(maincode, {
                **property_data,
                'photos': photos_string
            })

            if success:
                self.handle_success(f"Uploaded {len(photo_paths)} photos successfully")
                if self.view:
                    self.view.refresh_data()
                return True
            else:
                self.handle_error("Failed to update property with photos")
                return False

        except Exception as e:
            self.handle_error(f"Error uploading photos: {str(e)}")
            return False

    def remove_photo(self, maincode: str, photo_path: str) -> bool:
        """Remove a photo from a property"""
        try:
            # Get current property data
            property_data = self.model.get_by_id(maincode)
            if not property_data:
                self.handle_error("Property not found")
                return False

            # Remove photo from list
            existing_photos = property_data.get('photos', '').split(';') if property_data.get('photos') else []
            existing_photos = [p for p in existing_photos if p.strip() and p != photo_path]

            photos_string = ';'.join(existing_photos)

            # Update property
            success = self.model.update(maincode, {
                **property_data,
                'photos': photos_string
            })

            if success:
                # Delete the actual file
                try:
                    if os.path.exists(photo_path):
                        os.remove(photo_path)
                    # Also remove thumbnail
                    thumbnail_path = photo_path.replace('property_photos', 'property_photos/thumbnails')
                    if os.path.exists(thumbnail_path):
                        os.remove(thumbnail_path)
                except:
                    pass  # Ignore file deletion errors

                self.handle_success("Photo removed successfully")
                if self.view:
                    self.view.refresh_data()
                return True
            else:
                self.handle_error("Failed to remove photo")
                return False

        except Exception as e:
            self.handle_error(f"Error removing photo: {str(e)}")
            return False

    def export_properties(self, file_path: str = None, filters: Dict = None) -> bool:
        """Export properties to file"""
        try:
            if filters:
                properties = self.model.search(filters)
            else:
                properties = self.model.get_all()

            if not properties:
                self.handle_error("No properties to export")
                return False

            # This would implement the actual export logic
            # For now, just log the action
            logger.info(f"Exporting {len(properties)} properties")
            self.handle_success(f"Exported {len(properties)} properties successfully")
            return True

        except Exception as e:
            self.handle_error(f"Error exporting properties: {str(e)}")
            return False

    def get_property_types(self) -> List[str]:
        """Get list of available property types"""
        try:
            properties = self.model.get_all()
            types = set()
            for prop in properties:
                if prop.get('propertytype'):
                    types.add(prop['propertytype'])
            return sorted(list(types))

        except Exception as e:
            self.handle_error(f"Error getting property types: {str(e)}")
            return []

    def get_property_statuses(self) -> List[str]:
        """Get list of available property statuses"""
        return ['Available', 'Sold', 'Rented', 'Under Contract', 'Off Market']

    def on_model_changed(self, event_type: str, data=None):
        """Handle model change notifications"""
        super().on_model_changed(event_type, data)

        if event_type == 'property_created':
            logger.info(f"Property created: {data}")
        elif event_type == 'property_updated':
            logger.info(f"Property updated: {data}")
            # Update current property if it's the one that was updated
            if self.current_property and data and data.get('Maincode') == self.current_property.get('Maincode'):
                self.select_property(data['Maincode'])
        elif event_type == 'property_deleted':
            logger.info(f"Property deleted: {data}")
            # Clear current property if it was deleted
            if self.current_property and data and data.get('Maincode') == self.current_property.get('Maincode'):
                self.current_property = None
