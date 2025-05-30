# Real Estate Management System - Deployment Guide

## نظام إدارة العقارات - دليل النشر

### System Requirements / متطلبات النظام

#### Minimum Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 500MB free space
- **Display**: 1024x768 minimum (1366x768 recommended)

#### Recommended Specifications

- **Operating System**: Windows 11, macOS 12+, Ubuntu 20.04+
- **Python**: 3.10 or higher
- **RAM**: 8GB or more
- **Storage**: 2GB free space (for photos and reports)
- **Display**: 1920x1080 or higher

### Quick Installation / التثبيت السريع

#### Windows Users

1. Download the project files
2. Double-click `run.bat`
3. The application will automatically install dependencies and start

#### Linux/macOS Users

1. Download the project files
2. Open terminal in the project directory
3. Run: `chmod +x run.sh && ./run.sh`

### Manual Installation / التثبيت اليدوي

```bash
# 1. Ensure Python 3.8+ is installed
python --version

# 2. Install required packages
pip install -r requirements.txt

# 3. Run the application
python main.py
```

### Application Features / مميزات التطبيق

#### ✅ Completed Features

1. **Database Management**

   - SQLite database with proper schema
   - Automatic database initialization
   - Data integrity and relationships
   - Backup system

2. **Owner Management**

   - Add, edit, delete owners
   - Contact information tracking
   - Search and filter capabilities
   - Data validation

3. **Property Management**

   - Comprehensive property details
   - Photo gallery with thumbnails
   - Property specifications
   - Location and address management
   - Property status tracking

4. **Search & Reports**

   - Advanced search functionality
   - Multiple filter options
   - Export capabilities (CSV, reports)
   - Statistics dashboard

5. **User Interface**

   - Bilingual Arabic/English support
   - RTL text rendering
   - Modern, responsive design
   - Error handling and validation

6. **File Management**
   - Photo upload and management
   - Thumbnail generation
   - Report generation
   - Data export

### Project Structure / هيكل المشروع

```
Real Estate Management System/
├── main.py                 # Main application entry point
├── run.bat                # Windows startup script
├── run.sh                 # Linux/macOS startup script
├── config.ini             # Configuration file
├── requirements.txt       # Python dependencies
├── README.md              # Documentation
├── DEPLOYMENT.md          # This file
├── app/                   # Application source code
│   ├── config.py          # Configuration management
│   ├── database.py        # Database operations
│   ├── utils.py           # Utility functions
│   ├── components.py      # UI components
│   └── screens/           # Application screens
├── property_photos/       # Property images storage
├── backups/              # Database backups
├── reports/              # Generated reports
└── app-images/           # Application assets
```

### Usage Instructions / تعليمات الاستخدام

#### First Run

1. Start the application using `run.bat` (Windows) or `run.sh` (Linux/macOS)
2. The database will be automatically created
3. Use the main menu to navigate between sections

#### Adding Owners

1. Go to "إدارة الملاك" (Owner Management)
2. Fill in owner details
3. Click "حفظ" (Save)

#### Adding Properties

1. Go to "إدارة العقارات" (Property Management)
2. Fill in property details
3. Upload photos if needed
4. Click "حفظ" (Save)

#### Searching & Reports

1. Go to "البحث والتقارير" (Search & Reports)
2. Use filters to find specific properties
3. Export results using the export button

### Troubleshooting / استكشاف الأخطاء

#### Common Issues

1. **"Python is not recognized"**

   - Install Python from https://python.org
   - Ensure Python is added to PATH

2. **"Module not found" errors**

   - Run: `pip install -r requirements.txt`
   - Ensure all dependencies are installed

3. **Database errors**

   - Check if the application has write permissions
   - Ensure the directory is not read-only

4. **Display issues**
   - Ensure minimum screen resolution (1024x768)
   - Check graphics drivers are updated

### Performance Tips / نصائح الأداء

1. **Photo Management**

   - Keep photos under 5MB for better performance
   - Use JPG format for smaller file sizes
   - Clean up unused photos periodically

2. **Database Maintenance**

   - Regular backups are automatically created
   - Clear old log files periodically
   - Keep the database file under 100MB for optimal performance

3. **System Resources**
   - Close other applications when working with large datasets
   - Ensure sufficient RAM (8GB recommended)

### Support / الدعم

For technical support or questions:

- **Developer**: Luay Alkawaz
- **Email**: [Contact information]
- **Version**: 1.0.0
- **Last Updated**: May 29, 2025

### License / الترخيص

This software is proprietary and developed specifically for real estate management.
All rights reserved.

### Version History / تاريخ الإصدارات

- **v1.0.0** (May 29, 2025)
  - Initial production release
  - Complete feature implementation
  - Bilingual support
  - Database management
  - Photo management
  - Search and reporting
