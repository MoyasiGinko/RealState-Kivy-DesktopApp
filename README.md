# Real Estate Management System نظام إدارة العقارات

A comprehensive desktop application for managing real estate properties with bilingual Arabic/English support.

## 🎯 Project Overview

This is a production-ready desktop application built with Python and Kivy framework for managing real estate properties. The system provides a complete solution for real estate professionals to manage owners, properties, search data, and generate reports.

## ✨ Key Features

### 🏠 Property Management

- Complete property information tracking
- Property specifications (area, rooms, bathrooms, etc.)
- Building details and construction information
- Location and address management
- Photo gallery with thumbnail generation
- Property status tracking (for sale, rent, sold)

### 👥 Owner Management

- Comprehensive owner database
- Contact information tracking
- Notes and additional details
- Owner-property relationship management

### 🔍 Advanced Search & Filtering

- Multi-criteria search functionality
- Filter by property type, location, owner, price range
- Real-time search results
- Export search results to various formats

### 📊 Reports & Analytics

- Real-time statistics dashboard
- Property distribution analysis
- Comprehensive reporting system
- Data export capabilities (CSV, PDF)

### 🌐 Bilingual Support

- Full Arabic and English interface
- RTL (Right-to-Left) text support
- Professional real estate terminology
- Unicode text handling

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Windows, macOS, or Linux

### Installation & Running

#### Windows

1. Double-click `run.bat` to start the application
2. The script will automatically install dependencies if needed

#### Linux/macOS

1. Make the script executable: `chmod +x run.sh`
2. Run: `./run.sh`

#### Manual Installation

```bash
# Clone the repository
git clone [repository-url]
cd Kivy-Desktop

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 📁 Project Structure

```
Real Estate Management System/
├── main.py                 # Application entry point
├── config.ini             # Configuration file
├── requirements.txt       # Python dependencies
├── run.bat                # Windows startup script
├── run.sh                 # Linux/macOS startup script
├── README.md              # This file
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── database.py        # Database operations
│   ├── utils.py           # Utility functions
│   ├── components.py      # UI components
│   └── screens/           # Application screens
│       ├── dashboard.py   # Main dashboard
│       ├── owners.py      # Owner management
│       ├── properties.py  # Property management
│       └── search.py      # Search and reports
├── property_photos/       # Property images
│   └── thumbnails/        # Auto-generated thumbnails
├── backups/              # Database backups
├── reports/              # Generated reports
└── app-images/           # Application icons and logos
```

## 🗄️ Database Schema

- **Owners Table**: Owner information management
- **Realstatspecification Table**: Property details and specifications
- **realstatephotos Table**: Property photo management
- **Maincode Table**: Reference data for provinces and regions

#### Technology Stack

- **Python 3.x**: Core programming language
- **Kivy 2.3+**: Cross-platform GUI framework
- **SQLite**: Embedded database system
- **Pillow**: Image processing library

### Installation & Setup

#### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

#### Installation Steps

1. **Clone or Download the Project**

   ```bash
   cd /path/to/project
   ```

2. **Set up Virtual Environment** (if not already done)

   ```bash
   python -m venv kivy_venv
   ```

3. **Activate Virtual Environment**

   - Windows:
     ```bash
     kivy_venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source kivy_venv/bin/activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**
   - Windows: Double-click `start_app.bat`
   - Linux/Mac: `./start_app.sh`
   - Or directly: `python main.py`

### Project Structure

```
Kivy-Desktop/
├── main.py                    # Main application entry point
├── properties_screen.py       # Property management interface
├── search_reports.py          # Search and reports functionality
├── requirements.txt           # Python dependencies
├── config.ini                # Application configuration
├── start_app.bat             # Windows startup script
├── start_app.sh              # Linux/Mac startup script
├── userdesktop-rs-database.db # SQLite database
├── property_photos/          # Directory for property images
└── kivy_venv/               # Virtual environment
```

