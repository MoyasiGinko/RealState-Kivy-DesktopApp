#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Enhanced Owners Management Screen (Backup)
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


class OwnersScreen(Screen):
    """Simplified Owners Management Screen without pagination"""

    def __init__(self, db_manager: DatabaseManager, **kwargs):
        super().__init__(**kwargs)
        self.name = 'owners'
        self.db = db_manager
        self.current_owner = None
        self.owners_data = []

        self.build_ui()
        self.load_owners()

    def build_ui(self):
        """Build the modern responsive owners management UI"""
        # Main layout with modern spacing
        main_layout = BoxLayout(orientation='vertical', spacing=dp(15), padding=[20, 10, 20, 20])

        # Navigation header
        nav_header = NavigationHeader(
            screen_title_key='owners_management',
            show_back_button=True
        )
        main_layout.add_widget(nav_header)

        # Content area
        content_layout = BoxLayout(orientation='horizontal', spacing=dp(20))

        # Left panel - Form in responsive card
        left_panel = ResponsiveCard(
            orientation='vertical',
            size_hint_x=0.4,
            spacing=dp(15),
            padding=dp(20)
        )

        # Form title
        left_panel.add_widget(BilingualLabel(
            translation_key='owner_information',
            font_size=dp(18),
            bold=True,
            size_hint_y=None,
            height=dp(40),
            halign='center'
        ))

        # Form scroll
        form_scroll = ScrollView()
        self.form_layout = BoxLayout(orientation='vertical', spacing=dp(10),
                                    size_hint_y=None)
        self.form_layout.bind(minimum_height=self.form_layout.setter('height'))

        # Owner Code (auto-generated)
        self.owner_code_field = FormField(language_manager.get_text('owner_code'), required=True)
        self.owner_code_field.input.readonly = True
        self.owner_code_field.input.text = self.db.generate_owner_code()
        self.form_layout.add_widget(self.owner_code_field)

        # Owner Name
        self.owner_name_field = FormField(language_manager.get_text('owner_name'), required=True)
        self.form_layout.add_widget(self.owner_name_field)

        # Owner Phone
        self.owner_phone_field = FormField(language_manager.get_text('phone'))
        self.form_layout.add_widget(self.owner_phone_field)

        # Notes
        self.notes_field = FormField(language_manager.get_text('notes'), multiline=True, height=dp(100))
        self.form_layout.add_widget(self.notes_field)

        # Action buttons
        self.build_action_buttons()

        form_scroll.add_widget(self.form_layout)
        left_panel.add_widget(form_scroll)

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

        content_layout.add_widget(left_panel)
        content_layout.add_widget(right_panel)
        main_layout.add_widget(content_layout)

        self.add_widget(main_layout)

    def build_action_buttons(self):
        """Build action buttons for the form"""
        buttons_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )

        # Save button
        self.save_btn = ActionButton(
            text=language_manager.get_text('save'),
            button_type='success',
            size_hint_x=0.25
        )
        self.save_btn.bind(on_press=lambda x: self.save_owner())
        buttons_layout.add_widget(self.save_btn)

        # Update button
        self.update_btn = ActionButton(
            text=language_manager.get_text('update'),
            button_type='primary',
            size_hint_x=0.25,
            disabled=True
        )
        self.update_btn.bind(on_press=lambda x: self.update_owner())
        buttons_layout.add_widget(self.update_btn)

        # Delete button
        self.delete_btn = ActionButton(
            text=language_manager.get_text('delete'),
            button_type='danger',
            size_hint_x=0.25,
            disabled=True
        )
        self.delete_btn.bind(on_press=lambda x: self.delete_owner())
        buttons_layout.add_widget(self.delete_btn)

        # Clear button
        clear_btn = ActionButton(
            text=language_manager.get_text('clear'),
            button_type='secondary',
            size_hint_x=0.25
        )
        clear_btn.bind(on_press=lambda x: self.clear_form())
        buttons_layout.add_widget(clear_btn)

        self.form_layout.add_widget(buttons_layout)

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

    def search_owners(self, search_text):
        """Search owners based on text"""
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

        def confirm_delete():
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
                        language_manager.get_text('delete_failed'),
                        'error'
                    )
            except Exception as e:
                logger.error(f"Error deleting owner: {e}")
                self.show_message(
                    language_manager.get_text('error'),
                    f'{language_manager.get_text("delete_failed")}: {str(e)}',
                    'error'
                )

        # Show confirmation dialog
        dialog = ConfirmDialog(
            title=language_manager.get_text('confirm_delete'),
            message=language_manager.get_text('confirm_delete_owner'),
            on_confirm=confirm_delete
        )
        dialog.open()

    def clear_form(self):
        """Clear the form"""
        self.current_owner = None
        self.owner_code_field.set_value(self.db.generate_owner_code())
        self.owner_name_field.set_value('')
        self.owner_phone_field.set_value('')
        self.notes_field.set_value('')

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
            logger.error(f"Error updating stats: {e}")

    def show_message(self, title: str, message: str, msg_type: str = 'info'):
        """Show message dialog"""
        dialog = MessageDialog(title=title, message=message, message_type=msg_type)
        dialog.open()

    def go_back(self, instance=None):
        """Go back to dashboard"""
        self.manager.current = 'dashboard'

    def on_enter(self, *args):
        """Called when screen is entered"""
        self.load_owners()
