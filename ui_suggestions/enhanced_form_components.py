#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Form Design Patterns
Modern form components to enhance your existing property and owner forms
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.slider import Slider
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.clock import Clock


class ModernFormField(BoxLayout):
    """Enhanced form field with Material Design styling"""

    def __init__(self, label_text, field_type='text', options=None, **kwargs):
        super().__init__(orientation='vertical', spacing=dp(4), **kwargs)
        self.size_hint_y = None
        self.height = dp(80)

        self.label_text = label_text
        self.field_type = field_type
        self.options = options or []

        self._build_field()

    def _build_field(self):
        """Build the form field based on type"""
        # Label
        self.label = Label(
            text=self.label_text,
            font_size='14sp',
            color=[0.3, 0.3, 0.3, 1],
            size_hint_y=None,
            height=dp(20),
            halign='left'
        )
        self.add_widget(self.label)

        # Input container
        input_container = BoxLayout(
            size_hint_y=None,
            height=dp(48),
            padding=[dp(2), dp(2)]
        )

        # Field background
        with input_container.canvas.before:
            Color(1, 1, 1, 1)
            self.field_bg = RoundedRectangle(radius=[dp(8)])
            Color(0.9, 0.9, 0.9, 1)
            self.field_border = Line(rounded_rectangle=[0, 0, 0, 0, dp(8)], width=1)
            input_container.bind(
                pos=self._update_field_graphics,
                size=self._update_field_graphics
            )

        # Create appropriate input widget
        if self.field_type == 'text':
            self.input_widget = self._create_text_input()
        elif self.field_type == 'number':
            self.input_widget = self._create_number_input()
        elif self.field_type == 'multiline':
            self.input_widget = self._create_multiline_input()
        elif self.field_type == 'dropdown':
            self.input_widget = self._create_dropdown()
        elif self.field_type == 'checkbox':
            self.input_widget = self._create_checkbox()
        elif self.field_type == 'slider':
            self.input_widget = self._create_slider()
        else:
            self.input_widget = self._create_text_input()

        input_container.add_widget(self.input_widget)
        self.add_widget(input_container)

        # Store reference to container for styling updates
        self.input_container = input_container

    def _create_text_input(self):
        """Create enhanced text input"""
        text_input = TextInput(
            multiline=False,
            background_color=[0, 0, 0, 0],  # Transparent
            foreground_color=[0.2, 0.2, 0.2, 1],
            cursor_color=[0.13, 0.39, 0.65, 1],
            font_size='16sp',
            padding=[dp(12), dp(8)]
        )

        # Add focus effects
        text_input.bind(focus=self._on_focus_change)
        return text_input

    def _create_number_input(self):
        """Create number-only input with validation"""
        text_input = TextInput(
            input_filter='float',
            multiline=False,
            background_color=[0, 0, 0, 0],
            foreground_color=[0.2, 0.2, 0.2, 1],
            cursor_color=[0.13, 0.39, 0.65, 1],
            font_size='16sp',
            padding=[dp(12), dp(8)]
        )

        text_input.bind(focus=self._on_focus_change)
        return text_input

    def _create_multiline_input(self):
        """Create multiline text input"""
        text_input = TextInput(
            multiline=True,
            background_color=[0, 0, 0, 0],
            foreground_color=[0.2, 0.2, 0.2, 1],
            cursor_color=[0.13, 0.39, 0.65, 1],
            font_size='16sp',
            padding=[dp(12), dp(8)]
        )

        # Adjust height for multiline
        self.height = dp(120)
        self.input_container.height = dp(88)

        text_input.bind(focus=self._on_focus_change)
        return text_input

    def _create_dropdown(self):
        """Create enhanced dropdown with custom styling"""
        spinner = Spinner(
            values=self.options,
            background_color=[0, 0, 0, 0],
            color=[0.2, 0.2, 0.2, 1],
            font_size='16sp'
        )

        return spinner

    def _create_checkbox(self):
        """Create checkbox with label"""
        container = BoxLayout(orientation='horizontal', spacing=dp(8))

        checkbox = CheckBox(
            size_hint_x=None,
            width=dp(32),
            color=[0.13, 0.39, 0.65, 1]
        )

        label = Label(
            text="Enable option",
            color=[0.2, 0.2, 0.2, 1],
            font_size='16sp',
            halign='left'
        )

        container.add_widget(checkbox)
        container.add_widget(label)

        return container

    def _create_slider(self):
        """Create styled slider"""
        slider = Slider(
            min=0,
            max=100,
            value=50,
            step=1,
            cursor_size=(dp(20), dp(20)),
            value_track_color=[0.13, 0.39, 0.65, 1],
            cursor_color=[0.13, 0.39, 0.65, 1]
        )

        return slider

    def _update_field_graphics(self, *args):
        """Update field background graphics"""
        self.field_bg.pos = self.input_container.pos
        self.field_bg.size = self.input_container.size
        self.field_border.rounded_rectangle = [
            *self.input_container.pos,
            *self.input_container.size,
            dp(8)
        ]

    def _on_focus_change(self, instance, focused):
        """Handle focus change effects"""
        if focused:
            # Change border color to primary
            Animation(duration=0.2).start(self.field_border)
            # You would update the border color here
        else:
            # Revert to normal border
            Animation(duration=0.2).start(self.field_border)

    def get_value(self):
        """Get the current field value"""
        if hasattr(self.input_widget, 'text'):
            return self.input_widget.text
        elif hasattr(self.input_widget, 'value'):
            return self.input_widget.value
        elif self.field_type == 'checkbox':
            return self.input_widget.children[1].active  # Checkbox is second child
        return None

    def set_value(self, value):
        """Set the field value"""
        if hasattr(self.input_widget, 'text'):
            self.input_widget.text = str(value)
        elif hasattr(self.input_widget, 'value'):
            self.input_widget.value = value
        elif self.field_type == 'checkbox':
            self.input_widget.children[1].active = bool(value)


