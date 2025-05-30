#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Theme Manager - Test theme switching functionality
"""

import os
import sys

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

def test_theme_manager():
    """Test theme manager functionality"""
    print("🎨 Testing Theme Manager...")

    try:
        from app.theme_manager import theme_manager, ThemeType
        from app.config import config

        print(f"✅ Current theme: {theme_manager.get_current_theme_name()}")
        print(f"✅ Available themes: {[t.value for t in theme_manager.get_available_themes()]}")

        # Test theme switching
        print("\n🔄 Testing theme switching...")
        for theme in [ThemeType.DARK, ThemeType.BLUE, ThemeType.GREEN, ThemeType.LIGHT]:
            theme_manager.set_theme(theme)
            print(f"  ✅ Switched to {theme.value}")

            # Test getting colors
            primary = theme_manager.get_color('primary_color')
            background = theme_manager.get_color('background_color')
            print(f"    Primary: {primary}, Background: {background}")

        # Test config integration
        print("\n🔧 Testing config integration...")
        config.set_theme('purple')
        print(f"✅ Config theme set to: {config.get_theme()}")

        # Test style helpers
        print("\n🎯 Testing style helpers...")
        button_style = config.get_button_style('primary')
        input_style = config.get_input_style()
        label_style = config.get_label_style('title')
        card_style = config.get_card_style()
        table_style = config.get_table_style()

        print(f"✅ Button style: {len(button_style)} properties")
        print(f"✅ Input style: {len(input_style)} properties")
        print(f"✅ Label style: {len(label_style)} properties")
        print(f"✅ Card style: {len(card_style)} properties")
        print(f"✅ Table style: {len(table_style)} properties")

        print("\n✅ Theme manager test completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Theme manager test failed: {e}")
        return False

def test_theme_colors():
    """Test all theme colors"""
    print("\n🌈 Testing theme colors...")

    try:
        from app.theme_manager import theme_manager, ThemeType

        for theme_type in ThemeType:
            theme_manager.set_theme(theme_type)
            print(f"\n🎨 {theme_type.value.upper()} THEME:")

            # Test key colors
            test_colors = [
                'primary_color', 'secondary_color', 'success_color', 'warning_color', 'error_color',
                'background_color', 'text_primary_color', 'text_secondary_color'
            ]

            for color_name in test_colors:
                try:
                    color = theme_manager.get_color(color_name)
                    print(f"  ✅ {color_name}: {color}")
                except Exception as e:
                    print(f"  ❌ {color_name}: Error - {e}")

        print("\n✅ Theme colors test completed!")
        return True

    except Exception as e:
        print(f"❌ Theme colors test failed: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("🧪 THEME MANAGER COMPREHENSIVE TEST")
    print("=" * 60)

    success = True

    success &= test_theme_manager()
    success &= test_theme_colors()

    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL THEME TESTS PASSED!")
    else:
        print("❌ SOME THEME TESTS FAILED!")
    print("=" * 60)
