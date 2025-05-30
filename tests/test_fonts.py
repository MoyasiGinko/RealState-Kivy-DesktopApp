#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Test - Quick test to verify Arabic font integration
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / 'app'
sys.path.insert(0, str(app_dir))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

# Import our modules
from font_manager import font_manager

class FontTestApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=20, padding=20)

        # Test Arabic text
        arabic_text = "مرحبا بكم في نظام إدارة العقارات"
        english_text = "Welcome to Real Estate Management System"
        mixed_text = f"{arabic_text}\n{english_text}"

        # Test font detection
        print(f"Arabic font detected: {font_manager.get_font_name(arabic_text)}")
        print(f"English font detected: {font_manager.get_font_name(english_text)}")
        print(f"Mixed font detected: {font_manager.get_font_name(mixed_text)}")

        # Test label with Arabic text
        arabic_label = Label(
            text=arabic_text,
            font_size='20sp',
            font_name=font_manager.get_font_name(arabic_text)
        )
        layout.add_widget(arabic_label)

        # Test label with English text
        english_label = Label(
            text=english_text,
            font_size='20sp',
            font_name=font_manager.get_font_name(english_text)
        )
        layout.add_widget(english_label)

        # Test button with mixed text
        mixed_button = Button(
            text=mixed_text,
            font_size='18sp',
            font_name=font_manager.get_font_name(mixed_text)
        )
        layout.add_widget(mixed_button)

        return layout

if __name__ == '__main__':
    FontTestApp().run()
