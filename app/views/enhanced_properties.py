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
    ModernCard, EnhancedStatsCard, DesignTokens
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

        self.build_ui()
        self.load_data()

    def build_ui(self):
        """Build the enhanced properties management UI"""
        # Main layout
        main_layout = MDBoxLayout(orientation='vertical')

        # Top app bar
        self.build_top_bar(main_layout)

        # Content area
        content_scroll = MDScrollView()
        content_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            adaptive_height=True
        )

        # Statistics cards
        self.build_stats_section(content_layout)

        # Main content with form and list
        self.build_main_content(content_layout)

        content_scroll.add_widget(content_layout)
        main_layout.add_widget(content_scroll)

        # Floating action button
        self.build_fab(main_layout)

        self.add_widget(main_layout)

    def build_top_bar(self, parent):
        """Build the top navigation bar"""
        self.toolbar = MDTopAppBar(
            title=language_manager.get_text('manage_properties'),
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[
                ["refresh", lambda x: self.refresh_data()],
                ["magnify", lambda x: self.toggle_search()],
                ["camera", lambda x: self.manage_photos()]
            ],
            md_bg_color=DesignTokens.COLORS['primary'],
            specific_text_color=DesignTokens.COLORS['text_primary']
        )
        parent.add_widget(self.toolbar)

    def build_stats_section(self, parent):
        """Build statistics section"""
        stats_title = MDLabel(
            text=language_manager.get_text('properties_statistics'),
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_primary'],
            font_style="H5",
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        parent.add_widget(stats_title)

        # Stats grid
        self.stats_grid = MDGridLayout(
            cols=3,
            adaptive_height=True,
            spacing=dp(15),
            size_hint_y=None
        )

        self.update_stats_display()
        parent.add_widget(self.stats_grid)

    def build_main_content(self, parent):
        """Build main content with form and list"""
        # Content card
        content_card = ModernCard(
            orientation='horizontal',
            adaptive_height=True,
            padding=dp(20),
            spacing=dp(20)
        )

        # Left side - Form
        self.build_form_section(content_card)        # Divider
        from kivy.uix.widget import Widget
        divider = Widget(
            size_hint_x=None,
            width=dp(1)
        )
        content_card.add_widget(divider)

        # Right side - Properties list
        self.build_list_section(content_card)

        parent.add_widget(content_card)

    def build_form_section(self, parent):
        """Build the property form section"""
        form_scroll = MDScrollView(size_hint_x=0.45)
        form_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            adaptive_height=True,
            padding=[0, 0, dp(10), 0]
        )

        # Form title
        form_title = MDLabel(
            text=language_manager.get_text('property_information'),
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['primary'],
            font_style="H6",
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        form_layout.add_widget(form_title)

        # Basic Information Section
        self.build_basic_info_section(form_layout)

        # Property Details Section
        self.build_details_section(form_layout)

        # Location Section
        self.build_location_section(form_layout)

        # Action buttons
        self.build_action_buttons(form_layout)

        form_scroll.add_widget(form_layout)
        parent.add_widget(form_scroll)

    def build_basic_info_section(self, parent):
        """Build basic information section"""
        # Section header
        basic_header = MDLabel(
            text=language_manager.get_text('basic_information'),
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['secondary'],
            font_style="Subtitle1",
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )
        parent.add_widget(basic_header)

        # Company code (read-only)
        self.company_code_field = MDTextField(
            hint_text=language_manager.get_text('company_code'),
            readonly=True,
            icon_left="identifier",
            size_hint_y=None,
            height=dp(48)
        )
        parent.add_widget(self.company_code_field)

        # Real estate code
        self.realstate_code_field = MDTextField(
            hint_text=language_manager.get_text('realstate_code'),
            icon_left="home-outline",
            size_hint_y=None,
            height=dp(48)
        )
        parent.add_widget(self.realstate_code_field)

        # Property address
        self.address_field = MDTextField(
            hint_text=language_manager.get_text('property_address'),
            required=True,
            icon_left="map-marker",
            size_hint_y=None,
            height=dp(48)
        )
        parent.add_widget(self.address_field)

        # Property type dropdown (you can replace with actual dropdown)
        self.property_type_field = MDTextField(
            hint_text=language_manager.get_text('property_type'),
            icon_left="home-variant",
            size_hint_y=None,
            height=dp(48)
        )
        parent.add_widget(self.property_type_field)

    def build_details_section(self, parent):
        """Build property details section"""
        # Section header
        details_header = MDLabel(
            text=language_manager.get_text('property_details'),
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['secondary'],
            font_style="Subtitle1",
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )
        parent.add_widget(details_header)

        # Two-column layout for details
        details_grid = MDGridLayout(
            cols=2,
            adaptive_height=True,
            spacing=dp(10)
        )

        # Area
        self.area_field = MDTextField(
            hint_text=language_manager.get_text('area'),
            icon_left="ruler-square",
            input_type="number",
            size_hint_y=None,
            height=dp(48)
        )
        details_grid.add_widget(self.area_field)

        # Year make
        self.year_make_field = MDTextField(
            hint_text=language_manager.get_text('year_make'),
            icon_left="calendar",
            input_type="number",
            size_hint_y=None,
            height=dp(48)
        )
        details_grid.add_widget(self.year_make_field)

        # Bedrooms
        self.bedrooms_field = MDTextField(
            hint_text=language_manager.get_text('bedrooms'),
            icon_left="bed",
            input_type="number",
            size_hint_y=None,
            height=dp(48)
        )
        details_grid.add_widget(self.bedrooms_field)

        # Bathrooms
        self.bathrooms_field = MDTextField(
            hint_text=language_manager.get_text('bathrooms'),
            icon_left="shower",
            input_type="number",
            size_hint_y=None,
            height=dp(48)
        )
        details_grid.add_widget(self.bathrooms_field)

        parent.add_widget(details_grid)

        # Description
        self.description_field = MDTextField(
            hint_text=language_manager.get_text('description'),
            multiline=True,
            icon_left="text",
            size_hint_y=None,
            height=dp(96)
        )
        parent.add_widget(self.description_field)

    def build_location_section(self, parent):
        """Build location section"""
        # Section header
        location_header = MDLabel(
            text=language_manager.get_text('location_information'),
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['secondary'],
            font_style="Subtitle1",
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )
        parent.add_widget(location_header)

        # Owner selection
        self.owner_field = MDTextField(
            hint_text=language_manager.get_text('select_owner'),
            icon_left="account",
            size_hint_y=None,
            height=dp(48),
            readonly=True,
            on_focus=self.show_owner_selection
        )
        parent.add_widget(self.owner_field)

        # Province and region in grid
        location_grid = MDGridLayout(
            cols=2,
            adaptive_height=True,
            spacing=dp(10)
        )

        self.province_field = MDTextField(
            hint_text=language_manager.get_text('province'),
            icon_left="map",
            size_hint_y=None,
            height=dp(48)
        )
        location_grid.add_widget(self.province_field)

        self.region_field = MDTextField(
            hint_text=language_manager.get_text('region'),
            icon_left="map-marker-outline",
            size_hint_y=None,
            height=dp(48)
        )
        location_grid.add_widget(self.region_field)

        parent.add_widget(location_grid)

    def build_action_buttons(self, parent):
        """Build action buttons for the form"""
        buttons_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(140)
        )

        # First row
        row1 = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(48)
        )

        # Save button
        self.save_btn = MDRaisedButton(
            text=language_manager.get_text('save'),
            icon="content-save",
            md_bg_color=DesignTokens.COLORS['success'],
            on_release=self.save_property
        )
        row1.add_widget(self.save_btn)

        # Update button
        self.update_btn = MDFlatButton(
            text=language_manager.get_text('update'),
            icon="pencil",
            disabled=True,
            on_release=self.update_property
        )
        row1.add_widget(self.update_btn)

        buttons_layout.add_widget(row1)

        # Second row
        row2 = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(48)
        )

        # Delete button
        self.delete_btn = MDFlatButton(
            text=language_manager.get_text('delete'),
            icon="delete",
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['error'],
            disabled=True,
            on_release=self.confirm_delete_property
        )
        row2.add_widget(self.delete_btn)

        # Clear button
        clear_btn = MDFlatButton(
            text=language_manager.get_text('clear'),
            icon="refresh",
            on_release=self.clear_form
        )
        row2.add_widget(clear_btn)

        buttons_layout.add_widget(row2)

        # Third row - Photos button
        photos_btn = MDRaisedButton(
            text=language_manager.get_text('manage_photos'),
            icon="camera",
            md_bg_color=DesignTokens.COLORS['secondary'],
            size_hint_y=None,
            height=dp(48),
            on_release=self.manage_photos
        )
        buttons_layout.add_widget(photos_btn)

        parent.add_widget(buttons_layout)

    def build_list_section(self, parent):
        """Build the properties list section"""
        list_layout = MDBoxLayout(
            orientation='vertical',
            size_hint_x=0.55,
            spacing=dp(15)
        )

        # List header with search and filters
        self.build_list_header(list_layout)

        # Properties list
        self.properties_list_scroll = MDScrollView()
        self.properties_list = MDList()
        self.properties_list_scroll.add_widget(self.properties_list)
        list_layout.add_widget(self.properties_list_scroll)

        parent.add_widget(list_layout)

    def build_list_header(self, parent):
        """Build list header with search and filters"""
        header_layout = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            spacing=dp(10)
        )

        # Title and search row
        title_row = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(48),
            spacing=dp(10)
        )

        list_title = MDLabel(
            text=language_manager.get_text('properties_list'),
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['primary'],
            font_style="H6",
            bold=True
        )
        title_row.add_widget(list_title)

        # Search field
        self.search_field = MDTextField(
            hint_text=language_manager.get_text('search_properties'),
            icon_right="magnify",
            size_hint_x=0.5,
            size_hint_y=None,
            height=dp(48),
            on_text=self.on_search_text
        )
        title_row.add_widget(self.search_field)

        header_layout.add_widget(title_row)

        # Filter chips
        filter_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )        # Property type filter
        self.type_chip = MDChip(
            type="filter",
            on_release=self.show_type_filter
        )
        self.type_chip.add_widget(IconLeftWidget(
            icon="home-variant"
        ))
        self.type_chip.add_widget(MDLabel(
            text=language_manager.get_text('all_types'),
            halign="center",
            adaptive_size=True
        ))
        filter_layout.add_widget(self.type_chip)        # Owner filter
        self.owner_chip = MDChip(
            type="filter",
            on_release=self.show_owner_filter
        )
        self.owner_chip.add_widget(IconLeftWidget(
            icon="account"
        ))
        self.owner_chip.add_widget(MDLabel(
            text=language_manager.get_text('all_owners'),
            halign="center",
            adaptive_size=True
        ))
        filter_layout.add_widget(self.owner_chip)

        header_layout.add_widget(filter_layout)
        parent.add_widget(header_layout)

    def build_fab(self, parent):
        """Build floating action button"""
        fab = MDFloatingActionButton(
            icon="plus",
            md_bg_color=DesignTokens.COLORS['secondary'],
            pos_hint={'center_x': 0.9, 'center_y': 0.1},
            on_release=self.clear_form
        )
        parent.add_widget(fab)

    def update_stats_display(self):
        """Update statistics display"""
        self.stats_grid.clear_widgets()

        try:
            total_properties = len(self.properties_data)

            # Total properties card
            total_card = EnhancedStatsCard(
                title=language_manager.get_text('total_properties'),
                value=str(total_properties),
                icon='home-city',
                color_scheme='primary',
                size_hint_y=None,
                height=dp(100)
            )
            self.stats_grid.add_widget(total_card)

            # Available properties
            available_card = EnhancedStatsCard(
                title=language_manager.get_text('available_properties'),
                value=str(total_properties),  # Assuming all are available
                icon='home-outline',
                color_scheme='success',
                size_hint_y=None,
                height=dp(100)
            )
            self.stats_grid.add_widget(available_card)

            # With photos
            with_photos = sum(1 for prop in self.properties_data if prop.get('Photosituation') != 'لا توجد صور')
            photos_card = EnhancedStatsCard(
                title=language_manager.get_text('with_photos'),
                value=str(with_photos),
                icon='camera',
                color_scheme='warning',
                size_hint_y=None,
                height=dp(100)
            )
            self.stats_grid.add_widget(photos_card)

        except Exception as e:
            logger.error(f"Error updating stats: {e}")

    def load_data(self):
        """Load properties and owners data"""
        try:
            if not self.db:
                return

            self.properties_data = self.db.get_properties()
            self.owners_data = self.db.get_owners()
            self.display_properties(self.properties_data)
            self.update_stats_display()

        except Exception as e:
            logger.error(f"Error loading data: {e}")
            self.show_snackbar(language_manager.get_text('error_loading_data'))

    def display_properties(self, properties):
        """Display properties in the list"""
        try:
            self.properties_list.clear_widgets()

            for prop in properties:
                # Get property details
                company_code = prop.get('Companyco', '')
                address = prop.get('Property-address', '') or language_manager.get_text('no_address')
                property_type = prop.get('Rstatetcode', '') or language_manager.get_text('unknown_type')
                owner_name = prop.get('ownername', '') or language_manager.get_text('no_owner')

                # Create list item
                item = ThreeLineAvatarIconListItem(
                    text=address[:50] + ('...' if len(address) > 50 else ''),
                    secondary_text=f"{language_manager.get_text('type')}: {property_type}",
                    tertiary_text=f"{language_manager.get_text('owner')}: {owner_name}",
                    on_release=lambda x, data=prop: self.select_property(data)
                )

                # Icon based on property type
                item.add_widget(IconLeftWidget(icon="home"))

                # Action button
                item.add_widget(IconRightWidget(
                    icon="chevron-right",
                    on_release=lambda x, data=prop: self.select_property(data)
                ))

                self.properties_list.add_widget(item)

        except Exception as e:
            logger.error(f"Error displaying properties: {e}")

    def select_property(self, property_data):
        """Select property for editing"""
        try:
            self.current_property = property_data

            # Populate form
            self.company_code_field.text = property_data.get('Companyco', '')
            self.realstate_code_field.text = property_data.get('realstatecode', '')
            self.address_field.text = property_data.get('Property-address', '')
            self.property_type_field.text = property_data.get('Rstatetcode', '')
            self.area_field.text = str(property_data.get('Property-area', ''))
            self.year_make_field.text = property_data.get('Yearmake', '')
            self.bedrooms_field.text = str(property_data.get('N-of-bedrooms', ''))
            self.bathrooms_field.text = str(property_data.get('N-of bathrooms', ''))
            self.description_field.text = property_data.get('Descriptions', '')
            self.province_field.text = property_data.get('Province-code ', '')
            self.region_field.text = property_data.get('Region-code', '')

            # Set owner field
            self.owner_field.text = property_data.get('ownername', '')

            # Enable update/delete buttons
            self.update_btn.disabled = False
            self.delete_btn.disabled = False
            self.save_btn.disabled = True

        except Exception as e:
            logger.error(f"Error selecting property: {e}")

    def save_property(self, instance=None):
        """Save new property"""
        try:
            if not self.validate_form():
                return

            property_data = self.get_form_data()

            if not self.db:
                self.show_snackbar(language_manager.get_text('database_error'))
                return

            company_code = self.db.add_property(property_data)
            if company_code:
                self.show_snackbar(language_manager.get_text('property_saved_successfully'))
                self.clear_form()
                self.load_data()
            else:
                self.show_snackbar(language_manager.get_text('error_saving_property'))

        except Exception as e:
            logger.error(f"Error saving property: {e}")
            self.show_snackbar(language_manager.get_text('error_saving_property'))

    def update_property(self, instance=None):
        """Update existing property"""
        try:
            if not self.current_property or not self.validate_form():
                return

            company_code = self.company_code_field.text
            property_data = self.get_form_data()

            if not self.db:
                self.show_snackbar(language_manager.get_text('database_error'))
                return

            if self.db.update_property(company_code, property_data):
                self.show_snackbar(language_manager.get_text('property_updated_successfully'))
                self.clear_form()
                self.load_data()
            else:
                self.show_snackbar(language_manager.get_text('error_updating_property'))

        except Exception as e:
            logger.error(f"Error updating property: {e}")
            self.show_snackbar(language_manager.get_text('error_updating_property'))

    def confirm_delete_property(self, instance=None):
        """Confirm property deletion"""
        if not self.current_property:
            return

        address = self.current_property.get('Property-address', language_manager.get_text('unknown_property'))
        dialog = ConfirmationDialog(
            title=language_manager.get_text('confirm_deletion'),
            message=f"{language_manager.get_text('confirm_delete_property')}: {address}?",
            confirm_callback=self.delete_property
        )
        dialog.open()

    def delete_property(self, instance=None):
        """Delete selected property"""
        try:
            if not self.current_property:
                return

            company_code = self.current_property.get('Companyco', '')

            if not self.db:
                self.show_snackbar(language_manager.get_text('database_error'))
                return

            if self.db.delete_property(company_code):
                self.show_snackbar(language_manager.get_text('property_deleted_successfully'))
                self.clear_form()
                self.load_data()
            else:
                self.show_snackbar(language_manager.get_text('error_deleting_property'))

        except Exception as e:
            logger.error(f"Error deleting property: {e}")
            self.show_snackbar(language_manager.get_text('error_deleting_property'))

    def get_form_data(self):
        """Get form data as dictionary"""
        return {
            'realstatecode': self.realstate_code_field.text.strip(),
            'address': self.address_field.text.strip(),
            'property_type': self.property_type_field.text.strip(),
            'area': self.area_field.text.strip(),
            'year_make': self.year_make_field.text.strip(),
            'bedrooms': self.bedrooms_field.text.strip(),
            'bathrooms': self.bathrooms_field.text.strip(),
            'description': self.description_field.text.strip(),
            'province_code': self.province_field.text.strip(),
            'region_code': self.region_field.text.strip(),
            'owner_code': getattr(self, 'selected_owner_code', '')
        }

    def clear_form(self, instance=None):
        """Clear the form"""
        self.current_property = None

        # Clear all fields
        fields = [
            self.company_code_field, self.realstate_code_field, self.address_field,
            self.property_type_field, self.area_field, self.year_make_field,
            self.bedrooms_field, self.bathrooms_field, self.description_field,
            self.province_field, self.region_field, self.owner_field
        ]

        for field in fields:
            field.text = ''

        # Reset button states
        self.save_btn.disabled = False
        self.update_btn.disabled = True
        self.delete_btn.disabled = True

    def validate_form(self):
        """Validate form data"""
        if not self.address_field.text.strip():
            self.show_snackbar(language_manager.get_text('address_required'))
            return False
        return True

    def on_search_text(self, instance, text):
        """Handle search text change"""
        if text.strip():
            filtered_properties = []
            search_lower = text.lower()

            for prop in self.properties_data:
                address = (prop.get('Property-address', '') or '').lower()
                owner_name = (prop.get('ownername', '') or '').lower()
                company_code = (prop.get('Companyco', '') or '').lower()

                if (search_lower in address or
                    search_lower in owner_name or
                    search_lower in company_code):
                    filtered_properties.append(prop)

            self.display_properties(filtered_properties)
        else:
            self.display_properties(self.properties_data)

    def show_owner_selection(self, instance, value):
        """Show owner selection menu"""
        if not value:  # Only show when gaining focus
            return

        menu_items = []
        for owner in self.owners_data:
            owner_code, owner_name, _, _ = owner
            menu_items.append({
                "text": f"{owner_name} ({owner_code})",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=owner_code, y=owner_name: self.select_owner(x, y),
            })

        if menu_items:
            self.owner_menu = MDDropdownMenu(
                caller=self.owner_field,
                items=menu_items,
            )
            self.owner_menu.open()

    def select_owner(self, owner_code, owner_name):
        """Select owner for property"""
        self.owner_field.text = f"{owner_name} ({owner_code})"
        self.selected_owner_code = owner_code
        if hasattr(self, 'owner_menu'):
            self.owner_menu.dismiss()

    def show_type_filter(self, instance):
        """Show property type filter"""
        # Implement type filtering
        pass

    def show_owner_filter(self, instance):
        """Show owner filter"""
        # Implement owner filtering
        pass

    def manage_photos(self, instance=None):
        """Open photo management"""
        self.show_snackbar(language_manager.get_text('photo_management_coming_soon'))

    def toggle_search(self, instance=None):
        """Toggle search field focus"""
        self.search_field.focus = True

    def refresh_data(self, instance=None):
        """Refresh properties data"""
        self.load_data()
        self.show_snackbar(language_manager.get_text('data_refreshed'))

    def show_snackbar(self, message):
        """Show snackbar message"""
        snackbar = Snackbar(
            text=message,
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=(
                self.width - (2 * 10)
            ) / self.width
        )
        snackbar.open()

    def go_back(self, instance=None):
        """Go back to enhanced dashboard"""
        if hasattr(self, 'manager') and self.manager:
            self.manager.current = 'enhanced_dashboard'

    def on_enter(self, *args):
        """Called when screen is entered"""
        self.load_data()

    def on_leave(self, *args):
        """Called when leaving screen"""
        pass
