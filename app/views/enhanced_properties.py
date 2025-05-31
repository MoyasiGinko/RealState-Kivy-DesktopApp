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
from kivymd.uix.list import MDList, ThreeLineAvatarIconListItem, OneLineListItem, IconLeftWidget, IconRightWidget
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
        """Build the enhanced properties management UI with responsive design"""
        # Main scrollable container for full responsiveness
        main_scroll = MDScrollView(
            do_scroll_x=False,
            do_scroll_y=True
        )

        # Main content container
        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=[dp(16), dp(8)],
            size_hint_y=None
        )

        # Top app bar
        self.build_top_bar(main_layout)

        main_layout.bind(minimum_height=main_layout.setter('height'))

        # Top section: Header stats (responsive)
        self.build_responsive_header(main_layout)

        # Search and filters section (always on top)
        self.build_compact_search_section(main_layout)

        # Action bar (compact design)
        self.build_modern_action_bar(main_layout)

        # Main content area with responsive layout
        self.build_responsive_content_area(main_layout)

        main_scroll.add_widget(main_layout)
        self.add_widget(main_scroll)



    def build_top_bar(self, parent):
            """Build the top navigation bar"""
            self.toolbar = MDTopAppBar(
                title=language_manager.get_text('manage_property_owners'),
                left_action_items=[["arrow-left", lambda x: self.go_back()]],
                right_action_items=[
                    ["refresh", lambda x: self.refresh_data()],
                    ["magnify", lambda x: self.toggle_search()]
                ],
                md_bg_color=DesignTokens.COLORS['primary'],
                specific_text_color=DesignTokens.COLORS['text_primary']
            )
            parent.add_widget(self.toolbar)

    def build_responsive_header(self, parent_layout):
        """Build responsive header with statistics cards"""
        header_card = ModernCard(
            size_hint_y=None,
            height=dp(100),
            elevation=2
        )

        # Use responsive grid layout
        header_layout = MDGridLayout(
            cols=4,  # Will be responsive
            spacing=dp(12),
            padding=dp(12),
            size_hint_y=None,
            height=dp(76)
        )

        # Statistics
        total_properties = len(self.properties_data)
        available_count = len([p for p in self.properties_data if p.get('status') == 'Available'])
        sold_count = len([p for p in self.properties_data if p.get('status') == 'Sold'])
        rented_count = len([p for p in self.properties_data if p.get('status') == 'Rented'])

        stats = [
            {'title': 'Total', 'value': str(total_properties), 'icon': 'home-group', 'color': DesignTokens.COLORS['primary']},
            {'title': 'Available', 'value': str(available_count), 'icon': 'home-plus', 'color': DesignTokens.COLORS['success']},
            {'title': 'Sold', 'value': str(sold_count), 'icon': 'home-check', 'color': DesignTokens.COLORS['warning']},
            {'title': 'Rented', 'value': str(rented_count), 'icon': 'home-heart', 'color': DesignTokens.COLORS['error']}
        ]

        for stat in stats:
            stat_card = self.create_compact_stat_card(
                title=stat['title'],
                value=stat['value'],
                icon=stat['icon'],
                color=stat['color']
            )
            header_layout.add_widget(stat_card)

        header_card.add_widget(header_layout)
        parent_layout.add_widget(header_card)

    def create_compact_stat_card(self, title, value, icon, color):
        """Create compact statistics card"""
        card = MDCard(
            md_bg_color=color,
            radius=[8],
            elevation=1,
            padding=dp(8)
        )

        layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8)
        )

        # Icon
        icon_widget = MDIconButton(
            icon=icon,
            theme_icon_color="Custom",
            icon_color=(1, 1, 1, 1),
            icon_size=dp(24),
            size_hint=(None, None),
            size=(dp(32), dp(32))
        )
        layout.add_widget(icon_widget)

        # Text content
        text_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(2)
        )

        value_label = MDLabel(
            text=value,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H6",
            bold=True,
            size_hint_y=None,
            height=dp(20)
        )
        text_layout.add_widget(value_label)

        title_label = MDLabel(
            text=title,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.8),
            font_style="Caption",
            size_hint_y=None,
            height=dp(16)
        )
        text_layout.add_widget(title_label)

        layout.add_widget(text_layout)
        card.add_widget(layout)

        return card

    def build_compact_search_section(self, parent_layout):
        """Build a visually appealing, well-spaced search and filter section"""
        search_card = ModernCard(
            size_hint_y=None,
            height=dp(84),  # Increased height for better spacing
            elevation=2,
            padding=[dp(16), dp(12)]
        )

        search_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(20),  # More spacing between search and filters
            padding=[dp(8), dp(8), dp(8), dp(8)],
            size_hint_y=None,
            height=dp(60)
        )

        # Search field
        self.search_field = MDTextField(
            hint_text="Search properties...",
            mode="line",
            size_hint_x=0.62,
            height=dp(48),
            padding=[dp(12), 0, dp(12), 0]
        )
        self.search_field.bind(text=self.on_search_text_change)
        search_layout.add_widget(self.search_field)

        # Filter buttons container
        filter_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(16),  # More space between filter buttons
            size_hint_x=0.38,
            size_hint_y=None,
            height=dp(48),
            padding=[0, 0, 0, 0]
        )

        # Status filter
        self.status_filter_button = MDRaisedButton(
            text="Status",
            md_bg_color=DesignTokens.COLORS['primary'],
            size_hint_x=0.5,
            height=dp(44),
            padding=[dp(8), 0]
        )
        self.status_filter_button.bind(on_release=self.show_status_filter_menu)
        filter_layout.add_widget(self.status_filter_button)

        # Type filter
        self.type_filter_button = MDRaisedButton(
            text="Type",
            md_bg_color=DesignTokens.COLORS['secondary'],
            size_hint_x=0.5,
            height=dp(44),
            padding=[dp(8), 0]
        )
        self.type_filter_button.bind(on_release=self.show_type_filter_menu)
        filter_layout.add_widget(self.type_filter_button)

        search_layout.add_widget(filter_layout)
        search_card.add_widget(search_layout)
        parent_layout.add_widget(search_card)

    def build_modern_action_bar(self, parent_layout):
        """Build modern compact action bar with improved spacing and responsiveness"""
        action_card = ModernCard(
            size_hint_y=None,
            height=dp(72),  # Increased height for better visual balance
            elevation=2,
            padding=[dp(16), dp(12)]
        )

        action_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(20),  # More spacing between main and secondary actions
            padding=[dp(8), dp(8), dp(8), dp(8)],
            size_hint_y=None,
            height=dp(48)
        )

        # Add property button (primary action)
        add_button = MDRaisedButton(
            text="Add Property",
            md_bg_color=DesignTokens.COLORS['primary'],
            icon="plus",
            size_hint=(None, None),
            width=dp(160),
            height=dp(44)
        )
        add_button.bind(on_release=self.add_new_property)
        action_layout.add_widget(add_button)

        # Spacer for responsiveness
        action_layout.add_widget(MDLabel(size_hint_x=0.05))

        # Secondary actions
        actions_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(12),
            size_hint=(1, None),
            height=dp(44)
        )

        # Import/Export buttons
        import_btn = MDIconButton(
            icon="upload",
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['secondary'],
            icon_size=dp(28),
            size_hint=(None, None),
            size=(dp(44), dp(44))
        )
        import_btn.bind(on_release=self.import_properties)
        actions_layout.add_widget(import_btn)

        export_btn = MDIconButton(
            icon="download",
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['secondary'],
            icon_size=dp(28),
            size_hint=(None, None),
            size=(dp(44), dp(44))
        )
        export_btn.bind(on_release=self.export_properties)
        actions_layout.add_widget(export_btn)

        # View toggle
        self.view_toggle_button = MDIconButton(
            icon="view-grid",
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['primary'],
            icon_size=dp(28),
            size_hint=(None, None),
            size=(dp(44), dp(44))
        )
        self.view_toggle_button.bind(on_release=self.toggle_view)
        actions_layout.add_widget(self.view_toggle_button)

        # Add a flexible spacer to push actions to the right if space allows
        actions_layout.add_widget(MDLabel(size_hint_x=1))

        action_layout.add_widget(actions_layout)
        action_card.add_widget(action_layout)
        parent_layout.add_widget(action_card)

    def build_responsive_content_area(self, parent_layout):
        """Build responsive content area with adaptive layout"""
        # Content container that adapts to screen size
        content_container = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(16),
            size_hint_y=None,
            height=dp(600)  # Fixed height for content area
        )

        # Left panel - Property form (collapsible on small screens)
        self.build_responsive_form_panel(content_container)

        # Right panel - Properties display
        self.build_responsive_properties_panel(content_container)

        parent_layout.add_widget(content_container)

    def build_responsive_form_panel(self, parent_layout):
        """Build responsive property form panel"""
        # Form panel with adaptive width
        form_panel = MDCard(
            size_hint_x=0.35,  # 35% width on desktop
            elevation=2,
            padding=dp(12)
        )

        # Scrollable form content
        form_scroll = MDScrollView(
            do_scroll_x=False,
            do_scroll_y=True
        )

        form_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(12),
            size_hint_y=None,
            padding=[0, dp(8)]
        )
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Form title
        form_title = MDLabel(
            text="Property Details",
            theme_text_color="Primary",
            font_style="H6",
            bold=True,
            size_hint_y=None,
            height=dp(32)
        )
        form_layout.add_widget(form_title)

        # Form fields - simplified and responsive
        self.build_form_fields(form_layout)

        # Action buttons
        self.build_form_actions(form_layout)

        form_scroll.add_widget(form_layout)
        form_panel.add_widget(form_scroll)
        parent_layout.add_widget(form_panel)

    def build_form_fields(self, parent_layout):
        """Build responsive form fields"""
        fields_data = [
            {'name': 'location', 'hint': 'Location *', 'required': True},
            {'name': 'propertytype', 'hint': 'Property Type *', 'required': True},
            {'name': 'area', 'hint': 'Area (m²) *', 'required': True},
            {'name': 'price', 'hint': 'Price *', 'required': True},
            {'name': 'status', 'hint': 'Status *', 'required': True},
            {'name': 'description', 'hint': 'Description'},        ]

        self.form_fields = {}

        for field_data in fields_data:
            field = MDTextField(
                hint_text=field_data['hint'],
                mode="line",
                size_hint_y=None,
                height=dp(48)
            )
            self.form_fields[field_data['name']] = field
            parent_layout.add_widget(field)

        # Boolean fields
        furnished_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(32)
        )

        self.furnished_switch = MDSwitch(
            size_hint_x=None,
            width=dp(48)
        )
        furnished_label = MDLabel(
            text="Furnished",
            theme_text_color="Primary",
            size_hint_x=None,
            width=dp(80)
        )

        furnished_layout.add_widget(furnished_label)
        furnished_layout.add_widget(self.furnished_switch)
        furnished_layout.add_widget(MDLabel())  # Spacer

        parent_layout.add_widget(furnished_layout)

    def build_form_actions(self, parent_layout):
        """Build form action buttons"""
        actions_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(48)
        )

        save_button = MDRaisedButton(
            text="Save",
            md_bg_color=DesignTokens.COLORS['primary'],
            size_hint_x=0.6
        )
        save_button.bind(on_release=self.save_property_simple)
        actions_layout.add_widget(save_button)

        clear_button = MDFlatButton(
            text="Clear",
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['secondary'],
            size_hint_x=0.4
        )
        clear_button.bind(on_release=self.clear_form_simple)
        actions_layout.add_widget(clear_button)

        parent_layout.add_widget(actions_layout)

    def build_responsive_properties_panel(self, parent_layout):
        """Build responsive properties display panel"""
        # Properties panel with adaptive width
        properties_panel = MDCard(
            size_hint_x=0.65,  # 65% width on desktop
            elevation=2,
            padding=dp(12)
        )

        properties_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8)
        )

        # Panel header
        header_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40)
        )

        properties_title = MDLabel(
            text="Properties",
            theme_text_color="Primary",
            font_style="H6",
            bold=True,
            size_hint_x=0.8
        )
        header_layout.add_widget(properties_title)

        properties_layout.add_widget(header_layout)

        # Properties content area
        self.build_properties_content(properties_layout)

        properties_panel.add_widget(properties_layout)
        parent_layout.add_widget(properties_panel)

    def build_properties_content(self, parent_layout):
        """Build properties content area"""
        # Scrollable properties container
        self.properties_scroll = MDScrollView(
            do_scroll_x=False,
            do_scroll_y=True
        )

        self.properties_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8),
            size_hint_y=None,
            padding=[dp(4), dp(4)]
        )
        self.properties_container.bind(minimum_height=self.properties_container.setter('height'))

        # Initialize grid view
        self.properties_grid = ModernGridView(
            cols=2,
            spacing=dp(8)
        )

        # Empty state
        self.empty_state = EmptyState(
            icon="home-search",
            message="No Properties Found\nAdd your first property to get started"
        )

        # Initially show grid
        self.properties_container.add_widget(self.properties_grid)
        self.properties_scroll.add_widget(self.properties_container)
        parent_layout.add_widget(self.properties_scroll)

    # Additional helper methods
    def on_search_text_change(self, instance, text):
        """Handle search text changes"""
        search_text = text.lower().strip()

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

    def save_property_simple(self, instance):
        """Save property with simplified form handling"""
        try:
            # Collect form data
            property_data = {}
            for field_name, field_widget in self.form_fields.items():
                property_data[field_name] = field_widget.text.strip()

            property_data['is_furnished'] = self.furnished_switch.active

            # Basic validation
            required_fields = ['location', 'propertytype', 'area', 'price', 'status']
            missing_fields = [field for field in required_fields if not property_data.get(field)]

            if missing_fields:
                self.show_error_snackbar(f"Required fields missing: {', '.join(missing_fields)}")
                return

            if self.current_property:
                # Update existing
                property_data['id'] = self.current_property['id']
                self.db.update_property(property_data)
                self.show_success_snackbar("Property updated successfully")
            else:
                # Add new
                property_data['company_code'] = self.db.generate_company_code()
                property_data['realstate_code'] = self.db.generate_realstate_code()
                self.db.add_property(property_data)
                self.show_success_snackbar("Property added successfully")

            self.load_data()
            self.clear_form_simple(None)

        except Exception as e:
            logger.error(f"Error saving property: {e}")
            self.show_error_snackbar("Failed to save property")

    def clear_form_simple(self, instance):
        """Clear form with simplified handling"""
        for field_widget in self.form_fields.values():
            field_widget.text = ""
        self.furnished_switch.active = False
        self.current_property = None

    # Keep existing methods for compatibility

    def load_data(self):
        """Load properties and owners data from database"""
        try:
            self.properties_data = self.db.get_properties()
            self.owners_data = self.db.get_owners()
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

    # Additional missing methods for full functionality

    def show_status_filter_menu(self, instance):
        """Show status filter dropdown menu"""
        try:
            status_options = ['All', 'Available', 'Sold', 'Rented']
            menu_items = [
                {
                    "text": status,
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=status: self.filter_by_status(x),
                } for status in status_options
            ]

            self.status_menu = MDDropdownMenu(
                caller=instance,
                items=menu_items,
                width_mult=4
            )
            self.status_menu.open()
        except Exception as e:
            logger.error(f"Error showing status filter menu: {e}")

    def show_type_filter_menu(self, instance):
        """Show type filter dropdown menu"""
        try:
            type_options = ['All', 'House', 'Apartment', 'Villa', 'Commercial']
            menu_items = [
                {
                    "text": prop_type,
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=prop_type: self.filter_by_type(x),
                } for prop_type in type_options
            ]

            self.type_menu = MDDropdownMenu(
                caller=instance,
                items=menu_items,
                width_mult=4
            )
            self.type_menu.open()
        except Exception as e:
            logger.error(f"Error showing type filter menu: {e}")

    def filter_by_status(self, status):
        """Filter properties by status"""
        try:
            if hasattr(self, 'status_menu'):
                self.status_menu.dismiss()

            if status == 'All':
                self.filtered_properties = self.properties_data.copy()
            else:
                self.filtered_properties = [
                    prop for prop in self.properties_data
                    if prop.get('status', '').lower() == status.lower()
                ]

            self.status_filter_button.text = f"Status: {status}"
            self.update_properties_display()
        except Exception as e:
            logger.error(f"Error filtering by status: {e}")

    def filter_by_type(self, prop_type):
        """Filter properties by type"""
        try:
            if hasattr(self, 'type_menu'):
                self.type_menu.dismiss()

            if prop_type == 'All':
                self.filtered_properties = self.properties_data.copy()
            else:
                self.filtered_properties = [
                    prop for prop in self.properties_data
                    if prop.get('propertytype', '').lower() == prop_type.lower()
                ]

            self.type_filter_button.text = f"Type: {prop_type}"
            self.update_properties_display()
        except Exception as e:
            logger.error(f"Error filtering by type: {e}")

    def add_new_property(self, instance):
        """Start adding a new property"""
        try:
            self.current_property = None
            self.clear_form_simple(None)
        except Exception as e:
            logger.error(f"Error adding new property: {e}")

    def import_properties(self, instance):
        """Import properties from file"""
        try:
            # Placeholder for import functionality
            self.show_info_snackbar("Import functionality not yet implemented")
        except Exception as e:
            logger.error(f"Error importing properties: {e}")

    def export_properties(self, instance):
        """Export properties to file"""
        try:
            # Placeholder for export functionality
            self.show_info_snackbar("Export functionality not yet implemented")
        except Exception as e:
            logger.error(f"Error exporting properties: {e}")

    def toggle_view(self, instance):
        """Toggle between grid and table view"""
        try:
            if self.current_view == 'grid':
                self.current_view = 'table'
                self.view_toggle_button.icon = "view-list"
            else:
                self.current_view = 'grid'
                self.view_toggle_button.icon = "view-grid"

            self.update_properties_display()
        except Exception as e:
            logger.error(f"Error toggling view: {e}")

    def update_properties_display(self):
        """Update the properties display based on current view and filters"""
        try:
            if not hasattr(self, 'properties_container'):
                return

            self.properties_container.clear_widgets()

            if not self.filtered_properties:
                self.properties_container.add_widget(self.empty_state)
                return

            if self.current_view == 'grid':
                # Grid view
                self.properties_grid.clear_widgets()
                for prop in self.filtered_properties:
                    property_card = self.create_property_card(prop)
                    self.properties_grid.add_widget(property_card)
                self.properties_container.add_widget(self.properties_grid)
            else:
                # Table view - simplified for now
                for prop in self.filtered_properties:
                    property_item = self.create_property_list_item(prop)
                    self.properties_container.add_widget(property_item)

        except Exception as e:
            logger.error(f"Error updating properties display: {e}")

    def create_property_card(self, property_data):
        """Create a property card for grid view"""
        try:
            card = MDCard(
                md_bg_color=DesignTokens.COLORS['card'],
                radius=[8],
                elevation=2,
                padding=dp(12),
                size_hint_y=None,
                height=dp(180)
            )

            layout = MDBoxLayout(
                orientation='vertical',
                spacing=dp(8)
            )

            # Property title
            title = MDLabel(
                text=property_data.get('location', 'Unknown Location'),
                theme_text_color="Primary",
                font_style="H6",
                bold=True,
                size_hint_y=None,
                height=dp(24)
            )
            layout.add_widget(title)

            # Property details
            details_text = f"Type: {property_data.get('propertytype', 'N/A')}\n"
            details_text += f"Area: {property_data.get('area', 'N/A')} m²\n"
            details_text += f"Price: ${property_data.get('price', 'N/A')}\n"
            details_text += f"Status: {property_data.get('status', 'N/A')}"

            details = MDLabel(
                text=details_text,
                theme_text_color="Secondary",
                font_style="Body2",
                size_hint_y=None,                height=dp(80)
            )
            layout.add_widget(details)

            # Action buttons
            actions = MDBoxLayout(
                orientation='horizontal',
                spacing=dp(8),
                size_hint_y=None,
                height=dp(36)
            )

            edit_btn = MDIconButton(
                icon="pencil",
                theme_icon_color="Custom",
                icon_color=DesignTokens.COLORS['primary']
            )
            edit_btn.bind(on_release=lambda x: self.edit_property(property_data))
            actions.add_widget(edit_btn)

            delete_btn = MDIconButton(
                icon="delete",
                theme_icon_color="Custom",
                icon_color=DesignTokens.COLORS['error']
            )
            delete_btn.bind(on_release=lambda x: self.delete_property(property_data))
            actions.add_widget(delete_btn)

            layout.add_widget(actions)
            card.add_widget(layout)

            return card

        except Exception as e:
            logger.error(f"Error creating property card: {e}")
            return MDLabel(text="Error loading property")

    def create_property_list_item(self, property_data):
        """Create a property list item for table view"""
        try:
            item = ThreeLineAvatarIconListItem(
                text=property_data.get('location', 'Unknown Location'),
                secondary_text=f"Type: {property_data.get('propertytype', 'N/A')} | Area: {property_data.get('area', 'N/A')} m²",
                tertiary_text=f"Price: ${property_data.get('price', 'N/A')} | Status: {property_data.get('status', 'N/A')}"
            )

            # Add click handler for editing
            item.bind(on_release=lambda x: self.edit_property(property_data))

            return item

        except Exception as e:
            logger.error(f"Error creating property list item: {e}")
            return MDLabel(text="Error loading property")

    # Additional required methods

    def edit_property(self, property_data):
        """Edit a property"""
        try:
            self.current_property = property_data
            # Fill form fields with property data
            for field_name, field_widget in self.form_fields.items():
                field_widget.text = str(property_data.get(field_name, ''))

            self.furnished_switch.active = property_data.get('is_furnished', False)

        except Exception as e:
            logger.error(f"Error editing property: {e}")
            self.show_error_snackbar("Failed to load property for editing")

    def delete_property(self, property_data):
        """Delete a property with confirmation"""
        try:
            def confirm_delete():
                try:
                    self.db.delete_property(property_data['id'])
                    self.show_success_snackbar("Property deleted successfully")
                    self.load_data()
                except Exception as e:
                    logger.error(f"Error deleting property: {e}")
                    self.show_error_snackbar("Failed to delete property")

            # Show confirmation dialog
            dialog = ConfirmationDialog(
                title="Delete Property",
                message=f"Are you sure you want to delete the property at {property_data.get('location', 'Unknown Location')}?",
                confirm_callback=confirm_delete
            )
            dialog.open()

        except Exception as e:
            logger.error(f"Error in delete property: {e}")

    def show_success_snackbar(self, message):
        """Show success snackbar"""
        try:
            snackbar = Snackbar(
                text=message,
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=(1.0 - (20 / 400)),
                bg_color=DesignTokens.COLORS['success']
            )
            snackbar.open()
        except Exception as e:
            logger.error(f"Error showing success snackbar: {e}")

    def show_error_snackbar(self, message):
        """Show error snackbar"""
        try:
            snackbar = Snackbar(
                text=message,
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=(1.0 - (20 / 400)),
                bg_color=DesignTokens.COLORS['error']
            )
            snackbar.open()
        except Exception as e:
            logger.error(f"Error showing error snackbar: {e}")

    def show_info_snackbar(self, message):
        """Show info snackbar"""
        try:
            snackbar = Snackbar(
                text=message,
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=(1.0 - (20 / 400)),
                bg_color=DesignTokens.COLORS['primary']
            )
            snackbar.open()
        except Exception as e:
            logger.error(f"Error showing info snackbar: {e}")

    def upload_photos(self, instance):
        """Upload photos for properties"""
        try:
            self.show_info_snackbar("Photo upload functionality not yet implemented")
        except Exception as e:
            logger.error(f"Error in upload photos: {e}")
