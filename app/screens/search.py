#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Search and Reports Screen
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.filechooser import FileChooserIconView
from kivy.metrics import dp
from kivy.clock import Clock
import os
from datetime import datetime
import logging

from app.components import (RTLLabel, CustomActionButton as ActionButton, FormField, DataTable,
                            ConfirmDialog, MessageDialog, SearchBox, StatsCard)
from app.database import DatabaseManager
from app.font_manager import font_manager
from app.utils import ExportUtils
from app.config import config

logger = logging.getLogger(__name__)


class SearchScreen(Screen):
    """Search and Reports screen"""

    def __init__(self, db_manager: DatabaseManager, **kwargs):
        super().__init__(**kwargs)
        self.name = 'search'
        self.db = db_manager
        self.search_results = []

        self.build_ui()

    def build_ui(self):
        """Build the search and reports UI"""
        main_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))

        # Header
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        header_layout.add_widget(RTLLabel(
            text='البحث والتقارير',
            font_size='24sp',
            bold=True
        ))

        # Back button
        back_btn = ActionButton(
            text='العودة',
            size_hint_x=None,
            width=dp(80),
            action=self.go_back
        )
        header_layout.add_widget(back_btn)
        main_layout.add_widget(header_layout)

        # Tabbed panel
        tabs = TabbedPanel(do_default_tab=False)

        # Search tab
        search_tab = TabbedPanelItem(text='البحث المتقدم')
        search_tab.content = self.build_search_tab()
        tabs.add_widget(search_tab)

        # Reports tab
        reports_tab = TabbedPanelItem(text='التقارير')
        reports_tab.content = self.build_reports_tab()
        tabs.add_widget(reports_tab)

        # Statistics tab
        stats_tab = TabbedPanelItem(text='الإحصائيات')
        stats_tab.content = self.build_statistics_tab()
        tabs.add_widget(stats_tab)

        main_layout.add_widget(tabs)
        self.add_widget(main_layout)

    def build_search_tab(self):
        """Build search tab content"""
        layout = BoxLayout(orientation='horizontal', spacing=dp(10))

        # Left panel - Search criteria
        left_panel = BoxLayout(orientation='vertical', size_hint_x=0.3, spacing=dp(10))

        left_panel.add_widget(RTLLabel(
            text='معايير البحث',
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height=dp(40)
        ))

        # Search form
        search_form = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        search_form.bind(minimum_height=search_form.setter('height'))

        # Property type filter
        property_types = self.db.get_property_types()
        type_values = ['كل الأنواع'] + [pt[1] for pt in property_types]
        self.search_type_field = FormField('نوع العقار', 'spinner', type_values)
        search_form.add_widget(self.search_type_field)

        # Offer type filter
        offer_types = self.db.get_offer_types()
        offer_values = ['كل العروض'] + [ot[1] for ot in offer_types]
        self.search_offer_field = FormField('نوع العرض', 'spinner', offer_values)
        search_form.add_widget(self.search_offer_field)

        # Province filter
        provinces = self.db.get_provinces()
        province_values = ['كل المحافظات'] + [p[1] for p in provinces]
        self.search_province_field = FormField('المحافظة', 'spinner', province_values)
        search_form.add_widget(self.search_province_field)

        # Owner filter
        owners = self.db.get_owners()
        owner_values = ['كل الملاك'] + [f"{o[1]} ({o[0]})" for o in owners]
        self.search_owner_field = FormField('المالك', 'spinner', owner_values)
        search_form.add_widget(self.search_owner_field)

        # Area range
        area_layout = BoxLayout(orientation='horizontal', spacing=dp(5),
                               size_hint_y=None, height=dp(40))
        area_layout.add_widget(RTLLabel(text='المساحة من:', size_hint_x=0.3))

        self.min_area_input = TextInput(multiline=False, size_hint_x=0.35)
        area_layout.add_widget(self.min_area_input)

        area_layout.add_widget(RTLLabel(text='إلى:', size_hint_x=0.1))

        self.max_area_input = TextInput(multiline=False, size_hint_x=0.25)
        area_layout.add_widget(self.max_area_input)

        search_form.add_widget(area_layout)

        # Address search
        self.search_address_field = FormField('البحث في العنوان')
        search_form.add_widget(self.search_address_field)

        left_panel.add_widget(search_form)

        # Search buttons
        search_buttons = BoxLayout(orientation='vertical', spacing=dp(10),
                                  size_hint_y=None, height=dp(100))

        search_btn = ActionButton(
            text='بحث',
            button_type='primary',
            action=self.perform_search
        )
        search_buttons.add_widget(search_btn)

        clear_search_btn = ActionButton(
            text='مسح الفلاتر',
            button_type='secondary',
            action=self.clear_search_filters
        )
        search_buttons.add_widget(clear_search_btn)

        left_panel.add_widget(search_buttons)
        layout.add_widget(left_panel)

        # Right panel - Results
        right_panel = BoxLayout(orientation='vertical', size_hint_x=0.7, spacing=dp(10))

        # Results header
        results_header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))

        self.results_label = RTLLabel(
            text='نتائج البحث',
            font_size='18sp',
            bold=True
        )
        results_header.add_widget(self.results_label)

        # Export button
        export_btn = ActionButton(
            text='تصدير النتائج',
            size_hint_x=None,
            width=dp(120),
            action=self.export_results
        )
        results_header.add_widget(export_btn)

        right_panel.add_widget(results_header)

        # Results table
        table_columns = [
            {'title': 'كود الشركة', 'field': 'Companyco'},
            {'title': 'نوع العقار', 'field': 'property_type_name'},
            {'title': 'المساحة', 'field': 'Property-area'},
            {'title': 'نوع العرض', 'field': 'offer_type_name'},
            {'title': 'المحافظة', 'field': 'province_name'},
            {'title': 'المالك', 'field': 'ownername'},
            {'title': 'العنوان', 'field': 'Property-address'}
        ]

        self.search_results_table = DataTable(
            columns=table_columns,
            row_callback=self.view_property_details
        )
        right_panel.add_widget(self.search_results_table)

        layout.add_widget(right_panel)
        return layout

    def build_reports_tab(self):
        """Build reports tab content"""
        layout = BoxLayout(orientation='vertical', spacing=dp(20), padding=dp(20))

        layout.add_widget(RTLLabel(
            text='التقارير',
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(40)
        ))

        # Reports grid
        reports_grid = GridLayout(cols=2, spacing=dp(20), size_hint_y=None, height=dp(300))

        # Property summary report
        property_report_layout = BoxLayout(orientation='vertical', spacing=dp(10))
        property_report_layout.add_widget(RTLLabel(
            text='تقرير ملخص العقارات',
            font_size='16sp',
            bold=True
        ))
        property_report_layout.add_widget(RTLLabel(
            text='تقرير شامل لجميع العقارات مع التفاصيل الأساسية',
            font_size='12sp'
        ))
        property_report_btn = ActionButton(
            text='إنشاء التقرير',
            action=self.generate_property_report
        )
        property_report_layout.add_widget(property_report_btn)
        reports_grid.add_widget(property_report_layout)

        # Owners report
        owners_report_layout = BoxLayout(orientation='vertical', spacing=dp(10))
        owners_report_layout.add_widget(RTLLabel(
            text='تقرير الملاك',
            font_size='16sp',
            bold=True
        ))
        owners_report_layout.add_widget(RTLLabel(
            text='قائمة بجميع الملاك وعقاراتهم',
            font_size='12sp'
        ))
        owners_report_btn = ActionButton(
            text='إنشاء التقرير',
            action=self.generate_owners_report
        )
        owners_report_layout.add_widget(owners_report_btn)
        reports_grid.add_widget(owners_report_layout)

        # Property types report
        types_report_layout = BoxLayout(orientation='vertical', spacing=dp(10))
        types_report_layout.add_widget(RTLLabel(
            text='تقرير أنواع العقارات',
            font_size='16sp',
            bold=True
        ))
        types_report_layout.add_widget(RTLLabel(
            text='توزيع العقارات حسب النوع',
            font_size='12sp'
        ))
        types_report_btn = ActionButton(
            text='إنشاء التقرير',
            action=self.generate_types_report
        )
        types_report_layout.add_widget(types_report_btn)
        reports_grid.add_widget(types_report_layout)

        # Provinces report
        provinces_report_layout = BoxLayout(orientation='vertical', spacing=dp(10))
        provinces_report_layout.add_widget(RTLLabel(
            text='تقرير المحافظات',
            font_size='16sp',
            bold=True
        ))
        provinces_report_layout.add_widget(RTLLabel(
            text='توزيع العقارات حسب المحافظة',
            font_size='12sp'
        ))
        provinces_report_btn = ActionButton(
            text='إنشاء التقرير',
            action=self.generate_provinces_report
        )
        provinces_report_layout.add_widget(provinces_report_btn)
        reports_grid.add_widget(provinces_report_layout)

        layout.add_widget(reports_grid)

        # Custom report section
        layout.add_widget(RTLLabel(
            text='تقرير مخصص',
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height=dp(40)
        ))

        custom_layout = BoxLayout(orientation='horizontal', spacing=dp(10),
                                 size_hint_y=None, height=dp(60))

        custom_layout.add_widget(RTLLabel(
            text='اختر نوع التقرير:',
            size_hint_x=0.3
        ))

        self.custom_report_spinner = Spinner(
            text='اختر...',
            values=['عقارات للبيع', 'عقارات للإيجار', 'عقارات حسب المالك', 'عقارات حسب المساحة'],
            size_hint_x=0.4,
            font_name=font_manager.get_font_name('اختر...')
        )
        custom_layout.add_widget(self.custom_report_spinner)

        custom_report_btn = ActionButton(
            text='إنشاء',
            size_hint_x=0.3,
            action=self.generate_custom_report
        )
        custom_layout.add_widget(custom_report_btn)

        layout.add_widget(custom_layout)

        return layout

    def build_statistics_tab(self):
        """Build statistics tab content"""
        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))

        layout.add_widget(RTLLabel(
            text='إحصائيات النظام',
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(40)
        ))

        # Statistics container
        self.stats_scroll = ScrollView()
        self.stats_container = BoxLayout(orientation='vertical', spacing=dp(20),
                                        size_hint_y=None)
        self.stats_container.bind(minimum_height=self.stats_container.setter('height'))

        self.stats_scroll.add_widget(self.stats_container)
        layout.add_widget(self.stats_scroll)

        # Refresh button
        refresh_btn = ActionButton(
            text='تحديث الإحصائيات',
            action=self.refresh_statistics,
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(refresh_btn)

        # Load initial statistics
        self.refresh_statistics()

        return layout

    def perform_search(self):
        """Perform advanced search"""
        try:
            # Build filters from form
            filters = {}

            # Property type
            if self.search_type_field.get_value() != 'كل الأنواع':
                property_types = self.db.get_property_types()
                for pt in property_types:
                    if pt[1] == self.search_type_field.get_value():
                        filters['property_type'] = pt[0]
                        break

            # Offer type
            if self.search_offer_field.get_value() != 'كل العروض':
                offer_types = self.db.get_offer_types()
                for ot in offer_types:
                    if ot[1] == self.search_offer_field.get_value():
                        filters['offer_type'] = ot[0]
                        break

            # Province
            if self.search_province_field.get_value() != 'كل المحافظات':
                provinces = self.db.get_provinces()
                for p in provinces:
                    if p[1] == self.search_province_field.get_value():
                        filters['province_code'] = p[0]
                        break

            # Owner
            if self.search_owner_field.get_value() != 'كل الملاك':
                owner_text = self.search_owner_field.get_value()
                if '(' in owner_text:
                    owner_code = owner_text.split('(')[-1].replace(')', '')
                    filters['owner_code'] = owner_code

            # Get properties with filters
            properties = self.db.get_properties(filters)

            # Apply additional filters (area, address)
            filtered_properties = []
            for prop in properties:
                # Area filter
                prop_area = float(prop.get('Property-area', 0))
                min_area = self.min_area_input.text
                max_area = self.max_area_input.text

                if min_area:
                    try:
                        if prop_area < float(min_area):
                            continue
                    except ValueError:
                        pass

                if max_area:
                    try:
                        if prop_area > float(max_area):
                            continue
                    except ValueError:
                        pass

                # Address filter
                address_search = self.search_address_field.get_value().lower()
                if address_search:
                    property_address = prop.get('Property-address', '').lower()
                    if address_search not in property_address:
                        continue

                # Add reference names
                processed_prop = self._add_reference_names(prop)
                filtered_properties.append(processed_prop)

            self.search_results = filtered_properties
            self.search_results_table.update_data(filtered_properties)

            # Update results label
            self.results_label.text = f'نتائج البحث ({len(filtered_properties)} عقار)'

        except Exception as e:
            logger.error(f"Error performing search: {e}")
            self.show_message('خطأ', f'خطأ في البحث: {str(e)}', 'error')

    def _add_reference_names(self, property_data: dict) -> dict:
        """Add reference names to property data"""
        processed = dict(property_data)

        # Property type name
        property_types = self.db.get_property_types()
        for pt in property_types:
            if pt[0] == property_data.get('Rstatetcode'):
                processed['property_type_name'] = pt[1]
                break
        else:
            processed['property_type_name'] = 'غير محدد'

        # Offer type name
        offer_types = self.db.get_offer_types()
        for ot in offer_types:
            if ot[0] == property_data.get('Offer-Type-Code'):
                processed['offer_type_name'] = ot[1]
                break
        else:
            processed['offer_type_name'] = 'غير محدد'

        # Province name
        provinces = self.db.get_provinces()
        for p in provinces:
            if p[0] == property_data.get('Province-code'):
                processed['province_name'] = p[1]
                break
        else:
            processed['province_name'] = 'غير محدد'

        return processed

    def clear_search_filters(self):
        """Clear all search filters"""
        # Reset spinner fields
        spinners = [
            self.search_type_field,
            self.search_offer_field,
            self.search_province_field,
            self.search_owner_field
        ]

        for spinner in spinners:
            spinner.input.text = spinner.input.values[0]

        # Clear text inputs
        self.min_area_input.text = ''
        self.max_area_input.text = ''
        self.search_address_field.clear()

        # Clear results
        self.search_results = []
        self.search_results_table.update_data([])
        self.results_label.text = 'نتائج البحث'

    def view_property_details(self, property_data: dict):
        """View property details"""
        try:
            # Create property details popup
            details_popup = Popup(
                title='تفاصيل العقار',
                size_hint=(0.8, 0.9)
            )

            content = ScrollView()
            details_layout = BoxLayout(orientation='vertical', spacing=dp(10),
                                     size_hint_y=None, padding=dp(20))
            details_layout.bind(minimum_height=details_layout.setter('height'))

            # Property details
            details_items = [
                ('كود الشركة', property_data.get('Companyco', '')),
                ('كود العقار', property_data.get('realstatecode', '')),
                ('نوع العقار', property_data.get('property_type_name', '')),
                ('سنة البناء', property_data.get('Yearmake', '')),
                ('المساحة', f"{property_data.get('Property-area', 0)} م²"),
                ('الواجهة', f"{property_data.get('Property-facade', 0)} م"),
                ('العمق', f"{property_data.get('Property-depth', 0)} م"),
                ('غرف النوم', property_data.get('N-of-bedrooms', 0)),
                ('دورات المياه', property_data.get('N-of bathrooms', 0)),
                ('عقار زاوية', property_data.get('Property-corner', '')),
                ('نوع العرض', property_data.get('offer_type_name', '')),
                ('المحافظة', property_data.get('province_name', '')),
                ('العنوان', property_data.get('Property-address', '')),
                ('المالك', property_data.get('ownername', '')),
                ('الوصف', property_data.get('Descriptions', ''))
            ]

            for label, value in details_items:
                item_layout = BoxLayout(orientation='horizontal', spacing=dp(10),
                                      size_hint_y=None, height=dp(30))

                item_layout.add_widget(RTLLabel(
                    text=f"{label}:",
                    size_hint_x=0.3,
                    bold=True
                ))

                item_layout.add_widget(RTLLabel(
                    text=str(value),
                    size_hint_x=0.7
                ))

                details_layout.add_widget(item_layout)

            content.add_widget(details_layout)

            # Popup content
            popup_content = BoxLayout(orientation='vertical', spacing=dp(10))
            popup_content.add_widget(content)

            # Close button
            close_btn = ActionButton(
                text='إغلاق',
                action=details_popup.dismiss,
                size_hint_y=None,
                height=dp(40)
            )
            popup_content.add_widget(close_btn)

            details_popup.content = popup_content
            details_popup.open()

        except Exception as e:
            logger.error(f"Error viewing property details: {e}")
            self.show_message('خطأ', f'خطأ في عرض التفاصيل: {str(e)}', 'error')

    def export_results(self):
        """Export search results"""
        if not self.search_results:
            self.show_message('تنبيه', 'لا توجد نتائج للتصدير', 'warning')
            return

        try:
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'search_results_{timestamp}.txt'

            # Export data
            if ExportUtils.export_to_text(self.search_results, filename, 'نتائج البحث'):
                self.show_message('نجح', f'تم تصدير النتائج إلى: {filename}', 'success')
            else:
                self.show_message('خطأ', 'فشل في تصدير النتائج', 'error')

        except Exception as e:
            logger.error(f"Error exporting results: {e}")
            self.show_message('خطأ', f'خطأ في التصدير: {str(e)}', 'error')

    def generate_property_report(self):
        """Generate property summary report"""
        try:
            properties = self.db.get_properties()
            if not properties:
                self.show_message('تنبيه', 'لا توجد عقارات لإنشاء التقرير', 'warning')
                return

            # Add reference names
            processed_properties = [self._add_reference_names(prop) for prop in properties]

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'property_report_{timestamp}.txt'

            if ExportUtils.export_to_text(processed_properties, filename, 'تقرير ملخص العقارات'):
                self.show_message('نجح', f'تم إنشاء التقرير: {filename}', 'success')
            else:
                self.show_message('خطأ', 'فشل في إنشاء التقرير', 'error')

        except Exception as e:
            logger.error(f"Error generating property report: {e}")
            self.show_message('خطأ', f'خطأ في إنشاء التقرير: {str(e)}', 'error')

    def generate_owners_report(self):
        """Generate owners report"""
        try:
            owners = self.db.get_owners()
            if not owners:
                self.show_message('تنبيه', 'لا توجد ملاك لإنشاء التقرير', 'warning')
                return

            # Convert to dict format
            owners_data = [{
                'كود المالك': owner[0],
                'اسم المالك': owner[1],
                'رقم الهاتف': owner[2] or '',
                'ملاحظات': owner[3] or ''
            } for owner in owners]

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'owners_report_{timestamp}.txt'

            if ExportUtils.export_to_text(owners_data, filename, 'تقرير الملاك'):
                self.show_message('نجح', f'تم إنشاء التقرير: {filename}', 'success')
            else:
                self.show_message('خطأ', 'فشل في إنشاء التقرير', 'error')

        except Exception as e:
            logger.error(f"Error generating owners report: {e}")
            self.show_message('خطأ', f'خطأ في إنشاء التقرير: {str(e)}', 'error')

    def generate_types_report(self):
        """Generate property types report"""
        try:
            stats = self.db.get_statistics()
            types_data = stats.get('properties_by_type', [])

            if not types_data:
                self.show_message('تنبيه', 'لا توجد بيانات لإنشاء التقرير', 'warning')
                return

            # Convert to dict format
            report_data = [{
                'كود النوع': item[0] or 'غير محدد',
                'نوع العقار': item[1] or 'غير محدد',
                'عدد العقارات': item[2]
            } for item in types_data]

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'types_report_{timestamp}.txt'

            if ExportUtils.export_to_text(report_data, filename, 'تقرير أنواع العقارات'):
                self.show_message('نجح', f'تم إنشاء التقرير: {filename}', 'success')
            else:
                self.show_message('خطأ', 'فشل في إنشاء التقرير', 'error')

        except Exception as e:
            logger.error(f"Error generating types report: {e}")
            self.show_message('خطأ', f'خطأ في إنشاء التقرير: {str(e)}', 'error')

    def generate_provinces_report(self):
        """Generate provinces report"""
        try:
            stats = self.db.get_statistics()
            provinces_data = stats.get('properties_by_province', [])

            if not provinces_data:
                self.show_message('تنبيه', 'لا توجد بيانات لإنشاء التقرير', 'warning')
                return

            # Convert to dict format
            report_data = [{
                'كود المحافظة': item[0] or 'غير محدد',
                'اسم المحافظة': item[1] or 'غير محدد',
                'عدد العقارات': item[2]
            } for item in provinces_data]

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'provinces_report_{timestamp}.txt'

            if ExportUtils.export_to_text(report_data, filename, 'تقرير المحافظات'):
                self.show_message('نجح', f'تم إنشاء التقرير: {filename}', 'success')
            else:
                self.show_message('خطأ', 'فشل في إنشاء التقرير', 'error')

        except Exception as e:
            logger.error(f"Error generating provinces report: {e}")
            self.show_message('خطأ', f'خطأ في إنشاء التقرير: {str(e)}', 'error')

    def generate_custom_report(self):
        """Generate custom report"""
        report_type = self.custom_report_spinner.text

        if report_type == 'اختر...':
            self.show_message('تنبيه', 'يرجى اختيار نوع التقرير', 'warning')
            return

        try:
            if report_type == 'عقارات للبيع':
                filters = {'offer_type': '03001'}
            elif report_type == 'عقارات للإيجار':
                filters = {'offer_type': '03002'}
            else:
                self.show_message('معلومات', 'نوع التقرير قيد التطوير', 'info')
                return

            properties = self.db.get_properties(filters)
            processed_properties = [self._add_reference_names(prop) for prop in properties]

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'custom_report_{timestamp}.txt'

            if ExportUtils.export_to_text(processed_properties, filename, f'تقرير مخصص - {report_type}'):
                self.show_message('نجح', f'تم إنشاء التقرير: {filename}', 'success')
            else:
                self.show_message('خطأ', 'فشل في إنشاء التقرير', 'error')

        except Exception as e:
            logger.error(f"Error generating custom report: {e}")
            self.show_message('خطأ', f'خطأ في إنشاء التقرير: {str(e)}', 'error')

    def refresh_statistics(self):
        """Refresh statistics display"""
        try:
            stats = self.db.get_statistics()

            # Clear existing stats
            self.stats_container.clear_widgets()

            # Overall statistics
            overall_layout = BoxLayout(orientation='vertical', spacing=dp(10),
                                     size_hint_y=None, height=dp(150))

            overall_layout.add_widget(RTLLabel(
                text='إحصائيات عامة',
                font_size='18sp',
                bold=True,
                size_hint_y=None,
                height=dp(30)
            ))

            stats_grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(120))

            # Stats cards
            overall_stats = [
                ('إجمالي الملاك', str(stats.get('total_owners', 0)), [0.2, 0.7, 0.3, 1]),
                ('إجمالي العقارات', str(stats.get('total_properties', 0)), [0.2, 0.4, 0.8, 1])
            ]

            for title, value, color in overall_stats:
                card = StatsCard(title=title, value=value, color=color)
                stats_grid.add_widget(card)

            overall_layout.add_widget(stats_grid)
            self.stats_container.add_widget(overall_layout)

            # Property types statistics
            if stats.get('properties_by_type'):
                types_layout = self._create_stats_section(
                    'توزيع العقارات حسب النوع',
                    stats['properties_by_type']
                )
                self.stats_container.add_widget(types_layout)

            # Offer types statistics
            if stats.get('properties_by_offer'):
                offers_layout = self._create_stats_section(
                    'توزيع العقارات حسب نوع العرض',
                    stats['properties_by_offer']
                )
                self.stats_container.add_widget(offers_layout)

            # Provinces statistics
            if stats.get('properties_by_province'):
                provinces_layout = self._create_stats_section(
                    'توزيع العقارات حسب المحافظة',
                    stats['properties_by_province'][:5]  # Top 5 provinces
                )
                self.stats_container.add_widget(provinces_layout)

        except Exception as e:
            logger.error(f"Error refreshing statistics: {e}")
            self.show_message('خطأ', f'خطأ في تحديث الإحصائيات: {str(e)}', 'error')

    def _create_stats_section(self, title: str, data: list) -> BoxLayout:
        """Create statistics section"""
        section_layout = BoxLayout(orientation='vertical', spacing=dp(10),
                                  size_hint_y=None)

        # Title
        section_layout.add_widget(RTLLabel(
            text=title,
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height=dp(30)
        ))

        # Data
        data_layout = BoxLayout(orientation='vertical', spacing=dp(5),
                               size_hint_y=None)

        for item in data:
            code, name, count = item

            item_layout = BoxLayout(orientation='horizontal', spacing=dp(10),
                                   size_hint_y=None, height=dp(25))

            item_layout.add_widget(RTLLabel(
                text=name or 'غير محدد',
                size_hint_x=0.7
            ))

            item_layout.add_widget(RTLLabel(
                text=str(count),
                size_hint_x=0.3,
                bold=True
            ))

            data_layout.add_widget(item_layout)

        data_layout.bind(minimum_height=data_layout.setter('height'))
        section_layout.add_widget(data_layout)
        section_layout.bind(minimum_height=section_layout.setter('height'))

        return section_layout

    def show_message(self, title: str, message: str, msg_type: str = 'info'):
        """Show message dialog"""
        dialog = MessageDialog(title=title, message=message, message_type=msg_type)
        dialog.open()

    def go_back(self):
        """Go back to dashboard"""
        self.manager.current = 'dashboard'

    def on_enter(self, *args):
        """Called when screen is entered"""
        # Refresh data when entering screen
        self.refresh_statistics()
