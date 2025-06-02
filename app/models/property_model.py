#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Property Model
Handles all property-related database operations and business logic
"""

from typing import Dict, List, Optional
import logging
from datetime import datetime

from .base_model import BaseModel

logger = logging.getLogger(__name__)


class PropertyModel(BaseModel):
    """Model for managing properties"""

    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.table_name = 'Realstatspecification'

    def get_all(self) -> List[Dict]:
        """Get all properties with owner information"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT r.Companyco, r.realstatecode, r.Rstatetcode, r.Yearmake,
                       r."Buildtcode ", r."Property-area", r."Unitm-code",
                       r."Property-facade", r."Property-depth", r."N-of-bedrooms",
                       r."N-of bathrooms", r."Property-corner", r."Offer-Type-Code",
                       r."Province-code ", r."Region-code", r."Property-address",
                       r.Photosituation, r.Ownercode, r.Descriptions, o.ownername
                FROM Realstatspecification r
                LEFT JOIN Owners o ON r.Ownercode = o.Ownercode
                ORDER BY r.Companyco DESC
            """)

            columns = [description[0] for description in cursor.description]
            results = []

            for row in cursor.fetchall():
                property_dict = dict(zip(columns, row))
                results.append(property_dict)

            conn.close()
            return results

        except Exception as e:
            logger.error(f"Error getting all properties: {e}")
            return []

    def get_by_id(self, company_code: str) -> Optional[Dict]:
        """Get property by company code"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT r.Companyco, r.realstatecode, r.Rstatetcode, r.Yearmake,
                       r."Buildtcode ", r."Property-area", r."Unitm-code",
                       r."Property-facade", r."Property-depth", r."N-of-bedrooms",
                       r."N-of bathrooms", r."Property-corner", r."Offer-Type-Code",
                       r."Province-code ", r."Region-code", r."Property-address",
                       r.Photosituation, r.Ownercode, r.Descriptions, o.ownername
                FROM Realstatspecification r
                LEFT JOIN Owners o ON r.Ownercode = o.Ownercode
                WHERE r.Companyco = ?
            """, (company_code,))

            row = cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                result = dict(zip(columns, row))
                conn.close()
                return result

            conn.close()
            return None

        except Exception as e:
            logger.error(f"Error getting property {company_code}: {e}")
            return None

    def create(self, data: Dict) -> bool:
        """Create new property"""
        try:
            # Validate data
            is_valid, error_msg = self.validate_data(data)
            if not is_valid:
                logger.error(f"Invalid property data: {error_msg}")
                return False

            # Use database manager's add_property method
            company_code = self.db_manager.add_property(data)
            if company_code:
                logger.info(f"Property created with company code: {company_code}")
                return True
            else:
                logger.error("Failed to create property")
                return False

        except Exception as e:
            logger.error(f"Error creating property: {e}")
            return False

    def update(self, company_code: str, data: Dict) -> bool:
        """Update existing property"""
        try:
            # Validate data
            is_valid, error_msg = self.validate_data(data)
            if not is_valid:
                logger.error(f"Invalid property data: {error_msg}")
                return False

            # Use database manager's update_property method
            success = self.db_manager.update_property(company_code, data)
            if success:
                logger.info(f"Property {company_code} updated successfully")
                return True
            else:
                logger.error(f"Failed to update property {company_code}")
                return False

        except Exception as e:
            logger.error(f"Error updating property {company_code}: {e}")
            return False

    def delete(self, company_code: str) -> bool:
        """Delete property"""
        try:
            # Use database manager's delete_property method
            success = self.db_manager.delete_property(company_code)
            if success:
                logger.info(f"Property {company_code} deleted successfully")
                return True
            else:
                logger.error(f"Failed to delete property {company_code}")
                return False

        except Exception as e:
            logger.error(f"Error deleting property {company_code}: {e}")
            return False

    def search(self, filters: Dict) -> List[Dict]:
        """Search properties with filters"""
        try:
            # Use database manager's get_properties method with filters
            properties = self.db_manager.get_properties(filters)
            logger.info(f"Found {len(properties)} properties matching filters")
            return properties

        except Exception as e:
            logger.error(f"Error searching properties: {e}")
            return []

    def advanced_search(self, criteria: Dict) -> List[Dict]:
        """Perform advanced search with multiple criteria"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            # Build dynamic query based on criteria
            base_query = """
                SELECT r.Companyco, r.realstatecode, r.Rstatetcode, r.Yearmake,
                       r."Buildtcode ", r."Property-area", r."Unitm-code",
                       r."Property-facade", r."Property-depth", r."N-of-bedrooms",
                       r."N-of bathrooms", r."Property-corner", r."Offer-Type-Code",
                       r."Province-code ", r."Region-code", r."Property-address",
                       r.Photosituation, r.Ownercode, r.Descriptions, o.ownername,
                       pt.Description as property_type_desc,
                       bt.Description as build_type_desc,                ot.name as offer_type_desc
                FROM Realstatspecification r
                LEFT JOIN Owners o ON r.Ownercode = o.Ownercode
                LEFT JOIN Maincode pt ON r.Rstatetcode = pt.code AND pt.recty = '03'
                LEFT JOIN Maincode bt ON r."Buildtcode " = bt.code AND bt.recty = '04'
                LEFT JOIN Maincode ot ON r."Offer-Type-Code" = ot.code AND ot.recty = '06'
                WHERE 1=1
            """

            params = []

            # Add search conditions based on criteria
            if criteria.get('search_term'):
                base_query += """ AND (
                    r.realstatecode LIKE ? OR
                    o.ownername LIKE ? OR
                    r."Property-address" LIKE ? OR
                    r.Descriptions LIKE ?
                )"""
                search_term = f"%{criteria['search_term']}%"
                params.extend([search_term, search_term, search_term, search_term])

            if criteria.get('property_type'):
                base_query += " AND r.Rstatetcode = ?"
                params.append(criteria['property_type'])

            if criteria.get('build_type'):
                base_query += " AND r.\"Buildtcode \" = ?"
                params.append(criteria['build_type'])

            if criteria.get('offer_type'):
                base_query += " AND r.\"Offer-Type-Code\" = ?"
                params.append(criteria['offer_type'])

            if criteria.get('province'):
                base_query += " AND r.\"Province-code \" = ?"
                params.append(criteria['province'])

            if criteria.get('region'):
                base_query += " AND r.\"Region-code\" = ?"
                params.append(criteria['region'])

            if criteria.get('min_area'):
                base_query += " AND r.\"Property-area\" >= ?"
                params.append(float(criteria['min_area']))

            if criteria.get('max_area'):
                base_query += " AND r.\"Property-area\" <= ?"
                params.append(float(criteria['max_area']))

            if criteria.get('min_bedrooms'):
                base_query += " AND r.\"N-of-bedrooms\" >= ?"
                params.append(int(criteria['min_bedrooms']))

            if criteria.get('max_bedrooms'):
                base_query += " AND r.\"N-of-bedrooms\" <= ?"
                params.append(int(criteria['max_bedrooms']))

            if criteria.get('min_bathrooms'):
                base_query += " AND r.\"N-of bathrooms\" >= ?"
                params.append(int(criteria['min_bathrooms']))

            if criteria.get('max_bathrooms'):
                base_query += " AND r.\"N-of bathrooms\" <= ?"
                params.append(int(criteria['max_bathrooms']))

            if criteria.get('is_corner') is not None:
                base_query += " AND r.\"Property-corner\" = ?"
                params.append(1 if criteria['is_corner'] else 0)

            if criteria.get('year_from'):
                base_query += " AND r.Yearmake >= ?"
                params.append(criteria['year_from'])

            if criteria.get('year_to'):
                base_query += " AND r.Yearmake <= ?"
                params.append(criteria['year_to'])

            if criteria.get('owner_name'):
                base_query += " AND o.ownername LIKE ?"
                params.append(f"%{criteria['owner_name']}%")

            base_query += " ORDER BY r.Companyco DESC"

            cursor.execute(base_query, params)
            columns = [description[0] for description in cursor.description]
            results = []

            for row in cursor.fetchall():
                property_dict = dict(zip(columns, row))
                results.append(property_dict)

            conn.close()
            logger.info(f"Advanced search found {len(results)} properties")
            return results

        except Exception as e:
            logger.error(f"Error in advanced search: {e}")
            return []

    def get_property_summary(self, company_code: str) -> Optional[Dict]:
        """Get property summary with all related information"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT r.*, o.ownername, o.ownerphone,
                       pt.Description as property_type_desc,
                       bt.Description as build_type_desc,
                       ot.Description as offer_type_desc,                       pr.name as province_desc,
                       reg.name as region_desc
                FROM Realstatspecification r
                LEFT JOIN Owners o ON r.Ownercode = o.Ownercode
                LEFT JOIN Maincode pt ON r.Rstatetcode = pt.code AND pt.recty = '03'
                LEFT JOIN Maincode bt ON r."Buildtcode " = bt.code AND bt.recty = '04'
                LEFT JOIN Maincode ot ON r."Offer-Type-Code" = ot.code AND ot.recty = '06'
                LEFT JOIN Maincode pr ON r."Province-code " = pr.code AND pr.recty = '01'
                LEFT JOIN Maincode reg ON r."Region-code" = reg.code AND reg.recty = '02'
                WHERE r.Companyco = ?
            """, (company_code,))

            row = cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                property_dict = dict(zip(columns, row))

                # Get photos
                photos = self.get_photos(company_code)
                property_dict['photos'] = photos

                conn.close()
                return property_dict

            conn.close()
            return None

        except Exception as e:
            logger.error(f"Error getting property summary for {company_code}: {e}")
            return None

    def export_properties(self, properties: List[Dict], format_type: str = 'csv') -> Optional[str]:
        """Export properties to file"""
        try:
            import csv
            import json
            from datetime import datetime
            import os

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            if format_type.lower() == 'csv':
                filename = f"properties_export_{timestamp}.csv"

                if properties:
                    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                        fieldnames = properties[0].keys()
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        for property_data in properties:
                            writer.writerow(property_data)

                    logger.info(f"Properties exported to CSV: {filename}")
                    return os.path.abspath(filename)

            elif format_type.lower() == 'json':
                filename = f"properties_export_{timestamp}.json"

                with open(filename, 'w', encoding='utf-8') as jsonfile:
                    json.dump(properties, jsonfile, indent=2, ensure_ascii=False, default=str)

                logger.info(f"Properties exported to JSON: {filename}")
                return os.path.abspath(filename)

            else:
                logger.error(f"Unsupported export format: {format_type}")
                return None

        except Exception as e:
            logger.error(f"Error exporting properties: {e}")
            return None

    def get_photos(self, company_code: str) -> List[Dict]:
        """Get property photos"""
        try:
            photos = self.db_manager.get_property_photos(company_code)
            logger.info(f"Found {len(photos)} photos for property {company_code}")
            return photos

        except Exception as e:
            logger.error(f"Error getting photos for property {company_code}: {e}")
            return []

    def add_photo(self, company_code: str, photo_path: str, photo_name: str) -> bool:
        """Add photo to property"""
        try:
            success = self.db_manager.add_property_photo(company_code, photo_path, photo_name)
            if success:
                logger.info(f"Photo added to property {company_code}: {photo_name}")
                return True
            else:
                logger.error(f"Failed to add photo to property {company_code}")
                return False

        except Exception as e:
            logger.error(f"Error adding photo to property {company_code}: {e}")
            return False

    def delete_photo(self, photo_name: str) -> bool:
        """Delete property photo"""
        try:
            success = self.db_manager.delete_property_photo(photo_name)
            if success:
                logger.info(f"Photo deleted: {photo_name}")
                return True
            else:
                logger.error(f"Failed to delete photo: {photo_name}")
                return False

        except Exception as e:
            logger.error(f"Error deleting photo {photo_name}: {e}")
            return False

    def get_reference_data(self, category: str) -> List[tuple]:
        """Get reference data by category"""
        try:
            data = self.db_manager.get_reference_data(category)
            logger.info(f"Found {len(data)} items for category {category}")
            return data

        except Exception as e:
            logger.error(f"Error getting reference data for category {category}: {e}")
            return []

    def get_property_types(self) -> List[tuple]:
        """Get all property types"""
        return self.get_reference_data('03')

    def get_build_types(self) -> List[tuple]:
        """Get all build types"""
        return self.get_reference_data('04')

    def get_offer_types(self) -> List[tuple]:
        """Get all offer types"""
        return self.get_reference_data('06')

    def get_provinces(self) -> List[tuple]:
        """Get all provinces"""
        return self.db_manager.get_provinces()

    def validate_data(self, data: Dict) -> tuple[bool, str]:
        """Validate property data"""
        required_fields = ['property_type', 'area', 'address', 'owner_code']

        for field in required_fields:
            if not data.get(field):
                return False, f"Missing required field: {field}"

        # Validate numeric fields
        if data.get('area') and not isinstance(data['area'], (int, float)):
            try:
                float(data['area'])
            except (ValueError, TypeError):
                return False, "Area must be a valid number"

        if data.get('facade') and data['facade']:
            try:
                float(data['facade'])
            except (ValueError, TypeError):
                return False, "Facade must be a valid number"

        if data.get('depth') and data['depth']:
            try:
                float(data['depth'])
            except (ValueError, TypeError):
                return False, "Depth must be a valid number"

        # Validate integer fields
        if data.get('bedrooms') and data['bedrooms']:
            try:
                int(data['bedrooms'])
            except (ValueError, TypeError):
                return False, "Bedrooms must be a valid number"

        if data.get('bathrooms') and data['bathrooms']:
            try:
                int(data['bathrooms'])
            except (ValueError, TypeError):
                return False, "Bathrooms must be a valid number"

        return True, ""

    def get_statistics(self) -> Dict:
        """Get property statistics"""
        try:
            stats = self.db_manager.get_statistics()
            return stats

        except Exception as e:
            logger.error(f"Error getting property statistics: {e}")
            return {}