class FormSection(BoxLayout):
    """Collapsible form section with header"""

    def __init__(self, title, fields=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.title = title
        self.fields = fields or []
        self.is_expanded = True

        self.size_hint_y = None
        self.spacing = dp(8)

        self._build_section()

    def _build_section(self):
        """Build the form section"""
        # Section header
        self.header = self._create_header()
        self.add_widget(self.header)

        # Fields container
        self.fields_container = BoxLayout(
            orientation='vertical',
            spacing=dp(12),
            size_hint_y=None,
            padding=[dp(16), dp(8)]
        )
        self.fields_container.bind(minimum_height=self.fields_container.setter('height'))

        # Add fields
        for field_config in self.fields:
            field = ModernFormField(**field_config)
            self.fields_container.add_widget(field)

        self.add_widget(self.fields_container)

        # Calculate total height
        self.height = dp(56) + self.fields_container.height  # Header + fields

    def _create_header(self):
        """Create collapsible section header"""
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(56),
            spacing=dp(12),
            padding=[dp(16), dp(8)]
        )

        # Header background
        with header.canvas.before:
            Color(0.98, 0.98, 0.98, 1)
            self.header_bg = RoundedRectangle(radius=[dp(8)])
            header.bind(pos=self._update_header_bg, size=self._update_header_bg)

        # Expand/collapse icon
        self.expand_icon = Label(
            text="▼" if self.is_expanded else "▶",
            font_size='16sp',
            color=[0.5, 0.5, 0.5, 1],
            size_hint_x=None,
            width=dp(24)
        )
        header.add_widget(self.expand_icon)

        # Title
        header.add_widget(Label(
            text=self.title,
            font_size='18sp',
            color=[0.2, 0.2, 0.2, 1],
            bold=True,
            halign='left'
        ))

        # Make header clickable
        header.bind(on_touch_down=self._on_header_touch)

        return header

    def _update_header_bg(self, *args):
        """Update header background"""
        self.header_bg.pos = self.header.pos
        self.header_bg.size = self.header.size

    def _on_header_touch(self, instance, touch):
        """Handle header touch to toggle section"""
        if instance.collide_point(*touch.pos):
            self.toggle_section()
            return True
        return False

    def toggle_section(self):
        """Toggle section expand/collapse"""
        self.is_expanded = not self.is_expanded

        # Update icon
        self.expand_icon.text = "▼" if self.is_expanded else "▶"

        # Animate fields container
        if self.is_expanded:
            # Expand
            self.fields_container.opacity = 0
            self.add_widget(self.fields_container)
            Animation(
                opacity=1,
                duration=0.3,
                transition='out_cubic'
            ).start(self.fields_container)
        else:
            # Collapse
            Animation(
                opacity=0,
                duration=0.3,
                transition='in_cubic'
            ).start(self.fields_container)
            Clock.schedule_once(
                lambda dt: self.remove_widget(self.fields_container),
                0.3
            )


