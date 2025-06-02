#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Property Controller
Handles property-related business logic and view interactions
"""

from typing import Dict, List, Optional
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

    def update_property(self, company_code: str, property_data: Dict) -> bool:
        """Update an existing property"""
        try:
            # Validate data
            is_valid, error_msg = self.validate_input(property_data)
            if not is_valid:
                self.handle_error(error_msg, "Validation Error")
                return False

            # Update property
            success = self.model.update(company_code, property_data)
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

    def delete_property(self, company_code: str) -> bool:
        """Delete a property with confirmation"""
        try:
            # Confirm deletion
            if self.view and hasattr(self.view, 'confirm_deletion'):
                confirmed = self.view.confirm_deletion(f"Are you sure you want to delete this property?")
                if not confirmed:
                    return False

            # Delete property
            success = self.model.delete(company_code)
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
        """Search properties by various criteria"""
        try:
            if not search_query.strip():
                return self.load_properties()

            # Create search filters based on query
            filters = {
                'search_term': search_query
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

    def select_property(self, company_code: str):
        """Select a property for viewing/editing"""
        try:
            property_data = self.model.get_by_id(company_code)
            if property_data:
                self.current_property = property_data
                logger.info(f"Selected property: {company_code}")

                # Update view with selected property data
                if self.view and hasattr(self.view, 'load_property_data'):
                    self.view.load_property_data(property_data)
            else:
                self.handle_error(f"Property not found: {company_code}")

        except Exception as e:
            self.handle_error(f"Error selecting property: {str(e)}")

    def get_properties_by_owner(self, owner_code: str) -> List[Dict]:
        """Get properties for a specific owner"""
        try:
            filters = {'owner_code': owner_code}
            properties = self.model.search(filters)
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

    def get_property_photos(self, company_code: str) -> List[Dict]:
        """Get photos for a property"""
        try:
            photos = self.model.get_photos(company_code)
            logger.info(f"Found {len(photos)} photos for property {company_code}")
            return photos

        except Exception as e:
            self.handle_error(f"Error getting photos for property {company_code}: {str(e)}")
            return []

    def add_property_photo(self, company_code: str, photo_path: str, photo_name: str) -> bool:
        """Add photo to a property"""
        try:
            success = self.model.add_photo(company_code, photo_path, photo_name)
            if success:
                self.handle_success("Photo added successfully")
                if self.view:
                    self.view.refresh_data()
                return True
            else:
                self.handle_error("Failed to add photo")
                return False

        except Exception as e:
            self.handle_error(f"Error adding photo: {str(e)}")
            return False

    def remove_property_photo(self, photo_name: str) -> bool:
        """Remove a photo from a property"""
        try:
            success = self.model.delete_photo(photo_name)
            if success:
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

    def advanced_search(self, criteria: Dict) -> List[Dict]:
        """Perform advanced search with multiple criteria"""
        try:
            properties = self.model.advanced_search(criteria)
            logger.info(f"Advanced search found {len(properties)} properties")
            return properties

        except Exception as e:
            self.handle_error(f"Error in advanced search: {str(e)}")
            return []

    def get_property_summary(self, company_code: str) -> Optional[Dict]:
        """Get detailed property information"""
        try:
            property_data = self.model.get_property_summary(company_code)
            if property_data:
                logger.info(f"Retrieved property summary for {company_code}")
                return property_data
            else:
                self.handle_error(f"Property not found: {company_code}")
                return None

        except Exception as e:
            self.handle_error(f"Error getting property summary: {str(e)}")
            return None

    def export_to_file(self, properties: List[Dict], format_type: str = 'csv') -> Optional[str]:
        """Export properties to file with enhanced functionality"""
        try:
            if not properties:
                self.handle_error("No properties to export")
                return None

            file_path = self.model.export_properties(properties, format_type)
            if file_path:
                self.handle_success(f"Properties exported to {file_path}")
                return file_path
            else:
                self.handle_error("Failed to export properties")
                return None

        except Exception as e:
            self.handle_error(f"Error exporting properties: {str(e)}")
            return None

    def generate_property_report(self, company_code: str, include_photos: bool = True) -> Optional[str]:
        """Generate comprehensive property report"""
        try:
            property_data = self.get_property_summary(company_code)
            if not property_data:
                return None

            # Create report content
            report_content = self._format_property_report(property_data, include_photos)

            # Save to file
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"property_report_{company_code}_{timestamp}.txt"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report_content)

            self.handle_success(f"Property report generated: {filename}")
            return filename

        except Exception as e:
            self.handle_error(f"Error generating property report: {str(e)}")
            return None

    def _format_property_report(self, property_data: Dict, include_photos: bool = True) -> str:
        """Format property data into a readable report"""
        report = f"""
