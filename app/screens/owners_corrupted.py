#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Enhanced Owners Management Screen
"""

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Line
import logging

from app.components import (RTLLabel, CustomActionButton as ActionButton, FormField, DataTable,
                            ConfirmDialog, MessageDialog, SearchBox, BilingualLabel, TranslatableButton,
                            NavigationHeader, ResponsiveCard, BilingualButton)
from app.database import DatabaseManager
from app.utils import DataValidator
from app.font_manager import font_manager
from app.language_manager import language_manager
from app.config import config

logger = logging.getLogger(__name__)


class EnhancedFormCard(BoxLayout):
    """Enhanced form card with modern styling"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(15)
        self.padding = [25, 20]
        self.size_hint_y = None
        self.height = dp(350)

        # Add modern background with gradient
        with self.canvas.before:
            Color(0.98, 0.99, 1, 1)  # Very light blue
            self.bg_rect = RoundedRectangle(radius=[12])
            self.bind(size=self._update_bg, pos=self._update_bg)

            # Add subtle border
            Color(0.8, 0.85, 0.9, 1)
            self.border = Line(rounded_rectangle=[0, 0, 0, 0, 12], width=1)
            self.bind(size=self._update_border, pos=self._update_border)

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def _update_border(self, *args):
        self.border.rounded_rectangle = [*self.pos, *self.size, 12]


