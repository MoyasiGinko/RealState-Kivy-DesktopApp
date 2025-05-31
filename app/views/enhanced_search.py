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
from app.views.enhanced_dialogs import ConfirmationDialog

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
        """Build the enhanced search and reports UI"""
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
            spacing=dp(20),
            padding=[dp(20), dp(20)],
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter('height'))

        # Statistics Cards Row
        stats_layout = self.build_stats_section()
        content.add_widget(stats_layout)

        # Search and Filter Section
        search_section = self.build_search_section()
        content.add_widget(search_section)

        # Advanced Filters Section
        filters_section = self.build_filters_section()
        content.add_widget(filters_section)

        # Results Section
        results_section = self.build_results_section()
        content.add_widget(results_section)

        # Reports Section
        reports_section = self.build_reports_section()
        content.add_widget(reports_section)

        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

    def build_stats_section(self):
        """Build statistics overview section"""
        stats_card = ModernCard(
            elevation=2,
            size_hint_y=None,
            height=dp(160)
        )

        # Add title explicitly
        stats_card.add_widget(MDLabel(
            text=language_manager.get_text('search_statistics'),
            font_style="H6",
            halign="center",
            size_hint_y=None,
            height=dp(32)
        ))

        stats_grid = MDGridLayout(cols=3, spacing=dp(15), padding=[dp(20), dp(10)])

        # Total Properties
        total_props = self.db.get_total_properties()
        props_card = EnhancedStatsCard(
            icon='home',
            title=language_manager.get_text('total_properties'),
            value=str(total_props),
            color_scheme='Primary'
        )
        stats_grid.add_widget(props_card)

        # Available Properties
        all_properties = self.db.get_properties()  # returns list of dicts
        available_props = len([p for p in all_properties if p.get('status') == 'Available'])
        available_card = EnhancedStatsCard(
            icon='home-outline',
            title=language_manager.get_text('available_properties'),
            value=str(available_props),
            color_scheme='success'
        )
        stats_grid.add_widget(available_card)

        # Total Owners
        total_owners = self.db.get_total_owners()
        owners_card = EnhancedStatsCard(
            icon='account-group',
            title=language_manager.get_text('total_owners'),
            value=str(total_owners),
            color_scheme='secondary'
        )
        stats_grid.add_widget(owners_card)

        stats_card.add_widget(stats_grid)
        return stats_card

    def build_search_section(self):
        """Build main search section"""
        search_card = ModernCard(
            elevation=2,
            size_hint_y=None,
            height=dp(180)
        )

        # Add icon and title explicitly
        icon_row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(32), spacing=dp(8))
        icon_row.add_widget(MDIconButton(icon='magnify', theme_icon_color="Custom", icon_color=DesignTokens.COLORS['primary']))
        icon_row.add_widget(MDLabel(
            text=language_manager.get_text('quick_search'),
            font_style="H6",
            halign="left"
        ))
        search_card.add_widget(icon_row)

        search_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=[dp(20), dp(10)]
        )

        # Search input
        self.search_input = MDTextField(
            hint_text=language_manager.get_text('search_properties_owners'),
            helper_text=language_manager.get_text('search_hint'),
            helper_text_mode="on_focus",
            icon_right="magnify",
            size_hint_y=None,
            height=dp(60)
        )
        self.search_input.bind(text=self.on_search_text_change)
        search_layout.add_widget(self.search_input)

        # Search buttons
        buttons_layout = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(40))

        search_btn = MDRaisedButton(
            text=language_manager.get_text('search'),
            md_bg_color=DesignTokens.COLORS['primary'],
            on_release=self.perform_search
        )
        buttons_layout.add_widget(search_btn)

        clear_btn = MDFlatButton(
            text=language_manager.get_text('clear'),
            on_release=self.clear_search
        )
        buttons_layout.add_widget(clear_btn)

        buttons_layout.add_widget(MDLabel())  # Spacer

        search_layout.add_widget(buttons_layout)
        search_card.add_widget(search_layout)
        return search_card

    def build_filters_section(self):
        """Build advanced filters section"""
        filters_card = ModernCard(
            elevation=2,
            size_hint_y=None,
            height=dp(300)
        )

        # Add icon and title explicitly
        icon_row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(32), spacing=dp(8))
        icon_row.add_widget(MDIconButton(icon='filter-variant', theme_icon_color="Custom", icon_color=DesignTokens.COLORS['primary']))
        icon_row.add_widget(MDLabel(
            text=language_manager.get_text('advanced_filters'),
            font_style="H6",
            halign="left"
        ))
        filters_card.add_widget(icon_row)

        filters_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=[dp(20), dp(10)]
        )

        # Property Type Filter
        type_layout = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(60))
        type_layout.add_widget(MDLabel(
            text=language_manager.get_text('property_type'),
            size_hint_x=None,
            width=dp(120),
            theme_text_color="Primary"
        ))

        self.type_chips_layout = MDBoxLayout(spacing=dp(5))
        property_types = ['Apartment', 'House', 'Commercial', 'Land']
        for prop_type in property_types:
            chip = MDChip(
                type="filter",
                on_release=lambda x, pt=prop_type: self.toggle_filter_chip(x, 'type', pt)
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
        status_layout = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(60))
        status_layout.add_widget(MDLabel(
            text=language_manager.get_text('status'),
            size_hint_x=None,
            width=dp(120),
            theme_text_color="Primary"
        ))

        self.status_chips_layout = MDBoxLayout(spacing=dp(5))
        statuses = ['Available', 'Occupied', 'Maintenance']
        for status in statuses:
            chip = MDChip(
                type="filter",
                on_release=lambda x, s=status: self.toggle_filter_chip(x, 'status', s)
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
        price_layout = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(60))
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
            width=dp(100)
        )
        price_layout.add_widget(self.min_price_input)

        price_layout.add_widget(MDLabel(text="-", size_hint_x=None, width=dp(20)))

        self.max_price_input = MDTextField(
            hint_text=language_manager.get_text('max_price'),
            input_filter="float",
            size_hint_x=None,
            width=dp(100)
        )
        price_layout.add_widget(self.max_price_input)

        filters_layout.add_widget(price_layout)

        # Apply Filters Button
        apply_filters_btn = MDRaisedButton(
            text=language_manager.get_text('apply_filters'),
            md_bg_color=DesignTokens.COLORS['secondary'],
            size_hint_y=None,
            height=dp(40),
            on_release=self.apply_filters
        )
        filters_layout.add_widget(apply_filters_btn)

        filters_card.add_widget(filters_layout)
        return filters_card

    def build_results_section(self):
        """Build search results section"""
        self.results_card = ModernCard(
            elevation=2,
            size_hint_y=None,
            height=dp(400)
        )

        # Add icon and title explicitly
        icon_row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(32), spacing=dp(8))
        icon_row.add_widget(MDIconButton(icon='format-list-bulleted', theme_icon_color="Custom", icon_color=DesignTokens.COLORS['primary']))
        icon_row.add_widget(MDLabel(
            text=language_manager.get_text('search_results'),
            font_style="H6",
            halign="left"
        ))
        self.results_card.add_widget(icon_row)

        # Results will be populated by search
        self.results_list = MDList()
        results_scroll = MDScrollView()
        results_scroll.add_widget(self.results_list)

        self.results_card.add_widget(results_scroll)
        return self.results_card

    def build_reports_section(self):
        """Build reports generation section"""
        reports_card = ModernCard(
            elevation=2,
            size_hint_y=None,
            height=dp(200)
        )

        # Add icon and title explicitly
        icon_row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(32), spacing=dp(8))
        icon_row.add_widget(MDIconButton(icon='file-document-outline', theme_icon_color="Custom", icon_color=DesignTokens.COLORS['primary']))
        icon_row.add_widget(MDLabel(
            text=language_manager.get_text('generate_reports'),
            font_style="H6",
            halign="left"
        ))
        reports_card.add_widget(icon_row)

        reports_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=[dp(20), dp(10)]
        )
        report_buttons_layout = MDGridLayout(cols=2, spacing=dp(10))

        # Properties Report
        properties_report_btn = MDRaisedButton(
            text=language_manager.get_text('properties_report'),
            on_release=lambda x: self.generate_report('properties')
        )
        report_buttons_layout.add_widget(properties_report_btn)

        # Owners Report
        owners_report_btn = MDRaisedButton(
            text=language_manager.get_text('owners_report'),
            on_release=lambda x: self.generate_report('owners')
        )
        report_buttons_layout.add_widget(owners_report_btn)

        # Financial Report
        financial_report_btn = MDRaisedButton(
            text=language_manager.get_text('financial_report'),
            on_release=lambda x: self.generate_report('financial')
        )
        report_buttons_layout.add_widget(financial_report_btn)

        # Custom Report
        custom_report_btn = MDRaisedButton(
            text=language_manager.get_text('custom_report'),
            on_release=lambda x: self.generate_report('custom')
        )
        report_buttons_layout.add_widget(custom_report_btn)

        reports_layout.add_widget(report_buttons_layout)
        reports_card.add_widget(reports_layout)
        return reports_card

    def load_initial_data(self):
        """Load initial data for the screen"""
        try:
            # Load all properties for search
            self.all_properties = self.db.get_properties()  # returns list of dicts
            self.all_owners = self.db.get_owners()  # returns list of tuples

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

            self.results_list.add_widget(list_item)

        # Update results count
        self.results_card.title = f"{language_manager.get_text('search_results')} ({len(results)})"

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
