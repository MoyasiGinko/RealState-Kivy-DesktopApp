#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Enhanced Search and Reports with KivyMD
Beautiful, modern search interface with advanced filtering and report generation
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
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.animation import Animation
import logging
from datetime import datetime, timedelta
import json

from app.views.modern_components import (
    ModernCard, EnhancedStatsCard, DesignTokens
)
from app.database import DatabaseManager
from app.language_manager import language_manager

logger = logging.getLogger(__name__)

class EnhancedSearchScreen(MDScreen):
    """Enhanced Search and Reports Screen with KivyMD components"""

    def __init__(self, db_manager: DatabaseManager, **kwargs):
        super().__init__(**kwargs)
        self.name = 'enhanced_search'
        self.db = db_manager
        self.search_results = []
        self.current_filters = {}

        self.build_ui()
        self.load_initial_data()

    def build_ui(self):
        """Build the enhanced search and reports UI with side-by-side layout"""
        # Main layout
        main_layout = MDBoxLayout(orientation='vertical')

        # Header toolbar
        toolbar = MDTopAppBar(
            title=language_manager.get_text('search_and_reports'),
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=2
        )
        main_layout.add_widget(toolbar)

        # Content scroll view
        scroll = MDScrollView()
        content = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['xl'],
            padding=[DesignTokens.SPACING['lg'], DesignTokens.SPACING['lg']],
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter('height'))

        # Statistics Cards Row (full width)
        stats_layout = self.build_stats_section()
        content.add_widget(stats_layout)

        # Main content area with horizontal layout (search/filters on left, results on right)
        main_content_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['lg'],
            size_hint_y=None,
            height=dp(600)  # Fixed height for the main content area
        )

        # Left side: Combined Search and Filters
        left_panel = self.build_search_and_filters_panel()
        main_content_layout.add_widget(left_panel)

        # Right side: Results
        right_panel = self.build_results_section()
        main_content_layout.add_widget(right_panel)

        content.add_widget(main_content_layout)

        # Reports Section (full width at bottom)
        reports_section = self.build_reports_section()
        content.add_widget(reports_section)

        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

    def build_stats_section(self):
        """Build statistics overview section with improved layout and responsiveness"""
        # Enhanced stats container with increased height and spacing
        stats_container = ModernCard(
            elevation=DesignTokens.ELEVATIONS['card'],
            size_hint_y=None,
            height=dp(260),  # Increased height for better fit
            md_bg_color=DesignTokens.COLORS['card'],
            padding=[DesignTokens.SPACING['lg'], DesignTokens.SPACING['md']]
        )

        stats_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['lg'],
            size_hint_y=None,
            height=dp(240)  # Make sure layout fits inside container
        )

        # Header section with icon and title
        header_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(56),
            spacing=DesignTokens.SPACING['md'],
            padding=[0, 0, 0, 0]
        )

        header_layout.add_widget(MDIconButton(
            icon='chart-box-outline',
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['primary'],
            size_hint=(None, None),
            size=(dp(36), dp(36))
        ))

        header_layout.add_widget(MDLabel(
            text=language_manager.get_text('search_statistics'),
            font_style="H6",
            theme_text_color="Primary",
            halign="left",
            valign="middle"
        ))

        stats_layout.add_widget(header_layout)

        # Stats grid with increased height and responsive sizing
        stats_grid = MDGridLayout(
            cols=3,
            spacing=DesignTokens.SPACING['lg'],
            padding=[0, 0, 0, 0],
            size_hint_y=None,
            height=dp(160)
        )

        # Total Properties
        total_props = self.db.get_total_properties()
        props_card = EnhancedStatsCard(
            icon='home',
            title=language_manager.get_text('total_properties'),
            value=str(total_props),
            color_scheme='Primary',
            size_hint_y=None,
            height=dp(140)
        )
        stats_grid.add_widget(props_card)

        # Available Properties
        all_properties = self.db.get_properties()
        available_props = len([p for p in all_properties if p.get('status') == 'Available'])
        available_card = EnhancedStatsCard(
            icon='home-outline',
            title=language_manager.get_text('available_properties'),
            value=str(available_props),
            color_scheme='success',
            size_hint_y=None,
            height=dp(140)
        )
        stats_grid.add_widget(available_card)

        # Total Owners
        total_owners = self.db.get_total_owners()
        owners_card = EnhancedStatsCard(
            icon='account-group',
            title=language_manager.get_text('total_owners'),
            value=str(total_owners),
            color_scheme='secondary',
            size_hint_y=None,
            height=dp(140)
        )
        stats_grid.add_widget(owners_card)

        stats_layout.add_widget(stats_grid)
        stats_container.add_widget(stats_layout)
        return stats_container

    def build_search_section(self):
        """Build main search section with improved layout and responsiveness"""
        # Enhanced search container with increased height and spacing
        search_container = ModernCard(
            elevation=DesignTokens.ELEVATIONS['card'],
            size_hint_y=None,
            height=dp(260),  # Increased height for better fit
            md_bg_color=DesignTokens.COLORS['card'],
            padding=[DesignTokens.SPACING['lg'], DesignTokens.SPACING['md']]
        )

        search_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['lg'],
            size_hint_y=None,
            height=dp(240)  # Ensure layout fits inside container
        )

        # Header section with icon and title
        header_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(56),
            spacing=DesignTokens.SPACING['md'],
            padding=[0, 0, 0, 0]
        )

        header_layout.add_widget(MDIconButton(
            icon='magnify',
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['primary'],
            size_hint=(None, None),
            size=(dp(36), dp(36))
        ))

        header_layout.add_widget(MDLabel(
            text=language_manager.get_text('quick_search'),
            font_style="H6",
            theme_text_color="Primary",
            halign="left",
            valign="middle"
        ))

        search_layout.add_widget(header_layout)

        # Search input with proper spacing
        input_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['md'],
            size_hint_y=None,
            height=dp(120)
        )

        # Search input
        self.search_input = MDTextField(
            hint_text=language_manager.get_text('search_properties_owners'),
            helper_text=language_manager.get_text('search_hint'),
            helper_text_mode="on_focus",
            icon_right="magnify",
            size_hint_y=None,
            height=dp(56)
        )
        self.search_input.bind(text=self.on_search_text_change)
        input_layout.add_widget(self.search_input)

        # Search buttons
        buttons_layout = MDBoxLayout(
            spacing=DesignTokens.SPACING['md'],
            size_hint_y=None,
            height=dp(50)
        )

        search_btn = MDRaisedButton(
            text=language_manager.get_text('search'),
            md_bg_color=DesignTokens.COLORS['primary'],
            size_hint=(None, None),
            height=dp(40),
            width=dp(120),
            on_release=self.perform_search
        )
        buttons_layout.add_widget(search_btn)

        clear_btn = MDFlatButton(
            text=language_manager.get_text('clear'),
            size_hint=(None, None),
            height=dp(40),
            width=dp(100),
            on_release=self.clear_search
        )
        buttons_layout.add_widget(clear_btn)

        # Spacer to push buttons to the left
        buttons_layout.add_widget(MDLabel(size_hint_x=1))

        input_layout.add_widget(buttons_layout)
        search_layout.add_widget(input_layout)
        search_container.add_widget(search_layout)
        return search_container

    def build_filters_section(self):
        """Build advanced filters section with improved layout and responsiveness"""
        # Enhanced filters container with increased height and spacing
        filters_container = ModernCard(
            elevation=DesignTokens.ELEVATIONS['card'],
            size_hint_y=None,
            height=dp(420),  # Increased height for better fit
            md_bg_color=DesignTokens.COLORS['card'],
            padding=[DesignTokens.SPACING['lg'], DesignTokens.SPACING['md']]
        )

        filters_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['lg'],
            size_hint_y=None,
            height=dp(400)  # Ensure layout fits inside container
        )

        # Header section with icon and title
        header_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(56),
            spacing=DesignTokens.SPACING['md'],
            padding=[0, 0, 0, 0]
        )

        header_layout.add_widget(MDIconButton(
            icon='filter-variant',
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['primary'],
            size_hint=(None, None),
            size=(dp(36), dp(36))
        ))

        header_layout.add_widget(MDLabel(
            text=language_manager.get_text('advanced_filters'),
            font_style="H6",
            theme_text_color="Primary",
            halign="left",
            valign="middle"
        ))

        filters_layout.add_widget(header_layout)

        # Filters content with proper spacing
        content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['lg'],
            size_hint_y=None,
            height=dp(320)
        )

        # Property Type Filter
        type_layout = MDBoxLayout(
            spacing=DesignTokens.SPACING['md'],
            size_hint_y=None,
            height=dp(70)
        )
        type_layout.add_widget(MDLabel(
            text=language_manager.get_text('property_type'),
            size_hint_x=None,
            width=dp(120),
            theme_text_color="Primary"
        ))

        self.type_chips_layout = MDBoxLayout(
            spacing=DesignTokens.SPACING['sm'],
            size_hint_y=None,
            height=dp(40)
        )
        property_types = ['Apartment', 'House', 'Commercial', 'Land']
        for prop_type in property_types:
            chip = MDChip(
                type="filter",
                on_release=lambda x, pt=prop_type: self.toggle_filter_chip(x, 'type', pt),
                size_hint=(None, None),
                height=dp(36)
            )
            chip.add_widget(MDLabel(
                text=prop_type,
                halign="center",
                adaptive_size=True
            ))
            self.type_chips_layout.add_widget(chip)

        type_layout.add_widget(self.type_chips_layout)
        content_layout.add_widget(type_layout)

        # Status Filter
        status_layout = MDBoxLayout(
            spacing=DesignTokens.SPACING['md'],
            size_hint_y=None,
            height=dp(70)
        )
        status_layout.add_widget(MDLabel(
            text=language_manager.get_text('status'),
            size_hint_x=None,
            width=dp(120),
            theme_text_color="Primary"
        ))

        self.status_chips_layout = MDBoxLayout(
            spacing=DesignTokens.SPACING['sm'],
            size_hint_y=None,
            height=dp(40)
        )
        statuses = ['Available', 'Occupied', 'Maintenance']
        for status in statuses:
            chip = MDChip(
                type="filter",
                on_release=lambda x, s=status: self.toggle_filter_chip(x, 'status', s),
                size_hint=(None, None),
                height=dp(36)
            )
            chip.add_widget(MDLabel(
                text=status,
                halign="center",
                adaptive_size=True
            ))
            self.status_chips_layout.add_widget(chip)

        status_layout.add_widget(self.status_chips_layout)
        content_layout.add_widget(status_layout)

        # Price Range Filter
        price_layout = MDBoxLayout(
            spacing=DesignTokens.SPACING['md'],
            size_hint_y=None,
            height=dp(70)
        )
        price_layout.add_widget(MDLabel(
            text=language_manager.get_text('price_range'),
            size_hint_x=None,
            width=dp(120),
            theme_text_color="Primary"
        ))

        self.min_price_input = MDTextField(
            hint_text=language_manager.get_text('min_price'),
            input_filter="float",
            size_hint_x=None,
            width=dp(100),
            height=dp(48)
        )
        price_layout.add_widget(self.min_price_input)

        price_layout.add_widget(MDLabel(text="-", size_hint_x=None, width=dp(20)))

        self.max_price_input = MDTextField(
            hint_text=language_manager.get_text('max_price'),
            input_filter="float",
            size_hint_x=None,
            width=dp(100),
            height=dp(48)
        )
        price_layout.add_widget(self.max_price_input)

        content_layout.add_widget(price_layout)

        # Apply Filters Button
        apply_filters_btn = MDRaisedButton(
            text=language_manager.get_text('apply_filters'),
            md_bg_color=DesignTokens.COLORS['secondary'],
            size_hint=(None, None),
            height=dp(48),
            width=dp(180),
            pos_hint={"center_x": 0.5},
            on_release=self.apply_filters
        )
        content_layout.add_widget(apply_filters_btn)

        filters_layout.add_widget(content_layout)
        filters_container.add_widget(filters_layout)
        return filters_container

    def build_results_section(self):
        """Build search results section optimized for right panel in side-by-side layout"""
        # Enhanced results container optimized for right panel
        self.results_card = ModernCard(
            elevation=DesignTokens.ELEVATIONS['card'],
            size_hint_x=1,  # Take remaining width in horizontal layout
            size_hint_y=None,
            height=dp(600),  # Match main content area height
            md_bg_color=DesignTokens.COLORS['card'],            padding=[DesignTokens.SPACING['lg'], DesignTokens.SPACING['md']]
        )

        results_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['lg'],
            size_hint_y=None,
            height=dp(580)  # Match container height minus padding
        )

        # Header section with icon and title
        header_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(56),
            spacing=DesignTokens.SPACING['md'],
            padding=[0, 0, 0, 0]
        )

        header_layout.add_widget(MDIconButton(
            icon='format-list-bulleted',
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['primary'],
            size_hint=(None, None),
            size=(dp(36), dp(36))
        ))

        # Store reference to results title for dynamic updates
        self.results_title_label = MDLabel(
            text=language_manager.get_text('search_results'),
            font_style="H6",
            theme_text_color="Primary",
            halign="left",
            valign="middle"
        )
        header_layout.add_widget(self.results_title_label)

        results_layout.add_widget(header_layout)

        # Results content with proper height and padding
        results_content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['md'],
            size_hint_y=None,
            height=dp(500)  # Increased height for better content display
        )

        self.results_list = MDList()
        results_scroll = MDScrollView(
            size_hint_y=None,
            height=dp(480)  # Increased scroll area height
        )
        results_scroll.add_widget(self.results_list)

        results_content_layout.add_widget(results_scroll)
        results_layout.add_widget(results_content_layout)
        self.results_card.add_widget(results_layout)
        return self.results_card

    def build_reports_section(self):
        """Build reports generation section with improved layout and responsiveness"""
        # Enhanced reports container with increased height and spacing
        reports_container = ModernCard(
            elevation=DesignTokens.ELEVATIONS['card'],
            size_hint_y=None,
            height=dp(340),  # Increased height for better fit
            md_bg_color=DesignTokens.COLORS['card'],
            padding=[DesignTokens.SPACING['lg'], DesignTokens.SPACING['md']]
        )

        reports_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['lg'],
            size_hint_y=None,
            height=dp(320)  # Ensure layout fits inside container
        )

        # Header section with icon and title
        header_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(56),
            spacing=DesignTokens.SPACING['md'],
            padding=[0, 0, 0, 0]
        )

        header_layout.add_widget(MDIconButton(
            icon='file-document-outline',
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['primary'],
            size_hint=(None, None),
            size=(dp(36), dp(36))
        ))

        header_layout.add_widget(MDLabel(
            text=language_manager.get_text('generate_reports'),
            font_style="H6",
            theme_text_color="Primary",
            halign="left",
            valign="middle"
        ))

        reports_layout.add_widget(header_layout)

        # Reports buttons with proper spacing and layout
        content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['lg'],
            size_hint_y=None,
            height=dp(240)
        )

        report_buttons_layout = MDGridLayout(
            cols=2,
            spacing=DesignTokens.SPACING['lg'],
            padding=[0, 0, 0, 0],
            size_hint_y=None,
            height=dp(160)
        )

        # Properties Report
        properties_report_btn = MDRaisedButton(
            text=language_manager.get_text('properties_report'),
            md_bg_color=DesignTokens.COLORS['primary'],
            size_hint=(1, None),
            height=dp(60),
            on_release=lambda x: self.generate_report('properties')
        )
        report_buttons_layout.add_widget(properties_report_btn)

        # Owners Report
        owners_report_btn = MDRaisedButton(
            text=language_manager.get_text('owners_report'),
            md_bg_color=DesignTokens.COLORS['secondary'],
            size_hint=(1, None),
            height=dp(60),
            on_release=lambda x: self.generate_report('owners')
        )
        report_buttons_layout.add_widget(owners_report_btn)

        # Financial Report
        financial_report_btn = MDRaisedButton(
            text=language_manager.get_text('financial_report'),
            md_bg_color=DesignTokens.COLORS['success'],
            size_hint=(1, None),
            height=dp(60),
            on_release=lambda x: self.generate_report('financial')
        )
        report_buttons_layout.add_widget(financial_report_btn)

        # Custom Report
        custom_report_btn = MDRaisedButton(
            text=language_manager.get_text('custom_report'),
            md_bg_color=DesignTokens.COLORS['info'],
            size_hint=(1, None),
            height=dp(60),
            on_release=lambda x: self.generate_report('custom')
        )
        report_buttons_layout.add_widget(custom_report_btn)

        content_layout.add_widget(report_buttons_layout)
        reports_layout.add_widget(content_layout)
        reports_container.add_widget(reports_layout)
        return reports_container

    def build_search_and_filters_panel(self):
        """Build combined search and filters panel for left side with consistent styling and spacing"""
        # Combined container with scroll view for all search and filter content
        combined_container = MDScrollView(
            size_hint_x=None,
            width=dp(400)  # Fixed width for left panel
        )

        combined_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['lg'],
            padding=[DesignTokens.SPACING['md'], DesignTokens.SPACING['md']],
            size_hint_y=None
        )
        combined_layout.bind(minimum_height=combined_layout.setter('height'))

        # --- Search Section (styled to match filters) ---
        search_card = ModernCard(
            elevation=DesignTokens.ELEVATIONS['card'],
            size_hint_y=None,
            height=dp(260),
            md_bg_color=DesignTokens.COLORS['card'],
            padding=[DesignTokens.SPACING['lg'], DesignTokens.SPACING['md']]
        )

        search_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['lg'],
            size_hint_y=None,
            height=dp(240)
        )

        # Search header
        search_header = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(56),
            spacing=DesignTokens.SPACING['md']
        )

        search_header.add_widget(MDIconButton(
            icon='magnify',
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['primary'],
            size_hint=(None, None),
            size=(dp(36), dp(36))
        ))

        search_header.add_widget(MDLabel(
            text=language_manager.get_text('quick_search'),
            font_style="H6",
            theme_text_color="Primary",
            halign="left",
            valign="middle"
        ))

        search_layout.add_widget(search_header)

        # Search input
        self.search_input = MDTextField(
            hint_text=language_manager.get_text('search_properties_owners'),
            helper_text=language_manager.get_text('search_hint'),
            helper_text_mode="on_focus",
            icon_right="magnify",
            size_hint_y=None,
            height=dp(56)
        )
        self.search_input.bind(text=self.on_search_text_change)
        search_layout.add_widget(self.search_input)

        # Search buttons
        search_buttons = MDBoxLayout(
            spacing=DesignTokens.SPACING['md'],
            size_hint_y=None,
            height=dp(50)
        )

        search_btn = MDRaisedButton(
            text=language_manager.get_text('search'),
            md_bg_color=DesignTokens.COLORS['primary'],
            size_hint=(None, None),
            height=dp(40),
            width=dp(120),
            on_release=self.perform_search
        )
        search_buttons.add_widget(search_btn)

        clear_btn = MDFlatButton(
            text=language_manager.get_text('clear'),
            size_hint=(None, None),
            height=dp(40),
            width=dp(100),
            on_release=self.clear_search
        )
        search_buttons.add_widget(clear_btn)

        search_buttons.add_widget(MDLabel(size_hint_x=1))  # Spacer

        search_layout.add_widget(search_buttons)
        search_card.add_widget(search_layout)
        combined_layout.add_widget(search_card)

        # --- Advanced Filters Section (styled to match search) ---
        filters_card = ModernCard(
            elevation=DesignTokens.ELEVATIONS['card'],
            size_hint_y=None,
            height=dp(420),
            md_bg_color=DesignTokens.COLORS['card'],
            padding=[DesignTokens.SPACING['lg'], DesignTokens.SPACING['md']]
        )

        filters_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['lg'],
            size_hint_y=None,
            height=dp(400)
        )

        # Filters header
        filters_header = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(56),
            spacing=DesignTokens.SPACING['md']
        )

        filters_header.add_widget(MDIconButton(
            icon='filter-variant',
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['primary'],
            size_hint=(None, None),
            size=(dp(36), dp(36))
        ))

        filters_header.add_widget(MDLabel(
            text=language_manager.get_text('advanced_filters'),
            font_style="H6",
            theme_text_color="Primary",
            halign="left",
            valign="middle"
        ))

        filters_layout.add_widget(filters_header)

        # Property Type Filter
        type_layout = MDBoxLayout(
            spacing=DesignTokens.SPACING['md'],
            size_hint_y=None,
            height=dp(70)
        )
        type_layout.add_widget(MDLabel(
            text=language_manager.get_text('property_type'),
            size_hint_x=None,
            width=dp(120),
            theme_text_color="Primary"
        ))

        self.type_chips_layout = MDBoxLayout(
            spacing=DesignTokens.SPACING['sm'],
            size_hint_y=None,
            height=dp(40)
        )
        property_types = ['Apartment', 'House', 'Commercial', 'Land']
        for prop_type in property_types:
            chip = MDChip(
                type="filter",
                on_release=lambda x, pt=prop_type: self.toggle_filter_chip(x, 'type', pt),
                size_hint=(None, None),
                height=dp(36)
            )
            chip.add_widget(MDLabel(
                text=prop_type,
                halign="center",
                adaptive_size=True
            ))
            self.type_chips_layout.add_widget(chip)

        type_layout.add_widget(self.type_chips_layout)
        filters_layout.add_widget(type_layout)

        # Status Filter
        status_layout = MDBoxLayout(
            spacing=DesignTokens.SPACING['md'],
            size_hint_y=None,
            height=dp(70)
        )
        status_layout.add_widget(MDLabel(
            text=language_manager.get_text('status'),
            size_hint_x=None,
            width=dp(120),
            theme_text_color="Primary"
        ))

        self.status_chips_layout = MDBoxLayout(
            spacing=DesignTokens.SPACING['sm'],
            size_hint_y=None,
            height=dp(40)
        )
        statuses = ['Available', 'Occupied', 'Maintenance']
        for status in statuses:
            chip = MDChip(
                type="filter",
                on_release=lambda x, s=status: self.toggle_filter_chip(x, 'status', s),
                size_hint=(None, None),
                height=dp(36)
            )
            chip.add_widget(MDLabel(
                text=status,
                halign="center",
                adaptive_size=True
            ))
            self.status_chips_layout.add_widget(chip)

        status_layout.add_widget(self.status_chips_layout)
        filters_layout.add_widget(status_layout)

        # Price Range Filter
        price_layout = MDBoxLayout(
            spacing=DesignTokens.SPACING['md'],
            size_hint_y=None,
            height=dp(70)
        )
        price_layout.add_widget(MDLabel(
            text=language_manager.get_text('price_range'),
            size_hint_x=None,
            width=dp(120),
            theme_text_color="Primary"
        ))

        self.min_price_input = MDTextField(
            hint_text=language_manager.get_text('min_price'),
            input_filter="float",
            size_hint_x=None,
            width=dp(100),
            height=dp(48)
        )
        price_layout.add_widget(self.min_price_input)

        price_layout.add_widget(MDLabel(text="-", size_hint_x=None, width=dp(20)))

        self.max_price_input = MDTextField(
            hint_text=language_manager.get_text('max_price'),
            input_filter="float",
            size_hint_x=None,
            width=dp(100),
            height=dp(48)
        )
        price_layout.add_widget(self.max_price_input)

        filters_layout.add_widget(price_layout)

        # Apply Filters Button
        apply_filters_btn = MDRaisedButton(
            text=language_manager.get_text('apply_filters'),
            md_bg_color=DesignTokens.COLORS['secondary'],
            size_hint=(None, None),
            height=dp(48),
            width=dp(180),
            pos_hint={"center_x": 0.5},
            on_release=self.apply_filters
        )
        filters_layout.add_widget(apply_filters_btn)

        filters_card.add_widget(filters_layout)
        combined_layout.add_widget(filters_card)

        combined_container.add_widget(combined_layout)
        return combined_container

    def load_initial_data(self):
        """Load initial data for the screen and ensure containers/content are visually responsive"""
        try:
            # Load all properties for search
            self.all_properties = self.db.get_properties()  # returns list of dicts
            self.all_owners = self.db.get_owners()  # returns list of tuples

            # Adjust container heights and spacing for responsiveness
            # Stats Section
            if hasattr(self, 'stats_layout'):
                self.stats_layout.height = dp(260)
                self.stats_layout.spacing = DesignTokens.SPACING['lg']

            # Search Section
            if hasattr(self, 'search_layout'):
                self.search_layout.height = dp(240)
                self.search_layout.spacing = DesignTokens.SPACING['lg']

            # Filters Section
            if hasattr(self, 'filters_layout'):
                self.filters_layout.height = dp(400)
                self.filters_layout.spacing = DesignTokens.SPACING['lg']

            # Results Section
            if hasattr(self, 'results_card'):
                self.results_card.height = dp(520)
                if hasattr(self, 'results_list'):
                    self.results_list.height = dp(400)

            # Reports Section
            if hasattr(self, 'reports_layout'):
                self.reports_layout.height = dp(320)
                self.reports_layout.spacing = DesignTokens.SPACING['lg']

            # Perform initial search to show all data
            self.perform_search()

        except Exception as e:
            logger.error(f"Error loading initial data: {e}")
            self.show_snackbar(language_manager.get_text('error_loading_data'))

    def on_search_text_change(self, instance, text):
        """Handle search text changes for real-time search"""
        if len(text) >= 3:  # Start searching after 3 characters
            Clock.unschedule(self.delayed_search)
            Clock.schedule_once(lambda dt: self.perform_search(), 0.5)

    def delayed_search(self, dt):
        """Delayed search to avoid too many searches while typing"""
        self.perform_search()

    def perform_search(self):
        """Perform search with current criteria"""
        try:
            search_text = self.search_input.text.lower().strip()
            results = []

            # Search in properties
            for prop in self.all_properties:
                # prop is a dict
                prop_id = prop.get('id')
                prop_type = prop.get('property_type')
                address = prop.get('address')
                city = prop.get('city')
                price = prop.get('price') if prop.get('price') is not None else 0
                area = prop.get('area') if prop.get('area') is not None else 0
                status = prop.get('status')
                owner_id = prop.get('owner_id')

                # Text search
                if search_text and search_text not in (
                    str(prop_type).lower() +
                    str(address).lower() +
                    str(city).lower() +
                    str(status).lower()
                ):
                    continue

                # Apply filters
                if not self.apply_property_filters(prop):
                    continue

                results.append({
                    'type': 'property',
                    'data': prop,
                    'display_text': f"{prop_type} - {address}, {city}",
                    'subtitle': f"{language_manager.get_text('status')}: {status} | {language_manager.get_text('price')}: ${price:,.0f}",
                    'details': f"{language_manager.get_text('area')}: {area} sq ft"
                })

            # Search in owners if no specific property filters
            if not any(self.current_filters.get(key) for key in ['type', 'status']) and search_text:
                for owner in self.all_owners:
                    owner_id, name, phone, email, address = owner

                    if search_text in (
                        str(name).lower() +
                        str(phone).lower() +
                        str(email).lower() +
                        str(address).lower()
                    ):
                        results.append({
                            'type': 'owner',
                            'data': owner,
                            'display_text': name,
                            'subtitle': f"{language_manager.get_text('phone')}: {phone}",
                            'details': f"{language_manager.get_text('email')}: {email}"
                        })

            self.display_search_results(results)

        except Exception as e:
            logger.error(f"Error performing search: {e}")
            self.show_snackbar(language_manager.get_text('search_error'))

    def apply_property_filters(self, prop):
        """Apply current filters to a property"""
        # prop is a dict
        prop_type = prop.get('property_type')
        status = prop.get('status')
        price = prop.get('price')

        # Type filter
        if self.current_filters.get('type') and prop_type not in self.current_filters['type']:
            return False

        # Status filter
        if self.current_filters.get('status') and status not in self.current_filters['status']:
            return False

        # Price range filter
        min_price = self.min_price_input.text
        max_price = self.max_price_input.text

        try:
            if min_price and float(min_price) > price:
                return False
            if max_price and float(max_price) < price:
                return False
        except ValueError:
            pass  # Invalid price input, ignore filter

        return True

    def display_search_results(self, results):
        """Display search results in the results list"""
        self.results_list.clear_widgets()

        if not results:
            no_results = MDLabel(
                text=language_manager.get_text('no_results_found'),
                theme_text_color="Secondary",
                halign="center",
                size_hint_y=None,
                height=dp(60)
            )
            self.results_list.add_widget(no_results)
            return

        for result in results[:50]:  # Limit to 50 results for performance
            icon = 'home' if result['type'] == 'property' else 'account'

            list_item = ThreeLineAvatarIconListItem(
                IconLeftWidget(icon=icon),
                text=result['display_text'],
                secondary_text=result['subtitle'],
                tertiary_text=result['details'],
                on_release=lambda x, r=result: self.on_result_selected(r)
            )

            self.results_list.add_widget(list_item)        # Update results count
        self.results_title_label.text = f"{language_manager.get_text('search_results')} ({len(results)})"

    def toggle_filter_chip(self, chip, filter_type, value):
        """Toggle filter chip selection"""
        chip.check = not chip.check

        if filter_type not in self.current_filters:
            self.current_filters[filter_type] = []

        if chip.check:
            if value not in self.current_filters[filter_type]:
                self.current_filters[filter_type].append(value)
        else:
            if value in self.current_filters[filter_type]:
                self.current_filters[filter_type].remove(value)

    def apply_filters(self):
        """Apply current filters and perform search"""
        self.perform_search()
        self.show_snackbar(language_manager.get_text('filters_applied'))

    def clear_search(self):
        """Clear search input and filters"""
        self.search_input.text = ""
        self.min_price_input.text = ""
        self.max_price_input.text = ""
        self.current_filters = {}

        # Reset all chips
        for chip in self.type_chips_layout.children + self.status_chips_layout.children:
            chip.check = False

        self.perform_search()
        self.show_snackbar(language_manager.get_text('search_cleared'))

    def on_result_selected(self, result):
        """Handle result selection"""
        if result['type'] == 'property':
            self.show_property_details(result['data'])
        else:
            self.show_owner_details(result['data'])

    def show_property_details(self, property_data):
        """Show property details in a dialog"""
        prop_id, prop_type, address, city, price, area, status, owner_id = property_data

        # Get owner name
        owner_name = "Unknown"
        if owner_id:
            owner = self.db.get_owner(owner_id)
            if owner:
                owner_name = owner[1]

        details_text = f"""
{language_manager.get_text('property_type')}: {prop_type}
{language_manager.get_text('address')}: {address}
{language_manager.get_text('city')}: {city}
{language_manager.get_text('price')}: ${price:,.0f}
{language_manager.get_text('area')}: {area} sq ft
{language_manager.get_text('status')}: {status}
{language_manager.get_text('owner')}: {owner_name}
        """.strip()

        self.show_snackbar(f"{language_manager.get_text('property_selected')}: {address}")

    def show_owner_details(self, owner_data):
        """Show owner details in a dialog"""
        owner_id, name, phone, email, address = owner_data

        # Get owner's properties count
        properties = [p for p in self.all_properties if p.get('owner_id') == owner_id]

        details_text = f"""
{language_manager.get_text('name')}: {name}
{language_manager.get_text('phone')}: {phone}
{language_manager.get_text('email')}: {email}
{language_manager.get_text('address')}: {address}
{language_manager.get_text('properties_count')}: {len(properties)}
        """.strip()

        self.show_snackbar(f"{language_manager.get_text('owner_selected')}: {name}")

    def generate_report(self, report_type):
        """Generate different types of reports"""
        try:
            if report_type == 'properties':
                self.generate_properties_report()
            elif report_type == 'owners':
                self.generate_owners_report()
            elif report_type == 'financial':
                self.generate_financial_report()
            elif report_type == 'custom':
                self.generate_custom_report()

        except Exception as e:
            logger.error(f"Error generating {report_type} report: {e}")
            self.show_snackbar(language_manager.get_text('report_generation_error'))

    def generate_properties_report(self):
        """Generate properties report"""
        # Create a simple report summary
        total_properties = len(self.all_properties)
        available_count = len([p for p in self.all_properties if p.get('status') == 'Available'])
        occupied_count = len([p for p in self.all_properties if p.get('status') == 'Occupied'])

        report_data = {
            'title': 'Properties Report',
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'total_properties': total_properties,
            'available': available_count,
            'occupied': occupied_count,
            'maintenance': total_properties - available_count - occupied_count
        }

        self.show_snackbar(f"{language_manager.get_text('properties_report')} {language_manager.get_text('generated')}")

    def generate_owners_report(self):
        """Generate owners report"""
        total_owners = len(self.all_owners)

        # Count properties per owner
        owner_properties = {}
        for prop in self.all_properties:
            owner_id = prop[7]
            if owner_id:
                owner_properties[owner_id] = owner_properties.get(owner_id, 0) + 1

        self.show_snackbar(f"{language_manager.get_text('owners_report')} {language_manager.get_text('generated')}")

    def generate_financial_report(self):
        """Generate financial report"""
        total_value = sum(prop[4] for prop in self.all_properties)  # Sum all property prices
        avg_price = total_value / len(self.all_properties) if self.all_properties else 0

        self.show_snackbar(f"{language_manager.get_text('financial_report')} {language_manager.get_text('generated')}")

    def generate_custom_report(self):
        """Generate custom report"""
        self.show_snackbar(f"{language_manager.get_text('custom_report')} {language_manager.get_text('generated')}")

    def go_back(self):
        """Navigate back to dashboard"""
        try:
            self.manager.current = 'enhanced_dashboard'
        except Exception as e:
            logger.error(f"Error navigating back: {e}")

    def show_snackbar(self, message):
        """Show snackbar message"""
        try:
            snackbar = Snackbar(text=message, duration=3)
            snackbar.open()
        except Exception as e:
            logger.error(f"Error showing snackbar: {e}")
