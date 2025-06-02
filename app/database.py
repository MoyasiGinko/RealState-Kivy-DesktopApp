#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Database Module
Handles all database operations and data models
"""

import sqlite3
import os
import uuid
import random
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Main database manager for the Real Estate Management System"""

    def __init__(self, db_path: str = "userdesktop-rs-database.db"):
        """Initialize database connection and create tables if needed"""
        self.db_path = db_path
        self.init_database()
        logger.info(f"Database initialized: {db_path}")

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        return sqlite3.connect(self.db_path)

    def init_database(self):
        """Create all necessary tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Create Owners table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Owners (
                    Ownercode TEXT PRIMARY KEY,
                    ownername TEXT NOT NULL,
                    ownerphone TEXT,
                    Note TEXT,
                    created_date TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Handle schema migrations for existing tables
            self._handle_schema_migrations(cursor)

            # Create Maincode table for reference data
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Maincode (
                    code TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    recty TEXT,
                    parent_code TEXT,
                    created_date TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create Realstatspecification table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Realstatspecification (
                    Companyco TEXT PRIMARY KEY,
                    realstatecode TEXT,
                    Rstatetcode TEXT,
                    Yearmake TEXT,
                    Buildtcode TEXT,
                    "Property-area" NUMERIC,
                    "Unitm-code" TEXT,
                    "Property-facade" NUMERIC,
                    "Property-depth" NUMERIC,
                    "N-of-bedrooms" INTEGER,
                    "N-of bathrooms" INTEGER,
                    "Property-corner" TEXT,
                    "Offer-Type-Code" TEXT,
                    "Province-code" TEXT,
                    "Region-code" TEXT,
                    "Property-address" TEXT,
                    Photosituation TEXT,
                    Ownercode TEXT,
                    Descriptions TEXT,
                    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (Ownercode) REFERENCES Owners(Ownercode)
                )
            ''')

            # Create realstatephotos table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS realstatephotos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Companyco TEXT,
                    photo_path TEXT,
                    photo_name TEXT,
                    upload_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (Companyco) REFERENCES Realstatspecification(Companyco)
                )
            ''')            # Insert default reference data if not exists
            self._insert_default_data(cursor)

            conn.commit()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            conn.rollback()
        finally:
            conn.close()

    def _handle_schema_migrations(self, cursor):
        """Handle database schema migrations for existing tables"""
        try:
            # Check if created_date column exists in Owners table
            cursor.execute("PRAGMA table_info(Owners)")
            columns = [row[1] for row in cursor.fetchall()]

            if 'created_date' not in columns:
                logger.info("Adding created_date column to Owners table...")
                # SQLite doesn't support CURRENT_TIMESTAMP in ALTER TABLE with DEFAULT
                # So we add the column without default, then update existing rows
                cursor.execute('''
                    ALTER TABLE Owners
                    ADD COLUMN created_date TEXT
                ''')
                # Update existing rows with current timestamp
                cursor.execute('''
                    UPDATE Owners
                    SET created_date = datetime('now')
                    WHERE created_date IS NULL
                ''')
                logger.info("Successfully added created_date column to Owners table")

            # Check if created_date column exists in Realstatspecification table
            cursor.execute("PRAGMA table_info(Realstatspecification)")
            columns = [row[1] for row in cursor.fetchall()]

            if 'created_date' not in columns:
                logger.info("Adding created_date column to Realstatspecification table...")
                cursor.execute('''
                    ALTER TABLE Realstatspecification
                    ADD COLUMN created_date TEXT
                ''')
                # Update existing rows with current timestamp
                cursor.execute('''
                    UPDATE Realstatspecification
                    SET created_date = datetime('now')
                    WHERE created_date IS NULL
                ''')
                logger.info("Successfully added created_date column to Realstatspecification table")

        except Exception as e:
            logger.error(f"Error in schema migration: {e}")

    def _insert_default_data(self, cursor):
        """Insert default reference data using translation keys"""

        # Import here to avoid circular import issues
        try:
            from app.language_manager import LanguageManager
        except ImportError:
            # Fallback for direct script execution
            from language_manager import LanguageManager

        # Initialize language manager to get localized text
        language_manager = LanguageManager()

        # Provinces data - using translation keys
        province_keys = [
            ('01001', 'baghdad', '01'),
            ('01002', 'basra', '01'),
            ('01003', 'najaf', '01'),
            ('01004', 'karbala', '01'),
            ('01005', 'erbil', '01'),
            ('01006', 'mosul', '01'),
            ('01007', 'anbar', '01'),
            ('01008', 'wasit', '01'),
            ('01009', 'dhi_qar', '01'),
            ('01010', 'muthanna', '01'),
            ('01011', 'qadisiyyah', '01'),
            ('01012', 'babylon', '01'),
            ('01013', 'kirkuk', '01'),
            ('01014', 'salah_al_din', '01'),
            ('01015', 'diyala', '01'),
            ('01016', 'maysan', '01'),
            ('01017', 'dohuk', '01'),
            ('01018', 'sulaymaniyah', '01'),
        ]

        # Property types - using translation keys
        property_type_keys = [
            ('02001', 'house', '02'),
            ('02002', 'apartment', '02'),
            ('02003', 'villa', '02'),
            ('02004', 'land', '02'),
            ('02005', 'commercial_shop', '02'),
            ('02006', 'office', '02'),
            ('02007', 'warehouse', '02'),
            ('02008', 'residential_complex', '02'),
        ]

        # Offer types - using translation keys
        offer_type_keys = [
            ('03001', 'for_sale', '03'),
            ('03002', 'for_rent', '03'),
            ('03003', 'for_investment', '03'),
        ]

        # Insert all reference data with localized text
        for data_set in [province_keys, property_type_keys, offer_type_keys]:
            for code, translation_key, recty in data_set:
                # Get the localized text for the current language
                localized_name = language_manager.get_text(translation_key)
                cursor.execute('''
                    INSERT OR IGNORE INTO Maincode (code, name, recty)
                    VALUES (?, ?, ?)
                ''', (code, localized_name, recty))

    def update_reference_data_language(self, language_manager=None):
        """Update reference data with current language translations"""

        # Import here to avoid circular import issues
        if language_manager is None:
            try:
                from app.language_manager import LanguageManager
            except ImportError:
                # Fallback for direct script execution
                from language_manager import LanguageManager
            language_manager = LanguageManager()

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Province translations
            province_updates = [
                ('01001', 'baghdad'),
                ('01002', 'basra'),
                ('01003', 'najaf'),
                ('01004', 'karbala'),
                ('01005', 'erbil'),
                ('01006', 'mosul'),
                ('01007', 'anbar'),
                ('01008', 'wasit'),
                ('01009', 'dhi_qar'),
                ('01010', 'muthanna'),
                ('01011', 'qadisiyyah'),
                ('01012', 'babylon'),
                ('01013', 'kirkuk'),
                ('01014', 'salah_al_din'),
                ('01015', 'diyala'),
                ('01016', 'maysan'),
                ('01017', 'dohuk'),
                ('01018', 'sulaymaniyah'),
            ]

            # Property type translations
            property_type_updates = [
                ('02001', 'house'),
                ('02002', 'apartment'),
                ('02003', 'villa'),
                ('02004', 'land'),
                ('02005', 'commercial_shop'),
                ('02006', 'office'),
                ('02007', 'warehouse'),
                ('02008', 'residential_complex'),
            ]

            # Offer type translations
            offer_type_updates = [
                ('03001', 'for_sale'),
                ('03002', 'for_rent'),
                ('03003', 'for_investment'),
            ]

            # Update all reference data
            for updates in [province_updates, property_type_updates, offer_type_updates]:
                for code, translation_key in updates:
                    localized_name = language_manager.get_text(translation_key)
                    cursor.execute('''
                        UPDATE Maincode SET name = ? WHERE code = ?
                    ''', (localized_name, code))

            conn.commit()
            logger.info("Reference data language updated successfully")
        except Exception as e:
            logger.error(f"Error updating reference data language: {e}")
            conn.rollback()
        finally:
            conn.close()

    # Owner management methods
    def add_owner(self, owner_name: str, owner_phone: str = "", note: str = "") -> str:
        """Add new owner and return owner code"""
        owner_code = self.generate_owner_code()

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO Owners (Ownercode, ownername, ownerphone, Note)
                VALUES (?, ?, ?, ?)
            ''', (owner_code, owner_name, owner_phone, note))
            conn.commit()
            logger.info(f"Owner added: {owner_code}")
            return owner_code
        except Exception as e:
            logger.error(f"Error adding owner: {e}")
            conn.rollback()
            return ""
        finally:
            conn.close()

    def get_owners(self) -> List[Tuple]:
        """Get all owners"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT Ownercode, ownername, ownerphone, Note
                FROM Owners
                ORDER BY ownername
            ''')
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error getting owners: {e}")
            return []
        finally:
            conn.close()

    def update_owner(self, owner_code: str, owner_name: str,
                    owner_phone: str = "", note: str = "") -> bool:
        """Update owner information"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE Owners
                SET ownername = ?, ownerphone = ?, Note = ?
                WHERE Ownercode = ?
            ''', (owner_name, owner_phone, note, owner_code))
            conn.commit()
            logger.info(f"Owner updated: {owner_code}")
            return True
        except Exception as e:
            logger.error(f"Error updating owner: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def delete_owner(self, owner_code: str) -> bool:
        """Delete owner if no properties are linked"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Check if owner has properties
            cursor.execute('''
                SELECT COUNT(*) FROM Realstatspecification
                WHERE Ownercode = ?
            ''', (owner_code,))

            if cursor.fetchone()[0] > 0:
                logger.warning(f"Cannot delete owner {owner_code}: has linked properties")
                return False

            cursor.execute('DELETE FROM Owners WHERE Ownercode = ?', (owner_code,))
            conn.commit()
            logger.info(f"Owner deleted: {owner_code}")
            return True
        except Exception as e:
            logger.error(f"Error deleting owner: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    # Property management methods
    def add_property(self, property_data: Dict) -> str:
        """Add new property and return company code"""
        company_code = self.generate_company_code()

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO Realstatspecification (
                    Companyco, realstatecode, Rstatetcode, Yearmake, "Buildtcode ",
                    "Property-area", "Unitm-code", "Property-facade", "Property-depth",
                    "N-of-bedrooms", "N-of bathrooms", "Property-corner",
                    "Offer-Type-Code", "Province-code ", "Region-code",
                    "Property-address", Photosituation, Ownercode, Descriptions
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                company_code,
                property_data.get('realstatecode', ''),
                property_data.get('property_type', ''),
                property_data.get('year_make', ''),
                property_data.get('build_type', ''),
                property_data.get('area', 0),
                property_data.get('unit_code', 'م²'),
                property_data.get('facade', 0),
                property_data.get('depth', 0),
                property_data.get('bedrooms', 0),
                property_data.get('bathrooms', 0),
                property_data.get('corner', 'لا'),
                property_data.get('offer_type', ''),
                property_data.get('province_code', ''),
                property_data.get('region_code', ''),
                property_data.get('address', ''),
                property_data.get('photo_situation', 'لا توجد صور'),
                property_data.get('owner_code', ''),
                property_data.get('description', '')
            ))
            conn.commit()
            logger.info(f"Property added: {company_code}")
            return company_code
        except Exception as e:
            logger.error(f"Error adding property: {e}")
            conn.rollback()
            return ""
        finally:
            conn.close()

    def get_properties(self, filters: Dict = None) -> List[Dict]:
        """Get properties with optional filters"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            query = '''
                SELECT r.*, o.ownername
                FROM Realstatspecification r
                LEFT JOIN Owners o ON r.Ownercode = o.Ownercode
            '''

            params = []
            if filters:
                conditions = []
                if filters.get('owner_code'):
                    conditions.append('r.Ownercode = ?')
                    params.append(filters['owner_code'])
                if filters.get('property_type'):
                    conditions.append('r.Rstatetcode = ?')
                    params.append(filters['property_type'])
                if filters.get('province_code'):
                    conditions.append('r."Province-code " = ?')
                    params.append(filters['province_code'])
                if filters.get('offer_type'):
                    conditions.append('r."Offer-Type-Code" = ?')
                    params.append(filters['offer_type'])

                if conditions:
                    query += ' WHERE ' + ' AND '.join(conditions)

            query += ' ORDER BY r.Companyco DESC'

            cursor.execute(query, params)
            columns = [description[0] for description in cursor.description]

            properties = []
            for row in cursor.fetchall():
                properties.append(dict(zip(columns, row)))

            return properties
        except Exception as e:
            logger.error(f"Error getting properties: {e}")
            return []
        finally:
            conn.close()

    def get_property_by_code(self, company_code: str) -> Optional[Dict]:
        """Get property by company code"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT r.*, o.ownername
                FROM Realstatspecification r
                LEFT JOIN Owners o ON r.Ownercode = o.Ownercode
                WHERE r.Companyco = ?
            ''', (company_code,))

            row = cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
        except Exception as e:
            logger.error(f"Error getting property: {e}")
            return None
        finally:
            conn.close()

    def update_property(self, company_code: str, property_data: Dict) -> bool:
        """Update property information"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Build dynamic UPDATE query based on provided data
            set_clauses = []
            values = []

            field_mapping = {
                'realstatecode': 'realstatecode',
                'property_type': 'Rstatetcode',
                'year_make': 'Yearmake',
                'build_type': '"Buildtcode "',
                'area': '"Property-area"',
                'unit_code': '"Unitm-code"',
                'facade': '"Property-facade"',
                'depth': '"Property-depth"',
                'bedrooms': '"N-of-bedrooms"',
                'bathrooms': '"N-of bathrooms"',
                'corner': '"Property-corner"',
                'offer_type': '"Offer-Type-Code"',
                'province_code': '"Province-code "',
                'region_code': '"Region-code"',
                'address': '"Property-address"',
                'owner_code': 'Ownercode',                'description': 'Descriptions'
            }

            for key, db_field in field_mapping.items():
                if key in property_data:
                    set_clauses.append(f"{db_field} = ?")
                    values.append(property_data[key])

            if not set_clauses:
                logger.warning("No data provided for property update")
                return False

            values.append(company_code)  # For WHERE clause

            query = f'''
                UPDATE Realstatspecification
                SET {", ".join(set_clauses)}
                WHERE Companyco = ?
            '''

            cursor.execute(query, values)
            conn.commit()

            if cursor.rowcount > 0:
                logger.info(f"Property updated: {company_code}")
                return True
            else:
                logger.warning(f"Property not found for update: {company_code}")
                return False

        except Exception as e:
            logger.error(f"Error updating property: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def delete_property(self, company_code: str) -> bool:
        """Delete property and associated photos"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # First get the realstatecode for this property to delete photos
            cursor.execute('SELECT realstatecode FROM Realstatspecification WHERE Companyco = ?', (company_code,))
            result = cursor.fetchone()

            if result:
                realstatecode = result[0]
                # Delete associated photos using realstatecode
                cursor.execute('DELETE FROM realstatephotos WHERE realstatecode = ?', (realstatecode,))

            # Then delete the property
            cursor.execute('DELETE FROM Realstatspecification WHERE Companyco = ?', (company_code,))
            conn.commit()

            if cursor.rowcount > 0:
                logger.info(f"Property deleted: {company_code}")
                return True
            else:
                logger.warning(f"Property not found for deletion: {company_code}")
                return False

        except Exception as e:
            logger.error(f"Error deleting property: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    # Photo management methods
    def add_property_photo(self, company_code: str, photo_path: str, photo_name: str) -> bool:
        """Add property photo

        Args:
            company_code: The company code of the property
            photo_path: The full path to the photo file
            photo_name: The filename of the photo
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Get the real estate code from the property
            property_data = self.get_property_by_code(company_code)
            if not property_data:
                logger.error(f"Property not found for photo upload: {company_code}")
                return False

            realstate_code = property_data.get('realstatecode')

            # Split the photo path and name into components expected by the database
            # Extract the directory path and filename components
            storage_path = os.path.dirname(photo_path)
            file_basename = os.path.basename(photo_name)

            # Split into filename and extension
            filename, extension = os.path.splitext(file_basename)

            # Execute the insert based on the actual schema
            cursor.execute('''
                INSERT INTO realstatephotos (realstatecode, Storagepath, photofilename, Photoextension)
                VALUES (?, ?, ?, ?)
            ''', (realstate_code, storage_path, filename, extension))

            conn.commit()
            logger.info(f"Photo added for property: {company_code}, realstate code: {realstate_code}")
            return True
        except Exception as e:
            logger.error(f"Error adding property photo: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def get_property_photos(self, company_code: str) -> List[Dict]:
        """Get property photos"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # First check if the Companyco column exists in the realstatephotos table
            cursor.execute("PRAGMA table_info(realstatephotos)")
            columns_info = cursor.fetchall()
            column_names = [col[1] for col in columns_info]

            # Get the real estate code from the property using company_code
            property_data = self.get_property_by_code(company_code)
            realstate_code = property_data.get('realstatecode') if property_data else None

            if 'Companyco' in column_names:
                # If the Companyco column exists, query by it
                cursor.execute('''
                    SELECT realstatecode, Storagepath, photofilename, Photoextension
                    FROM realstatephotos
                    WHERE Companyco = ?
                ''', (company_code,))
            elif realstate_code and 'realstatecode' in column_names:
                # Otherwise, try to match on realstatecode
                cursor.execute('''
                    SELECT realstatecode, Storagepath, photofilename, Photoextension
                    FROM realstatephotos
                    WHERE realstatecode = ?
                ''', (realstate_code,))
            else:
                logger.error(f"Cannot find photos: no suitable column to match on")
                return []

            columns = [description[0] for description in cursor.description]
            photos = []
            for row in cursor.fetchall():
                photo_dict = dict(zip(columns, row))

                # Add derived fields that the UI expects
                if 'Storagepath' in photo_dict and 'photofilename' in photo_dict:
                    # Build photo path from components
                    storage_path = photo_dict.get('Storagepath', '')
                    filename = photo_dict.get('photofilename', '')
                    extension = photo_dict.get('Photoextension', '')

                    # Ensure extension has a dot prefix if it doesn't already
                    if extension and not extension.startswith('.'):
                        extension = '.' + extension

                    # Build full path
                    photo_path = os.path.join(storage_path, filename)
                    if extension:
                        photo_path += extension

                    # Add the derived fields that the UI expects
                    photo_dict['photo_path'] = photo_path
                    photo_dict['photo_name'] = filename + (extension if extension else '')

                photos.append(photo_dict)

            logger.info(f"Found {len(photos)} photos for property {company_code}")
            return photos
        except Exception as e:
            logger.error(f"Error getting property photos: {e}")
            return []
        finally:
            conn.close()

    def delete_property_photo(self, photo_name: str) -> bool:
        """Delete property photo by photo name"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # First check what columns exist in the table
            cursor.execute("PRAGMA table_info(realstatephotos)")
            columns_info = cursor.fetchall()
            column_names = [col[1] for col in columns_info]

            # Use id or photo_name based on what's available
            if 'photo_name' in column_names:
                cursor.execute('DELETE FROM realstatephotos WHERE photo_name = ?', (photo_name,))
            elif 'id' in column_names and photo_name.isdigit():
                # In case photo_name is actually an ID
                cursor.execute('DELETE FROM realstatephotos WHERE id = ?', (int(photo_name),))
            else:
                # Fallback - try to delete with any identifying information we have
                logger.warning("No suitable column found for photo deletion. Using generic method.")
                found = False
                for column in column_names:
                    if column != 'Companyco' and column != 'upload_date':
                        cursor.execute(f'DELETE FROM realstatephotos WHERE {column} = ?', (photo_name,))
                        if cursor.rowcount > 0:
                            found = True
                            break
                if not found:
                    logger.warning(f"No suitable column found to delete photo: {photo_name}")
                    return False

            conn.commit()

            if cursor.rowcount > 0:
                logger.info(f"Photo deleted: {photo_name}")
                return True
            else:
                logger.warning(f"Photo not found for deletion: {photo_name}")
                return False
        except Exception as e:
            logger.error(f"Error deleting property photo: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def close_connection(self):
        """Close database connection - placeholder for any cleanup"""
        pass  # SQLite connections are closed automatically per operation

    # Statistics methods
    def get_statistics(self) -> Dict:
        """Get system statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            stats = {}

            # Total owners
            cursor.execute('SELECT COUNT(*) FROM Owners')
            stats['total_owners'] = cursor.fetchone()[0]

            # Total properties
            cursor.execute('SELECT COUNT(*) FROM Realstatspecification')
            stats['total_properties'] = cursor.fetchone()[0]

            # Properties by type
            cursor.execute('''
                SELECT r.Rstatetcode, m.name, COUNT(*) as count
                FROM Realstatspecification r
                LEFT JOIN Maincode m ON r.Rstatetcode = m.code
                GROUP BY r.Rstatetcode
                ORDER BY count DESC
            ''')
            stats['properties_by_type'] = cursor.fetchall()

            # Properties by offer type
            cursor.execute('''
                SELECT r."Offer-Type-Code", m.name, COUNT(*) as count
                FROM Realstatspecification r
                LEFT JOIN Maincode m ON r."Offer-Type-Code" = m.code
                GROUP BY r."Offer-Type-Code"
                ORDER BY count DESC
            ''')
            stats['properties_by_offer'] = cursor.fetchall()

            # Properties by province
            cursor.execute('''
                SELECT r."Province-code ", m.name, COUNT(*) as count
                FROM Realstatspecification r
                LEFT JOIN Maincode m ON r."Province-code " = m.code
                GROUP BY r."Province-code "
                ORDER BY count DESC
            ''')
            stats['properties_by_province'] = cursor.fetchall()

            return stats
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}
        finally:
            conn.close()

    # Code generation methods
    def generate_owner_code(self) -> str:
        """Generate unique owner code with max 4 characters"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Generate a 4-character alphanumeric code
            while True:
                # Generate random 4 character code (letters and numbers)
                code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=4))

                # Check if the code already exists
                cursor.execute('SELECT COUNT(*) FROM Owners WHERE Ownercode = ?', (code,))
                if cursor.fetchone()[0] == 0:
                    # Code is unique, so return it
                    return code
        except Exception as e:
            logger.error(f"Error generating unique owner code: {e}")
            # Fallback to a simpler code generation if there's an error
            return f"O{str(uuid.uuid4())[:3].upper()}"
        finally:
            conn.close()

    def generate_company_code(self) -> str:
        """Generate unique company code - used for database identification

        This is distinct from the company prefix used in the real estate code.
        This is a longer, unique identifier for the database record.
        """
        return f"COM{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"

    def generate_realstate_code(self) -> str:
        """Generate unique real estate code

        Format: CCCCNNNN where:
        - CCCC is the 4-character company code (1 alphabet + 3 digits)
        - NNNN is a 4-character unique random number

        Both the full code and the company prefix must be unique.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Keep generating until we find a unique combination
            while True:
                # First part: 4-character company code (1 alphabet + 3 digits)
                # 1 alphabet character
                alphabet_char = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                # 3 random digits
                numeric_part = ''.join(random.choices('0123456789', k=3))
                company_prefix = f"{alphabet_char}{numeric_part}"

                # Check if this company prefix already exists
                cursor.execute('''
                    SELECT COUNT(*) FROM Realstatspecification
                    WHERE realstatecode LIKE ?
                ''', (f"{company_prefix}%",))

                # If company prefix exists, try a different one
                if cursor.fetchone()[0] > 0:
                    continue

                # Second part: 4-character unique random number
                # Using numbers only for the second part
                random_part = ''.join(random.choices('0123456789', k=4))

                # Form the complete real estate code
                real_estate_code = f"{company_prefix}{random_part}"

                # Verify this code doesn't already exist
                cursor.execute('''
                    SELECT COUNT(*) FROM Realstatspecification
                    WHERE realstatecode = ?
                ''', (real_estate_code,))

                # If code doesn't exist, we've found a unique one
                if cursor.fetchone()[0] == 0:
                    return real_estate_code
        except Exception as e:
            logger.error(f"Error generating real estate code: {e}")
            # Fallback to a simple format if there's an error
            return f"{company_prefix}{random_part}"
        finally:
            conn.close()

    # Reference data methods
    def get_property_types(self) -> List[tuple]:
        """Get all property types"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT code, name, recty FROM Maincode WHERE recty = '02' ORDER BY name")
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error getting property types: {e}")
            return []
        finally:
            conn.close()

    def get_provinces(self) -> List[tuple]:
        """Get all provinces"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT code, name, recty FROM Maincode WHERE recty = '01' ORDER BY name")
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error getting provinces: {e}")
            return []
        finally:
            conn.close()

    def get_offer_types(self) -> List[tuple]:
        """Get all offer types"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT code, name, recty FROM Maincode WHERE recty = '03' ORDER BY name")
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error getting offer types: {e}")
            return []
        finally:
            conn.close()

    def get_reference_data(self, category: str) -> List[tuple]:
        """Get reference data by category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT code, name, recty FROM Maincode WHERE recty = ? ORDER BY name", (category,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error getting reference data for category {category}: {e}")
            return []
        finally:
            conn.close()

    # Dashboard Statistics Methods
    def get_total_owners(self) -> int:
        """Get total number of owners"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM Owners")
            result = cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            logger.error(f"Error getting total owners: {e}")
            return 0
        finally:
            conn.close()

    def get_total_properties(self) -> int:
        """Get total number of properties"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM Realstatspecification")
            result = cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            logger.error(f"Error getting total properties: {e}")
            return 0
        finally:
            conn.close()

    def get_total_transactions(self) -> int:
        """Get total number of transactions (placeholder - no transactions table exists)"""
        # Since there's no transactions table in the current schema,
        # we'll return the count of properties as a placeholder
        return self.get_total_properties()

    def get_available_properties_count(self) -> int:
        """Get count of available properties"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Since there's no status column, return total properties as all are considered available
            cursor.execute("SELECT COUNT(*) FROM Realstatspecification")
            result = cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            logger.error(f"Error getting available properties count: {e}")
            return 0
        finally:
            conn.close()

    def get_recent_owners(self, limit: int = 5) -> List[Tuple]:
        """Get recent owners"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT Ownercode, ownername, ownerphone, Note
                FROM Owners
                ORDER BY Ownercode DESC
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error getting recent owners: {e}")
            return []
        finally:
            conn.close()

    def get_recent_properties(self, limit: int = 5) -> List[Dict]:
        """Get recent properties"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT r.*, o.ownername
                FROM Realstatspecification r
                LEFT JOIN Owners o ON r.Ownercode = o.Ownercode
                ORDER BY r.Companyco DESC
                LIMIT ?
            ''', (limit,))

            columns = [description[0] for description in cursor.description]
            properties = []
            for row in cursor.fetchall():
                properties.append(dict(zip(columns, row)))
            return properties
        except sqlite3.Error as e:
            logger.error(f"Error getting recent properties: {e}")
            return []
        finally:
            conn.close()
    def get_statistics(self) -> dict:
        """Get comprehensive dashboard statistics"""
        stats = {
            'total_owners': self.get_total_owners(),
            'total_properties': self.get_total_properties(),
            'total_transactions': self.get_total_transactions(),
            'available_properties': self.get_available_properties_count()
        }
        return stats

    def _handle_schema_migrations(self, cursor):
        """Handle schema migrations for existing tables"""

        # Check and add missing columns to Owners table
        cursor.execute("PRAGMA table_info(Owners)")
        columns = [column[1] for column in cursor.fetchall()]

        # Add created_date column if it doesn't exist
        if 'created_date' not in columns:
            cursor.execute('''
                ALTER TABLE Owners
                ADD COLUMN created_date TEXT DEFAULT CURRENT_TIMESTAMP
            ''')
            logger.info("Added created_date column to Owners table")

        # Check and add missing columns to Realstatspecification table
        cursor.execute("PRAGMA table_info(Realstatspecification)")
        columns = [column[1] for column in cursor.fetchall()]

        # Add description column if it doesn't exist
        if 'Descriptions' not in columns:
            cursor.execute('''
                ALTER TABLE Realstatspecification
                ADD COLUMN Descriptions TEXT
            ''')
            logger.info("Added Descriptions column to Realstatspecification table")

        # Add missing foreign key constraint on Ownercode column
        # Execute statements individually to avoid "You can only execute one statement at a time" error
        cursor.execute('PRAGMA foreign_keys = OFF')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Realstatspecification_temp (
                Companyco TEXT PRIMARY KEY,
                realstatecode TEXT,
                Rstatetcode TEXT,
                Yearmake TEXT,
                "Buildtcode " TEXT,
                "Property-area" NUMERIC,
                "Unitm-code" TEXT,
                "Property-facade" NUMERIC,
                "Property-depth" NUMERIC,
                "N-of-bedrooms" INTEGER,
                "N-of bathrooms" INTEGER,
                "Property-corner" TEXT,
                "Offer-Type-Code" TEXT,
                "Province-code " TEXT,
                "Region-code" TEXT,
                "Property-address" TEXT,
                Photosituation TEXT,
                Ownercode TEXT,
                Descriptions TEXT,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (Ownercode) REFERENCES Owners(Ownercode)
            )
        ''')
        cursor.execute('''
            INSERT INTO Realstatspecification_temp (
                Companyco, realstatecode, Rstatetcode, Yearmake, "Buildtcode ",
                "Property-area", "Unitm-code", "Property-facade", "Property-depth",
                "N-of-bedrooms", "N-of bathrooms", "Property-corner",
                "Offer-Type-Code", "Province-code ", "Region-code",
                "Property-address", Photosituation, Ownercode, Descriptions
            )
            SELECT
                Companyco, realstatecode, Rstatetcode, Yearmake, "Buildtcode ",
                "Property-area", "Unitm-code", "Property-facade", "Property-depth",
                "N-of-bedrooms", "N-of bathrooms", "Property-corner",
                "Offer-Type-Code", "Province-code ", "Region-code",
                "Property-address", Photosituation, Ownercode, Descriptions
            FROM Realstatspecification
        ''')
        cursor.execute('DROP TABLE Realstatspecification')
        cursor.execute('ALTER TABLE Realstatspecification_temp RENAME TO Realstatspecification')
        cursor.execute('PRAGMA foreign_keys = ON')
        logger.info("Updated Realstatspecification table schema")
