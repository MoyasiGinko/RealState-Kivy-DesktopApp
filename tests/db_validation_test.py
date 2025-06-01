#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Validation Test Script
Tests the database operations, especially photo-related functionality
"""

import os
import sys
import logging
import shutil
from datetime import datetime
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / 'app'
sys.path.insert(0, str(app_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('db_validation_test.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import our modules
from app.database import DatabaseManager
from app.image_manager import PhotoManager

def test_database_connection():
    """Test basic database connection"""
    try:
        db = DatabaseManager()
        logger.info("Database connection successful")
        return db
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None

def test_get_properties(db):
    """Test fetching properties"""
    try:
        properties = db.get_properties()
        logger.info(f"Successfully retrieved {len(properties)} properties")

        if properties:
            # Return the first property for further testing
            return properties[0]
        else:
            logger.warning("No properties found for testing")
            return None
    except Exception as e:
        logger.error(f"Error getting properties: {e}")
        return None

def test_photo_operations(db, property_data):
    """Test photo operations with a property"""
    if not property_data:
        logger.error("No property data provided for photo testing")
        return False

    company_code = property_data['Companyco']
    logger.info(f"Testing photo operations for property: {company_code}")

    # 1. Create test photo
    photo_manager = PhotoManager()
    test_image = "app-images/alkawaz-logo.jpg"

    if not os.path.exists(test_image):
        logger.error(f"Test image not found: {test_image}")
        return False

    # Generate a unique filename for the test photo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_photo_name = f"TEST_{timestamp}.jpg"
    test_photo_path = os.path.join("property_photos", test_photo_name)

    # Copy test image to property_photos directory
    try:
        shutil.copy(test_image, test_photo_path)
        logger.info(f"Test photo created: {test_photo_path}")
    except Exception as e:
        logger.error(f"Error creating test photo: {e}")
        return False

    # 2. Test adding photo to database
    try:
        result = db.add_property_photo(company_code, test_photo_path, test_photo_name)
        logger.info(f"Photo add result: {result}")

        if not result:
            logger.error("Failed to add photo to database")
            return False
    except Exception as e:
        logger.error(f"Error adding photo to database: {e}")
        return False

    # 3. Test retrieving photos
    try:
        photos = db.get_property_photos(company_code)
        logger.info(f"Retrieved {len(photos)} photos for property {company_code}")

        # Check if our test photo is in the results
        test_photo_found = False
        for photo in photos:
            logger.info(f"Photo data: {photo}")
            if 'photo_name' in photo and photo['photo_name'] == test_photo_name:
                test_photo_found = True
                break
            # Also check other possible column names
            elif any(key for key in photo.keys() if 'name' in key.lower() and photo[key] == test_photo_name):
                test_photo_found = True
                break

        if not test_photo_found:
            logger.warning("Test photo not found in retrieved photos")
    except Exception as e:
        logger.error(f"Error retrieving photos: {e}")
        return False

    # 4. Test deleting photo (optional - uncomment if you want to test deletion)
    """
    try:
        result = db.delete_property_photo(test_photo_name)
        logger.info(f"Photo delete result: {result}")

        # Verify deletion
        photos_after = db.get_property_photos(company_code)
        test_photo_found = False
        for photo in photos_after:
            if 'photo_name' in photo and photo['photo_name'] == test_photo_name:
                test_photo_found = True
                break

        if test_photo_found:
            logger.warning("Test photo still exists after deletion")
        else:
            logger.info("Test photo successfully deleted")
    except Exception as e:
        logger.error(f"Error deleting photo: {e}")
        return False
    """

    return True

def inspect_database_structure():
    """Inspect and log database structure"""
    try:
        db_path = 'userdesktop-rs-database.db'

        if not os.path.exists(db_path):
            logger.error(f"Database file not found: {db_path}")
            return

        logger.info(f"Database file exists: {db_path}")
        logger.info(f"File size: {os.path.getsize(db_path)} bytes")

        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        logger.info("Tables in the database:")
        for table in tables:
            table_name = table[0]
            logger.info(f"- {table_name}")

            # Get schema for table
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            logger.info(f"  Columns in {table_name}:")
            for column in columns:
                logger.info(f"    - {column[1]} ({column[2]})")

            # Count rows in the table
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            logger.info(f"  Rows: {count}")

            # If it's the photos table, get more details
            if table_name.lower() == 'realstatephotos':
                logger.info("\nSample rows from realstatephotos:")
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                rows = cursor.fetchall()
                if rows:
                    for row in rows:
                        logger.info(f"  Row: {row}")
                else:
                    logger.info("  No rows found")

        conn.close()

    except Exception as e:
        logger.error(f"Error inspecting database: {e}")

def main():
    """Main test function"""
    logger.info("Starting database validation test")

    # First, let's inspect the database structure
    inspect_database_structure()

    # Test database connection
    db = test_database_connection()
    if not db:
        logger.error("Database connection test failed")
        return False

    # Test getting properties
    property_data = test_get_properties(db)

    # Test photo operations if we have a property
    if property_data:
        test_photo_operations(db, property_data)

    logger.info("Database validation test completed")
    return True

if __name__ == "__main__":
    main()
