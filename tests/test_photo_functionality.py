import sqlite3
import os
import sys
from datetime import datetime

# Add the app directory to Python path
sys.path.insert(0, './app')

from database import DatabaseManager

def test_get_property_photos():
    """Test the get_property_photos method with the actual database schema"""

    db_manager = DatabaseManager()

    # First, check what properties exist
    print("Checking available properties...")
    properties = db_manager.get_properties()

    if not properties:
        print("No properties found in the database. Test cannot proceed.")
        return

    # Select the first property for testing
    test_property = properties[0]
    company_code = test_property.get('Companyco')
    realstate_code = test_property.get('realstatecode')

    print(f"Testing with property: Company code: {company_code}, Real estate code: {realstate_code}")

    # Try to get photos
    print("\nGetting photos...")
    photos = db_manager.get_property_photos(company_code)

    print(f"Found {len(photos)} photos")

    if photos:
        print("\nPhoto details:")
        for i, photo in enumerate(photos):
            print(f"\nPhoto {i+1}:")
            for key, value in photo.items():
                print(f"  {key}: {value}")

            # Check if the expected derived fields exist
            if 'photo_path' in photo:
                print(f"  photo_path exists: {os.path.exists(photo['photo_path'])}")
            else:
                print("  photo_path field is missing!")

            if 'photo_name' in photo:
                print(f"  photo_name exists: {photo['photo_name']}")
            else:
                print("  photo_name field is missing!")
    else:
        print("No photos found for this property.")

        # If no photos exist, let's add a test photo
        print("\nAdding a test photo...")

        # Use an existing image as test
        test_image_source = "app-images/alkawaz-logo.jpg"

        if os.path.exists(test_image_source):
            # Create property_photos directory if it doesn't exist
            photos_dir = "property_photos"
            if not os.path.exists(photos_dir):
                os.makedirs(photos_dir)

            # Copy the test image to a new location
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_photo_name = f"TEST_{timestamp}.jpg"
            test_photo_path = os.path.join(photos_dir, test_photo_name)

            import shutil
            shutil.copy(test_image_source, test_photo_path)

            print(f"Test photo created at: {test_photo_path}")

            # Add the photo to the database
            result = db_manager.add_property_photo(company_code, test_photo_path, test_photo_name)
            print(f"Photo add result: {result}")

            # Try to get photos again
            print("\nGetting photos after adding test photo...")
            photos = db_manager.get_property_photos(company_code)

            print(f"Found {len(photos)} photos")

            if photos:
                print("\nPhoto details:")
                for i, photo in enumerate(photos):
                    print(f"\nPhoto {i+1}:")
                    for key, value in photo.items():
                        print(f"  {key}: {value}")

                    # Check if the expected derived fields exist
                    if 'photo_path' in photo:
                        print(f"  photo_path exists: {os.path.exists(photo['photo_path'])}")
                    else:
                        print("  photo_path field is missing!")

                    if 'photo_name' in photo:
                        print(f"  photo_name exists: {photo['photo_name']}")
                    else:
                        print("  photo_name field is missing!")
        else:
            print(f"Test image not found: {test_image_source}")

if __name__ == "__main__":
    test_get_property_photos()