class EnhancedDataList(BoxLayout):
    """Enhanced data list with modern pagination"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = [15, 15]

        # Add background
        with self.canvas.before:
            Color(0.99, 0.99, 0.99, 1)
            self.bg_rect = RoundedRectangle(radius=[12])
            self.bind(size=self._update_bg, pos=self._update_bg)

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos


class OwnersScreen(Screen):
    """Enhanced Owners Management Screen with Top Form and Bottom List"""

    def __init__(self, db_manager: DatabaseManager, **kwargs):
        super().__init__(**kwargs)
        self.name = 'owners'
        self.db = db_manager
        self.current_owner = None
        self.owners_data = []

        self.build_modern_ui()
        self.load_owners()

    def build_modern_ui(self):
        """Build the enhanced modern owners management UI"""
        # Main scrollable container
        main_scroll = ScrollView()
        main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(25),
            padding=[25, 20, 25, 25],
            size_hint_y=None
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))

        # Enhanced Header Section
        self.build_header_section(main_layout)

        # Enhanced Form Section (Top)
        self.build_form_section(main_layout)

        # Enhanced List Section (Bottom)
        self.build_list_section(main_layout)

        main_scroll.add_widget(main_layout)
        self.add_widget(main_scroll)

    def build_header_section(self, main_layout):
        """Build enhanced header with navigation and controls"""
        header_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(70),
            spacing=20,
            padding=[0, 10]
        )

        # Add gradient background
        with header_layout.canvas.before:
            Color(0.1, 0.4, 0.7, 1)  # Blue gradient
            self.header_bg = RoundedRectangle(radius=[15])
            header_layout.bind(
                size=lambda *args: setattr(self.header_bg, 'size', header_layout.size),
                pos=lambda *args: setattr(self.header_bg, 'pos', header_layout.pos)
            )

        # Back button
        back_btn = BilingualButton(
            translation_key='back_to_dashboard',
            background_color=[0.9, 0.9, 0.9, 1],
            color=[0.2, 0.2, 0.2, 1],
            size_hint=(None, None),
            size=(dp(170), dp(45))
        )
        back_btn.bind(on_press=self.go_back)
        header_layout.add_widget(back_btn)

        # Title
        title = BilingualLabel(
            translation_key='owners_management',
            font_size='26sp',
            bold=True,
            color=[1, 1, 1, 1],
            halign='center'
        )
        header_layout.add_widget(title)

        # Search section
        search_layout = BoxLayout(
            size_hint=(None, None),
            size=(dp(250), dp(50)),
            spacing=10
        )

        self.search_input = TextInput(
            hint_text=language_manager.get_text('search_owners'),
            size_hint_y=None,
            height=dp(40),
            multiline=False,
            font_size='14sp'
        )
        self.search_input.bind(text=self.on_search_text)
        search_layout.add_widget(self.search_input)

        header_layout.add_widget(search_layout)
        main_layout.add_widget(header_layout)

    def build_form_section(self, main_layout):
        """Build enhanced form section at the top"""
        # Form section with title
        form_section = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None,
            height=dp(420)
        )

        # Section title
        section_title = BilingualLabel(
            translation_key='owner_information_form',
            font_size='20sp',
            bold=True,
            color=[0.2, 0.2, 0.2, 1],
            size_hint_y=None,
            height=dp(40),
            halign='center'
        )
        form_section.add_widget(section_title)

        # Enhanced form card
        form_card = EnhancedFormCard()

        # Form fields in grid layout
        form_grid = GridLayout(
            cols=2,
            spacing=dp(15),
            size_hint_y=None,
            height=dp(200)
        )

        # Owner Code (auto-generated, read-only)
        self.owner_code_field = FormField(
            language_manager.get_text('owner_code'),
            required=True
        )
        self.owner_code_field.input.readonly = True
        self.owner_code_field.input.text = self.db.generate_owner_code()
        form_grid.add_widget(self.owner_code_field)

        # Owner Name
        self.owner_name_field = FormField(
            language_manager.get_text('owner_name'),
            required=True
        )
        form_grid.add_widget(self.owner_name_field)

        # Owner Phone
        self.owner_phone_field = FormField(
            language_manager.get_text('phone')
        )
        form_grid.add_widget(self.owner_phone_field)

        # Owner Email
        self.owner_email_field = FormField(
            language_manager.get_text('email')
        )
        form_grid.add_widget(self.owner_email_field)

        form_card.add_widget(form_grid)

        # Notes field (full width)
        self.notes_field = FormField(
            language_manager.get_text('notes'),
            input_type='multiline'
        )
        self.notes_field.size_hint_y = None
        self.notes_field.height = dp(80)
        form_card.add_widget(self.notes_field)

        # Action buttons
        self.build_action_buttons(form_card)

        form_section.add_widget(form_card)
        main_layout.add_widget(form_section)

    def build_action_buttons(self, form_card):
        """Build enhanced action buttons"""
        button_layout = GridLayout(
            cols=4,
            spacing=dp(15),
            size_hint_y=None,
            height=dp(50)
        )

        # Save button
        self.save_btn = BilingualButton(
            translation_key='save_owner',
            background_color=[0.2, 0.7, 0.3, 1],
            font_size='16sp'
        )
        self.save_btn.bind(on_press=self.save_owner)
        button_layout.add_widget(self.save_btn)

        # Update button
        self.update_btn = BilingualButton(
            translation_key='update_owner',
            background_color=[0.8, 0.6, 0.1, 1],
            font_size='16sp'
        )
        self.update_btn.bind(on_press=self.update_owner)
        self.update_btn.disabled = True
        button_layout.add_widget(self.update_btn)

        # Delete button
        self.delete_btn = BilingualButton(
            translation_key='delete_owner',
            background_color=[0.8, 0.3, 0.3, 1],
            font_size='16sp'
        )
        self.delete_btn.bind(on_press=self.delete_owner)
        self.delete_btn.disabled = True
        button_layout.add_widget(self.delete_btn)

        # Clear button
        self.clear_btn = BilingualButton(
            translation_key='clear_form',
            background_color=[0.6, 0.6, 0.6, 1],
            font_size='16sp'
        )
        self.clear_btn.bind(on_press=self.clear_form)
        button_layout.add_widget(self.clear_btn)

        form_card.add_widget(button_layout)

    def build_list_section(self, main_layout):
        """Build enhanced list section at the bottom"""
        list_section = BoxLayout(
            orientation='vertical',
            spacing=dp(15)
        )

        # List title with count
        list_header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=10
        )

        list_title = BilingualLabel(
            translation_key='owners_list',
            font_size='20sp',
            bold=True,
            color=[0.2, 0.2, 0.2, 1],
            size_hint_x=0.7
        )
        list_header.add_widget(list_title)

        # Records count
        self.count_label = RTLLabel(
            text='',
            font_size='14sp',
            color=[0.5, 0.5, 0.5, 1],
            size_hint_x=0.3,
            halign='right'
        )
        list_header.add_widget(self.count_label)

        list_section.add_widget(list_header)        # Enhanced data list container
        data_container = EnhancedDataList()        # Data table
        table_columns = [
            {'title': language_manager.get_text('owner_code'), 'field': 'Ownercode'},
            {'title': language_manager.get_text('owner_name'), 'field': 'ownername'},
            {'title': language_manager.get_text('phone'), 'field': 'ownerphone'},
            {'title': language_manager.get_text('notes'), 'field': 'Note'}
        ]

        self.owners_table = DataTable(
            columns=table_columns,
            row_callback=self.select_owner
        )
        data_container.add_widget(self.owners_table)        # Statistics label
        self.stats_label = RTLLabel(
            text='',
            size_hint_y=None,
            height=dp(30),
            font_size='14sp',
            color=[0.5, 0.5, 0.5, 1]
        )
        data_container.add_widget(self.stats_label)

        list_section.add_widget(data_container)
        main_layout.add_widget(list_section)

        def create_data_row(self, owner_data, index):
        """Create enhanced data row"""
        row_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10),
            padding=[15, 10]
        )

        # Alternate row colors
        bg_color = [0.98, 0.98, 0.98, 1] if index % 2 == 0 else [1, 1, 1, 1]
        with row_layout.canvas.before:
            Color(*bg_color)
            bg = RoundedRectangle(radius=[6])
            row_layout.bg = bg
            row_layout.bind(
                size=lambda *args: setattr(bg, 'size', row_layout.size),
                pos=lambda *args: setattr(bg, 'pos', row_layout.pos)
            )

        # Owner code
        code_label = RTLLabel(
            text=str(owner_data.get('Owner-code', '')),
            font_size='14sp',
            size_hint_x=0.2,
            color=[0.2, 0.2, 0.2, 1]
        )
        row_layout.add_widget(code_label)

        # Owner name
        name_label = RTLLabel(
            text=str(owner_data.get('Owner-name', '')),
            font_size='14sp',
            size_hint_x=0.3,
            color=[0.2, 0.2, 0.2, 1]
        )
        row_layout.add_widget(name_label)

        # Phone
        phone_label = RTLLabel(
            text=str(owner_data.get('Phone', '')),
            font_size='14sp',
            size_hint_x=0.25,
            color=[0.2, 0.2, 0.2, 1]
        )
        row_layout.add_widget(phone_label)

        # Actions
        actions_layout = BoxLayout(
            orientation='horizontal',
            size_hint_x=0.25,
            spacing=dp(5)
        )

        # Edit button
        edit_btn = Button(
            text='✎',
            size_hint=(None, None),
            size=(dp(35), dp(35)),
            background_color=[0.1, 0.6, 0.9, 1]
        )
        edit_btn.bind(on_press=lambda x: self.edit_owner(owner_data))
        actions_layout.add_widget(edit_btn)        # Delete button
        del_btn = Button(
            text='✖',
            size_hint=(None, None),
            size=(dp(35), dp(35)),
            background_color=[0.9, 0.3, 0.3, 1]
        )
        del_btn.bind(on_press=lambda x: self.confirm_delete_owner(owner_data))
        actions_layout.add_widget(del_btn)

        row_layout.add_widget(actions_layout)
        return row_layout

        # Right panel - Data table in responsive card
        right_panel = ResponsiveCard(
            orientation='vertical',
            size_hint_x=0.6,
            spacing=dp(15),
            padding=dp(20)
        )

        # Table title
        right_panel.add_widget(BilingualLabel(
            translation_key='owners_list',
            font_size=dp(18),
            bold=True,
            size_hint_y=None,
            height=dp(40),
            halign='center'
        ))

        # Search box
        self.search_box = SearchBox(search_callback=self.search_owners)
        right_panel.add_widget(self.search_box)

        # Data table
        table_columns = [
            {'title': language_manager.get_text('owner_code'), 'field': 'Ownercode'},
            {'title': language_manager.get_text('owner_name'), 'field': 'ownername'},
            {'title': language_manager.get_text('phone'), 'field': 'ownerphone'},
            {'title': language_manager.get_text('notes'), 'field': 'Note'}
        ]

        self.owners_table = DataTable(
            columns=table_columns,
            row_callback=self.select_owner
        )
        right_panel.add_widget(self.owners_table)

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

    def load_owners(self):
        """Load all owners from database"""
        try:
            self.owners_data = self.db.get_owners()
            self.owners_table.update_data([{
                'Ownercode': owner[0],
                'ownername': owner[1],
                'ownerphone': owner[2] or '',
                'Note': owner[3] or ''
            } for owner in self.owners_data])

            # Update statistics
            self.update_stats()

        except Exception as e:
            logger.error(f"Error loading owners: {e}")
            self.show_message(
                language_manager.get_text('error'),
                f'{language_manager.get_text("error_loading_data")}: {str(e)}',
                'error'
            )

    def on_search_text(self, instance, text):
        """Handle search text changes with debouncing"""
        # Cancel previous search if any
        if hasattr(self, '_search_clock'):
            self._search_clock.cancel()        # Schedule new search with delay
        self._search_clock = Clock.schedule_once(
            lambda dt: self.perform_search(text), 0.5
        )

    def perform_search(self, search_text):
        """Perform the actual search"""
        try:
            if search_text.strip():
                # Filter owners based on search text
                filtered_owners = []
                for owner in self.owners_data:
                    search_lower = search_text.lower()
                    owner_name = owner[1].lower() if owner[1] else ''
                    owner_code = owner[0].lower() if owner[0] else ''
                    owner_phone = owner[2].lower() if owner[2] else ''

                    if (search_lower in owner_name or
                        search_lower in owner_code or
                        search_lower in owner_phone):
                        filtered_owners.append(owner)

                self.display_owners(filtered_owners)
            else:
                # Show all owners if search is empty
                self.load_owners()
        except Exception as e:
            logger.error(f"Error performing search: {e}")

    def display_owners(self, owners):
        """Display filtered owners in the table"""
        try:
            self.owners_table.update_data([{
                'Ownercode': owner[0],
                'ownername': owner[1],
                'ownerphone': owner[2] or '',
                'Note': owner[3] or ''
            } for owner in owners])

        except Exception as e:
            logger.error(f"Error displaying owners: {e}")

    def select_owner(self, owner_data: dict):
        """Select owner for editing"""
        try:
            self.current_owner = owner_data

            # Populate form
            self.owner_code_field.set_value(owner_data['Ownercode'])
            self.owner_name_field.set_value(owner_data['ownername'])
            self.owner_phone_field.set_value(owner_data['ownerphone'])
            self.notes_field.set_value(owner_data['Note'])

            # Enable update/delete buttons
            self.update_btn.disabled = False
            self.delete_btn.disabled = False
            self.save_btn.disabled = True

        except Exception as e:
            logger.error(f"Error selecting owner: {e}")

    def save_owner(self):
        """Save new owner"""
        try:
            # Validate form
            if not self.validate_form():
                return

            # Get form data
            owner_name = self.owner_name_field.get_value().strip()
            owner_phone = self.owner_phone_field.get_value().strip()
            notes = self.notes_field.get_value().strip()

            # Save to database
            owner_code = self.db.add_owner(owner_name, owner_phone, notes)

            if owner_code:
                self.show_message(
                    language_manager.get_text('success'),
                    language_manager.get_text('operation_successful'),
                    'success'
                )
                self.clear_form()
                self.load_owners()
            else:
                self.show_message(
                    language_manager.get_text('error'),
                    language_manager.get_text('save_failed'),
                    'error'
                )

        except Exception as e:
            logger.error(f"Error saving owner: {e}")
            self.show_message(
                language_manager.get_text('error'),
                f'{language_manager.get_text("save_failed")}: {str(e)}',
                'error'
            )
            logger.error(f"Error saving owner: {e}")
            self.show_message(
                language_manager.get_text('error'),
                f'{language_manager.get_text("save_failed")}: {str(e)}',
                'error'
            )

    def update_owner(self):
        """Update existing owner"""
        try:
            if not self.current_owner:
                return

            # Validate form
            if not self.validate_form():
                return

            # Get form data
            owner_code = self.owner_code_field.get_value()
            owner_name = self.owner_name_field.get_value().strip()
            owner_phone = self.owner_phone_field.get_value().strip()
            notes = self.notes_field.get_value().strip()

            # Update in database
            if self.db.update_owner(owner_code, owner_name, owner_phone, notes):
                self.show_message(
                    language_manager.get_text('success'),
                    language_manager.get_text('operation_successful'),
                    'success'
                )
                self.clear_form()
                self.load_owners()
            else:
                self.show_message(
                    language_manager.get_text('error'),
                    language_manager.get_text('update_failed'),
                    'error'
                )

        except Exception as e:
            logger.error(f"Error updating owner: {e}")
            self.show_message(
                language_manager.get_text('error'),
                f'{language_manager.get_text("update_failed")}: {str(e)}',
                'error'
            )

    def delete_owner(self):
        """Delete selected owner"""
        if not self.current_owner:
            return

        # Show confirmation dialog
        confirm_dialog = ConfirmDialog(
            title=language_manager.get_text('confirm_delete'),
            message=f'{language_manager.get_text("confirm_delete")} "{self.current_owner["ownername"]}"?',
            confirm_callback=self._confirm_delete
        )
        confirm_dialog.open()

    def _confirm_delete(self):
        """Confirm owner deletion"""
        try:
            owner_code = self.current_owner['Ownercode']

            if self.db.delete_owner(owner_code):
                self.show_message(
                    language_manager.get_text('success'),
                    language_manager.get_text('operation_successful'),
                    'success'
                )
                self.clear_form()
                self.load_owners()
            else:
                self.show_message(
                    language_manager.get_text('error'),
                    language_manager.get_text('cannot_delete_owner_has_properties'),
                    'warning'
                )

        except Exception as e:
            logger.error(f"Error deleting owner: {e}")
            self.show_message(
                language_manager.get_text('error'),
                f'{language_manager.get_text("delete_failed")}: {str(e)}',
                'error'
            )

    def clear_form(self):
        """Clear the form"""
        self.current_owner = None

        # Generate new owner code
        self.owner_code_field.set_value(self.db.generate_owner_code())
        self.owner_name_field.clear()
        self.owner_phone_field.clear()
        self.notes_field.clear()

        # Reset button states
        self.save_btn.disabled = False
        self.update_btn.disabled = True
        self.delete_btn.disabled = True

    def validate_form(self) -> bool:
        """Validate form data"""
        # Check required fields
        if not self.owner_name_field.get_value().strip():
            self.show_message(
                language_manager.get_text('error'),
                language_manager.get_text('owner_name_required'),
                'warning'
            )
            return False

        # Validate phone number
        phone = self.owner_phone_field.get_value().strip()
        if phone and not DataValidator.validate_phone(phone):
            self.show_message(
                language_manager.get_text('error'),
                language_manager.get_text('invalid_phone'),
                'warning'
            )
            return False

        return True

    def update_stats(self):
        """Update statistics display"""
        try:
            total_owners = len(self.owners_data)
            self.stats_label.text = f'{language_manager.get_text("total_owners")}: {total_owners}'
        except Exception as e:
            logger.error(f"Error updating stats: {e}")    def show_message(self, title: str, message: str, msg_type: str = 'info'):
        """Show message dialog"""
        dialog = MessageDialog(title=title, message=message, message_type=msg_type)
        dialog.open()

    def go_back(self, instance=None):
        """Go back to dashboard"""
        self.manager.current = 'dashboard'

    def on_enter(self, *args):
        """Called when screen is entered"""
        self.load_owners()
