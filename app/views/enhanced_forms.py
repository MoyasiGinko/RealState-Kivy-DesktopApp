#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Enhanced Form Components
Beautiful, accessible form components with validation and animations
"""

from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDSwitch, MDCheckbox
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.clock import Clock
from typing import List, Dict, Any, Callable
import logging

from app.views.modern_components import DesignTokens, ModernCard
from app.language_manager import language_manager

logger = logging.getLogger(__name__)


class EnhancedFormField(MDBoxLayout):
    """Enhanced form field with validation and animations"""

    def __init__(self, label: str, field_type: str = 'text',
                 required: bool = False, validation_rules: List[str] = None,
                 options: List[str] = None, **kwargs):
        super().__init__(**kwargs)

        self.label = label
        self.field_type = field_type
        self.required = required
        self.validation_rules = validation_rules or []
        self.options = options or []
        self.is_valid = True
        self.error_message = ""

        self.orientation = 'vertical'
        self.adaptive_height = True
        self.spacing = DesignTokens.SPACING['xs']

        self.build_field()

    def build_field(self):
        """Build the form field based on type"""
        # Field label
        label_text = self.label
        if self.required:
            label_text += " *"

        self.label_widget = MDLabel(
            text=label_text,
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_primary'],
            font_style="Body2",
            size_hint_y=None,
            height=dp(20),
            bold=self.required
        )
        self.add_widget(self.label_widget)

        # Build input based on type
        if self.field_type == 'text':
            self.build_text_field()
        elif self.field_type == 'number':
            self.build_number_field()
        elif self.field_type == 'email':
            self.build_email_field()
        elif self.field_type == 'password':
            self.build_password_field()
        elif self.field_type == 'multiline':
            self.build_multiline_field()
        elif self.field_type == 'dropdown':
            self.build_dropdown_field()
        elif self.field_type == 'switch':
            self.build_switch_field()
        elif self.field_type == 'checkbox':
            self.build_checkbox_field()

        # Error label (hidden by default)
        self.error_label = MDLabel(
            text="",
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['error'],
            font_style="Caption",
            size_hint_y=None,
            height=0,  # Hidden by default
            opacity=0
        )
        self.add_widget(self.error_label)

    def build_text_field(self):
        """Build standard text field"""
        self.input = MDTextField(
            hint_text=self.label,
            mode="outlined",
            size_hint_y=None,
            height=dp(56),
            line_color_normal=DesignTokens.COLORS['divider'],
            line_color_focus=DesignTokens.COLORS['primary'],
            text_color_normal=DesignTokens.COLORS['text_primary'],
            text_color_focus=DesignTokens.COLORS['text_primary'],
            hint_text_color_normal=DesignTokens.COLORS['text_hint'],
            hint_text_color_focus=DesignTokens.COLORS['primary']
        )
        self.input.bind(text=self.on_text_change)
        self.input.bind(focus=self.on_focus_change)
        self.add_widget(self.input)

    def build_number_field(self):
        """Build number input field"""
        self.build_text_field()
        self.input.input_filter = 'float'
        self.input.hint_text = f"{self.label} (Numbers only)"

    def build_email_field(self):
        """Build email input field"""
        self.build_text_field()
        self.input.hint_text = f"{self.label} (Email format)"

    def build_password_field(self):
        """Build password input field"""
        self.build_text_field()
        self.input.password = True
        self.input.hint_text = f"{self.label} (Password)"

    def build_multiline_field(self):
        """Build multiline text field"""
        self.input = MDTextField(
            hint_text=self.label,
            mode="outlined",
            multiline=True,
            size_hint_y=None,
            height=dp(100),
            line_color_normal=DesignTokens.COLORS['divider'],
            line_color_focus=DesignTokens.COLORS['primary'],
            text_color_normal=DesignTokens.COLORS['text_primary'],
            text_color_focus=DesignTokens.COLORS['text_primary'],
            hint_text_color_normal=DesignTokens.COLORS['text_hint'],
            hint_text_color_focus=DesignTokens.COLORS['primary']
        )
        self.input.bind(text=self.on_text_change)
        self.input.bind(focus=self.on_focus_change)
        self.add_widget(self.input)

    def build_dropdown_field(self):
        """Build dropdown selection field"""
        self.input = MDTextField(
            hint_text=f"Select {self.label}",
            mode="outlined",
            readonly=True,
            size_hint_y=None,
            height=dp(56),
            line_color_normal=DesignTokens.COLORS['divider'],
            line_color_focus=DesignTokens.COLORS['primary']
        )

        # Create dropdown menu
        menu_items = [
            {
                "text": option,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=option: self.select_option(x),
            } for option in self.options
        ]

        self.dropdown_menu = MDDropdownMenu(
            caller=self.input,
            items=menu_items,
            max_height=dp(200)
        )

        self.input.bind(on_release=self.dropdown_menu.open)
        self.add_widget(self.input)

    def build_switch_field(self):
        """Build switch toggle field"""
        switch_container = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True,
            spacing=DesignTokens.SPACING['md']
        )

        self.input = MDSwitch(
            size_hint=(None, None),
            size=(dp(50), dp(30)),
            theme_thumb_color="Custom",            thumb_color_active=DesignTokens.COLORS['primary'],
            theme_track_color="Custom",
            track_color_active=(DesignTokens.COLORS['primary'][0], DesignTokens.COLORS['primary'][1], DesignTokens.COLORS['primary'][2], 0.3)
        )
        switch_container.add_widget(self.input)

        switch_label = MDLabel(
            text=self.label,
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_primary'],
            font_style="Body1"
        )
        switch_container.add_widget(switch_label)

        self.add_widget(switch_container)

    def build_checkbox_field(self):
        """Build checkbox field"""
        checkbox_container = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True,
            spacing=DesignTokens.SPACING['md']
        )

        self.input = MDCheckbox(
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            theme_icon_color="Custom",
            icon_color_active=DesignTokens.COLORS['primary'],
            theme_outline_color="Custom",
            outline_color_normal=DesignTokens.COLORS['divider']
        )
        checkbox_container.add_widget(self.input)

        checkbox_label = MDLabel(
            text=self.label,
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_primary'],
            font_style="Body1"
        )
        checkbox_container.add_widget(checkbox_label)

        self.add_widget(checkbox_container)

    def select_option(self, option: str):
        """Handle dropdown option selection"""
        self.input.text = option
        self.dropdown_menu.dismiss()
        self.validate()

    def on_text_change(self, instance, text):
        """Handle text changes"""
        # Clear error when user starts typing
        if self.error_message:
            self.clear_error()

        # Validate after a short delay
        Clock.unschedule(self.delayed_validate)
        Clock.schedule_once(self.delayed_validate, 0.5)

    def delayed_validate(self, dt):
        """Validate after delay to avoid constant validation while typing"""
        self.validate()

    def on_focus_change(self, instance, focused):
        """Handle focus changes"""
        if not focused:  # Lost focus
            self.validate()

    def validate(self) -> bool:
        """Validate field value"""
        value = self.get_value()

        # Required field validation
        if self.required and not value.strip():
            self.show_error(language_manager.get_text('field_required'))
            return False

        # Type-specific validation
        if value and self.field_type == 'email':
            if '@' not in value or '.' not in value:
                self.show_error(language_manager.get_text('invalid_email'))
                return False

        elif value and self.field_type == 'number':
            try:
                float(value)
            except ValueError:
                self.show_error(language_manager.get_text('invalid_number'))
                return False

        # Custom validation rules
        for rule in self.validation_rules:
            if rule == 'phone' and value:
                if len(value) < 10:
                    self.show_error(language_manager.get_text('invalid_phone'))
                    return False

        self.clear_error()
        return True

    def show_error(self, message: str):
        """Show validation error with animation"""
        self.is_valid = False
        self.error_message = message
        self.error_label.text = message

        # Animate error appearance
        self.error_label.height = dp(20)
        anim = Animation(opacity=1, duration=0.2)
        anim.start(self.error_label)

        # Highlight field
        if hasattr(self.input, 'line_color_focus'):
            self.input.line_color_focus = DesignTokens.COLORS['error']

    def clear_error(self):
        """Clear validation error"""
        self.is_valid = True
        self.error_message = ""

        # Animate error disappearance
        anim = Animation(opacity=0, duration=0.2)
        anim.bind(on_complete=lambda *args: setattr(self.error_label, 'height', 0))
        anim.start(self.error_label)

        # Reset field color
        if hasattr(self.input, 'line_color_focus'):
            self.input.line_color_focus = DesignTokens.COLORS['primary']

    def get_value(self) -> str:
        """Get field value"""
        if hasattr(self.input, 'text'):
            return self.input.text
        elif hasattr(self.input, 'active'):
            return str(self.input.active)
        return ""

    def set_value(self, value: str):
        """Set field value"""
        if hasattr(self.input, 'text'):
            self.input.text = str(value) if value else ""
        elif hasattr(self.input, 'active'):
            self.input.active = bool(value)

    def clear(self):
        """Clear field value"""
        self.set_value("")
        self.clear_error()


class EnhancedFormCard(ModernCard):
    """Enhanced form container with validation and submission handling"""

    def __init__(self, title: str, fields: List[Dict],
                 on_submit: Callable = None, **kwargs):
        kwargs['variant'] = 'form'
        super().__init__(**kwargs)

        self.title = title
        self.fields_config = fields
        self.on_submit = on_submit
        self.form_fields = {}

        self.build_form()

    def build_form(self):
        """Build the complete form"""
        # Form title
        title_label = MDLabel(
            text=self.title,
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_primary'],
            font_style="H6",
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        self.add_widget(title_label)

        # Form fields
        for field_config in self.fields_config:
            field = EnhancedFormField(**field_config)
            self.form_fields[field_config['label']] = field
            self.add_widget(field)

        # Form actions
        self.build_form_actions()

    def build_form_actions(self):
        """Build form action buttons"""
        actions_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['md'],
            size_hint_y=None,
            height=dp(50)
        )

        # Clear button
        clear_btn = MDFlatButton(
            text=language_manager.get_text('clear'),
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['text_secondary'],
            on_release=self.clear_form
        )
        actions_layout.add_widget(clear_btn)

        # Submit button
        submit_btn = MDRaisedButton(
            text=language_manager.get_text('submit'),
            md_bg_color=DesignTokens.COLORS['primary'],
            theme_text_color="Custom",
            text_color=DesignTokens.COLORS['card'],
            on_release=self.submit_form
        )
        actions_layout.add_widget(submit_btn)

        self.add_widget(actions_layout)

    def validate_form(self) -> bool:
        """Validate all form fields"""
        is_valid = True
        for field in self.form_fields.values():
            if not field.validate():
                is_valid = False
        return is_valid

    def get_form_data(self) -> Dict[str, Any]:
        """Get all form data"""
        data = {}
        for label, field in self.form_fields.items():
            data[label] = field.get_value()
        return data

    def clear_form(self, instance=None):
        """Clear all form fields"""
        for field in self.form_fields.values():
            field.clear()

    def submit_form(self, instance=None):
        """Submit form if validation passes"""
        if self.validate_form():
            if self.on_submit:
                data = self.get_form_data()
                self.on_submit(data)
            else:
                # Show success message
                snackbar = Snackbar(
                    text=language_manager.get_text('form_submitted'),
                    bg_color=DesignTokens.COLORS['success']
                )
                snackbar.open()
        else:
            # Show validation error
            snackbar = Snackbar(
                text=language_manager.get_text('form_validation_failed'),
                bg_color=DesignTokens.COLORS['error']
            )
            snackbar.open()

    def populate_form(self, data: Dict[str, Any]):
        """Populate form with data"""
        for label, value in data.items():
            if label in self.form_fields:
                self.form_fields[label].set_value(value)