PROPERTY REPORT
================

Property Code: {property_data.get('realstatecode', 'N/A')}
Company Code: {property_data.get('Companyco', 'N/A')}

BASIC INFORMATION
-----------------
Property Type: {property_data.get('property_type_desc', 'N/A')}
Build Type: {property_data.get('build_type_desc', 'N/A')}
Year Built: {property_data.get('Yearmake', 'N/A')}
Offer Type: {property_data.get('offer_type_desc', 'N/A')}

SPECIFICATIONS
--------------
Area: {property_data.get('Property-area', 'N/A')} sqm
Facade: {property_data.get('Property-facade', 'N/A')} m
Depth: {property_data.get('Property-depth', 'N/A')} m
Bedrooms: {property_data.get('N-of-bedrooms', 'N/A')}
Bathrooms: {property_data.get('N-of bathrooms', 'N/A')}
Corner Property: {'Yes' if property_data.get('Property-corner') else 'No'}

LOCATION
--------
Province: {property_data.get('province_desc', 'N/A')}
Region: {property_data.get('region_desc', 'N/A')}
Address: {property_data.get('Property-address', 'N/A')}

OWNER INFORMATION
-----------------
Owner: {property_data.get('ownername', 'N/A')}
Phone: {property_data.get('ownerphone', 'N/A')}

DESCRIPTION
-----------
{property_data.get('Descriptions', 'No description available')}
"""

        if include_photos and property_data.get('photos'):
            report += "\n\nPHOTOS\n------\n"
            for i, photo in enumerate(property_data['photos'], 1):
                report += f"{i}. {photo.get('Photoname', 'Unknown')}\n"

        return report

    def get_reference_data(self, category: str) -> List[tuple]:
        """Get reference data for dropdowns"""
        try:
            data = self.model.get_reference_data(category)
            logger.info(f"Retrieved {len(data)} items for category {category}")
            return data

        except Exception as e:
            self.handle_error(f"Error getting reference data: {str(e)}")
            return []

    def get_property_types(self) -> List[tuple]:
        """Get property types for dropdown"""
        return self.model.get_property_types()

    def get_build_types(self) -> List[tuple]:
        """Get build types for dropdown"""
        return self.model.get_build_types()

    def get_offer_types(self) -> List[tuple]:
        """Get offer types for dropdown"""
        return self.model.get_offer_types()

    def get_provinces(self) -> List[tuple]:
        """Get provinces for dropdown"""
        return self.model.get_provinces()

    def get_statistics(self) -> Dict:
        """Get property statistics"""
        try:
            stats = self.model.get_statistics()
            logger.info("Retrieved property statistics")
            return stats

        except Exception as e:
            self.handle_error(f"Error getting statistics: {str(e)}")
            return {}

    def on_model_changed(self, event_type: str, data=None):
        """Handle model change notifications"""
        super().on_model_changed(event_type, data)

        if event_type == 'property_created':
            logger.info(f"Property created: {data}")
        elif event_type == 'property_updated':
            logger.info(f"Property updated: {data}")
            # Update current property if it's the one that was updated
            if self.current_property and data and data.get('Companyco') == self.current_property.get('Companyco'):
                self.select_property(data['Companyco'])
        elif event_type == 'property_deleted':
            logger.info(f"Property deleted: {data}")
            # Clear current property if it was deleted
            if self.current_property and data and data.get('Companyco') == self.current_property.get('Companyco'):
                self.current_property = None
