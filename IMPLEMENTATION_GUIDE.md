# Real Estate Management System - Implementation Guide

## Overview

This document provides a comprehensive guide for using the newly implemented Real Estate Management System controllers and models. The system now includes full MVC architecture with enhanced functionality for property management, owner management, settings, activity tracking, reporting, and backup operations.

## Architecture

The system follows a modular MVC (Model-View-Controller) architecture:

### Models

- **PropertyModel**: Handles property data operations and database interactions
- **OwnerModel**: Manages owner information and related operations
- **SettingsModel**: JSON-based configuration management
- **ActivityModel**: Activity logging and tracking

### Controllers

- **MainController**: Central orchestrator that coordinates all system components
- **PropertyController**: Property management operations
- **OwnerController**: Owner management operations
- **SettingsController**: System settings and configuration
- **ActivityController**: Activity logging and statistics
- **BackupController**: Database backup, restore, and data export
- **ReportController**: Report generation and data analysis

## Quick Start

### 1. Initialize the System

```python
from app.database import DatabaseManager
from app.controllers import create_main_controller

# Initialize database
db_manager = DatabaseManager('path/to/database.db')

# Create main controller (handles all sub-controllers)
with create_main_controller(db_manager) as main_controller:
    # System is ready to use
    status = main_controller.get_system_status()
    print(f"System status: {status['system_health']}")
```

### 2. Property Management

```python
# Create a new property
property_data = {
    'realstatecode': 'PROP001',
    'property_type': '03',
    'build_type': '04',
    'area': 150.5,
    'facade': 12.0,
    'depth': 20.0,
    'bedrooms': 3,
    'bathrooms': 2,
    'is_corner': True,
    'offer_type': '06',
    'province': '01',
    'region': '02',
    'address': '123 Main Street',
    'owner_code': 'OWN001',
    'description': 'Beautiful property in prime location'
}

success = main_controller.create_property(property_data)

# Search properties with advanced criteria
search_criteria = {
    'property_type': '03',
    'min_area': 100,
    'max_area': 200,
    'min_bedrooms': 2,
    'is_corner': True,
    'province': '01'
}

properties = main_controller.search_properties(search_criteria)

# Get property summary with all details
property_summary = main_controller.get_controller('property').get_property_summary('COMP001')
```

### 3. Owner Management

```python
# Create a new owner
owner_data = {
    'ownername': 'John Doe',
    'ownerphone': '+1234567890',
    'note': 'Preferred contact method: email'
}

success = main_controller.create_owner(owner_data)

# Get all owners
owners = main_controller.get_all_owners()

# Update owner information
updated_data = {
    'ownername': 'John Doe Jr.',
    'ownerphone': '+1234567891'
}
success = main_controller.update_owner('OWN001', updated_data)
```

### 4. Report Generation

```python
# Generate property summary report
report_path = main_controller.generate_property_summary_report()

# Generate owner properties report for specific owner
owner_report = main_controller.generate_owner_properties_report('OWN001')

# Generate market analysis report
market_report = main_controller.generate_market_analysis_report()

# Export properties to CSV
properties = main_controller.search_properties({})
csv_path = main_controller.export_properties_to_csv(properties)

# Generate custom report with specific criteria
report_controller = main_controller.get_controller('report')
custom_report = report_controller.generate_custom_report(
    criteria={'property_type': '03'},
    report_type='detailed'
)
```

### 5. Backup and Data Management

```python
# Create full database backup
backup_path = main_controller.create_full_backup()

# List available backups
backups = main_controller.list_backups()

# Restore from backup
success = main_controller.restore_from_backup('backups/backup_20231215_143022.db')

# Clean up old backups (keep last 10)
deleted_count = main_controller.cleanup_old_backups(keep_count=10)

# Export specific data
backup_controller = main_controller.get_controller('backup')
export_path = backup_controller.create_data_export(
    tables=['Realstatspecification', 'Owners'],
    format_type='json'
)
```

### 6. Settings Management

```python
# Get current settings
settings = main_controller.get_settings()

# Update settings
new_settings = {
    'company_code': 'COMP001',
    'default_photo_path': '/path/to/photos',
    'backup_directory': '/path/to/backups',
    'auto_backup_enabled': True,
    'logging_level': 'INFO'
}
success = main_controller.update_settings(new_settings)

# Reset to defaults
success = main_controller.reset_settings()
```

### 7. Activity Tracking

```python
# Get recent activities
activities = main_controller.get_recent_activities(limit=20)

# Get activity statistics
stats = main_controller.get_activity_statistics()

# Activities are automatically logged for all operations
# Manual logging (if needed)
main_controller.log_activity('custom_action', {'detail': 'value'})
```

### 8. Reference Data

