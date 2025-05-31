#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Enhanced UI Example
Example implementation showing how to use the new enhanced components
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
import logging

from app.views.enhanced_forms import EnhancedFormCard
from app.views.enhanced_table import EnhancedDataTable
from app.views.enhanced_dashboard import EnhancedDashboardScreen
from app.views.modern_components import DesignTokens, EnhancedStatsCard, ModernNavigationCard
from app.language_manager import language_manager

logger = logging.getLogger(__name__)


class EnhancedOwnersScreen(MDScreen):
    """Example of enhanced owners screen using new components"""

    def __init__(self, db_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.name = 'enhanced_owners'
        self.db = db_manager

        self.build_ui()

    def build_ui(self):
        """Build UI using enhanced components"""
        # Main container
        main_layout = MDBoxLayout(
            orientation='vertical',
            md_bg_color=DesignTokens.COLORS['background'],
            spacing=DesignTokens.SPACING['md'],
            padding=DesignTokens.SPACING['md']
        )

        # Scrollable content
        scroll = MDScrollView()
        content = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['lg'],
            adaptive_height=True
        )

        # Left panel - Form
        self.build_form_panel(content)

        # Right panel - Data table
        self.build_table_panel(content)

        scroll.add_widget(content)
        main_layout.add_widget(scroll)

        self.add_widget(main_layout)

    def build_form_panel(self, parent):
        """Build form panel with enhanced form"""
        form_fields = [
            {
                'label': language_manager.get_text('owner_code'),
                'field_type': 'text',
                'required': True
            },
            {
                'label': language_manager.get_text('owner_name'),
                'field_type': 'text',
                'required': True
            },
            {
                'label': language_manager.get_text('phone'),
                'field_type': 'text',
                'validation_rules': ['phone']
            },
            {
                'label': language_manager.get_text('email'),
                'field_type': 'email'
            },
            {
                'label': language_manager.get_text('notes'),
                'field_type': 'multiline'
            },
            {
                'label': language_manager.get_text('active'),
                'field_type': 'switch'
            }
        ]

        self.form_card = EnhancedFormCard(
            title=language_manager.get_text('owner_information'),
            fields=form_fields,
            on_submit=self.on_form_submit,
            size_hint_x=0.4
        )

        parent.add_widget(self.form_card)

    def build_table_panel(self, parent):
        """Build table panel with enhanced data table"""
        table_columns = [
            {
                'field': 'owner_code',
                'title': language_manager.get_text('owner_code'),
                'width': 0.2,
                'sortable': True
            },
            {
                'field': 'owner_name',
                'title': language_manager.get_text('owner_name'),
                'width': 0.3,
                'sortable': True
            },
            {
                'field': 'phone',
                'title': language_manager.get_text('phone'),
                'width': 0.25,
                'sortable': False
            },
            {
                'field': 'email',
                'title': language_manager.get_text('email'),
                'width': 0.25,
                'sortable': False
            }
        ]

        # Sample data - in real app this would come from database
        sample_data = [
            {
                'owner_code': 'OWN001',
                'owner_name': 'John Smith',
                'phone': '+1234567890',
                'email': 'john@example.com'
            },
            {
                'owner_code': 'OWN002',
                'owner_name': 'Jane Doe',
                'phone': '+1234567891',
                'email': 'jane@example.com'
            }
        ]

        self.data_table = EnhancedDataTable(
            columns=table_columns,
            data=sample_data,
            on_row_select=self.on_row_select,
            on_row_action=self.on_row_action,
            pagination=True,
            page_size=10,
            size_hint_x=0.6
        )

        parent.add_widget(self.data_table)

    def on_form_submit(self, form_data):
        """Handle form submission"""
        logger.info(f"Form submitted with data: {form_data}")

        # Here you would save to database
        if self.db:
            # self.db.add_owner(form_data)
            pass

        # Update table
        # self.refresh_table()

    def on_row_select(self, row_data, selected):
        """Handle row selection"""
        logger.info(f"Row {'selected' if selected else 'deselected'}: {row_data}")

        if selected:
            # Populate form with selected data
            self.form_card.populate_form(row_data)

    def on_row_action(self, action, row_data):
        """Handle row actions"""
        logger.info(f"Action '{action}' triggered for row: {row_data}")

        if action == 'edit':
            self.form_card.populate_form(row_data)
        elif action == 'delete':
            # Show confirmation dialog and delete
            pass


