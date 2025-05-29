#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Custom UI Components
Reusable UI components and widgets
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.progressbar import ProgressBar
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, Line
from kivy.clock import Clock
from typing import Callable, List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class RTLLabel(Label):
    """Label with RTL text support for Arabic"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text_size = (None, None)
        self.halign = 'right'
        self.valign = 'middle'
        self.bind(size=self.update_text_size)

    def update_text_size(self, *args):
        """Update text size when widget size changes"""
        self.text_size = self.size


class FormField(BoxLayout):
    """Custom form field with label and input"""

    def __init__(self, label_text: str, input_type: str = 'text',
                 values: List[str] = None, required: bool = False, **kwargs):
        super().__init__(orientation='horizontal', spacing=dp(10),
                        size_hint_y=None, height=dp(40), **kwargs)

        # Label
        label = RTLLabel(
            text=label_text + (' *' if required else ''),
            size_hint_x=0.3,
            font_size='14sp'
        )
        self.add_widget(label)

        # Input widget based on type
        if input_type == 'spinner' and values:
            self.input = Spinner(
                text='اختر...',
                values=values,
                size_hint_x=0.7
            )
        elif input_type == 'multiline':
            self.input = TextInput(
                multiline=True,
                size_hint_x=0.7,
                height=dp(80)
            )
            self.height = dp(80)
        else:
            self.input = TextInput(
                multiline=False,
                size_hint_x=0.7
            )

        self.add_widget(self.input)

    def get_value(self) -> str:
        """Get input value"""
        return self.input.text

    def set_value(self, value: str):
        """Set input value"""
        self.input.text = str(value) if value else ''

    def clear(self):
        """Clear input"""
        if hasattr(self.input, 'text'):
            self.input.text = ''


class CustomActionButton(Button):
    """Custom action button with icon and styling"""

    def __init__(self, text: str, icon_path: str = None,
                 action: Callable = None, button_type: str = 'primary', **kwargs):
        super().__init__(**kwargs)

        self.text = text
        self.size_hint_y = None
        self.height = dp(40)

        # Set button color based on type
        colors = {
            'primary': [0.2, 0.4, 0.8, 1],
            'success': [0.2, 0.7, 0.3, 1],
            'warning': [0.8, 0.5, 0.2, 1],
            'danger': [0.7, 0.3, 0.2, 1],
            'secondary': [0.5, 0.5, 0.5, 1]
        }

        self.background_color = colors.get(button_type, colors['primary'])

        # Bind action if provided
        if action:
            self.bind(on_press=lambda x: action())


class SearchBox(BoxLayout):
    """Search input with filter options"""

    def __init__(self, search_callback: Callable = None, **kwargs):
        super().__init__(orientation='horizontal', spacing=dp(10),
                        size_hint_y=None, height=dp(40), **kwargs)

        self.search_callback = search_callback

        # Search input
        self.search_input = TextInput(
            hint_text='البحث...',
            multiline=False,
            size_hint_x=0.7
        )
        self.search_input.bind(text=self.on_search_text)
        self.add_widget(self.search_input)

        # Search button
        search_btn = CustomActionButton(
            text='بحث',
            size_hint_x=0.15,
            action=self.perform_search
        )
        self.add_widget(search_btn)

        # Clear button
        clear_btn = CustomActionButton(
            text='مسح',
            button_type='secondary',
            size_hint_x=0.15,
            action=self.clear_search
        )
        self.add_widget(clear_btn)

    def on_search_text(self, instance, value):
        """Handle search text change"""
        if len(value) > 2 or value == '':
            Clock.schedule_once(lambda dt: self.perform_search(), 0.5)

    def perform_search(self):
        """Perform search"""
        if self.search_callback:
            self.search_callback(self.search_input.text)

    def clear_search(self):
        """Clear search"""
        self.search_input.text = ''
        self.perform_search()


class DataTable(BoxLayout):
    """Custom data table with scrolling"""

    def __init__(self, columns: List[Dict], data: List[Dict] = None,
                 row_callback: Callable = None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.columns = columns
        self.row_callback = row_callback
        self.data = data or []

        # Header
        header_layout = GridLayout(
            cols=len(columns),
            size_hint_y=None,
            height=dp(40),
            spacing=1
        )

        # Add column headers
        for col in columns:
            header_btn = Button(
                text=col['title'],
                size_hint_y=None,
                height=dp(40),
                background_color=[0.3, 0.3, 0.3, 1]
            )
            header_layout.add_widget(header_btn)

        self.add_widget(header_layout)

        # Scrollable content
        self.scroll = ScrollView()
        self.content_layout = GridLayout(
            cols=len(columns),
            spacing=1,
            size_hint_y=None
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))

        self.scroll.add_widget(self.content_layout)
        self.add_widget(self.scroll)

        # Load initial data
        if self.data:
            self.update_data(self.data)

    def update_data(self, data: List[Dict]):
        """Update table data"""
        self.data = data
        self.content_layout.clear_widgets()

        for row_data in data:
            for col in self.columns:
                field_key = col['field']
                value = str(row_data.get(field_key, ''))

                # Truncate long text
                if len(value) > 30:
                    value = value[:27] + '...'

                cell_btn = Button(
                    text=value,
                    size_hint_y=None,
                    height=dp(35),
                    background_color=[1, 1, 1, 1],
                    color=[0, 0, 0, 1]
                )

                # Bind row selection
                if self.row_callback:
                    cell_btn.bind(on_press=lambda x, r=row_data: self.row_callback(r))

                self.content_layout.add_widget(cell_btn)


class ConfirmDialog(Popup):
    """Confirmation dialog popup"""

    def __init__(self, title: str, message: str,
                 confirm_callback: Callable = None, **kwargs):
        super().__init__(**kwargs)

        self.title = title
        self.size_hint = (0.8, 0.4)
        self.auto_dismiss = False
        self.confirm_callback = confirm_callback

        # Content layout
        content = BoxLayout(orientation='vertical', spacing=dp(20), padding=dp(20))

        # Message
        message_label = RTLLabel(
            text=message,
            font_size='16sp'
        )
        content.add_widget(message_label)

        # Buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=dp(10),
                                 size_hint_y=None, height=dp(40))

        confirm_btn = CustomActionButton(
            text='نعم',
            button_type='success',
            action=self.confirm_action
        )
        button_layout.add_widget(confirm_btn)

        cancel_btn = CustomActionButton(
            text='إلغاء',
            button_type='secondary',
            action=self.dismiss
        )
        button_layout.add_widget(cancel_btn)

        content.add_widget(button_layout)
        self.content = content

    def confirm_action(self):
        """Handle confirm action"""
        if self.confirm_callback:
            self.confirm_callback()
        self.dismiss()


class MessageDialog(Popup):
    """Message dialog popup"""

    def __init__(self, title: str, message: str, message_type: str = 'info', **kwargs):
        super().__init__(**kwargs)

        self.title = title
        self.size_hint = (0.6, 0.3)
        self.auto_dismiss = True

        # Content layout
        content = BoxLayout(orientation='vertical', spacing=dp(20), padding=dp(20))

        # Message with appropriate color
        colors = {
            'success': [0.2, 0.7, 0.3, 1],
            'warning': [0.8, 0.5, 0.2, 1],
            'error': [0.7, 0.3, 0.2, 1],
            'info': [0.2, 0.4, 0.8, 1]
        }

        message_label = RTLLabel(
            text=message,
            font_size='16sp',
            color=colors.get(message_type, colors['info'])
        )
        content.add_widget(message_label)

        # OK button
        ok_btn = CustomActionButton(
            text='موافق',
            action=self.dismiss,
            size_hint_y=None,
            height=dp(40)
        )
        content.add_widget(ok_btn)

        self.content = content


class ImageViewer(Popup):
    """Image viewer popup"""

    def __init__(self, image_path: str, title: str = "عرض الصورة", **kwargs):
        super().__init__(**kwargs)

        self.title = title
        self.size_hint = (0.9, 0.9)

        # Content layout
        content = BoxLayout(orientation='vertical', spacing=dp(10))

        # Image
        try:
            image = Image(
                source=image_path,
                fit_mode="contain"
            )
            content.add_widget(image)
        except Exception as e:
            error_label = RTLLabel(
                text=f"خطأ في تحميل الصورة: {str(e)}",
                font_size='16sp'
            )
            content.add_widget(error_label)

        # Close button
        close_btn = CustomActionButton(
            text='إغلاق',
            action=self.dismiss,
            size_hint_y=None,
            height=dp(40)
        )
        content.add_widget(close_btn)

        self.content = content


class PhotoUploader(Popup):
    """Photo upload dialog"""

    def __init__(self, upload_callback: Callable = None, **kwargs):
        super().__init__(**kwargs)

        self.title = 'رفع صورة'
        self.size_hint = (0.9, 0.8)
        self.upload_callback = upload_callback

        # Content layout
        content = BoxLayout(orientation='vertical', spacing=dp(10))

        # File chooser
        self.file_chooser = FileChooserIconView(
            filters=['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif'],
            path=os.path.expanduser('~')
        )
        content.add_widget(self.file_chooser)

        # Buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=dp(10),
                                 size_hint_y=None, height=dp(40))

        upload_btn = CustomActionButton(
            text='رفع',
            button_type='success',
            action=self.upload_file
        )
        button_layout.add_widget(upload_btn)

        cancel_btn = CustomActionButton(
            text='إلغاء',
            button_type='secondary',
            action=self.dismiss
        )
        button_layout.add_widget(cancel_btn)

        content.add_widget(button_layout)
        self.content = content

    def upload_file(self):
        """Handle file upload"""
        if self.file_chooser.selection:
            file_path = self.file_chooser.selection[0]
            if self.upload_callback:
                self.upload_callback(file_path)
            self.dismiss()


class ProgressDialog(Popup):
    """Progress dialog for long operations"""

    def __init__(self, title: str = "يرجى الانتظار...", **kwargs):
        super().__init__(**kwargs)

        self.title = title
        self.size_hint = (0.6, 0.2)
        self.auto_dismiss = False

        # Content layout
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))

        # Progress bar
        self.progress_bar = ProgressBar(max=100)
        content.add_widget(self.progress_bar)

        # Status label
        self.status_label = RTLLabel(
            text='جارٍ المعالجة...',
            font_size='14sp'
        )
        content.add_widget(self.status_label)

        self.content = content

    def update_progress(self, value: int, status: str = None):
        """Update progress value and status"""
        self.progress_bar.value = value
        if status:
            self.status_label.text = status


class StatsCard(BoxLayout):
    """Statistics card widget"""

    def __init__(self, title: str, value: str, icon_path: str = None,
                 color: List[float] = None, **kwargs):
        super().__init__(orientation='vertical', spacing=dp(5),
                        size_hint_y=None, height=dp(120), **kwargs)

        # Set background color
        with self.canvas.before:
            Color(*(color or [0.2, 0.4, 0.8, 1]))
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

        # Icon (if provided)
        if icon_path:
            icon = Image(
                source=icon_path,
                size_hint_y=0.4
            )
            self.add_widget(icon)

        # Value
        value_label = Label(
            text=str(value),
            font_size='24sp',
            bold=True,
            size_hint_y=0.4
        )
        self.add_widget(value_label)

        # Title
        title_label = RTLLabel(
            text=title,
            font_size='14sp',
            size_hint_y=0.2
        )
        self.add_widget(title_label)

    def update_rect(self, *args):
        """Update background rectangle"""
        self.rect.pos = self.pos
        self.rect.size = self.size


# Import os for PhotoUploader
import os
