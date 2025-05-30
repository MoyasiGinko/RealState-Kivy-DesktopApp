import sys
import os
from datetime import datetime

# Add the app directory to Python path
sys.path.insert(0, './app')

from app.database import DatabaseManager
from app.utils import PhotoManager
from app.config import config

def verify_photo_display():
    """Verify that photos can be displayed correctly"""

    print("Initializing database...")
    db = DatabaseManager()
    photo_manager = PhotoManager(config.photos_dir)

    # Get properties
    print("Getting properties...")
    properties = db.get_properties()
    if not properties:
        print("No properties found!")
        return

    # Use the first property for testing
    test_property = properties[0]
    company_code = test_property.get('Companyco')

    print(f"Testing with property: {company_code}")

    # Get photos
    print("Getting photos...")
    try:
        photos = db.get_property_photos(company_code)

        if not photos:
            print("No photos found for this property")
            return

        print(f"Found {len(photos)} photos")

        # Verify the photos have the expected fields
        for i, photo in enumerate(photos):
            print(f"\nPhoto {i+1}:")

            if 'photo_path' not in photo:
                print("  Error: Missing 'photo_path' field")
            else:
                print(f"  photo_path: {photo['photo_path']}")
                print(f"  File exists: {os.path.exists(photo['photo_path'])}")

            if 'photo_name' not in photo:
                print("  Error: Missing 'photo_name' field")
            else:
                print(f"  photo_name: {photo['photo_name']}")

            # Print all fields for debugging
            print("\n  All fields:")
            for key, value in photo.items():
                print(f"    {key}: {value}")

        print("\nVerification complete - all photos have the required fields!")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    verify_photo_display()
