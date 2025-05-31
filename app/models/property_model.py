#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Property Model
Handles all property-related database operations and business logic
"""

from typing import Dict, List, Optional
import uuid
import os
import logging
from datetime import datetime

from .base_model import BaseModel

logger = logging.getLogger(__name__)


class PropertyModel(BaseModel):
    """Model for managing properties"""

    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.table_name = 'Maincode'

    def get_all(self) -> List[Dict]:
        """Get all properties with owner information"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT m.Maincode, m.Ownercode, o.ownername, m.location, m.area,
                       m.propertytype, m.price, m.status, m.photos, m.Note,
                       m.created_date, m.updated_date
                FROM Maincode m
                LEFT JOIN Owners o ON m.Ownercode = o.Ownercode
                ORDER BY m.created_date DESC
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

    def get_by_id(self, maincode: str) -> Optional[Dict]:
        """Get property by maincode"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT m.Maincode, m.Ownercode, o.ownername, m.location, m.area,
                       m.propertytype, m.price, m.status, m.photos, m.Note,
                       m.created_date, m.updated_date
                FROM Maincode m
                LEFT JOIN Owners o ON m.Ownercode = o.Ownercode
                WHERE m.Maincode = ?
            """, (maincode,))

            row = cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                result = dict(zip(columns, row))
                conn.close()
                return result

            conn.close()
            return None

        except Exception as e:
            logger.error(f"Error getting property {maincode}: {e}")
            return None

    def create(self, data: Dict) -> bool:
        """Create new property"""
        try:
            # Validate data
            is_valid, error_msg = self.validate_data(data)
            if not is_valid:
                logger.error(f"Invalid property data: {error_msg}")
                return False

            # Generate maincode if not provided
            maincode = data.get('Maincode') or self._generate_maincode()

            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Maincode (Maincode, Ownercode, location, area, propertytype,
                                     price, status, photos, Note, created_date, updated_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                maincode,
                data.get('Ownercode', ''),
                data.get('location', ''),
                data.get('area', ''),
                data.get('propertytype', ''),
                data.get('price', 0),
                data.get('status', 'Available'),
                data.get('photos', ''),
                data.get('Note', ''),
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))

            conn.commit()
            conn.close()

            # Notify observers
            self.notify_observers('property_created', {'Maincode': maincode})
            logger.info(f"Property created successfully: {maincode}")
            return True

        except Exception as e:
            logger.error(f"Error creating property: {e}")
            return False

    def update(self, maincode: str, data: Dict) -> bool:
        """Update existing property"""
        try:
            # Validate data
            is_valid, error_msg = self.validate_data(data)
            if not is_valid:
                logger.error(f"Invalid property data: {error_msg}")
                return False

            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE Maincode
                SET Ownercode = ?, location = ?, area = ?, propertytype = ?,
                    price = ?, status = ?, photos = ?, Note = ?, updated_date = ?
                WHERE Maincode = ?
            """, (
                data.get('Ownercode', ''),
                data.get('location', ''),
                data.get('area', ''),
                data.get('propertytype', ''),
                data.get('price', 0),
                data.get('status', 'Available'),
                data.get('photos', ''),
                data.get('Note', ''),
                datetime.now().isoformat(),
                maincode
            ))

            conn.commit()
            conn.close()

            # Notify observers
            self.notify_observers('property_updated', {'Maincode': maincode})
            logger.info(f"Property updated successfully: {maincode}")
            return True

        except Exception as e:
            logger.error(f"Error updating property {maincode}: {e}")
            return False

    def delete(self, maincode: str) -> bool:
        """Delete property"""
        try:
            # Get property data before deletion for cleanup
            property_data = self.get_by_id(maincode)

            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM Maincode WHERE Maincode = ?", (maincode,))

            if cursor.rowcount > 0:
                conn.commit()
                conn.close()

                # Clean up photos if they exist
                if property_data and property_data.get('photos'):
                    self._cleanup_photos(property_data['photos'])

                # Notify observers
                self.notify_observers('property_deleted', {'Maincode': maincode})
                logger.info(f"Property deleted successfully: {maincode}")
                return True
            else:
                conn.close()
                logger.warning(f"Property not found for deletion: {maincode}")
                return False

        except Exception as e:
            logger.error(f"Error deleting property {maincode}: {e}")
            return False

    def search(self, filters: Dict) -> List[Dict]:
        """Search properties with various filters"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            # Build dynamic query based on filters
            where_conditions = []
            params = []

            if filters.get('location'):
                where_conditions.append("m.location LIKE ?")
                params.append(f"%{filters['location']}%")

            if filters.get('propertytype'):
                where_conditions.append("m.propertytype = ?")
                params.append(filters['propertytype'])

            if filters.get('status'):
                where_conditions.append("m.status = ?")
                params.append(filters['status'])

            if filters.get('min_price'):
                where_conditions.append("m.price >= ?")
                params.append(filters['min_price'])

            if filters.get('max_price'):
                where_conditions.append("m.price <= ?")
                params.append(filters['max_price'])

            if filters.get('owner_name'):
                where_conditions.append("o.ownername LIKE ?")
                params.append(f"%{filters['owner_name']}%")

            where_clause = ""
            if where_conditions:
                where_clause = "WHERE " + " AND ".join(where_conditions)

            query = f"""
                SELECT m.Maincode, m.Ownercode, o.ownername, m.location, m.area,
                       m.propertytype, m.price, m.status, m.photos, m.Note,
                       m.created_date, m.updated_date
                FROM Maincode m
                LEFT JOIN Owners o ON m.Ownercode = o.Ownercode
                {where_clause}
                ORDER BY m.created_date DESC
            """

            cursor.execute(query, params)

            columns = [description[0] for description in cursor.description]
            results = []

            for row in cursor.fetchall():
                property_dict = dict(zip(columns, row))
                results.append(property_dict)

            conn.close()
            return results

        except Exception as e:
            logger.error(f"Error searching properties: {e}")
            return []

    def get_by_owner(self, owner_code: str) -> List[Dict]:
        """Get all properties for a specific owner"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT m.Maincode, m.Ownercode, o.ownername, m.location, m.area,
                       m.propertytype, m.price, m.status, m.photos, m.Note,
                       m.created_date, m.updated_date
                FROM Maincode m
                LEFT JOIN Owners o ON m.Ownercode = o.Ownercode
                WHERE m.Ownercode = ?
                ORDER BY m.created_date DESC
            """, (owner_code,))

            columns = [description[0] for description in cursor.description]
            results = []

            for row in cursor.fetchall():
                property_dict = dict(zip(columns, row))
                results.append(property_dict)

            conn.close()
            return results

        except Exception as e:
            logger.error(f"Error getting properties for owner {owner_code}: {e}")
            return []

    def get_statistics(self) -> Dict:
        """Get property statistics"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            stats = {}

            # Total properties
            cursor.execute("SELECT COUNT(*) FROM Maincode")
            stats['total_properties'] = cursor.fetchone()[0]

            # Properties by status
            cursor.execute("""
                SELECT status, COUNT(*)
                FROM Maincode
                GROUP BY status
            """)
            stats['by_status'] = dict(cursor.fetchall())

            # Properties by type
            cursor.execute("""
                SELECT propertytype, COUNT(*)
                FROM Maincode
                GROUP BY propertytype
            """)
            stats['by_type'] = dict(cursor.fetchall())

            # Average price
            cursor.execute("SELECT AVG(price) FROM Maincode WHERE price > 0")
            avg_price = cursor.fetchone()[0]
            stats['average_price'] = avg_price if avg_price else 0

            # Total value
            cursor.execute("SELECT SUM(price) FROM Maincode")
            total_value = cursor.fetchone()[0]
            stats['total_value'] = total_value if total_value else 0

            conn.close()
            return stats

        except Exception as e:
            logger.error(f"Error getting property statistics: {e}")
            return {}

    def validate_data(self, data: Dict) -> tuple[bool, str]:
        """Validate property data"""
        if not data.get('location', '').strip():
            return False, "Location is required"

        if not data.get('Ownercode', '').strip():
            return False, "Owner is required"

        # Validate price is a valid number
        try:
            price = float(data.get('price', 0))
            if price < 0:
                return False, "Price cannot be negative"
        except (ValueError, TypeError):
            return False, "Invalid price format"

        # Validate area is a valid number
        try:
            area = float(data.get('area', 0))
            if area <= 0:
                return False, "Area must be positive"
        except (ValueError, TypeError):
            return False, "Invalid area format"

        return True, ""

    def _generate_maincode(self) -> str:
        """Generate unique property code"""
        return f"PROP-{uuid.uuid4().hex[:8].upper()}"

    def _cleanup_photos(self, photos_string: str):
        """Clean up photo files when property is deleted"""
        try:
            if not photos_string:
                return

            photo_paths = photos_string.split(';')
            for photo_path in photo_paths:
                if photo_path and os.path.exists(photo_path):
                    os.remove(photo_path)
                    logger.info(f"Deleted photo file: {photo_path}")

                # Also delete thumbnail if exists
                if photo_path:
                    thumbnail_path = photo_path.replace('property_photos', 'property_photos/thumbnails')
                    if os.path.exists(thumbnail_path):
                        os.remove(thumbnail_path)
                        logger.info(f"Deleted thumbnail: {thumbnail_path}")

        except Exception as e:
            logger.error(f"Error cleaning up photos: {e}")
