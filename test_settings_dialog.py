#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Script for Settings Dialog with Theme Switcher
"""

import os
import sys
import logging
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / 'app'
sys.path.insert(0, str(app_dir))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from app.components import SettingsDialog

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestApp(App):
    """Test application for settings dialog"""

    def build(self):
        """Build test UI"""
        main_layout = BoxLayout(orientation='vertical', padding=[30, 30], spacing=20)

        # Test button
        test_button = Button(
            text='Open Settings Dialog',
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={'center_x': 0.5}
        )
        test_button.bind(on_press=self.open_settings)
        main_layout.add_widget(test_button)

        return main_layout

    def open_settings(self, instance):
        """Open settings dialog"""
        settings_dialog = SettingsDialog()
        settings_dialog.open()


if __name__ == '__main__':
    TestApp().run()
