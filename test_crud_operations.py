#!/usr/bin/env python3
"""
Test script to verify Update and Delete functionality in Enhanced Properties
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from database import DatabaseManager

def test_property_operations():
    """Test property CRUD operations"""
    try:
        # Initialize database
        db = DatabaseManager()

        print("=== Testing Property Operations ===")

        # Get existing properties
        properties = db.get_properties()
        print(f"Found {len(properties)} existing properties")

        if properties:
            # Test with first property
            test_property = properties[0]
            print(f"\nProperty data structure keys: {list(test_property.keys())}")

            # Find the correct ID field
            property_id = test_property.get('Companyco') or test_property.get('companycode') or test_property.get('id')
            print(f"Testing with Property ID: {property_id}")
            print(f"Address: {test_property.get('Property-address', 'N/A')}")

            # Test update operation
            update_data = {
                'address': test_property.get('Property-address', '') + ' [UPDATED]',
                'description': test_property.get('Descriptions', '') + ' [UPDATED]',
                'area': test_property.get('Property-area', 0) + 10
            }

            print(f"\n--- Testing Update Operation ---")
            try:
                result = db.update_property(property_id, update_data)
                print(f"Update result: {result}")

                if result:
                    # Verify update
                    updated_properties = db.get_properties()
                    updated_property = next((p for p in updated_properties if p.get('Companyco') == property_id), None)
                    if updated_property:
                        print(f"Verified update - New address: {updated_property.get('Property-address', 'N/A')}")
                    else:
                        print("Could not verify update")
                else:
                    print("Update operation failed")

            except Exception as e:
                print(f"Error during update test: {e}")

            print(f"\n--- Testing Delete Operation ---")
            try:
                # Test that delete method exists and can be called
                print("Testing delete_property method availability...")
                if hasattr(db, 'delete_property'):
                    print("✓ delete_property method exists")

                    # Test actual delete functionality (we'll create a test property first)
                    print("\nCreating test property for deletion...")
                    test_prop_data = {
                        'realstatecode': 'TEST001',
                        'property_type': '02001',
                        'year_make': '2024',
                        'area': 100,
                        'address': 'Test Address for Deletion',
                        'owner_code': test_property.get('Ownercode', ''),
                        'description': 'Test property for deletion'
                    }

                    test_company_code = db.add_property(test_prop_data)
                    if test_company_code:
                        print(f"✓ Test property created with ID: {test_company_code}")

                        # Now test deletion
                        delete_result = db.delete_property(test_company_code)
                        if delete_result:
                            print(f"✓ Test property deleted successfully")
                        else:
                            print(f"✗ Failed to delete test property")
                    else:
                        print("✗ Failed to create test property")
                else:
                    print("✗ delete_property method not found")

                print("✓ Delete operation test complete")

            except Exception as e:
                print(f"Error during delete test: {e}")

        else:
            print("No properties found for testing")

        print(f"\n=== Test Complete ===")

    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_property_operations()