```python
# Get dropdown data for forms
property_types = main_controller.get_property_types()
build_types = main_controller.get_build_types()
offer_types = main_controller.get_offer_types()
provinces = main_controller.get_provinces()

# Example usage in a form
for code, description in property_types:
    print(f"{code}: {description}")
```

## Advanced Features

### Enhanced Search

The PropertyModel now supports advanced search with multiple criteria:

```python
property_controller = main_controller.get_controller('property')

# Complex search with multiple filters
advanced_criteria = {
    'search_term': 'downtown',           # Text search in multiple fields
    'property_type': '03',               # Specific property type
    'build_type': '04',                  # Specific build type
    'offer_type': '06',                  # Specific offer type
    'province': '01',                    # Province filter
    'region': '02',                      # Region filter
    'min_area': 100,                     # Minimum area
    'max_area': 300,                     # Maximum area
    'min_bedrooms': 2,                   # Minimum bedrooms
    'max_bedrooms': 5,                   # Maximum bedrooms
    'min_bathrooms': 1,                  # Minimum bathrooms
    'max_bathrooms': 3,                  # Maximum bathrooms
    'is_corner': True,                   # Corner property filter
    'year_from': 2020,                   # Built after year
    'year_to': 2023,                     # Built before year
    'owner_name': 'John'                 # Owner name filter
}

results = property_controller.advanced_search(advanced_criteria)
```

### Photo Management

```python
property_controller = main_controller.get_controller('property')

# Get property photos
photos = property_controller.model.get_photos('COMP001')

# Add photo to property
success = property_controller.model.add_photo(
    'COMP001',
    '/path/to/photo.jpg',
    'front_view.jpg'
)

# Delete photo
success = property_controller.model.delete_photo('front_view.jpg')
```

### Export Functionality

```python
property_controller = main_controller.get_controller('property')

# Export properties to different formats
properties = property_controller.load_properties()

# Export to CSV
csv_path = property_controller.model.export_properties(properties, 'csv')

# Export to JSON
json_path = property_controller.model.export_properties(properties, 'json')

# Generate comprehensive property report
report_path = property_controller.generate_property_report(
    'COMP001',
    include_photos=True
)
```

### Statistics and Analytics

```python
# Get property statistics
property_stats = main_controller.get_controller('property').get_statistics()

# Get system status
system_status = main_controller.get_system_status()

# Get activity statistics
activity_stats = main_controller.get_activity_statistics()
```

## Error Handling

All controllers include comprehensive error handling:

```python
try:
    success = main_controller.create_property(property_data)
    if not success:
        print("Property creation failed - check validation errors")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Database Compatibility

The system has been updated to work with the existing database schema:

- Table name changed from 'Properties' to 'Realstatspecification'
- All methods use 'company_code' parameter consistently
- Proper integration with existing Owners, Maincode, and realstatephotos tables

## File Structure

```
app/
├── controllers/
│   ├── __init__.py           # Controller exports and factory functions
│   ├── base_controller.py    # Base controller class
│   ├── main_controller.py    # Central system controller
│   ├── property_controller.py# Property management
│   ├── owner_controller.py   # Owner management
│   ├── settings_controller.py# Settings management
│   ├── activity_controller.py# Activity tracking
│   ├── backup_controller.py  # Backup and data export
│   └── report_controller.py  # Report generation
├── models/
│   ├── property_model.py     # Enhanced property model
│   ├── owner_model.py        # Owner model
│   ├── settings_model.py     # Settings model
│   └── activity_model.py     # Activity model
└── database.py               # Database manager
```

## Testing

Basic system validation:

```python
# Test system initialization
with create_main_controller(db_manager) as main_controller:
    # Check system health
    status = main_controller.get_system_status()
    assert status['system_health'] == 'healthy'

    # Test basic operations
    owners = main_controller.get_all_owners()
    properties = main_controller.get_all_properties()

    # Test backup creation
    backup_path = main_controller.create_full_backup()
    assert backup_path is not None

    print("All basic tests passed!")
```

## Next Steps

The system is now fully implemented with:

- ✅ Enhanced PropertyModel with advanced search
- ✅ Complete PropertyController with export/reporting features
- ✅ Settings system (Dashboard Item #5)
- ✅ Activity tracking system (Dashboard Item #6)
- ✅ Comprehensive backup and data management
- ✅ Advanced reporting and analytics
- ✅ Reference data management
- ✅ Error handling and logging

For production deployment:

1. Integrate controllers with your Kivy views
2. Add user authentication if required
3. Configure logging levels and file paths
4. Set up automatic backup scheduling
5. Add validation for user inputs
6. Implement role-based access control if needed

The system is ready for integration with your existing Kivy desktop application!
