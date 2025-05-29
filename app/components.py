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
from app.font_manager import font_manager
from app.language_manager import language_manager

logger = logging.getLogger(__name__)


class RTLLabel(Label):
    """Label with RTL text support for Arabic"""

    def __init__(self, **kwargs):
        # Set font name based on text content before calling super
        text = kwargs.get('text', '')
        if 'font_name' not in kwargs:
            kwargs['font_name'] = font_manager.get_font_name(text)

        super().__init__(**kwargs)
        self.text_size = (None, None)
        self.halign = 'right'
        self.valign = 'middle'
        self.bind(size=self.update_text_size)
        self.bind(text=self.update_font)

    def update_text_size(self, *args):
        """Update text size when widget size changes"""
        self.text_size = self.size

    def update_font(self, *args):
        """Update font when text changes"""
        self.font_name = font_manager.get_font_name(self.text)


class FormField(BoxLayout):
    """Custom form field with label and input"""

    def __init__(self, label_text: str, input_type: str = 'text',
                 values: List[str] = None, required: bool = False, **kwargs):
        # Handle size_hint_y conflict by extracting it before calling super
        size_hint_y = kwargs.pop('size_hint_y', None)
        height = kwargs.pop('height', dp(40))

        super().__init__(orientation='horizontal', spacing=dp(10), **kwargs)

        # Set size properties after initialization
        self.size_hint_y = size_hint_y if size_hint_y is not None else None
        self.height = height

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
                size_hint_x=0.7,
                font_name=font_manager.get_font_name('اختر...')
            )
        elif input_type == 'multiline':
            self.input = TextInput(
                multiline=True,
                size_hint_x=0.7,
                height=dp(80),
                font_name=font_manager.get_font_name()
            )
            self.height = dp(80)
        else:
            self.input = TextInput(
                multiline=False,
                size_hint_x=0.7,
                font_name=font_manager.get_font_name()
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
        # Handle size_hint_y conflict by extracting it before calling super
        size_hint_y = kwargs.pop('size_hint_y', None)
        height = kwargs.pop('height', dp(40))

        # Set font name before calling super
        if 'font_name' not in kwargs:
            kwargs['font_name'] = font_manager.get_font_name(text)

        super().__init__(**kwargs)

        self.text = text
        # Set size properties after initialization
        self.size_hint_y = size_hint_y if size_hint_y is not None else None
        self.height = height

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
            size_hint_x=0.7,
            font_name=font_manager.get_font_name('البحث...')
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
                background_color=[0.3, 0.3, 0.3, 1],
                font_name=font_manager.get_font_name(col['title'])
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
                    color=[0, 0, 0, 1],
                    font_name=font_manager.get_font_name(value)
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


class LanguageSwitcher(BoxLayout):
    """Language switcher component"""

    def __init__(self, **kwargs):
        # Extract size_hint_y and height to avoid multiple values error
        size_hint_y = kwargs.pop('size_hint_y', None)
        height = kwargs.pop('height', None)
        super().__init__(orientation='horizontal', spacing=dp(5), **kwargs)
        if size_hint_y is not None:
            self.size_hint_y = size_hint_y
        if height is not None:
            self.height = height

        # Language label
        self.language_label = RTLLabel(
            text=language_manager.get_text('language'),
            size_hint_x=0.4,
            font_size='14sp'
        )
        self.add_widget(self.language_label)

        # Language toggle button
        self.toggle_btn = Button(
            text=self.get_toggle_text(),
            size_hint_x=0.6,
            font_size='14sp',
            font_name=font_manager.get_font_name(self.get_toggle_text()),
            background_color=[0.2, 0.6, 0.8, 1]
        )
        self.toggle_btn.bind(on_press=self.toggle_language)
        self.add_widget(self.toggle_btn)

        # Register for language change notifications
        language_manager.add_observer(self)

    def get_toggle_text(self):
        """Get text for toggle button"""
        if language_manager.current_language == 'ar':
            return 'EN | English'
        else:
            return 'ع | العربية'

    def toggle_language(self, *args):
        """Toggle between Arabic and English"""
        language_manager.switch_language()

    def on_language_changed(self):
        """Called when language changes"""
        self.language_label.text = language_manager.get_text('language')
        self.toggle_btn.text = self.get_toggle_text()
        self.toggle_btn.font_name = font_manager.get_font_name(self.toggle_btn.text)


class TranslatableLabel(RTLLabel):
    """Label that updates when language changes"""

    def __init__(self, translation_key: str, **kwargs):
        self.translation_key = translation_key
        kwargs['text'] = language_manager.get_text(translation_key)
        super().__init__(**kwargs)
        language_manager.add_observer(self)

    def on_language_changed(self):
        """Called when language changes"""
        self.text = language_manager.get_text(self.translation_key)
        self.font_name = font_manager.get_font_name(self.text)


class BilingualLabel(RTLLabel):
    """Label that shows both Arabic and English text"""

    def __init__(self, translation_key: str = None, text_en: str = None, text_ar: str = None, **kwargs):
        # Handle size_hint_y conflict by extracting it before calling super
        size_hint_y = kwargs.pop('size_hint_y', None)
        height = kwargs.pop('height', None)

        # Support both translation_key and direct text_en/text_ar approach
        if translation_key:
            self.translation_key = translation_key
            kwargs['text'] = language_manager.get_text(translation_key)
        elif text_en and text_ar:
            self.translation_key = None
            self.text_en = text_en
            self.text_ar = text_ar
            # Use current language to determine which text to show
            if language_manager.current_language == 'en':
                kwargs['text'] = text_en
            else:
                kwargs['text'] = text_ar
        else:
            raise ValueError("BilingualLabel requires either translation_key or both text_en and text_ar")

        super().__init__(**kwargs)

        # Set size properties after initialization
        if size_hint_y is not None:
            self.size_hint_y = size_hint_y
        if height is not None:
            self.height = height

        language_manager.add_observer(self)

    def on_language_changed(self):
        """Called when language changes"""
        if self.translation_key:
            self.text = language_manager.get_text(self.translation_key)
        elif hasattr(self, 'text_en') and hasattr(self, 'text_ar'):
            if language_manager.current_language == 'en':
                self.text = self.text_en
            else:
                self.text = self.text_ar
        self.font_name = font_manager.get_font_name(self.text)


class TranslatableButton(CustomActionButton):
    """Button that updates when language changes"""

    def __init__(self, translation_key: str, **kwargs):
        # Handle size_hint_y conflict by extracting it before calling super
        size_hint_y = kwargs.pop('size_hint_y', None)
        height = kwargs.pop('height', None)

        self.translation_key = translation_key
        text = language_manager.get_text(translation_key)
        super().__init__(text=text, **kwargs)

        # Set size properties after initialization
        if size_hint_y is not None:
            self.size_hint_y = size_hint_y
        if height is not None:
            self.height = height

        language_manager.add_observer(self)

    def on_language_changed(self):
        """Called when language changes"""
        self.text = language_manager.get_text(self.translation_key)
        self.font_name = font_manager.get_font_name(self.text)


class BilingualButton(CustomActionButton):
    """Button that shows both Arabic and English text"""

    def __init__(self, translation_key: str, **kwargs):
        # Handle size_hint_y conflict by extracting it before calling super
        size_hint_y = kwargs.pop('size_hint_y', None)
        height = kwargs.pop('height', None)

        self.translation_key = translation_key
        text = language_manager.get_text(translation_key)
        super().__init__(text=text, **kwargs)

        # Set size properties after initialization
        if size_hint_y is not None:
            self.size_hint_y = size_hint_y
        if height is not None:
            self.height = height

        language_manager.add_observer(self)

    def on_language_changed(self):
        """Called when language changes"""
        self.text = language_manager.get_text(self.translation_key)
        self.font_name = font_manager.get_font_name(self.text)


class NavigationHeader(BoxLayout):
    """Modern navigation header with back to menu button and screen title"""

    def __init__(self, screen_title_key: str = None, show_back_button: bool = True, **kwargs):
        # Extract size_hint_y and height to avoid conflicts
        size_hint_y = kwargs.pop('size_hint_y', None)
        height = kwargs.pop('height', dp(60))

        super().__init__(orientation='horizontal', spacing=dp(15), padding=[20, 10, 20, 10], **kwargs)

        # Set size properties after initialization
        if size_hint_y is not None:
            self.size_hint_y = size_hint_y
        else:
            self.size_hint_y = None
        self.height = height

        # Back to menu button (if enabled)
        if show_back_button:
            self.back_btn = TranslatableButton(
                translation_key='back_to_menu',
                size_hint_x=None,
                width=dp(120),
                height=dp(40),
                background_color=[0.3, 0.6, 0.9, 1],
                font_size='14sp'
            )
            self.back_btn.bind(on_press=self.go_back_to_menu)
            self.add_widget(self.back_btn)

        # Screen title
        if screen_title_key:
            self.title_label = BilingualLabel(
                translation_key=screen_title_key,
                font_size='24sp',
                bold=True,
                color=[0.2, 0.2, 0.3, 1],
                halign='center',
                valign='middle'
            )
            self.add_widget(self.title_label)

        # Language switcher (right side)
        self.lang_switcher = LanguageSwitcher(
            size_hint_x=None,
            width=dp(150),
            height=dp(35)
        )
        self.add_widget(self.lang_switcher)

    def go_back_to_menu(self, instance):
        """Navigate back to dashboard"""
        from kivy.app import App
        app = App.get_running_app()
        if app and hasattr(app, 'goto_dashboard'):
            app.goto_dashboard()
        elif app and hasattr(app.screen_manager, 'current'):
            # Fallback to direct navigation
            app.screen_manager.current = 'dashboard'


class ResponsiveCard(BoxLayout):
    """Modern card layout with shadow effect and responsive design"""

    def __init__(self, title: str = None, **kwargs):
        # Extract conflicting parameters
        size_hint_y = kwargs.pop('size_hint_y', None)
        height = kwargs.pop('height', None)
        orientation = kwargs.pop('orientation', 'vertical')  # Default to vertical
        spacing = kwargs.pop('spacing', dp(10))
        padding = kwargs.pop('padding', [20, 15, 20, 15])

        super().__init__(orientation=orientation, spacing=spacing, padding=padding, **kwargs)

        # Set size properties
        if size_hint_y is not None:
            self.size_hint_y = size_hint_y
        if height is not None:
            self.height = height

        # Add card styling with canvas
        with self.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(1, 1, 1, 0.95)  # White background with slight transparency
            self.bg_rect = RoundedRectangle(radius=[10])
            self.bind(size=self._update_bg, pos=self._update_bg)

        # Card title if provided
        if title:
            title_label = BilingualLabel(
                translation_key=title,
                font_size='18sp',
                bold=True,
                color=[0.2, 0.2, 0.3, 1],
                size_hint_y=None,
                height=dp(35)
            )
            self.add_widget(title_label)

    def _update_bg(self, *args):
        """Update background rectangle size and position"""
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
