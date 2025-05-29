#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Language Management
Handles multilingual support for Arabic and English
"""

import json
import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class LanguageManager:
    """Manages application languages and translations"""

    def __init__(self):
        self.current_language = 'ar'  # Default to Arabic
        self.translations = {}
        self.observers = []  # Components that need to update when language changes
        self.load_translations()

    def load_translations(self):
        """Load translation data"""
        self.translations = {
            'ar': {
                # Application
                'app_title': 'نظام إدارة العقارات',
                'version': 'النسخة',
                'developed_by': 'تطوير',

                # Navigation
                'dashboard': 'لوحة التحكم',
                'owners_management': 'إدارة الملاك',
                'properties_management': 'إدارة العقارات',
                'search_reports': 'البحث والتقارير',
                'back': 'رجوع',
                'back_to_menu': 'العودة للقائمة الرئيسية',                'home': 'الرئيسية',
                'menu': 'القائمة',
                'enter_dashboard': 'دخول لوحة التحكم',

                # Common Actions
                'save': 'حفظ',
                'update': 'تحديث',
                'delete': 'حذف',
                'clear': 'مسح',
                'search': 'بحث',
                'add': 'إضافة',
                'edit': 'تعديل',
                'cancel': 'إلغاء',
                'ok': 'موافق',
                'yes': 'نعم',
                'no': 'لا',
                'close': 'إغلاق',                # Form Fields - Owner
                'owner_code': 'كود المالك',
                'owner_name': 'اسم المالك',
                'phone': 'الهاتف',
                'email': 'البريد الإلكتروني',
                'address': 'العنوان',
                'notes': 'ملاحظات',
                'id_number': 'رقم الهوية',                # Form Fields - Property
                'company_code': 'كود الشركة',
                'property_code': 'كود العقار',
                'property_number': 'رقم العقار',
                'property_type': 'نوع العقار',
                'construction_year': 'سنة البناء',
                'property_area': 'المساحة (م²)',
                'facade': 'الواجهة (م)',
                'depth': 'العمق (م)',
                'bedrooms': 'غرف النوم',
                'bathrooms': 'دورات المياه',
                'corner_property': 'عقار زاوية',
                'price': 'السعر',
                'rent_price': 'سعر الإيجار',
                'status': 'الحالة',
                'description': 'الوصف',                'location': 'الموقع',
                'neighborhood': 'الحي',
                'street': 'الشارع',
                'offer_type': 'نوع العرض',
                'province': 'المحافظة',
                'detailed_address': 'العنوان التفصيلي',

                # Property Types
                'house': 'منزل',
                'apartment': 'شقة',
                'villa': 'فيلا',
                'land': 'أرض',
                'commercial': 'تجاري',
                'office': 'مكتب',

                # Property Status
                'available': 'متاح',
                'sold': 'مباع',
                'rented': 'مؤجر',
                'reserved': 'محجوز',                # Dashboard
                'system_statistics': 'إحصائيات النظام',
                'quick_actions': 'الإجراءات السريعة',
                'recent_activity': 'النشاط الأخير',
                'total_properties': 'إجمالي العقارات',
                'total_owners': 'إجمالي الملاك',
                'properties_for_sale': 'عقارات للبيع',
                'properties_for_rent': 'عقارات للإيجار',                'available_properties': 'العقارات المتاحة',
                'sold_properties': 'العقارات المباعة',
                'recent_properties': 'العقارات الحديثة',
                'quick_stats': 'إحصائيات سريعة',
                'no_properties_registered': 'لا توجد عقارات مسجلة',
                'property_no_address': 'عقار بدون عنوان',
                'owner': 'المالك',
                'database_status': 'حالة قاعدة البيانات',
                'active': 'نشط',

                # New Dashboard Elements
                'no_recent_activity': 'لا يوجد نشاط حديث',
                'add_new_owner': 'إضافة مالك جديد',
                'add_new_property': 'إضافة عقار جديد',
                'view_all_properties': 'عرض جميع العقارات',
                'view_all_owners': 'عرض جميع الملاك',
                'advanced_search': 'البحث المتقدم',
                'generate_reports': 'إنشاء التقارير',
                'statistics': 'الإحصائيات',
                'reports': 'التقارير',

                # Screen Titles
                'owners_management': 'إدارة الملاك',
                'properties_management': 'إدارة العقارات',
                'search_reports': 'البحث والتقارير',                # Messages
                'success': 'نجح',
                'error': 'خطأ',
                'warning': 'تحذير',
                'info': 'معلومات',
                'confirm_delete': 'هل تريد حذف هذا العنصر؟',
                'operation_successful': 'تمت العملية بنجاح',
                'operation_failed': 'فشلت العملية',
                'required_field': 'هذا الحقل مطلوب',
                'invalid_data': 'البيانات غير صحيحة',
                'error_loading_data': 'خطأ في تحميل البيانات',

                # Search
                'search_properties': 'البحث في العقارات',
                'search_owners': 'البحث في الملاك',
                'filter_by': 'تصفية حسب',
                'results': 'النتائج',
                'no_results': 'لا توجد نتائج',

                # Photos
                'upload_photo': 'رفع صورة',
                'view_photos': 'عرض الصور',
                'no_photos': 'لا توجد صور',
                'photo_uploaded': 'تم رفع الصورة',                # Language
                'language': 'اللغة',
                'arabic': 'العربية',
                'english': 'English',
                'switch_language': 'تغيير اللغة',
                'settings': 'الإعدادات',
                'feature_coming_soon': 'هذه الميزة قيد التطوير',
            },

            'en': {
                # Application
                'app_title': 'Real Estate Management System',
                'version': 'Version',
                'developed_by': 'Developed by',

                # Navigation
                'dashboard': 'Dashboard',
                'owners_management': 'Owners Management',
                'properties_management': 'Properties Management',
                'search_reports': 'Search & Reports',
                'back': 'Back',
                'back_to_menu': 'Back to Main Menu',                'home': 'Home',
                'menu': 'Menu',
                'enter_dashboard': 'Enter Dashboard',

                # Common Actions
                'save': 'Save',
                'update': 'Update',
                'delete': 'Delete',
                'clear': 'Clear',
                'search': 'Search',
                'add': 'Add',
                'edit': 'Edit',
                'cancel': 'Cancel',
                'ok': 'OK',
                'yes': 'Yes',
                'no': 'No',
                'close': 'Close',                # Form Fields - Owner
                'owner_code': 'Owner Code',
                'owner_name': 'Owner Name',
                'phone': 'Phone',
                'email': 'Email',
                'address': 'Address',
                'notes': 'Notes',
                'id_number': 'ID Number',                # Form Fields - Property
                'company_code': 'Company Code',
                'property_code': 'Property Code',
                'property_number': 'Property Number',
                'property_type': 'Property Type',
                'construction_year': 'Construction Year',
                'property_area': 'Area (m²)',
                'facade': 'Facade (m)',
                'depth': 'Depth (m)',
                'bedrooms': 'Bedrooms',
                'bathrooms': 'Bathrooms',
                'corner_property': 'Corner Property',
                'price': 'Price',
                'rent_price': 'Rent Price',
                'status': 'Status',
                'description': 'Description',                'location': 'Location',
                'neighborhood': 'Neighborhood',
                'street': 'Street',
                'offer_type': 'Offer Type',
                'province': 'Province',
                'detailed_address': 'Detailed Address',

                # Property Types
                'house': 'House',
                'apartment': 'Apartment',
                'villa': 'Villa',
                'land': 'Land',
                'commercial': 'Commercial',
                'office': 'Office',

                # Property Status
                'available': 'Available',
                'sold': 'Sold',
                'rented': 'Rented',
                'reserved': 'Reserved',                # Dashboard
                'system_statistics': 'System Statistics',
                'quick_actions': 'Quick Actions',
                'recent_activity': 'Recent Activity',
                'total_properties': 'Total Properties',
                'total_owners': 'Total Owners',
                'properties_for_sale': 'Properties for Sale',
                'properties_for_rent': 'Properties for Rent',
                'available_properties': 'Available Properties',
                'sold_properties': 'Sold Properties',
                'recent_properties': 'Recent Properties',
                'quick_stats': 'Quick Statistics',                'no_properties_registered': 'No properties registered',
                'property_no_address': 'Property without address',
                'owner': 'Owner',
                'database_status': 'Database Status',
                'active': 'Active',

                # New Dashboard Elements
                'no_recent_activity': 'No recent activity',
                'add_new_owner': 'Add New Owner',
                'add_new_property': 'Add New Property',
                'view_all_properties': 'View All Properties',
                'view_all_owners': 'View All Owners',
                'advanced_search': 'Advanced Search',
                'generate_reports': 'Generate Reports',
                'statistics': 'Statistics',
                'reports': 'Reports',

                # Screen Titles
                'owners_management': 'Owners Management',
                'properties_management': 'Properties Management',
                'search_reports': 'Search & Reports',

                # Messages                'success': 'Success',
                'error': 'Error',
                'warning': 'Warning',
                'info': 'Information',
                'confirm_delete': 'Do you want to delete this item?',
                'operation_successful': 'Operation completed successfully',
                'operation_failed': 'Operation failed',
                'required_field': 'This field is required',
                'invalid_data': 'Invalid data',
                'error_loading_data': 'Error loading data',

                # Search
                'search_properties': 'Search Properties',
                'search_owners': 'Search Owners',
                'filter_by': 'Filter by',
                'results': 'Results',
                'no_results': 'No results found',

                # Photos
                'upload_photo': 'Upload Photo',
                'view_photos': 'View Photos',
                'no_photos': 'No photos available',
                'photo_uploaded': 'Photo uploaded',                # Language
                'language': 'Language',
                'arabic': 'العربية',
                'english': 'English',
                'switch_language': 'Switch Language',
                'settings': 'Settings',
                'feature_coming_soon': 'This feature is coming soon',
            }
        }

    def get_text(self, key: str, default: str = None) -> str:
        """Get translated text for a key"""
        if default is None:
            default = key

        return self.translations.get(self.current_language, {}).get(key, default)

    def get_bilingual_text(self, key: str) -> str:
        """Get bilingual text (Arabic + English)"""
        arabic_text = self.translations.get('ar', {}).get(key, key)
        english_text = self.translations.get('en', {}).get(key, key)

        if self.current_language == 'ar':
            return f"{arabic_text}\n{english_text}"
        else:
            return f"{english_text}\n{arabic_text}"

    def switch_language(self):
        """Switch between Arabic and English"""
        self.current_language = 'en' if self.current_language == 'ar' else 'ar'
        self.notify_observers()
        logger.info(f"Language switched to: {self.current_language}")

    def set_language(self, language_code: str):
        """Set specific language"""
        if language_code in ['ar', 'en']:
            self.current_language = language_code
            self.notify_observers()
            logger.info(f"Language set to: {self.current_language}")

    def is_rtl(self) -> bool:
        """Check if current language is RTL"""
        return self.current_language == 'ar'

    def add_observer(self, observer):
        """Add observer for language changes"""
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        """Remove observer"""
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self):
        """Notify all observers of language change"""
        for observer in self.observers[:]:  # Create a copy to avoid issues during iteration
            try:
                if hasattr(observer, 'on_language_changed'):
                    observer.on_language_changed()
            except Exception as e:
                logger.error(f"Error notifying observer: {e}")

    def get_current_language(self) -> str:
        """Get current language code"""
        return self.current_language

    def get_available_languages(self) -> Dict[str, str]:
        """Get available languages"""
        return {
            'ar': self.get_text('arabic'),
            'en': self.get_text('english')
        }


# Global language manager instance
language_manager = LanguageManager()
