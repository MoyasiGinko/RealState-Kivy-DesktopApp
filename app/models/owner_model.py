#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Owner Model
Handles all owner-related database operations and business logic
"""

from typing import Dict, List, Optional
import uuid
import logging
from datetime import datetime

from .base_model import BaseModel

logger = logging.getLogger(__name__)


class OwnerModel(BaseModel):
    """Model for managing property owners"""

    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.table_name = 'Owners'

    def get_all(self) -> List[Dict]:
        """Get all owners"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT Ownercode, ownername, ownerphone, Note, created_date
                FROM Owners
                ORDER BY ownername
            """)

            columns = [description[0] for description in cursor.description]
            results = []

            for row in cursor.fetchall():
                owner_dict = dict(zip(columns, row))
                results.append(owner_dict)

            conn.close()
            return results

        except Exception as e:
            logger.error(f"Error getting all owners: {e}")
            return []

    def get_by_id(self, owner_code: str) -> Optional[Dict]:
        """Get owner by owner code"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT Ownercode, ownername, ownerphone, Note, created_date
                FROM Owners
                WHERE Ownercode = ?
            """, (owner_code,))

            row = cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                result = dict(zip(columns, row))
                conn.close()
                return result

            conn.close()
            return None

        except Exception as e:
            logger.error(f"Error getting owner {owner_code}: {e}")
            return None

    def create(self, data: Dict) -> bool:
        """Create new owner"""
        try:
            # Validate data
            is_valid, error_msg = self.validate_data(data)
            if not is_valid:
                logger.error(f"Invalid owner data: {error_msg}")
                return False

            # Generate owner code if not provided
            owner_code = data.get('Ownercode') or self._generate_owner_code()

            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Owners (Ownercode, ownername, ownerphone, Note, created_date)
                VALUES (?, ?, ?, ?, ?)
            """, (
                owner_code,
                data.get('ownername', ''),
                data.get('ownerphone', ''),
                data.get('Note', ''),
                datetime.now().isoformat()
            ))

            conn.commit()
            conn.close()

            # Notify observers
            self.notify_observers('owner_created', {'Ownercode': owner_code})
            logger.info(f"Owner created successfully: {owner_code}")
            return True

        except Exception as e:
            logger.error(f"Error creating owner: {e}")
            return False

    def update(self, owner_code: str, data: Dict) -> bool:
        """Update existing owner"""
        try:
            # Validate data
            is_valid, error_msg = self.validate_data(data)
            if not is_valid:
                logger.error(f"Invalid owner data: {error_msg}")
                return False

            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE Owners
                SET ownername = ?, ownerphone = ?, Note = ?
                WHERE Ownercode = ?
            """, (
                data.get('ownername', ''),
                data.get('ownerphone', ''),
                data.get('Note', ''),
                owner_code
            ))

            conn.commit()
            conn.close()

            # Notify observers
            self.notify_observers('owner_updated', {'Ownercode': owner_code})
            logger.info(f"Owner updated successfully: {owner_code}")
            return True

        except Exception as e:
            logger.error(f"Error updating owner {owner_code}: {e}")
            return False

    def delete(self, owner_code: str) -> bool:
        """Delete owner"""
        try:
            # Check if owner has properties
            if self._has_properties(owner_code):
                logger.warning(f"Cannot delete owner {owner_code}: has associated properties")
                return False

            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM Owners WHERE Ownercode = ?", (owner_code,))

            if cursor.rowcount > 0:
                conn.commit()
                conn.close()

                # Notify observers
                self.notify_observers('owner_deleted', {'Ownercode': owner_code})
                logger.info(f"Owner deleted successfully: {owner_code}")
                return True
            else:
                conn.close()
                logger.warning(f"Owner not found for deletion: {owner_code}")
                return False

        except Exception as e:
            logger.error(f"Error deleting owner {owner_code}: {e}")
            return False

    def search(self, query: str) -> List[Dict]:
        """Search owners by name or phone"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            search_pattern = f"%{query}%"
            cursor.execute("""
                SELECT Ownercode, ownername, ownerphone, Note, created_date
                FROM Owners
                WHERE ownername LIKE ? OR ownerphone LIKE ?
                ORDER BY ownername
            """, (search_pattern, search_pattern))

            columns = [description[0] for description in cursor.description]
            results = []

            for row in cursor.fetchall():
                owner_dict = dict(zip(columns, row))
                results.append(owner_dict)

            conn.close()
            return results

        except Exception as e:
            logger.error(f"Error searching owners: {e}")
            return []

    def get_owner_properties_count(self, owner_code: str) -> int:
        """Get count of properties for an owner"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM Maincode WHERE Ownercode = ?", (owner_code,))
            count = cursor.fetchone()[0]

            conn.close()
            return count

        except Exception as e:
            logger.error(f"Error getting properties count for owner {owner_code}: {e}")
            return 0

    def validate_data(self, data: Dict) -> tuple[bool, str]:
        """Validate owner data"""
        if not data.get('ownername', '').strip():
            return False, "Owner name is required"

        # Check for duplicate owner name (case-insensitive)
        existing_owners = self.get_all()
        owner_name = data.get('ownername', '').strip().lower()

        for owner in existing_owners:
            if owner['ownername'].lower() == owner_name:
                # If updating, allow same name for same owner
                if data.get('Ownercode') != owner['Ownercode']:
                    return False, "Owner name already exists"

        return True, ""

    def _generate_owner_code(self) -> str:
        """Generate unique owner code"""
        return f"OWN-{uuid.uuid4().hex[:8].upper()}"

    def _has_properties(self, owner_code: str) -> bool:
        """Check if owner has associated properties"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM Maincode WHERE Ownercode = ?", (owner_code,))
            count = cursor.fetchone()[0]

            conn.close()
            return count > 0

        except Exception as e:
            logger.error(f"Error checking properties for owner {owner_code}: {e}")
            return True  # Err on the side of caution
