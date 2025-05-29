#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Ma        # Form title
        left_panel.add_widget(BilingualLabel(
            translation_key='owner_information',
            font_size=dp(18),
            bold=True,
            size_hint_y=None,
            height=dp(40),
            halign='center'
        ))ystem - Owners Management Screen
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
import logging

from app.components import (RTLLabel, CustomActionButton as ActionButton, FormField, DataTable,
                            ConfirmDialog, MessageDialog, SearchBox, BilingualLabel, TranslatableButton,
                            NavigationHeader, ResponsiveCard)
from app.database import DatabaseManager
from app.utils import DataValidator
from app.font_manager import font_manager
from app.language_manager import language_manager
from app.config import config

logger = logging.getLogger(__name__)


class OwnersScreen(Screen):
    """Owners management screen"""

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
        title_style = config.get_label_style('header')
        left_panel.add_widget(BilingualLabel(
            translation_key='owner_information',
            font_size=title_style['font_size'],
            bold=True,
            color=title_style['color'],
            size_hint_y=None,
            height=dp(40),
            halign='center'
        ))

        # Form
        form_scroll = ScrollView()
        self.form_layout = BoxLayout(orientation='vertical', spacing=dp(10),
                                    size_hint_y=None)
        self.form_layout.bind(minimum_height=self.form_layout.setter('height'))

        # Owner Code (auto-generated, read-only)
        self.owner_code_field = FormField(
            language_manager.get_text('owner_code'),
            required=True
        )
        self.owner_code_field.input.readonly = True
        self.owner_code_field.input.text = self.db.generate_owner_code()
        self.form_layout.add_widget(self.owner_code_field)

        # Owner Name
        self.owner_name_field = FormField(
            language_manager.get_text('owner_name'),
            required=True
        )
        self.form_layout.add_widget(self.owner_name_field)

        # Owner Phone
        self.owner_phone_field = FormField(
            language_manager.get_text('phone')
        )
        self.form_layout.add_widget(self.owner_phone_field)

        # Notes
        self.notes_field = FormField(
            language_manager.get_text('notes'),
            input_type='multiline'
        )
        self.form_layout.add_widget(self.notes_field)

        form_scroll.add_widget(self.form_layout)
        left_panel.add_widget(form_scroll)

        # Action buttons
        button_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(50))

        self.save_btn = TranslatableButton(
            translation_key='save',
            button_type='success',
            action=self.save_owner
        )
        button_layout.add_widget(self.save_btn)

        self.clear_btn = TranslatableButton(
            translation_key='clear',
            button_type='secondary',
            action=self.clear_form
        )
        button_layout.add_widget(self.clear_btn)

        self.update_btn = TranslatableButton(
            translation_key='update',
            button_type='warning',
            action=self.update_owner
        )
        self.update_btn.disabled = True
        button_layout.add_widget(self.update_btn)

        self.delete_btn = TranslatableButton(
            translation_key='delete',
            button_type='danger',
            action=self.delete_owner
        )
        self.delete_btn.disabled = True
        button_layout.add_widget(self.delete_btn)

        left_panel.add_widget(button_layout)
        content_layout.add_widget(left_panel)

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

    def search_owners(self, search_text: str):
        """Search owners by name or phone"""
        try:
            if not search_text:
                self.load_owners()
                return

            filtered_data = []
            for owner in self.owners_data:
                if (search_text.lower() in owner[1].lower() or  # name
                    search_text in (owner[2] or '')):  # phone
                    filtered_data.append({
                        'Ownercode': owner[0],
                        'ownername': owner[1],
                        'ownerphone': owner[2] or '',
                        'Note': owner[3] or ''
                    })

            self.owners_table.update_data(filtered_data)

        except Exception as e:
            logger.error(f"Error searching owners: {e}")

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
            logger.error(f"Error updating stats: {e}")

    def show_message(self, title: str, message: str, msg_type: str = 'info'):
        """Show message dialog"""
        dialog = MessageDialog(title=title, message=message, message_type=msg_type)
        dialog.open()

    def go_back(self):
        """Go back to dashboard"""
        self.manager.current = 'dashboard'

    def on_enter(self, *args):
        """Called when screen is entered"""
        self.load_owners()
