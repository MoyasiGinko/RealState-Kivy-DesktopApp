#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Enhanced Data Table
Modern, responsive data table with sorting, filtering, and pagination
"""

from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.metrics import dp
from kivy.animation import Animation
from typing import List, Dict, Any, Callable, Optional
import logging

from app.views.modern_components import DesignTokens, ModernCard
from app.language_manager import language_manager

logger = logging.getLogger(__name__)


class EnhancedDataTableHeader(MDBoxLayout):
    """Enhanced table header with sorting and filtering"""

    def __init__(self, columns: List[Dict], on_sort: Callable = None,
                 on_filter: Callable = None, **kwargs):
        super().__init__(**kwargs)

        self.columns = columns
        self.on_sort = on_sort
        self.on_filter = on_filter
        self.sort_column = None
        self.sort_direction = 'asc'

        self.orientation = 'vertical'
        self.adaptive_height = True
        self.spacing = DesignTokens.SPACING['xs']

        self.build_header()

    def build_header(self):
        """Build table header with controls"""
        # Filter row
        self.build_filter_row()

        # Header row
        self.build_header_row()

    def build_filter_row(self):
        """Build filter controls"""
        filter_container = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['sm'],
            size_hint_y=None,
            height=dp(50),
            md_bg_color=DesignTokens.COLORS['surface']
        )

        # Search field
        self.search_field = MDTextField(
            hint_text=language_manager.get_text('search_table'),
            mode="outlined",
            size_hint_x=0.4,
            size_hint_y=None,
            height=dp(40),
            line_color_normal=DesignTokens.COLORS['divider'],
            line_color_focus=DesignTokens.COLORS['primary']
        )
        self.search_field.bind(text=self.on_search_change)
        filter_container.add_widget(self.search_field)

        # Column filter dropdown
        self.filter_dropdown = MDTextField(
            hint_text=language_manager.get_text('filter_by_column'),
            mode="outlined",
            readonly=True,
            size_hint_x=0.3,
            size_hint_y=None,
            height=dp(40)
        )

        filter_items = [
            {
                "text": col.get('title', col.get('field', '')),
                "viewclass": "OneLineListItem",
                "on_release": lambda x=col['field']: self.select_filter_column(x),
            } for col in self.columns
        ]

        self.filter_menu = MDDropdownMenu(
            caller=self.filter_dropdown,
            items=filter_items,
        )

        self.filter_dropdown.bind(on_release=self.filter_menu.open)
        filter_container.add_widget(self.filter_dropdown)

        # Clear filters button
        clear_btn = MDIconButton(
            icon="filter-remove",
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['text_secondary'],
            on_release=self.clear_filters
        )
        filter_container.add_widget(clear_btn)

        self.add_widget(filter_container)

    def build_header_row(self):
        """Build main header row with column titles"""
        header_row = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            md_bg_color=DesignTokens.COLORS['primary']
        )

        # Selection checkbox
        self.select_all_checkbox = MDCheckbox(
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            theme_icon_color="Custom",
            icon_color_active=DesignTokens.COLORS['card'],
            on_active=self.on_select_all
        )
        header_row.add_widget(self.select_all_checkbox)

        # Column headers
        for col in self.columns:
            header_cell = self.build_header_cell(col)
            header_row.add_widget(header_cell)

        # Actions column
        actions_header = MDLabel(
            text=language_manager.get_text('actions'),
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['card'],
            font_style="Subtitle2",
            bold=True,
            size_hint_x=0.15,
            halign="center"
        )
        header_row.add_widget(actions_header)

        self.add_widget(header_row)

    def build_header_cell(self, column: Dict) -> MDBoxLayout:
        """Build individual header cell with sorting"""
        cell = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['xs'],
            size_hint_x=column.get('width', 1.0)
        )

        # Column title
        title_label = MDLabel(
            text=column.get('title', column.get('field', '')),
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['card'],
            font_style="Subtitle2",
            bold=True
        )
        cell.add_widget(title_label)

        # Sort button
        if column.get('sortable', True):
            sort_icon = "arrow-up-down"
            if self.sort_column == column['field']:
                sort_icon = "arrow-up" if self.sort_direction == 'asc' else "arrow-down"

            sort_btn = MDIconButton(
                icon=sort_icon,
                theme_icon_color="Custom",
                icon_color=DesignTokens.COLORS['card'],
                icon_size=dp(20),
                on_release=lambda x, field=column['field']: self.sort_by_column(field)
            )
            cell.add_widget(sort_btn)

        return cell

    def sort_by_column(self, field: str):
        """Handle column sorting"""
        if self.sort_column == field:
            self.sort_direction = 'desc' if self.sort_direction == 'asc' else 'asc'
        else:
            self.sort_column = field
            self.sort_direction = 'asc'

        # Rebuild header to update sort icons
        self.clear_widgets()
        self.build_header()

        # Trigger sort callback
        if self.on_sort:
            self.on_sort(field, self.sort_direction)

    def select_filter_column(self, field: str):
        """Select filter column"""
        column_title = next((col['title'] for col in self.columns if col['field'] == field), field)
        self.filter_dropdown.text = column_title
        self.filter_menu.dismiss()

        if self.on_filter:
            self.on_filter(field, self.search_field.text)

    def on_search_change(self, instance, text):
        """Handle search text changes"""
        if self.on_filter:
            filter_field = None
            if self.filter_dropdown.text:
                filter_field = next((col['field'] for col in self.columns
                                   if col['title'] == self.filter_dropdown.text), None)
            self.on_filter(filter_field, text)

    def clear_filters(self, instance):
        """Clear all filters"""
        self.search_field.text = ""
        self.filter_dropdown.text = ""
        if self.on_filter:
            self.on_filter(None, "")

    def on_select_all(self, instance, active):
        """Handle select all checkbox"""
        # This will be handled by the parent table
        pass


class EnhancedDataTableRow(MDBoxLayout):
    """Enhanced table row with selection and actions"""

    def __init__(self, data: Dict, columns: List[Dict],
                 on_select: Callable = None, on_action: Callable = None,
                 actions: List[Dict] = None, **kwargs):
        super().__init__(**kwargs)

        self.data = data
        self.columns = columns
        self.on_select = on_select
        self.on_action = on_action
        self.actions = actions or []
        self.selected = False

        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.spacing = DesignTokens.SPACING['xs']

        # Alternate row colors
        self.md_bg_color = DesignTokens.COLORS['card']

        self.build_row()

    def build_row(self):
        """Build table row"""
        # Selection checkbox
        self.checkbox = MDCheckbox(
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            theme_icon_color="Custom",
            icon_color_active=DesignTokens.COLORS['primary'],
            on_active=self.on_row_select
        )
        self.add_widget(self.checkbox)

        # Data cells
        for col in self.columns:
            cell_value = str(self.data.get(col['field'], ''))
            cell = self.build_data_cell(cell_value, col)
            self.add_widget(cell)

        # Actions cell
        self.build_actions_cell()

    def build_data_cell(self, value: str, column: Dict) -> MDLabel:
        """Build individual data cell"""
        # Truncate long text
        display_value = value
        if len(display_value) > 30:
            display_value = display_value[:27] + "..."

        cell = MDLabel(
            text=display_value,
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_primary'],
            font_style="Body2",
            size_hint_x=column.get('width', 1.0),
            valign="center"
        )

        # Add tooltip for long text
        if len(value) > 30:
            cell.tooltip_text = value

        return cell

    def build_actions_cell(self):
        """Build actions cell with buttons"""
        actions_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['xs'],
            size_hint_x=0.15
        )

        # Default actions if none provided
        if not self.actions:
            self.actions = [
                {'icon': 'pencil', 'action': 'edit', 'tooltip': 'Edit'},
                {'icon': 'delete', 'action': 'delete', 'tooltip': 'Delete'}
            ]

        for action in self.actions:
            btn = MDIconButton(
                icon=action['icon'],
                theme_icon_color="Custom",
                icon_color=DesignTokens.COLORS['text_secondary'],
                icon_size=dp(20),
                on_release=lambda x, act=action['action']: self.trigger_action(act)
            )
            actions_layout.add_widget(btn)

        self.add_widget(actions_layout)

    def on_row_select(self, instance, active):
        """Handle row selection"""
        self.selected = active        # Visual feedback
        if active:
            self.md_bg_color = (DesignTokens.COLORS['primary'][0], DesignTokens.COLORS['primary'][1], DesignTokens.COLORS['primary'][2], 0.1)
        else:
            self.md_bg_color = DesignTokens.COLORS['card']

        if self.on_select:
            self.on_select(self.data, active)

    def trigger_action(self, action: str):
        """Trigger row action"""
        if self.on_action:
            self.on_action(action, self.data)


class EnhancedDataTable(ModernCard):
    """Enhanced data table with all modern features"""

    def __init__(self, columns: List[Dict], data: List[Dict] = None,
                 on_row_select: Callable = None, on_row_action: Callable = None,
                 pagination: bool = True, page_size: int = 10, **kwargs):
        super().__init__(**kwargs)

        self.columns = columns
        self.original_data = data or []
        self.filtered_data = self.original_data.copy()
        self.displayed_data = []
        self.on_row_select = on_row_select
        self.on_row_action = on_row_action
        self.pagination = pagination
        self.page_size = page_size
        self.current_page = 1
        self.selected_rows = []

        self.build_table()
        self.update_display()

    def build_table(self):
        """Build complete table structure"""
        # Table header
        self.header = EnhancedDataTableHeader(
            columns=self.columns,
            on_sort=self.sort_data,
            on_filter=self.filter_data
        )
        self.add_widget(self.header)

        # Table content (scrollable)
        self.content_scroll = MDScrollView()
        self.content_layout = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            spacing=dp(1)
        )
        self.content_scroll.add_widget(self.content_layout)
        self.add_widget(self.content_scroll)

        # Pagination controls
        if self.pagination:
            self.build_pagination_controls()

    def build_pagination_controls(self):
        """Build pagination controls"""
        pagination_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=DesignTokens.SPACING['md'],
            md_bg_color=DesignTokens.COLORS['surface']
        )

        # Previous button
        self.prev_btn = MDIconButton(
            icon="chevron-left",
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['primary'],
            disabled=True,
            on_release=self.previous_page
        )
        pagination_layout.add_widget(self.prev_btn)

        # Page info
        self.page_info = MDLabel(
            text="",
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_primary'],
            font_style="Body2",
            halign="center"
        )
        pagination_layout.add_widget(self.page_info)

        # Next button
        self.next_btn = MDIconButton(
            icon="chevron-right",
            theme_icon_color="Custom",
            icon_color=DesignTokens.COLORS['primary'],
            on_release=self.next_page
        )
        pagination_layout.add_widget(self.next_btn)

        self.add_widget(pagination_layout)

    def update_display(self):
        """Update table display with current data"""
        # Clear existing rows
        self.content_layout.clear_widgets()

        # Calculate pagination
        if self.pagination:
            start_idx = (self.current_page - 1) * self.page_size
            end_idx = start_idx + self.page_size
            self.displayed_data = self.filtered_data[start_idx:end_idx]
        else:
            self.displayed_data = self.filtered_data

        # Add data rows
        for i, row_data in enumerate(self.displayed_data):
            row = EnhancedDataTableRow(
                data=row_data,
                columns=self.columns,
                on_select=self.on_row_selected,
                on_action=self.on_row_action
            )

            # Alternate row colors
            if i % 2 == 1:
                row.md_bg_color = DesignTokens.COLORS['surface']

            self.content_layout.add_widget(row)

        # Update pagination controls
        if self.pagination:
            self.update_pagination_controls()

    def update_pagination_controls(self):
        """Update pagination control states"""
        total_pages = max(1, (len(self.filtered_data) + self.page_size - 1) // self.page_size)

        self.prev_btn.disabled = self.current_page <= 1
        self.next_btn.disabled = self.current_page >= total_pages

        start_item = (self.current_page - 1) * self.page_size + 1
        end_item = min(self.current_page * self.page_size, len(self.filtered_data))

        self.page_info.text = f"{start_item}-{end_item} of {len(self.filtered_data)} items"

    def sort_data(self, field: str, direction: str):
        """Sort table data"""
        reverse = direction == 'desc'
        self.filtered_data.sort(key=lambda x: str(x.get(field, '')), reverse=reverse)
        self.current_page = 1
        self.update_display()

    def filter_data(self, field: Optional[str], search_text: str):
        """Filter table data"""
        if not search_text:
            self.filtered_data = self.original_data.copy()
        else:
            search_lower = search_text.lower()
            if field:
                # Filter by specific field
                self.filtered_data = [
                    row for row in self.original_data
                    if search_lower in str(row.get(field, '')).lower()
                ]
            else:
                # Search all fields
                self.filtered_data = [
                    row for row in self.original_data
                    if any(search_lower in str(value).lower()
                          for value in row.values())
                ]

        self.current_page = 1
        self.update_display()

    def on_row_selected(self, row_data: Dict, selected: bool):
        """Handle row selection"""
        if selected:
            if row_data not in self.selected_rows:
                self.selected_rows.append(row_data)
        else:
            if row_data in self.selected_rows:
                self.selected_rows.remove(row_data)

        if self.on_row_select:
            self.on_row_select(row_data, selected)

    def previous_page(self, instance):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.update_display()

    def next_page(self, instance):
        """Go to next page"""
        total_pages = (len(self.filtered_data) + self.page_size - 1) // self.page_size
        if self.current_page < total_pages:
            self.current_page += 1
            self.update_display()

    def update_data(self, new_data: List[Dict]):
        """Update table with new data"""
        self.original_data = new_data
        self.filtered_data = new_data.copy()
        self.current_page = 1
        self.selected_rows.clear()
        self.update_display()

    def get_selected_rows(self) -> List[Dict]:
        """Get all selected rows"""
        return self.selected_rows.copy()

    def clear_selection(self):
        """Clear all selections"""
        self.selected_rows.clear()
        self.update_display()
