#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Properties Management Screen
"""

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.clock import Clock
import os
import logging

from app.components import (RTLLabel, CustomActionButton as ActionButton, FormField, DataTable,
                            ConfirmDialog, MessageDialog, SearchBox,
                            PhotoUploader, ImageViewer, BilingualLabel, TranslatableButton,
                            NavigationHeader, ResponsiveCard)
from app.database import DatabaseManager
from app.utils import DataValidator, PhotoManager
from app.config import config
from app.font_manager import font_manager
from app.language_manager import language_manager

logger = logging.getLogger(__name__)


class PropertiesScreen(Screen):
    """Properties management screen"""

    def __init__(self, db_manager: DatabaseManager, **kwargs):
        super().__init__(**kwargs)
        self.name = 'properties'
        self.db = db_manager
        self.photo_manager = PhotoManager(config.photos_dir)
        self.current_property = None
        self.properties_data = []

        self.build_ui()
        self.load_properties()

    def build_ui(self):
        """Build the modern responsive properties management UI"""
        # Main layout with modern spacing
        main_layout = BoxLayout(orientation='vertical', spacing=dp(15), padding=[20, 10, 20, 20])

        # Navigation header
        nav_header = NavigationHeader(
            screen_title_key='properties_management',
            show_back_button=True
        )
        main_layout.add_widget(nav_header)

        # Content area
        content_layout = BoxLayout(orientation='horizontal', spacing=dp(20))

        # Left panel - Form in responsive card
        left_panel = ResponsiveCard(
            orientation='vertical',
            size_hint_x=0.5,
            spacing=dp(15),
            padding=dp(20)
        )

        # Form title
        left_panel.add_widget(BilingualLabel(
            text_en='Property Information',
            text_ar='معلومات العقار',
            font_size=dp(18),
            bold=True,
            size_hint_y=None,
            height=dp(40),
            halign='center'
        ))

        # Form scroll
        form_scroll = ScrollView()
        self.form_layout = BoxLayout(orientation='vertical', spacing=dp(10),
                                    size_hint_y=None)
        self.form_layout.bind(minimum_height=self.form_layout.setter('height'))

        # Company Code (auto-generated)
        self.company_code_field = FormField(language_manager.get_text('company_code'), required=True)
        self.company_code_field.input.readonly = True
        self.company_code_field.input.text = self.db.generate_company_code()
        self.form_layout.add_widget(self.company_code_field)

        # Real Estate Code (auto-generated)
        self.realstate_code_field = FormField(language_manager.get_text('property_code'), required=True)
        self.realstate_code_field.input.readonly = True
        self.realstate_code_field.input.text = self.db.generate_realstate_code()
        self.form_layout.add_widget(self.realstate_code_field)

        # Property Type
        property_types = self.db.get_property_types()
        type_values = [f"{pt[1]} ({pt[0]})" for pt in property_types]
        self.property_type_field = FormField(language_manager.get_text('property_type'), 'spinner', type_values, required=True)
        self.form_layout.add_widget(self.property_type_field)

        # Construction Year
        self.year_field = FormField(language_manager.get_text('construction_year'))
        self.form_layout.add_widget(self.year_field)

        # Property Area
        self.area_field = FormField(language_manager.get_text('property_area'), required=True)
        self.form_layout.add_widget(self.area_field)

        # Facade and Depth
        facade_depth_layout = BoxLayout(orientation='horizontal', spacing=dp(10),
                                       size_hint_y=None, height=dp(40))

        self.facade_field = FormField(language_manager.get_text('facade'))
        facade_depth_layout.add_widget(self.facade_field)

        self.depth_field = FormField(language_manager.get_text('depth'))
        facade_depth_layout.add_widget(self.depth_field)

        self.form_layout.add_widget(facade_depth_layout)

        # Bedrooms and Bathrooms
        rooms_layout = BoxLayout(orientation='horizontal', spacing=dp(10),
                                size_hint_y=None, height=dp(40))

        self.bedrooms_field = FormField(language_manager.get_text('bedrooms'))
        rooms_layout.add_widget(self.bedrooms_field)

        self.bathrooms_field = FormField(language_manager.get_text('bathrooms'))
        rooms_layout.add_widget(self.bathrooms_field)

        self.form_layout.add_widget(rooms_layout)

        # Corner Property
        corner_values = [language_manager.get_text('yes'), language_manager.get_text('no')]
        self.corner_field = FormField(language_manager.get_text('corner_property'), 'spinner', corner_values)
        self.form_layout.add_widget(self.corner_field)

        # Offer Type
        offer_types = self.db.get_offer_types()
        offer_values = [f"{ot[1]} ({ot[0]})" for ot in offer_types]
        self.offer_type_field = FormField(language_manager.get_text('offer_type'), 'spinner', offer_values, required=True)
        self.form_layout.add_widget(self.offer_type_field)

        # Province
        provinces = self.db.get_provinces()
        province_values = [f"{p[1]} ({p[0]})" for p in provinces]
        self.province_field = FormField(language_manager.get_text('province'), 'spinner', province_values, required=True)
        self.form_layout.add_widget(self.province_field)

        # Address
        self.address_field = FormField(language_manager.get_text('detailed_address'), 'multiline', required=True)
        self.form_layout.add_widget(self.address_field)

        # Owner
        owners = self.db.get_owners()
        owner_values = [f"{o[1]} ({o[0]})" for o in owners]
        self.owner_field = FormField(language_manager.get_text('owner'), 'spinner', owner_values, required=True)
        self.form_layout.add_widget(self.owner_field)

        # Description
        self.description_field = FormField(language_manager.get_text('description'), 'multiline')
        self.form_layout.add_widget(self.description_field)

        form_scroll.add_widget(self.form_layout)
        left_panel.add_widget(form_scroll)

        # Photo section
        photo_layout = BoxLayout(orientation='horizontal', spacing=dp(10),
                                size_hint_y=None, height=dp(50))

        upload_btn = TranslatableButton(
            translation_key='upload_photo',
            action=self.upload_photo,
            size_hint_x=0.5
        )
        photo_layout.add_widget(upload_btn)

        view_photos_btn = TranslatableButton(
            translation_key='view_photos',
            action=self.view_photos,
            size_hint_x=0.5
        )
        photo_layout.add_widget(view_photos_btn)

        left_panel.add_widget(photo_layout)

        # Action buttons
        button_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(50))

        self.save_btn = TranslatableButton(
            translation_key='save',
            button_type='success',
            action=self.save_property
        )
        button_layout.add_widget(self.save_btn)

        self.clear_btn = TranslatableButton(
            translation_key='clear',
            button_type='secondary',
            action=self.clear_form
        )
        button_layout.add_widget(self.clear_btn)

        self.update_btn = TranslatableButton(
            translation_key='update',
            button_type='warning',
            action=self.update_property
        )
        self.update_btn.disabled = True
        button_layout.add_widget(self.update_btn)

        self.delete_btn = TranslatableButton(
            translation_key='delete',
            button_type='danger',
            action=self.delete_property
        )
        self.delete_btn.disabled = True
        button_layout.add_widget(self.delete_btn)

        left_panel.add_widget(button_layout)
        content_layout.add_widget(left_panel)

        # Right panel - Data table in responsive card
        right_panel = ResponsiveCard(
            orientation='vertical',
            size_hint_x=0.5,
            spacing=dp(15),
            padding=dp(20)
        )

        # Table title
        right_panel.add_widget(BilingualLabel(
            text_en='Properties List',
            text_ar='قائمة العقارات',
            font_size=dp(18),
            bold=True,
            size_hint_y=None,
            height=dp(40),
            halign='center'
        ))

        # Search and filters
        search_layout = BoxLayout(orientation='vertical', spacing=dp(5),
                                 size_hint_y=None, height=dp(90))

        # Search box
        self.search_box = SearchBox(search_callback=self.search_properties)
        search_layout.add_widget(self.search_box)

        # Filter layout
        filter_layout = BoxLayout(orientation='horizontal', spacing=dp(5),
                                 size_hint_y=None, height=dp(40))

        # Property type filter
        self.type_filter = Spinner(
            text='كل الأنواع',
            values=['كل الأنواع'] + [pt[1] for pt in property_types],
            size_hint_x=0.33,
            font_name=font_manager.get_font_name('كل الأنواع')
        )
        self.type_filter.bind(text=self.apply_filters)
        filter_layout.add_widget(self.type_filter)

        # Offer type filter
        self.offer_filter = Spinner(
            text='كل العروض',
            values=['كل العروض'] + [ot[1] for ot in offer_types],
            size_hint_x=0.33,
            font_name=font_manager.get_font_name('كل العروض')
        )
        self.offer_filter.bind(text=self.apply_filters)
        filter_layout.add_widget(self.offer_filter)

        # Province filter
        self.province_filter = Spinner(
            text='كل المحافظات',
            values=['كل المحافظات'] + [p[1] for p in provinces],
            size_hint_x=0.34,
            font_name=font_manager.get_font_name('كل المحافظات')
        )
        self.province_filter.bind(text=self.apply_filters)
        filter_layout.add_widget(self.province_filter)

        search_layout.add_widget(filter_layout)
        right_panel.add_widget(search_layout)

        # Data table
        table_columns = [
            {'title': 'كود الشركة', 'field': 'Companyco'},
            {'title': 'نوع العقار', 'field': 'property_type_name'},
            {'title': 'المساحة', 'field': 'Property-area'},
            {'title': 'المالك', 'field': 'ownername'},
            {'title': 'العنوان', 'field': 'Property-address'}
        ]

        self.properties_table = DataTable(
            columns=table_columns,
            row_callback=self.select_property
        )
        right_panel.add_widget(self.properties_table)

        # Statistics
        self.stats_label = RTLLabel(
            text='',
            size_hint_y=None,
            height=dp(30),
            font_size='14sp'
        )
        right_panel.add_widget(self.stats_label)

        content_layout.add_widget(right_panel)
        main_layout.add_widget(content_layout)

        self.add_widget(main_layout)

    def load_properties(self):
        """Load all properties from database"""
        try:
            raw_properties = self.db.get_properties()

            # Process properties data
            self.properties_data = []
            for prop in raw_properties:
                # Get property type name
                property_types = self.db.get_property_types()
                type_name = 'غير محدد'
                for pt in property_types:
                    if pt[0] == prop.get('Rstatetcode'):
                        type_name = pt[1]
                        break

                processed_prop = dict(prop)
                processed_prop['property_type_name'] = type_name
                self.properties_data.append(processed_prop)

            # Update table
            self.properties_table.update_data(self.properties_data)
            self.update_stats()

        except Exception as e:
            logger.error(f"Error loading properties: {e}")
            self.show_message('خطأ', f'خطأ في تحميل بيانات العقارات: {str(e)}', 'error')

    def search_properties(self, search_text: str):
        """Search properties"""
        try:
            if not search_text:
                self.apply_filters()
                return

            filtered_data = []
            for prop in self.properties_data:
                if (search_text.lower() in (prop.get('Property-address', '').lower()) or
                    search_text.lower() in (prop.get('ownername', '').lower()) or
                    search_text in (prop.get('Companyco', ''))):
                    filtered_data.append(prop)

            self.properties_table.update_data(filtered_data)

        except Exception as e:
            logger.error(f"Error searching properties: {e}")

    def apply_filters(self, *args):
        """Apply selected filters"""
        try:
            filtered_data = self.properties_data.copy()

            # Apply type filter
            if self.type_filter.text != 'كل الأنواع':
                filtered_data = [p for p in filtered_data
                               if p.get('property_type_name') == self.type_filter.text]

            # Apply offer filter
            if self.offer_filter.text != 'كل العروض':
                offer_types = self.db.get_offer_types()
                offer_code = None
                for ot in offer_types:
                    if ot[1] == self.offer_filter.text:
                        offer_code = ot[0]
                        break

                if offer_code:
                    filtered_data = [p for p in filtered_data
                                   if p.get('Offer-Type-Code') == offer_code]

            # Apply province filter
            if self.province_filter.text != 'كل المحافظات':
                provinces = self.db.get_provinces()
                province_code = None
                for pv in provinces:
                    if pv[1] == self.province_filter.text:
                        province_code = pv[0]
                        break

                if province_code:
                    filtered_data = [p for p in filtered_data
                                   if p.get('Province-code') == province_code]

            self.properties_table.update_data(filtered_data)

        except Exception as e:
            logger.error(f"Error applying filters: {e}")

    def select_property(self, property_data: dict):
        """Select property for editing"""
        try:
            self.current_property = property_data
            self.load_property_data(property_data)

            # Enable update/delete buttons
            self.update_btn.disabled = False
            self.delete_btn.disabled = False
            self.save_btn.disabled = True

        except Exception as e:
            logger.error(f"Error selecting property: {e}")

    def load_property_data(self, property_data: dict):
        """Load property data into form"""
        try:
            # Basic fields
            self.company_code_field.set_value(property_data.get('Companyco', ''))
            self.realstate_code_field.set_value(property_data.get('realstatecode', ''))
            self.year_field.set_value(property_data.get('Yearmake', ''))
            self.area_field.set_value(str(property_data.get('Property-area', '')))
            self.facade_field.set_value(str(property_data.get('Property-facade', '')))
            self.depth_field.set_value(str(property_data.get('Property-depth', '')))
            self.bedrooms_field.set_value(str(property_data.get('N-of-bedrooms', '')))
            self.bathrooms_field.set_value(str(property_data.get('N-of bathrooms', '')))
            self.address_field.set_value(property_data.get('Property-address', ''))
            self.description_field.set_value(property_data.get('Descriptions', ''))

            # Spinner fields - find matching values
            # Property type
            property_types = self.db.get_property_types()
            for pt in property_types:
                if pt[0] == property_data.get('Rstatetcode'):
                    self.property_type_field.input.text = f"{pt[1]} ({pt[0]})"
                    break

            # Offer type
            offer_types = self.db.get_offer_types()
            for ot in offer_types:
                if ot[0] == property_data.get('Offer-Type-Code'):
                    self.offer_type_field.input.text = f"{ot[1]} ({ot[0]})"
                    break

            # Province
            provinces = self.db.get_provinces()
            for p in provinces:
                if p[0] == property_data.get('Province-code'):
                    self.province_field.input.text = f"{p[1]} ({p[0]})"
                    break

            # Owner
            owners = self.db.get_owners()
            for o in owners:
                if o[0] == property_data.get('Ownercode'):
                    self.owner_field.input.text = f"{o[1]} ({o[0]})"
                    break

            # Corner
            corner_value = property_data.get('Property-corner', 'لا')
            self.corner_field.input.text = corner_value

        except Exception as e:
            logger.error(f"Error loading property data: {e}")

    def save_property(self):
        """Save new property"""
        try:
            if not self.validate_form():
                return

            property_data = self.get_form_data()
            company_code = self.db.add_property(property_data)

            if company_code:
                self.show_message('نجح', 'تم حفظ العقار بنجاح', 'success')
                self.clear_form()
                self.load_properties()
            else:
                self.show_message('خطأ', 'فشل في حفظ العقار', 'error')

        except Exception as e:
            logger.error(f"Error saving property: {e}")
            self.show_message('خطأ', f'خطأ في حفظ العقار: {str(e)}', 'error')

    def update_property(self):
        """Update existing property"""
        # Note: This would require an update method in DatabaseManager
        self.show_message('معلومات', 'وظيفة التحديث قيد التطوير', 'info')

    def delete_property(self):
        """Delete selected property"""
        if not self.current_property:
            return

        confirm_dialog = ConfirmDialog(
            title='تأكيد الحذف',
            message='هل أنت متأكد من حذف هذا العقار؟',
            confirm_callback=self._confirm_delete
        )
        confirm_dialog.open()

    def _confirm_delete(self):
        """Confirm property deletion"""
        # Note: This would require a delete method in DatabaseManager
        self.show_message('معلومات', 'وظيفة الحذف قيد التطوير', 'info')

    def get_form_data(self) -> dict:
        """Get form data as dictionary"""
        return {
            'realstatecode': self.realstate_code_field.get_value(),
            'property_type': self.extract_code(self.property_type_field.get_value()),
            'year_make': self.year_field.get_value(),
            'area': float(self.area_field.get_value() or 0),
            'facade': float(self.facade_field.get_value() or 0),
            'depth': float(self.depth_field.get_value() or 0),
            'bedrooms': int(self.bedrooms_field.get_value() or 0),
            'bathrooms': int(self.bathrooms_field.get_value() or 0),
            'corner': self.corner_field.get_value(),
            'offer_type': self.extract_code(self.offer_type_field.get_value()),
            'province_code': self.extract_code(self.province_field.get_value()),
            'address': self.address_field.get_value(),
            'owner_code': self.extract_code(self.owner_field.get_value()),
            'description': self.description_field.get_value()
        }

    def extract_code(self, value: str) -> str:
        """Extract code from spinner value (format: Name (Code))"""
        if '(' in value and ')' in value:
            return value.split('(')[-1].replace(')', '')
        return value

    def validate_form(self) -> bool:
        """Validate form data"""
        # Check required fields
        required_fields = [
            (self.area_field, 'المساحة'),
            (self.property_type_field, 'نوع العقار'),
            (self.offer_type_field, 'نوع العرض'),
            (self.province_field, 'المحافظة'),
            (self.address_field, 'العنوان'),
            (self.owner_field, 'المالك')
        ]

        for field, name in required_fields:
            if not field.get_value().strip():
                self.show_message('خطأ', f'{name} مطلوب', 'warning')
                return False

        # Validate numeric fields
        if not DataValidator.validate_area(self.area_field.get_value()):
            self.show_message('خطأ', 'المساحة يجب أن تكون رقم صحيح', 'warning')
            return False

        year = self.year_field.get_value()
        if year and not DataValidator.validate_year(year):
            self.show_message('خطأ', 'سنة البناء غير صحيحة', 'warning')
            return False

        return True

    def clear_form(self):
        """Clear the form"""
        self.current_property = None

        # Generate new codes
        self.company_code_field.set_value(self.db.generate_company_code())
        self.realstate_code_field.set_value(self.db.generate_realstate_code())

        # Clear all fields
        fields = [
            self.year_field, self.area_field, self.facade_field, self.depth_field,
            self.bedrooms_field, self.bathrooms_field, self.address_field, self.description_field
        ]

        for field in fields:
            field.clear()

        # Reset spinners
        spinners = [
            self.property_type_field, self.corner_field, self.offer_type_field,
            self.province_field, self.owner_field
        ]

        for spinner in spinners:
            spinner.input.text = 'اختر...'

        # Reset button states
        self.save_btn.disabled = False
        self.update_btn.disabled = True
        self.delete_btn.disabled = True

    def upload_photo(self):
        """Upload property photo"""
        if not self.current_property:
            self.show_message('تنبيه', 'يرجى اختيار عقار أولاً', 'warning')
            return

        uploader = PhotoUploader(upload_callback=self._handle_photo_upload)
        uploader.open()

    def _handle_photo_upload(self, file_path: str):
        """Handle photo upload"""
        try:
            company_code = self.current_property['Companyco']
            filename = self.photo_manager.save_property_photo(file_path, company_code)

            if filename:
                # Save to database
                self.db.add_property_photo(company_code,
                                         self.photo_manager.get_photo_path(filename),
                                         filename)
                self.show_message('نجح', 'تم رفع الصورة بنجاح', 'success')
            else:
                self.show_message('خطأ', 'فشل في رفع الصورة', 'error')

        except Exception as e:
            logger.error(f"Error uploading photo: {e}")
            self.show_message('خطأ', f'خطأ في رفع الصورة: {str(e)}', 'error')

    def view_photos(self):
        """View property photos"""
        if not self.current_property:
            self.show_message('تنبيه', 'يرجى اختيار عقار أولاً', 'warning')
            return

        try:
            photos = self.db.get_property_photos(self.current_property['Companyco'])

            if not photos:
                self.show_message('معلومات', 'لا توجد صور لهذا العقار', 'info')
                return

            # Show photo gallery popup
            self._show_photo_gallery(photos)

        except Exception as e:
            logger.error(f"Error viewing photos: {e}")
            self.show_message('خطأ', f'خطأ في عرض الصور: {str(e)}', 'error')

    def _show_photo_gallery(self, photos: list):
        """Show photo gallery popup"""
        gallery_popup = Popup(
            title='معرض صور العقار',
            size_hint=(0.9, 0.8)
        )

        content = BoxLayout(orientation='vertical', spacing=dp(10))

        # Photos grid
        scroll = ScrollView()
        photos_grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None)
        photos_grid.bind(minimum_height=photos_grid.setter('height'))

        for photo in photos:
            photo_layout = BoxLayout(orientation='vertical', spacing=dp(5),
                                   size_hint_y=None, height=dp(200))

            # Photo image
            try:
                img = Image(
                    source=photo['photo_path'],
                    fit_mode="contain",
                    size_hint_y=0.8
                )
                photo_layout.add_widget(img)

                # View button
                view_btn = Button(
                    text='عرض',
                    size_hint_y=0.2,
                    font_name=font_manager.get_font_name('عرض'),
                    on_press=lambda x, path=photo['photo_path']:
                    self._view_single_photo(path)
                )
                photo_layout.add_widget(view_btn)

            except Exception as e:
                error_label = Label(text=f'خطأ في تحميل الصورة\n{photo["photo_name"]}')
                photo_layout.add_widget(error_label)

            photos_grid.add_widget(photo_layout)

        scroll.add_widget(photos_grid)
        content.add_widget(scroll)

        # Close button
        close_btn = Button(
            text='إغلاق',
            size_hint_y=None,
            height=dp(40),
            font_name=font_manager.get_font_name('إغلاق'),
            on_press=gallery_popup.dismiss
        )
        content.add_widget(close_btn)

        gallery_popup.content = content
        gallery_popup.open()

    def _view_single_photo(self, photo_path: str):
        """View single photo in full size"""
        viewer = ImageViewer(photo_path)
        viewer.open()

    def update_stats(self):
        """Update statistics display"""
        try:
            total_properties = len(self.properties_data)
            self.stats_label.text = f'إجمالي العقارات: {total_properties}'
        except Exception as e:
            logger.error(f"Error updating stats: {e}")

    def show_message(self, title: str, message: str, msg_type: str = 'info'):
        """Show message dialog"""
        dialog = MessageDialog(title=title, message=message, message_type=msg_type)
        dialog.open()

    def go_back(self):
        """Go back to dashboard"""
        self.manager.current = 'dashboard'

    def on_enter(self, *args):
        """Called when screen is entered"""
        self.load_properties()

        # Refresh owner list in case new owners were added
        owners = self.db.get_owners()
        owner_values = [f"{o[1]} ({o[0]})" for o in owners]
        self.owner_field.input.values = ['اختر...'] + owner_values
