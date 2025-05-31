#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Enhanced Properties Management with KivyMD
Beautiful, modern properties management interface with Material Design components
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton, MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import MDList, ThreeLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.chip import MDChip
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.animation import Animation
import logging

from app.views.modern_components import (
    DesignTokens, ModernCard, StatsCard, ModernTextField, ModernButton,
    ModernDataTable, PropertyCard, OwnerCard, ModernDialog, ModernSnackbar,
    LoadingSpinner, EmptyState, EnhancedStatsCard, ModernSearchBar,
    ModernActionBar, ModernListItem, ModernGridView, ModernFormCard
)
from app.database import DatabaseManager
from app.language_manager import language_manager
from app.views.enhanced_dialogs import ConfirmationDialog

logger = logging.getLogger(__name__)

class EnhancedPropertiesScreen(MDScreen):
    """Enhanced Properties Management Screen with KivyMD components"""

    def __init__(self, db_manager: DatabaseManager, **kwargs):
        super().__init__(**kwargs)
        self.name = 'enhanced_properties'
        self.db = db_manager
        self.current_property = None
        self.properties_data = []
        self.owners_data = []

        # UI State
        self.is_loading = False
        self.current_view = 'grid'  # 'grid' or 'table'
        self.sort_field = 'location'
        self.sort_order = 'asc'
        self.selected_properties = []
        self.filtered_properties = []

        self.build_ui()
        self.load_data()

    def build_ui(self):
        """Build the enhanced properties management UI with modern components"""
        # Main layout with modern spacing
        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['medium'],
            padding=DesignTokens.SPACING['large']
        )

        # Header with stats
        self.build_header(main_layout)

        # Search and filters
        self.build_search_section(main_layout)

        # Action bar
        self.build_action_bar(main_layout)

        # Content area (form + properties list/grid)
        content_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['large']
        )

        # Left panel - Property form
        self.build_form_panel(content_layout)

        # Right panel - Properties display
        self.build_properties_panel(content_layout)

        main_layout.add_widget(content_layout)
        self.add_widget(main_layout)

    def build_header(self, parent_layout):
        """Build header with statistics cards"""
        header_card = ModernCard(size_hint_y=None, height=dp(120))
        header_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['medium'],
            padding=DesignTokens.SPACING['medium']
        )

        # Statistics
        total_properties = len(self.properties_data)
        available_count = len([p for p in self.properties_data if p.get('status') == 'Available'])
        sold_count = len([p for p in self.properties_data if p.get('status') == 'Sold'])
        rented_count = len([p for p in self.properties_data if p.get('status') == 'Rented'])

        stats = [
            {'title': 'Total Properties', 'value': str(total_properties), 'icon': 'home-group'},
            {'title': 'Available', 'value': str(available_count), 'icon': 'home-plus', 'md_bg_color': DesignTokens.COLORS['success']},
            {'title': 'Sold', 'value': str(sold_count), 'icon': 'home-check', 'md_bg_color': DesignTokens.COLORS['warning']},
            {'title': 'Rented', 'value': str(rented_count), 'icon': 'home-heart', 'md_bg_color': DesignTokens.COLORS['info']}
        ]

        for stat in stats:
            stat_card = EnhancedStatsCard(
                title=stat['title'],
                value=stat['value'],
                icon=stat['icon'],
                md_bg_color=stat.get('md_bg_color', DesignTokens.COLORS['primary']),
                size_hint_x=0.25
            )
            header_layout.add_widget(stat_card)

        header_card.add_widget(header_layout)
        parent_layout.add_widget(header_card)

    def build_search_section(self, parent_layout):
        """Build search and filter section"""
        search_card = ModernCard(size_hint_y=None, height=dp(80))
        search_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['medium'],
            padding=DesignTokens.SPACING['medium']
        )

        # Search bar
        self.search_bar = ModernSearchBar(
            placeholder="Search properties...",
            on_search=self.on_search,
            size_hint_x=0.6
        )
        search_layout.add_widget(self.search_bar)

        # Filter buttons
        filter_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['small'],
            size_hint_x=0.4
        )

        # Status filter
        self.status_filter_button = MDFlatButton(
            text="All Status",
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['primary']
        )
        self.status_filter_button.bind(on_release=self.show_status_filter_menu)
        filter_layout.add_widget(self.status_filter_button)

        # Type filter
        self.type_filter_button = MDFlatButton(
            text="All Types",
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['primary']
        )
        self.type_filter_button.bind(on_release=self.show_type_filter_menu)
        filter_layout.add_widget(self.type_filter_button)

        # View toggle
        self.view_toggle_button = MDIconButton(
            icon="view-grid",
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['primary']
        )
        self.view_toggle_button.bind(on_release=self.toggle_view)
        filter_layout.add_widget(self.view_toggle_button)

        search_layout.add_widget(filter_layout)
        search_card.add_widget(search_layout)
        parent_layout.add_widget(search_card)

    def build_action_bar(self, parent_layout):
        """Build action bar with property management actions"""
        actions = [
            {
                'type': 'raised',
                'text': 'Add Property',
                'color': DesignTokens.COLORS['primary'],
                'callback': self.add_new_property
            },
            {
                'type': 'flat',
                'text': 'Import',
                'color': DesignTokens.COLORS['secondary'],
                'callback': self.import_properties
            },
            {
                'type': 'flat',
                'text': 'Export',
                'color': DesignTokens.COLORS['secondary'],
                'callback': self.export_properties
            },
            {
                'type': 'icon',
                'icon': 'delete',
                'color': DesignTokens.COLORS['error'],
                'callback': self.delete_selected_properties
            }
        ]

        self.action_bar = ModernActionBar(actions=actions)
        parent_layout.add_widget(self.action_bar)

    def build_form_panel(self, parent_layout):
        """Build property form panel"""
        form_fields = [
            {'name': 'location', 'type': 'text', 'hint': 'Property Location', 'required': True},
            {'name': 'propertytype', 'type': 'dropdown', 'hint': 'Property Type', 'required': True},
            {'name': 'area', 'type': 'text', 'hint': 'Area (m²)', 'required': True},
            {'name': 'price', 'type': 'text', 'hint': 'Price', 'required': True},
            {'name': 'status', 'type': 'dropdown', 'hint': 'Status', 'required': True},
            {'name': 'description', 'type': 'text', 'hint': 'Description'},
            {'name': 'features', 'type': 'text', 'hint': 'Features'},
            {'name': 'is_furnished', 'type': 'switch', 'label': 'Furnished'},
            {'name': 'has_parking', 'type': 'switch', 'label': 'Parking Available'}
        ]

        self.form_card = ModernFormCard(
            title="Property Information",
            fields=form_fields,
            size_hint_x=0.4
        )

        # Add photo upload section
        photo_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['small'],
            size_hint_y=None,
            height=dp(120)
        )

        photo_button = MDRaisedButton(
            text="Upload Photos",
            md_bg_color=DesignTokens.COLORS['secondary'],
            size_hint_y=None,
            height=dp(40)
        )
        photo_button.bind(on_release=self.upload_photos)
        photo_layout.add_widget(photo_button)

        # Photo preview area
        self.photo_preview = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['small'],
            size_hint_y=None,
            height=dp(60)
        )
        photo_layout.add_widget(self.photo_preview)

        # Form buttons
        button_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['medium'],
            size_hint_y=None,
            height=dp(50)
        )

        save_button = MDRaisedButton(
            text="Save Property",
            md_bg_color=DesignTokens.COLORS['primary']
        )
        save_button.bind(on_release=self.save_property)
        button_layout.add_widget(save_button)

        clear_button = MDFlatButton(
            text="Clear Form",
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_secondary']
        )
        clear_button.bind(on_release=self.clear_form)
        button_layout.add_widget(clear_button)

        # Combine form elements
        form_container = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['medium']
        )
        form_container.add_widget(self.form_card)
        form_container.add_widget(photo_layout)
        form_container.add_widget(button_layout)

        parent_layout.add_widget(form_container)

    def build_properties_panel(self, parent_layout):
        """Build properties display panel"""
        self.properties_container = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['medium'],
            size_hint_x=0.6
        )

        # Loading spinner
        self.loading_spinner = LoadingSpinner()
        self.loading_spinner.size_hint = (None, None)
        self.loading_spinner.size = (dp(50), dp(50))
        self.loading_spinner.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Empty state
        self.empty_state = EmptyState(
            icon="home-search",
            title="No Properties Found",
            subtitle="Add your first property to get started"
        )

        # Grid view for properties
        self.properties_grid = ModernGridView(cols=2)

        # Table view for properties
        self.properties_table = ModernDataTable(
            column_data=[
                ("Location", dp(150)),
                ("Type", dp(100)),
                ("Area", dp(80)),
                ("Price", dp(120)),
                ("Status", dp(100)),
                ("Actions", dp(100))
            ]
        )

        # Initially show grid view
        self.properties_container.add_widget(self.properties_grid)
        parent_layout.add_widget(self.properties_container)

    # Modern interaction methods
    def on_search(self, instance):
        """Handle search input"""
        search_text = self.search_bar.get_text().lower()

        if not search_text:
            self.filtered_properties = self.properties_data.copy()
        else:
            self.filtered_properties = [
                prop for prop in self.properties_data
                if search_text in prop.get('location', '').lower() or
                   search_text in prop.get('propertytype', '').lower() or
                   search_text in prop.get('status', '').lower()
            ]

        self.update_properties_display()

    def toggle_view(self, instance):
        """Toggle between grid and table view"""
        if self.current_view == 'grid':
            self.current_view = 'table'
            self.view_toggle_button.icon = "view-list"
        else:
            self.current_view = 'grid'
            self.view_toggle_button.icon = "view-grid"

        self.update_properties_display()

    def update_properties_display(self):
        """Update the properties display based on current view"""
        if self.current_view == 'grid':
            self.update_grid_view()
        else:
            self.update_table_view()

    def update_grid_view(self):
        """Update grid view with property cards"""
        self.properties_grid.clear_items()

        if not self.filtered_properties:
            self.properties_container.clear_widgets()
            self.properties_container.add_widget(self.empty_state)
            return

        # Ensure grid is in container
        if self.properties_grid not in self.properties_container.children:
            self.properties_container.clear_widgets()
            self.properties_container.add_widget(self.properties_grid)

        for property_data in self.filtered_properties:
            property_card = PropertyCard(
                property_data=property_data,
                on_edit=lambda x, prop=property_data: self.edit_property(prop),
                on_delete=lambda x, prop=property_data: self.delete_property(prop)
            )
            self.properties_grid.add_item(property_card)

    def update_table_view(self):
        """Update table view with property data"""
        if self.properties_table not in self.properties_container.children:
            self.properties_container.clear_widgets()
            self.properties_container.add_widget(self.properties_table)

        # Convert property data to table rows
        table_data = []
        for prop in self.filtered_properties:
            row = [
                prop.get('location', ''),
                prop.get('propertytype', ''),
                f"{prop.get('area', '')} m²",
                f"${prop.get('price', 0):,}",
                prop.get('status', ''),
                "Edit | Delete"  # Action buttons would be handled by table
            ]
            table_data.append(row)

        self.properties_table.update_data(table_data)

    def add_new_property(self, instance):
        """Add new property"""
        self.current_property = None
        self.clear_form(None)

    def edit_property(self, property_data):
        """Edit existing property"""
        self.current_property = property_data
        self.populate_form(property_data)

    def save_property(self, instance):
        """Save property to database"""
        # Validate form
        errors = self.form_card.validate_form()
        if errors:
            self.show_error_snackbar(f"Please fix errors: {', '.join(errors)}")
            return

        # Collect form data
        property_data = {}
        for field_name in ['location', 'propertytype', 'area', 'price', 'status', 'description', 'features']:
            property_data[field_name] = self.form_card.get_field_value(field_name)

        property_data['is_furnished'] = self.form_card.get_field_value('is_furnished')
        property_data['has_parking'] = self.form_card.get_field_value('has_parking')

        try:
            if self.current_property:
                # Update existing property
                property_data['id'] = self.current_property['id']
                self.db.update_property(property_data)
                self.show_success_snackbar("Property updated successfully")
            else:
                # Add new property
                property_data['company_code'] = self.db.generate_company_code()
                property_data['realstate_code'] = self.db.generate_realstate_code()
                self.db.add_property(property_data)
                self.show_success_snackbar("Property added successfully")

            self.load_data()
            self.clear_form(None)

        except Exception as e:
            logger.error(f"Error saving property: {e}")
            self.show_error_snackbar("Failed to save property")

    def delete_property(self, property_data):
        """Delete property with confirmation"""
        def confirm_delete(instance):
            try:
                self.db.delete_property(property_data['id'])
                self.show_success_snackbar("Property deleted successfully")
                self.load_data()
                dialog.dismiss()
            except Exception as e:
                logger.error(f"Error deleting property: {e}")
                self.show_error_snackbar("Failed to delete property")

        dialog = ModernDialog(
            title="Delete Property",
            text=f"Are you sure you want to delete the property at {property_data.get('location', 'Unknown')}?",
            buttons=[
                {"text": "Cancel", "action": lambda x: dialog.dismiss()},
                {"text": "Delete", "action": confirm_delete, "style": "error"}
            ]
        )
        dialog.open()

    def clear_form(self, instance):
        """Clear form fields"""
        for field_name in self.form_card.form_fields.keys():
            self.form_card.set_field_value(field_name, "")
        self.current_property = None

    def populate_form(self, property_data):
        """Populate form with property data"""
        for field_name, value in property_data.items():
            if field_name in self.form_card.form_fields:
                self.form_card.set_field_value(field_name, value)

    def upload_photos(self, instance):
        """Upload photos for property"""
        # Implement photo upload using file manager
        pass

    def show_status_filter_menu(self, instance):
        """Show status filter menu"""
        # Implement status filter dropdown
        pass

    def show_type_filter_menu(self, instance):
        """Show type filter menu"""
        # Implement type filter dropdown
        pass

    def import_properties(self, instance):
        """Import properties from file"""
        # Implement import functionality
        pass

    def export_properties(self, instance):
        """Export properties to file"""
        # Implement export functionality
        pass

    def delete_selected_properties(self, instance):
        """Delete selected properties"""
        # Implement bulk delete
        pass

    def show_success_snackbar(self, message: str):
        """Show success snackbar"""
        snackbar = Snackbar(text=message)
        snackbar.bg_color = DesignTokens.COLORS['success']
        snackbar.open()

    def show_error_snackbar(self, message: str):
        """Show error snackbar"""
        snackbar = Snackbar(text=message)
        snackbar.bg_color = DesignTokens.COLORS['error']
        snackbar.open()

    # Keep existing methods for compatibility

    def load_data(self):
        """Load properties and owners data from database"""
        try:
            self.properties_data = self.db.get_all_properties()
            self.owners_data = self.db.get_all_owners()
            self.filtered_properties = self.properties_data.copy()

            Clock.schedule_once(lambda dt: self.update_properties_display(), 0.1)
            Clock.schedule_once(lambda dt: self.update_header_stats(), 0.1)

        except Exception as e:
            logger.error(f"Error loading data: {e}")
            self.show_error_snackbar("Failed to load data")

    def update_header_stats(self):
        """Update header statistics - rebuild header with new stats"""
        # This is called after data changes to refresh statistics
        if hasattr(self, 'properties_container'):
            # We'll rebuild the header when we get the updated data
            pass

    def refresh_data(self):
        """Refresh all data from database"""
        self.load_data()

    def go_back(self):
        """Navigate back to dashboard"""
        if self.manager:
            self.manager.current = 'enhanced_dashboard'

    def toggle_search(self):
        """Toggle search visibility"""
        # Search is always visible in modern design
        pass

    def manage_photos(self):
        """Open photo management"""
        self.upload_photos(None)

    def show_loading(self, show: bool):
        """Show or hide loading spinner"""
        self.is_loading = show

        if show:
            self.properties_container.clear_widgets()
            self.properties_container.add_widget(self.loading_spinner)
        else:
            self.properties_container.clear_widgets()
            self.update_properties_display()