### Usage Guide

#### 1. Main Dashboard

- Overview of system statistics
- Quick navigation to all modules
- Real-time property and owner counts

#### 2. Owner Management

- Add new property owners
- Manage contact information
- View complete owner list
- Auto-generated owner codes

#### 3. Property Management

- Comprehensive property form
- Property type and specification selection
- Photo upload and management
- Owner assignment
- Location and address details

#### 4. Search & Filter

- Multi-criteria property search
- Detailed property view
- Photo gallery browsing
- Export search results to text files

#### 5. Reports

- System statistics overview
- Property type distribution
- Comprehensive report generation
- Data export capabilities

### Database Features

#### Reference Data Management

- Province codes (المحافظات)
- Region codes (المناطق)
- Property type classifications
- Offer type management

#### Data Integrity

- Foreign key relationships
- Data validation
- Automatic code generation
- Backup and recovery support

### Customization

#### Configuration Options

Edit `config.ini` to customize:

- Window dimensions
- Color schemes
- Database paths
- Font sizes

#### Adding New Features

The modular design allows easy extension:

- Add new screens by creating screen classes
- Extend database schema as needed
- Implement additional report types
- Add new search criteria

### Troubleshooting

#### Common Issues

1. **Application Won't Start**

   - Ensure virtual environment is activated
   - Check all dependencies are installed
   - Verify Python version compatibility

2. **Database Errors**

   - Check database file permissions
   - Ensure SQLite is available
   - Verify table structures

3. **Photo Upload Issues**
   - Check property_photos directory exists
   - Verify file permissions
   - Ensure image formats are supported

#### Performance Optimization

- Regular database maintenance
- Photo file management
- Cache clearing for large datasets

### Development

#### Code Structure

- **main.py**: Application core and main screen
- **properties_screen.py**: Property management functionality
- **search_reports.py**: Search and reporting features
- Modular design for easy maintenance

#### Contributing

1. Follow Python PEP 8 standards
2. Maintain Arabic/English bilingual support
3. Test thoroughly with sample data
4. Document new features

### Security & Backup

#### Data Protection

- Regular database backups recommended
- Photo file organization
- Access control considerations

#### Backup Strategy

```bash
# Create backup
cp userdesktop-rs-database.db backups/backup_$(date +%Y%m%d).db

# Backup photos
tar -czf backups/photos_$(date +%Y%m%d).tar.gz property_photos/
```

### Support & Contact

For technical support or feature requests:

- Review the documentation
- Check configuration settings
- Examine log files for errors

### License

This project is developed for real estate management purposes. Ensure compliance with local data protection regulations when handling personal information.

### Version History

**v1.0.0** - Initial Release

- Complete property management system
- Owner database management
- Search and filtering capabilities
- Report generation
- Photo management
- Bilingual interface

---

## نظام إدارة العقارات

نظام شامل لإدارة العقارات مبني بلغة Python وإطار عمل Kivy.

### المميزات الرئيسية

1. **إدارة الملاك**: إضافة وتعديل بيانات الملاك
2. **إدارة العقارات**: تسجيل تفاصيل العقارات والمواصفات
3. **البحث والتصفية**: بحث متقدم وتصفية حسب معايير متعددة
4. **التقارير**: إحصائيات شاملة وتقارير مفصلة
5. **إدارة الصور**: معرض صور لكل عقار
6. **واجهة ثنائية اللغة**: دعم كامل للعربية والإنجليزية

### متطلبات التشغيل

- Python 3.8 أو أحدث
- نظام تشغيل Windows، Linux، أو macOS
- مساحة تخزين كافية للصور والبيانات

### التشغيل السريع

1. تفعيل البيئة الافتراضية
2. تشغيل ملف `start_app.bat` (Windows) أو `start_app.sh` (Linux/Mac)
3. أو تشغيل `python main.py` مباشرة

---

_Real Estate Management System - Built with Python & Kivy_
