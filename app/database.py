#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Database Module
Handles all database operations and data models
"""

import sqlite3
import os
import uuid
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
            ''')

            # Insert default reference data if not exists
            self._insert_default_data(cursor)

            conn.commit()
            logger.info("Database tables created successfully")

        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            conn.rollback()
        finally:
            conn.close()

    def _insert_default_data(self, cursor):
        """Insert default reference data"""

        # Provinces data
        provinces = [
            ('01001', 'بغداد', '01'),
            ('01002', 'البصرة', '01'),
            ('01003', 'النجف', '01'),
            ('01004', 'كربلاء', '01'),
            ('01005', 'أربيل', '01'),
            ('01006', 'الموصل', '01'),
            ('01007', 'الأنبار', '01'),
            ('01008', 'واسط', '01'),
            ('01009', 'ذي قار', '01'),
            ('01010', 'المثنى', '01'),
            ('01011', 'القادسية', '01'),
            ('01012', 'بابل', '01'),
            ('01013', 'كركوك', '01'),
            ('01014', 'صلاح الدين', '01'),
            ('01015', 'ديالى', '01'),
            ('01016', 'ميسان', '01'),
            ('01017', 'دهوك', '01'),
            ('01018', 'السليمانية', '01'),
        ]

        # Property types
        property_types = [
            ('02001', 'منزل', '02'),
            ('02002', 'شقة', '02'),
            ('02003', 'فيلا', '02'),
            ('02004', 'أرض', '02'),
            ('02005', 'محل تجاري', '02'),
            ('02006', 'مكتب', '02'),
            ('02007', 'مستودع', '02'),
            ('02008', 'مجمع سكني', '02'),
        ]

        # Offer types
        offer_types = [
            ('03001', 'للبيع', '03'),
            ('03002', 'للإيجار', '03'),
            ('03003', 'للاستثمار', '03'),
        ]

        # Insert all reference data
        for data_set in [provinces, property_types, offer_types]:
            for item in data_set:
                cursor.execute('''
                    INSERT OR IGNORE INTO Maincode (code, name, recty)
                    VALUES (?, ?, ?)
                ''', item)

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
                    Companyco, realstatecode, Rstatetcode, Yearmake, Buildtcode,
                    "Property-area", "Unitm-code", "Property-facade", "Property-depth",
                    "N-of-bedrooms", "N-of bathrooms", "Property-corner",
                    "Offer-Type-Code", "Province-code", "Region-code",
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
                'owner_code': 'Ownercode',
                'description': 'Descriptions'
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
            # First delete associated photos
            cursor.execute('DELETE FROM realstatephotos WHERE Companyco = ?', (company_code,))

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
        """Generate unique owner code"""
        return f"OWN{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"

    def generate_company_code(self) -> str:
        """Generate unique company code"""
        return f"COM{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"

    def generate_realstate_code(self) -> str:
        """Generate unique real estate code"""
        return f"RS{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"

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