class EnhancedPropertiesScreen(MDScreen):
    """Example of enhanced properties screen"""

    def __init__(self, db_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.name = 'enhanced_properties'
        self.db = db_manager

        self.build_ui()

    def build_ui(self):
        """Build UI with property-specific components"""
        # Main container
        main_layout = MDBoxLayout(
            orientation='vertical',
            md_bg_color=DesignTokens.COLORS['background'],
            spacing=DesignTokens.SPACING['md'],
            padding=DesignTokens.SPACING['md']
        )

        # Stats cards row
        self.build_stats_row(main_layout)

        # Content area
        content_area = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['lg']
        )

        # Property form
        self.build_property_form(content_area)

        # Properties table
        self.build_properties_table(content_area)

        main_layout.add_widget(content_area)
        self.add_widget(main_layout)

    def build_stats_row(self, parent):
        """Build statistics row"""
        stats_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['md'],
            size_hint_y=None,
            height=dp(120)
        )

        # Sample stats
        stats = [
            {
                'title': language_manager.get_text('total_properties'),
                'value': '150',
                'icon': 'home-city',
                'color_scheme': 'primary'
            },
            {
                'title': language_manager.get_text('available_properties'),
                'value': '45',
                'icon': 'home-outline',
                'color_scheme': 'success'
            },
            {
                'title': language_manager.get_text('occupied_properties'),
                'value': '105',
                'icon': 'home',
                'color_scheme': 'warning'
            },
            {
                'title': language_manager.get_text('total_value'),
                'value': '$2.5M',
                'icon': 'currency-usd',
                'color_scheme': 'secondary'
            }
        ]

        for stat in stats:
            card = EnhancedStatsCard(
                title=stat['title'],
                value=stat['value'],
                icon=stat['icon'],
                color_scheme=stat['color_scheme']
            )
            stats_layout.add_widget(card)

        parent.add_widget(stats_layout)

    def build_property_form(self, parent):
        """Build property form"""
        form_fields = [
            {
                'label': language_manager.get_text('company_code'),
                'field_type': 'text',
                'required': True
            },
            {
                'label': language_manager.get_text('property_type'),
                'field_type': 'dropdown',
                'options': ['House', 'Apartment', 'Villa', 'Commercial'],
                'required': True
            },
            {
                'label': language_manager.get_text('property_area'),
                'field_type': 'number',
                'required': True
            },
            {
                'label': language_manager.get_text('address'),
                'field_type': 'multiline',
                'required': True
            },
            {
                'label': language_manager.get_text('bedrooms'),
                'field_type': 'number'
            },
            {
                'label': language_manager.get_text('bathrooms'),
                'field_type': 'number'
            },
            {
                'label': language_manager.get_text('available'),
                'field_type': 'switch'
            }
        ]

        self.property_form = EnhancedFormCard(
            title=language_manager.get_text('property_information'),
            fields=form_fields,
            on_submit=self.on_property_submit,
            size_hint_x=0.4
        )

        parent.add_widget(self.property_form)

    def build_properties_table(self, parent):
        """Build properties table"""
        table_columns = [
            {
                'field': 'company_code',
                'title': language_manager.get_text('company_code'),
                'width': 0.15
            },
            {
                'field': 'property_type',
                'title': language_manager.get_text('property_type'),
                'width': 0.2
            },
            {
                'field': 'area',
                'title': language_manager.get_text('area'),
                'width': 0.15
            },
            {
                'field': 'address',
                'title': language_manager.get_text('address'),
                'width': 0.3
            },
            {
                'field': 'status',
                'title': language_manager.get_text('status'),
                'width': 0.2
            }
        ]

        # Sample data
        sample_data = [
            {
                'company_code': 'PROP001',
                'property_type': 'House',
                'area': '250',
                'address': '123 Main Street, City Center',
                'status': 'Available'
            },
            {
                'company_code': 'PROP002',
                'property_type': 'Apartment',
                'area': '120',
                'address': '456 Oak Avenue, Downtown',
                'status': 'Occupied'
            }
        ]

        self.properties_table = EnhancedDataTable(
            columns=table_columns,
            data=sample_data,
            on_row_select=self.on_property_select,
            on_row_action=self.on_property_action,
            pagination=True,
            page_size=15,
            size_hint_x=0.6
        )

        parent.add_widget(self.properties_table)

    def on_property_submit(self, form_data):
        """Handle property form submission"""
        logger.info(f"Property form submitted: {form_data}")

    def on_property_select(self, row_data, selected):
        """Handle property selection"""
        if selected:
            self.property_form.populate_form(row_data)

    def on_property_action(self, action, row_data):
        """Handle property actions"""
        logger.info(f"Property action '{action}': {row_data}")


# Example of how to use enhanced dashboard
def create_enhanced_dashboard(db_manager):
    """Create enhanced dashboard screen"""
    return EnhancedDashboardScreen(db_manager=db_manager)


# Example of how to replace existing screens
def replace_with_enhanced_screens(screen_manager, db_manager):
    """Replace existing screens with enhanced versions"""

    # Remove old screens
    screens_to_remove = ['owners', 'properties', 'dashboard']
    for screen_name in screens_to_remove:
        if screen_manager.has_screen(screen_name):
            screen_manager.remove_widget(screen_manager.get_screen(screen_name))

    # Add enhanced screens
    enhanced_dashboard = EnhancedDashboardScreen(db_manager=db_manager, name='dashboard')
    enhanced_owners = EnhancedOwnersScreen(db_manager=db_manager, name='owners')
    enhanced_properties = EnhancedPropertiesScreen(db_manager=db_manager, name='properties')

    screen_manager.add_widget(enhanced_dashboard)
    screen_manager.add_widget(enhanced_owners)
    screen_manager.add_widget(enhanced_properties)
