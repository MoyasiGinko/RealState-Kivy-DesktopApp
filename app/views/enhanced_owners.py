#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Enhanced Owners Management with KivyMD
Beautiful, modern owners management interface with Material Design components
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
from kivymd.uix.list import MDList, ThreeLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.snackbar import Snackbar
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

class EnhancedOwnersScreen(MDScreen):
    """Enhanced Owners Management Screen with KivyMD components"""

    def __init__(self, db_manager: DatabaseManager, **kwargs):
        super().__init__(**kwargs)
        self.name = 'enhanced_owners'
        self.db = db_manager
        self.current_owner = None
        self.owners_data = []

        self.build_ui()
        self.load_owners()

    def build_ui(self):
        """Build the enhanced owners management UI"""
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

    def build_stats_section(self, parent):
        """Build statistics section"""
        stats_title = MDLabel(
            text=language_manager.get_text('owners_statistics'),
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
            cols=2,
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

        # Right side - Owners list
        self.build_list_section(content_card)

        parent.add_widget(content_card)

    def build_form_section(self, parent):
        """Build the owner form section"""
        form_layout = MDBoxLayout(
            orientation='vertical',
            size_hint_x=0.4,
            spacing=dp(15),
            adaptive_height=True
        )

        # Form title
        form_title = MDLabel(
            text=language_manager.get_text('owner_information'),
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['primary'],
            font_style="H6",
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        form_layout.add_widget(form_title)

        # Owner code field (read-only)
        self.owner_code_field = MDTextField(
            hint_text=language_manager.get_text('owner_code'),
            readonly=True,
            icon_left="identifier",
            size_hint_y=None,
            height=dp(48)
        )
        form_layout.add_widget(self.owner_code_field)

        # Owner name field
        self.owner_name_field = MDTextField(
            hint_text=language_manager.get_text('owner_name'),
            required=True,
            icon_left="account",
            size_hint_y=None,
            height=dp(48)
        )
        form_layout.add_widget(self.owner_name_field)

        # Owner phone field
        self.owner_phone_field = MDTextField(
            hint_text=language_manager.get_text('owner_phone'),
            icon_left="phone",
            input_type="tel",
            size_hint_y=None,
            height=dp(48)
        )
        form_layout.add_widget(self.owner_phone_field)

        # Notes field
        self.notes_field = MDTextField(
            hint_text=language_manager.get_text('notes'),
            multiline=True,
            icon_left="note-text",
            size_hint_y=None,
            height=dp(96)
        )
        form_layout.add_widget(self.notes_field)

        # Action buttons
        self.build_action_buttons(form_layout)

        parent.add_widget(form_layout)

    def build_action_buttons(self, parent):
        """Build action buttons for the form"""
        buttons_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(48),
            adaptive_width=True
        )

        # Save button
        self.save_btn = MDRaisedButton(
            text=language_manager.get_text('save'),
            icon="content-save",
            md_bg_color=DesignTokens.COLORS['success'],
            on_release=self.save_owner
        )
        buttons_layout.add_widget(self.save_btn)

        # Update button
        self.update_btn = MDFlatButton(
            text=language_manager.get_text('update'),
            icon="pencil",
            disabled=True,
            on_release=self.update_owner
        )
        buttons_layout.add_widget(self.update_btn)

        # Delete button
        self.delete_btn = MDFlatButton(
            text=language_manager.get_text('delete'),
            icon="delete",
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['error'],
            disabled=True,
            on_release=self.confirm_delete_owner
        )
        buttons_layout.add_widget(self.delete_btn)

        # Clear button
        clear_btn = MDFlatButton(
            text=language_manager.get_text('clear'),
            icon="refresh",
            on_release=self.clear_form
        )
        buttons_layout.add_widget(clear_btn)

        parent.add_widget(buttons_layout)

    def build_list_section(self, parent):
        """Build the owners list section"""
        list_layout = MDBoxLayout(
            orientation='vertical',
            size_hint_x=0.6,
            spacing=dp(15)
        )

        # List header with search
        header_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(48),
            spacing=dp(10)
        )

        list_title = MDLabel(
            text=language_manager.get_text('owners_list'),
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['primary'],
            font_style="H6",
            bold=True
        )
        header_layout.add_widget(list_title)

        # Search field
        self.search_field = MDTextField(
            hint_text=language_manager.get_text('search_owners'),
            icon_right="magnify",
            size_hint_x=0.4,
            size_hint_y=None,
            height=dp(48),
            on_text=self.on_search_text
        )
        header_layout.add_widget(self.search_field)

        list_layout.add_widget(header_layout)

        # Owners list
        self.owners_list_scroll = MDScrollView()
        self.owners_list = MDList()
        self.owners_list_scroll.add_widget(self.owners_list)
        list_layout.add_widget(self.owners_list_scroll)

        parent.add_widget(list_layout)

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
            total_owners = len(self.owners_data)

            # Total owners card
            total_card = EnhancedStatsCard(
                title=language_manager.get_text('total_owners'),
                value=str(total_owners),
                icon='account-group',
                color_scheme='primary',
                size_hint_y=None,
                height=dp(100)
            )
            self.stats_grid.add_widget(total_card)

            # Properties per owner (if available)
            if self.db:
                total_properties = self.db.get_total_properties()
                avg_props = round(total_properties / total_owners, 1) if total_owners > 0 else 0

                avg_card = EnhancedStatsCard(
                    title=language_manager.get_text('avg_properties_per_owner'),
                    value=str(avg_props),
                    icon='home-account',
                    color_scheme='success',
                    size_hint_y=None,
                    height=dp(100)
                )
                self.stats_grid.add_widget(avg_card)

        except Exception as e:
            logger.error(f"Error updating stats: {e}")

    def load_owners(self):
        """Load owners from database"""
        try:
            if not self.db:
                return

            self.owners_data = self.db.get_owners()
            self.display_owners(self.owners_data)
            self.update_stats_display()

        except Exception as e:
            logger.error(f"Error loading owners: {e}")
            self.show_snackbar(language_manager.get_text('error_loading_data'))

    def display_owners(self, owners):
        """Display owners in the list"""
        try:
            self.owners_list.clear_widgets()

            for owner in owners:
                owner_code, owner_name, owner_phone, note = owner

                # Create list item
                item = ThreeLineAvatarIconListItem(
                    text=owner_name or language_manager.get_text('unnamed_owner'),
                    secondary_text=f"{language_manager.get_text('code')}: {owner_code}",
                    tertiary_text=f"{language_manager.get_text('phone')}: {owner_phone or language_manager.get_text('no_phone')}",
                    on_release=lambda x, data=owner: self.select_owner(data)
                )

                # Icon
                item.add_widget(IconLeftWidget(icon="account"))

                # Action button
                item.add_widget(IconRightWidget(
                    icon="chevron-right",
                    on_release=lambda x, data=owner: self.select_owner(data)
                ))

                self.owners_list.add_widget(item)

        except Exception as e:
            logger.error(f"Error displaying owners: {e}")

    def select_owner(self, owner_data):
        """Select owner for editing"""
        try:
            owner_code, owner_name, owner_phone, note = owner_data
            self.current_owner = {
                'Ownercode': owner_code,
                'ownername': owner_name,
                'ownerphone': owner_phone,
                'Note': note
            }

            # Populate form
            self.owner_code_field.text = owner_code
            self.owner_name_field.text = owner_name or ''
            self.owner_phone_field.text = owner_phone or ''
            self.notes_field.text = note or ''

            # Enable update/delete buttons
            self.update_btn.disabled = False
            self.delete_btn.disabled = False
            self.save_btn.disabled = True

        except Exception as e:
            logger.error(f"Error selecting owner: {e}")

    def save_owner(self, instance=None):
        """Save new owner"""
        try:
            if not self.validate_form():
                return

            owner_name = self.owner_name_field.text.strip()
            owner_phone = self.owner_phone_field.text.strip()
            notes = self.notes_field.text.strip()

            if not self.db:
                self.show_snackbar(language_manager.get_text('database_error'))
                return

            owner_code = self.db.add_owner(owner_name, owner_phone, notes)
            if owner_code:
                self.show_snackbar(language_manager.get_text('owner_saved_successfully'))
                self.clear_form()
                self.load_owners()
            else:
                self.show_snackbar(language_manager.get_text('error_saving_owner'))

        except Exception as e:
            logger.error(f"Error saving owner: {e}")
            self.show_snackbar(language_manager.get_text('error_saving_owner'))

    def update_owner(self, instance=None):
        """Update existing owner"""
        try:
            if not self.current_owner or not self.validate_form():
                return

            owner_code = self.owner_code_field.text
            owner_name = self.owner_name_field.text.strip()
            owner_phone = self.owner_phone_field.text.strip()
            notes = self.notes_field.text.strip()

            if not self.db:
                self.show_snackbar(language_manager.get_text('database_error'))
                return

            if self.db.update_owner(owner_code, owner_name, owner_phone, notes):
                self.show_snackbar(language_manager.get_text('owner_updated_successfully'))
                self.clear_form()
                self.load_owners()
            else:
                self.show_snackbar(language_manager.get_text('error_updating_owner'))

        except Exception as e:
            logger.error(f"Error updating owner: {e}")
            self.show_snackbar(language_manager.get_text('error_updating_owner'))

    def confirm_delete_owner(self, instance=None):
        """Confirm owner deletion"""
        if not self.current_owner:
            return

        dialog = ConfirmationDialog(
            title=language_manager.get_text('confirm_deletion'),
            message=f"{language_manager.get_text('confirm_delete_owner')}: {self.current_owner['ownername']}?",
            confirm_callback=self.delete_owner
        )
        dialog.open()

    def delete_owner(self, instance=None):
        """Delete selected owner"""
        try:
            if not self.current_owner:
                return

            owner_code = self.current_owner['Ownercode']

            if not self.db:
                self.show_snackbar(language_manager.get_text('database_error'))
                return

            if self.db.delete_owner(owner_code):
                self.show_snackbar(language_manager.get_text('owner_deleted_successfully'))
                self.clear_form()
                self.load_owners()
            else:
                self.show_snackbar(language_manager.get_text('cannot_delete_owner_has_properties'))

        except Exception as e:
            logger.error(f"Error deleting owner: {e}")
            self.show_snackbar(language_manager.get_text('error_deleting_owner'))

    def clear_form(self, instance=None):
        """Clear the form"""
        self.current_owner = None
        self.owner_code_field.text = ''
        self.owner_name_field.text = ''
        self.owner_phone_field.text = ''
        self.notes_field.text = ''

        # Reset button states
        self.save_btn.disabled = False
        self.update_btn.disabled = True
        self.delete_btn.disabled = True

    def validate_form(self):
        """Validate form data"""
        if not self.owner_name_field.text.strip():
            self.show_snackbar(language_manager.get_text('owner_name_required'))
            return False
        return True

    def on_search_text(self, instance, text):
        """Handle search text change"""
        if text.strip():
            filtered_owners = []
            search_lower = text.lower()

            for owner in self.owners_data:
                owner_code, owner_name, owner_phone, note = owner
                if (search_lower in (owner_name or '').lower() or
                    search_lower in (owner_code or '').lower() or
                    search_lower in (owner_phone or '').lower()):
                    filtered_owners.append(owner)

            self.display_owners(filtered_owners)
        else:
            self.display_owners(self.owners_data)

    def toggle_search(self, instance=None):
        """Toggle search field focus"""
        self.search_field.focus = True

    def refresh_data(self, instance=None):
        """Refresh owners data"""
        self.load_owners()
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
        self.load_owners()

    def on_leave(self, *args):
        """Called when leaving screen"""
        pass