class SmartForm(BoxLayout):
    """Intelligent form with validation and progress tracking"""

    def __init__(self, form_config=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.form_config = form_config or {}
        self.sections = []
        self.validation_rules = {}

        self._build_form()

    def _build_form(self):
        """Build the complete form"""
        # Form header with progress
        self.form_header = self._create_form_header()
        self.add_widget(self.form_header)

        # Scrollable form content
        self.scroll = ScrollView()
        self.form_content = BoxLayout(
            orientation='vertical',
            spacing=dp(16),
            size_hint_y=None,
            padding=[dp(16), dp(16)]
        )
        self.form_content.bind(minimum_height=self.form_content.setter('height'))

        # Add sections
        for section_config in self.form_config.get('sections', []):
            section = FormSection(**section_config)
            self.sections.append(section)
            self.form_content.add_widget(section)

        self.scroll.add_widget(self.form_content)
        self.add_widget(self.scroll)

        # Form actions
        self.form_actions = self._create_form_actions()
        self.add_widget(self.form_actions)

    def _create_form_header(self):
        """Create form header with progress indicator"""
        header = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(80),
            spacing=dp(8),
            padding=[dp(16), dp(12)]
        )

        # Background
        with header.canvas.before:
            Color(0.13, 0.39, 0.65, 1)
            self.header_bg = RoundedRectangle(radius=[dp(12), dp(12), 0, 0])
            header.bind(pos=self._update_form_header_bg, size=self._update_form_header_bg)

        # Title
        header.add_widget(Label(
            text=self.form_config.get('title', 'Form'),
            font_size='20sp',
            color=[1, 1, 1, 1],
            bold=True,
            size_hint_y=None,
            height=dp(32)
        ))

        # Progress bar
        progress_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(24),
            spacing=dp(8)
        )

        progress_container.add_widget(Label(
            text="Progress:",
            font_size='12sp',
            color=[1, 1, 1, 0.8],
            size_hint_x=None,
            width=dp(60)
        ))

        # Progress bar
        self.progress_bar = self._create_progress_bar()
        progress_container.add_widget(self.progress_bar)

        header.add_widget(progress_container)

        return header

    def _create_progress_bar(self):
        """Create animated progress bar"""
        container = BoxLayout(size_hint_y=None, height=dp(8))

        with container.canvas:
            # Background
            Color(1, 1, 1, 0.3)
            self.progress_bg = RoundedRectangle(radius=[dp(4)])

            # Progress fill
            Color(0.96, 0.76, 0.24, 1)  # Gold color
            self.progress_fill = RoundedRectangle(radius=[dp(4)])

        container.bind(pos=self._update_progress_bar, size=self._update_progress_bar)
        return container

    def _update_form_header_bg(self, *args):
        """Update form header background"""
        self.header_bg.pos = self.form_header.pos
        self.header_bg.size = self.form_header.size

    def _update_progress_bar(self, *args):
        """Update progress bar graphics"""
        self.progress_bg.pos = self.progress_bar.pos
        self.progress_bg.size = self.progress_bar.size

        # Calculate progress (you would implement actual progress calculation)
        progress_percent = self._calculate_form_progress()
        progress_width = self.progress_bar.width * progress_percent

        self.progress_fill.pos = self.progress_bar.pos
        self.progress_fill.size = (progress_width, self.progress_bar.height)

    def _create_form_actions(self):
        """Create form action buttons"""
        actions = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(64),
            spacing=dp(16),
            padding=[dp(16), dp(12)]
        )

        # Cancel button
        cancel_btn = Button(
            text="Cancel",
            size_hint_x=0.3,
            background_color=[0.7, 0.7, 0.7, 1],
            color=[1, 1, 1, 1]
        )
        actions.add_widget(cancel_btn)

        # Spacer
        actions.add_widget(Label())

        # Save button
        save_btn = Button(
            text="Save",
            size_hint_x=0.3,
            background_color=[0.13, 0.39, 0.65, 1],
            color=[1, 1, 1, 1]
        )
        actions.add_widget(save_btn)

        return actions

    def _calculate_form_progress(self):
        """Calculate form completion progress"""
        total_fields = 0
        completed_fields = 0

        for section in self.sections:
            for field in section.fields_container.children:
                if isinstance(field, ModernFormField):
                    total_fields += 1
                    if field.get_value():  # Has value
                        completed_fields += 1

        return completed_fields / total_fields if total_fields > 0 else 0

    def validate_form(self):
        """Validate all form fields"""
        errors = []

        for section in self.sections:
            for field in section.fields_container.children:
                if isinstance(field, ModernFormField):
                    # Implement validation logic
                    value = field.get_value()
                    # Add validation rules as needed

        return len(errors) == 0, errors

    def get_form_data(self):
        """Get all form data as dictionary"""
        data = {}

        for section in self.sections:
            section_data = {}
            for field in section.fields_container.children:
                if isinstance(field, ModernFormField):
                    field_name = field.label_text.lower().replace(' ', '_')
                    section_data[field_name] = field.get_value()
            data[section.title.lower().replace(' ', '_')] = section_data

        return data


