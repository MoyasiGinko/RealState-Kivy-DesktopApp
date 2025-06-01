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
        self.owners_data = []        # UI State
        self.is_loading = False
        self.current_view = 'grid'  # 'grid' or 'table'
        self.sort_field = 'location'
        self.sort_order = 'asc'
        self.selected_properties = []
        self.filtered_properties = []

        self.build_ui()
        self.load_data()

    def build_ui(self):
        """Build the enhanced properties management UI with new layout design"""
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

        # Main horizontal layout: Search/Filters (left) + Results (right)
        self.build_main_horizontal_layout(main_layout)

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

    def build_main_horizontal_layout(self, parent_layout):
        """Build main horizontal layout: Search/Filters (left) + Results (right)"""
        # Main horizontal container
        main_horizontal = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(16),
            size_hint_y=None,
            height=dp(700)  # Fixed height for content area
        )

        # Left panel: Search and Advanced Filters
        self.build_search_and_filters_panel(main_horizontal)

        # Right panel: Search Results
        self.build_search_results_panel(main_horizontal)

        parent_layout.add_widget(main_horizontal)

    def build_search_and_filters_panel(self, parent_layout):
        """Build left panel with search and advanced filters"""
        # Left panel card
        left_panel = MDCard(
            size_hint_x=0.3,  # 30% width for search and filters
            elevation=2,
            padding=dp(16)
        )

        # Scrollable content for filters
        filter_scroll = MDScrollView(
            do_scroll_x=False,
            do_scroll_y=True
        )

        filter_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            size_hint_y=None,
            padding=[0, 0, 0, dp(8)]
        )
        filter_layout.bind(minimum_height=filter_layout.setter('height'))

        # Panel title
        title = MDLabel(
            text="Search & Filters",
            theme_text_color="Primary",
            font_style="H6",
            bold=True,
            size_hint_y=None,
            height=dp(32)
        )
        filter_layout.add_widget(title)

        # Search section
        self.build_search_section(filter_layout)

        # Advanced filters section
        self.build_advanced_filters_section(filter_layout)

        # Action buttons section
        self.build_filter_actions_section(filter_layout)

        filter_scroll.add_widget(filter_layout)
        left_panel.add_widget(filter_scroll)
        parent_layout.add_widget(left_panel)

    def build_search_section(self, parent_layout):
        """Build search section"""
        # Search title
        search_title = MDLabel(
            text="Search Properties",
            theme_text_color="Primary",
            font_style="Subtitle1",
            bold=True,
            size_hint_y=None,
            height=dp(24)
        )
        parent_layout.add_widget(search_title)

        # Search field
        self.search_field = MDTextField(
            hint_text="Search by location, type, or status...",
            mode="line",
            size_hint_y=None,
            height=dp(56),
            multiline=False
        )
        self.search_field.bind(text=self.on_search_text_change)
        parent_layout.add_widget(self.search_field)

    def build_advanced_filters_section(self, parent_layout):
        """Build advanced filters section"""
        # Filters title
        filters_title = MDLabel(
            text="Advanced Filters",
            theme_text_color="Primary",
            font_style="Subtitle1",
            bold=True,
            size_hint_y=None,
            height=dp(32)
        )
        parent_layout.add_widget(filters_title)

        # Status filter
        status_label = MDLabel(
            text="Status",
            theme_text_color="Secondary",
            font_style="Body2",
            size_hint_y=None,
            height=dp(20)
        )
        parent_layout.add_widget(status_label)

        self.status_filter_button = MDRaisedButton(
            text="All Statuses",
            md_bg_color=DesignTokens.COLORS['primary'],
            size_hint_y=None,
            height=dp(40)
        )
        self.status_filter_button.bind(on_release=self.show_status_filter_menu)
        parent_layout.add_widget(self.status_filter_button)

        # Property type filter
        type_label = MDLabel(
            text="Property Type",
            theme_text_color="Secondary",
            font_style="Body2",
            size_hint_y=None,
            height=dp(20)
        )
        parent_layout.add_widget(type_label)

        self.type_filter_button = MDRaisedButton(
            text="All Types",
            md_bg_color=DesignTokens.COLORS['secondary'],
            size_hint_y=None,
            height=dp(40)
        )
        self.type_filter_button.bind(on_release=self.show_type_filter_menu)
        parent_layout.add_widget(self.type_filter_button)

        # Price range filter
        price_label = MDLabel(
            text="Price Range",
            theme_text_color="Secondary",
            font_style="Body2",
            size_hint_y=None,
            height=dp(20)
        )
        parent_layout.add_widget(price_label)

        price_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(48)
        )

        self.min_price_field = MDTextField(
            hint_text="Min Price",
            mode="line",
            size_hint_x=0.5,
            input_filter="int"
        )
        self.min_price_field.bind(text=self.on_price_filter_change)
        price_layout.add_widget(self.min_price_field)

        self.max_price_field = MDTextField(
            hint_text="Max Price",
            mode="line",
            size_hint_x=0.5,
            input_filter="int"
        )
        self.max_price_field.bind(text=self.on_price_filter_change)
        price_layout.add_widget(self.max_price_field)

        parent_layout.add_widget(price_layout)

        # Area range filter
        area_label = MDLabel(
            text="Area Range (m²)",
            theme_text_color="Secondary",
            font_style="Body2",
            size_hint_y=None,
            height=dp(20)
        )
        parent_layout.add_widget(area_label)

        area_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(48)
        )

        self.min_area_field = MDTextField(
            hint_text="Min Area",
            mode="line",
            size_hint_x=0.5,
            input_filter="int"
        )
        self.min_area_field.bind(text=self.on_area_filter_change)
        area_layout.add_widget(self.min_area_field)

        self.max_area_field = MDTextField(
            hint_text="Max Area",
            mode="line",
            size_hint_x=0.5,
            input_filter="int"
        )
        self.max_area_field.bind(text=self.on_area_filter_change)
        area_layout.add_widget(self.max_area_field)

        parent_layout.add_widget(area_layout)

        # Furnished filter
        furnished_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(40)
        )

        furnished_label = MDLabel(
            text="Furnished Only",
            theme_text_color="Secondary",
            font_style="Body2",
            size_hint_x=0.7
        )
        furnished_layout.add_widget(furnished_label)

        self.furnished_filter_switch = MDSwitch(
            size_hint_x=0.3
        )
        self.furnished_filter_switch.bind(active=self.on_furnished_filter_change)
        furnished_layout.add_widget(self.furnished_filter_switch)

        parent_layout.add_widget(furnished_layout)

    def build_filter_actions_section(self, parent_layout):
        """Build filter action buttons"""
        actions_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(100)
        )

        # Clear filters button
        clear_filters_btn = MDFlatButton(
            text="Clear All Filters",
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['secondary'],
            size_hint_y=None,
            height=dp(40)
        )
        clear_filters_btn.bind(on_release=self.clear_all_filters)
        actions_layout.add_widget(clear_filters_btn)

        # Add property button
        add_property_btn = MDRaisedButton(
            text="Add New Property",
            md_bg_color=DesignTokens.COLORS['primary'],
            icon="plus",
            size_hint_y=None,
            height=dp(44)
        )
        add_property_btn.bind(on_release=self.add_new_property)
        actions_layout.add_widget(add_property_btn)

        parent_layout.add_widget(actions_layout)

    def build_search_results_panel(self, parent_layout):
        """Build right panel with search results"""
        # Right panel card
        right_panel = MDCard(
            size_hint_x=0.7,  # 70% width for results
            elevation=2,
            padding=dp(16)
        )

        results_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(12)
        )

        # Results header
        self.build_results_header(results_layout)

        # Results content
        self.build_results_content(results_layout)

        right_panel.add_widget(results_layout)
        parent_layout.add_widget(right_panel)

    def build_results_header(self, parent_layout):
        """Build results header with title and view controls"""
        header_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(48)
        )

        # Results title
        self.results_title = MDLabel(
            text="Properties (0)",
            theme_text_color="Primary",
            font_style="H6",
            bold=True,
            size_hint_x=0.7
        )
        header_layout.add_widget(self.results_title)

        # View controls
        controls_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_x=0.3
        )

        # View toggle
        self.view_toggle_button = MDIconButton(
            icon="view-grid",
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['primary'],
            size_hint=(None, None),
            size=(dp(40), dp(40))
        )
        self.view_toggle_button.bind(on_release=self.toggle_view)
        controls_layout.add_widget(self.view_toggle_button)

        # Export button
        export_btn = MDIconButton(
            icon="download",
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['secondary'],
            size_hint=(None, None),
            size=(dp(40), dp(40))
        )
        export_btn.bind(on_release=self.export_properties)
        controls_layout.add_widget(export_btn)

        header_layout.add_widget(controls_layout)
        parent_layout.add_widget(header_layout)

    def build_results_content(self, parent_layout):
        """Build results content area"""
        # Scrollable results container
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
            message="No Properties Found\nAdd your first property or adjust your filters"
        )

        # Initially show grid
        self.properties_container.add_widget(self.properties_grid)
        self.properties_scroll.add_widget(self.properties_container)
        parent_layout.add_widget(self.properties_scroll)

    # Filter event handlers
    def on_price_filter_change(self, instance, text):
        """Handle price filter changes"""
        Clock.schedule_once(lambda dt: self.apply_filters(), 0.5)

    def on_area_filter_change(self, instance, text):
        """Handle area filter changes"""
        Clock.schedule_once(lambda dt: self.apply_filters(), 0.5)

    def on_furnished_filter_change(self, instance, active):
        """Handle furnished filter changes"""
        self.apply_filters()

    def clear_all_filters(self, instance):
        """Clear all filters and reset search"""
        self.search_field.text = ""
        self.status_filter_button.text = "All Statuses"
        self.type_filter_button.text = "All Types"
        self.min_price_field.text = ""
        self.max_price_field.text = ""
        self.min_area_field.text = ""
        self.max_area_field.text = ""
        self.furnished_filter_switch.active = False

        self.filtered_properties = self.properties_data.copy()
        self.update_properties_display()

    def apply_filters(self):
        """Apply all active filters"""
        try:
            filtered = self.properties_data.copy()

            # Apply search filter
            search_text = self.search_field.text.lower().strip()
            if search_text:
                filtered = [
                    prop for prop in filtered
                    if search_text in prop.get('location', '').lower() or
                       search_text in prop.get('propertytype', '').lower() or
                       search_text in prop.get('status', '').lower()
                ]

            # Apply status filter
            if self.status_filter_button.text != "All Statuses":
                status = self.status_filter_button.text.replace("Status: ", "")
                filtered = [
                    prop for prop in filtered
                    if prop.get('status', '').lower() == status.lower()
                ]

            # Apply type filter
            if self.type_filter_button.text != "All Types":
                prop_type = self.type_filter_button.text.replace("Type: ", "")
                filtered = [
                    prop for prop in filtered
                    if prop.get('propertytype', '').lower() == prop_type.lower()
                ]

            # Apply price range filter
            min_price = self.min_price_field.text.strip()
            max_price = self.max_price_field.text.strip()
            if min_price or max_price:
                filtered = [
                    prop for prop in filtered
                    if self.price_in_range(prop.get('price', '0'), min_price, max_price)
                ]

            # Apply area range filter
            min_area = self.min_area_field.text.strip()
            max_area = self.max_area_field.text.strip()
            if min_area or max_area:
                filtered = [
                    prop for prop in filtered
                    if self.area_in_range(prop.get('area', '0'), min_area, max_area)
                ]

            # Apply furnished filter
            if self.furnished_filter_switch.active:
                filtered = [
                    prop for prop in filtered
                    if prop.get('is_furnished', False)
                ]

            self.filtered_properties = filtered
            self.update_properties_display()

        except Exception as e:
            logger.error(f"Error applying filters: {e}")

    def price_in_range(self, price_str, min_price_str, max_price_str):
        """Check if price is within range"""
        try:
            price = float(str(price_str).replace('$', '').replace(',', '') or 0)

            if min_price_str:
                min_price = float(min_price_str)
                if price < min_price:
                    return False

            if max_price_str:
                max_price = float(max_price_str)
                if price > max_price:
                    return False

            return True
        except (ValueError, TypeError):
            return True

    def area_in_range(self, area_str, min_area_str, max_area_str):
        """Check if area is within range"""
        try:
            area = float(str(area_str) or 0)

            if min_area_str:
                min_area = float(min_area_str)
                if area < min_area:
                    return False

            if max_area_str:
                max_area = float(max_area_str)
                if area > max_area:
                    return False

            return True
        except (ValueError, TypeError):
            return True

    def on_search_text_change(self, instance, text):
        """Handle search text changes"""
        # Use the new filter system
        Clock.schedule_once(lambda dt: self.apply_filters(), 0.3)

    def update_properties_display(self):
        """Update the properties display based on current view and filters"""
        try:
            if not hasattr(self, 'properties_container'):
                return

            self.properties_container.clear_widgets()

            # Update results title
            if hasattr(self, 'results_title'):
                self.results_title.text = f"Properties ({len(self.filtered_properties)})"

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

    # Data loading and management methods
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
                self.status_filter_button.text = "All Statuses"
            else:
                self.status_filter_button.text = f"Status: {status}"

            self.apply_filters()
        except Exception as e:
            logger.error(f"Error filtering by status: {e}")

    def filter_by_type(self, prop_type):
        """Filter properties by type"""
        try:
            if hasattr(self, 'type_menu'):
                self.type_menu.dismiss()

            if prop_type == 'All':
                self.type_filter_button.text = "All Types"
            else:
                self.type_filter_button.text = f"Type: {prop_type}"

            self.apply_filters()
        except Exception as e:
            logger.error(f"Error filtering by type: {e}")

    def add_new_property(self, instance):
        """Start adding a new property"""
        try:
            self.current_property = None
            # Clear form if we had one in the old layout
            # self.clear_form_simple(None)
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
                size_hint_y=None,
                height=dp(80)
            )
            layout.add_widget(details)

            # Action buttons
            buttons_layout = MDBoxLayout(
                orientation='horizontal',
                spacing=dp(8),
                size_hint_y=None,
                height=dp(36)
            )

            edit_btn = MDIconButton(
                icon="pencil",
                theme_icon_color="Custom",
                icon_color=DesignTokens.COLORS['primary'],
                on_release=lambda x: self.edit_property(property_data)
            )
            buttons_layout.add_widget(edit_btn)

            delete_btn = MDIconButton(
                icon="delete",
                theme_icon_color="Custom",
                icon_color=DesignTokens.COLORS['error'],
                on_release=lambda x: self.delete_property(property_data)
            )
            buttons_layout.add_widget(delete_btn)

            layout.add_widget(buttons_layout)
            card.add_widget(layout)

            return card
        except Exception as e:
            logger.error(f"Error creating property card: {e}")
            return MDCard()

    def edit_property(self, property_data):
        """Edit a property"""
        try:
            self.current_property = property_data
            self.show_info_snackbar(f"Editing property: {property_data.get('location', 'Unknown')}")
        except Exception as e:
            logger.error(f"Error editing property: {e}")

    def delete_property(self, property_data):
        """Delete a property with confirmation"""
        try:
            def confirm_delete():
                result = self.db.delete_property(property_data.get('id'))
                if result:
                    self.show_success_snackbar("Property deleted successfully")
                    self.load_data()
                else:
                    self.show_error_snackbar("Failed to delete property")

            dialog = ConfirmationDialog(
                title="Delete Property",
                text=f"Are you sure you want to delete the property at {property_data.get('location', 'Unknown')}?",
                confirm_callback=confirm_delete
            )
            dialog.open()
        except Exception as e:
            logger.error(f"Error deleting property: {e}")

    def show_info_snackbar(self, message):
        """Show info snackbar"""
        try:
            snackbar = ModernSnackbar(
                text=message,
                bg_color=DesignTokens.COLORS['primary']
            )
            snackbar.open()
        except Exception as e:
            logger.error(f"Error showing info snackbar: {e}")

    def show_success_snackbar(self, message):
        """Show success snackbar"""
        try:
            snackbar = ModernSnackbar(
                text=message,
                bg_color=DesignTokens.COLORS['success']
            )
            snackbar.open()
        except Exception as e:
            logger.error(f"Error showing success snackbar: {e}")

    def show_error_snackbar(self, message):
        """Show error snackbar"""
        try:
            snackbar = ModernSnackbar(
                text=message,
                bg_color=DesignTokens.COLORS['error']
            )
            snackbar.open()
        except Exception as e:
            logger.error(f"Error showing error snackbar: {e}")

    def go_back(self):
        """Navigate back to the previous screen"""
        try:
            if hasattr(self.parent, 'current'):
                self.parent.current = 'enhanced_dashboard'
        except Exception as e:
            logger.error(f"Error navigating back: {e}")

    def refresh_data(self):
        """Refresh all data"""
        try:
            self.load_data()
            self.show_info_snackbar("Data refreshed")
        except Exception as e:
            logger.error(f"Error refreshing data: {e}")

    def toggle_search(self):
        """Toggle search functionality"""
        try:
            if hasattr(self, 'search_field'):
                self.search_field.focus = True
        except Exception as e:
            logger.error(f"Error toggling search: {e}")