# Integration suggestions for your existing forms
class FormEnhancementSuggestions:
    """Suggestions for enhancing your existing property and owner forms"""

    @staticmethod
    def enhance_property_form():
        """Configuration for enhanced property form"""
        return {
            'title': 'Property Information',
            'sections': [
                {
                    'title': 'Basic Information',
                    'fields': [
                        {'label_text': 'Property Code', 'field_type': 'text'},
                        {'label_text': 'Property Type', 'field_type': 'dropdown',
                         'options': ['Apartment', 'House', 'Commercial', 'Land']},
                        {'label_text': 'Address', 'field_type': 'multiline'},
                    ]
                },
                {
                    'title': 'Specifications',
                    'fields': [
                        {'label_text': 'Area (m²)', 'field_type': 'number'},
                        {'label_text': 'Rooms', 'field_type': 'slider'},
                        {'label_text': 'Bathrooms', 'field_type': 'number'},
                    ]
                },
                {
                    'title': 'Additional Details',
                    'fields': [
                        {'label_text': 'Furnished', 'field_type': 'checkbox'},
                        {'label_text': 'Description', 'field_type': 'multiline'},
                    ]
                }
            ]
        }

    @staticmethod
    def enhance_owner_form():
        """Configuration for enhanced owner form"""
        return {
            'title': 'Owner Information',
            'sections': [
                {
                    'title': 'Personal Information',
                    'fields': [
                        {'label_text': 'Full Name', 'field_type': 'text'},
                        {'label_text': 'Phone Number', 'field_type': 'text'},
                        {'label_text': 'Email', 'field_type': 'text'},
                    ]
                },
                {
                    'title': 'Address Information',
                    'fields': [
                        {'label_text': 'Address', 'field_type': 'multiline'},
                        {'label_text': 'Province', 'field_type': 'dropdown'},
                    ]
                }
            ]
        }
