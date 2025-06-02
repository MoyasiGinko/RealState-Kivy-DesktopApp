#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Enhanced Settings Screen
Modern settings interface with integration layer support
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, OneLineListItem, OneLineIconListItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivy.metrics import dp
from kivy.clock import Clock
import logging
from datetime import datetime
import os

from app.views.modern_components import (
    DesignTokens, ModernCard, ModernButton, ModernTextField
)
from app.utils import BilingualLabel
from app.database import DatabaseManager

logger = logging.getLogger(__name__)


class EnhancedSettingsScreen(MDScreen):
    """Enhanced settings screen with modern design and full integration"""

    def __init__(self, db_manager: DatabaseManager = None, **kwargs):
        super().__init__(**kwargs)
        self.name = 'enhanced_settings'
        self.db = db_manager
        self.integration_layer = None
        self.current_settings = {}
        self.file_manager = None
        self.settings_dialog = None

        self.build_modern_ui()
        Clock.schedule_once(self.load_settings_data, 0.5)

    def set_integration_layer(self, integration_layer):
        """Set the integration layer for advanced functionality"""
        self.integration_layer = integration_layer
        logger.info("Integration layer connected to settings screen")
        self.load_settings_data()

    def build_modern_ui(self):
        """Build modern settings UI"""
        # Main container
        main_container = MDBoxLayout(
            orientation='vertical',
            md_bg_color=DesignTokens.COLORS['background']
        )

        # Top App Bar
        self.build_app_bar(main_container)

        # Scrollable content
        scroll = MDScrollView()
        content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['lg'],
            padding=[DesignTokens.SPACING['md'], DesignTokens.SPACING['md']],
            adaptive_height=True
        )

        # Settings sections
        self.build_system_section(content_layout)
        self.build_backup_section(content_layout)
        self.build_database_section(content_layout)
        self.build_interface_section(content_layout)
        self.build_advanced_section(content_layout)

        scroll.add_widget(content_layout)
        main_container.add_widget(scroll)
        self.add_widget(main_container)

    def build_app_bar(self, parent):
        """Build app bar for settings"""
        app_bar = MDTopAppBar(
            title="System Settings",
            md_bg_color=DesignTokens.COLORS['primary'],
            specific_text_color=DesignTokens.COLORS['card'],
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[
                ["content-save", lambda x: self.save_all_settings()],
                ["refresh", lambda x: self.reload_settings()]
            ]
        )
        parent.add_widget(app_bar)

    def build_system_section(self, parent):
        """Build system settings section"""
        # System Status Card
        system_card = ModernCard(
            title="System Status",
            elevation=2,
            padding=DesignTokens.SPACING['md']
        )

        system_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['sm']
        )

        # System health status
        self.system_status_label = MDLabel(
            text="Loading system status...",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(30)
        )
        system_layout.add_widget(self.system_status_label)

        # System actions
        actions_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['sm'],
            size_hint_y=None,
            height=dp(40)
        )

        health_check_btn = ModernButton(
            text="Check System Health",
            on_release=self.check_system_health
        )
        actions_layout.add_widget(health_check_btn)

        view_logs_btn = ModernButton(
            text="View Activity Logs",
            on_release=self.view_activity_logs
        )
        actions_layout.add_widget(view_logs_btn)

        system_layout.add_widget(actions_layout)
        system_card.add_widget(system_layout)
        parent.add_widget(system_card)

    def build_backup_section(self, parent):
        """Build backup settings section"""
        backup_card = ModernCard(
            title="Backup & Data Management",
            elevation=2,
            padding=DesignTokens.SPACING['md']
        )

        backup_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['sm']
        )

        # Last backup info
        self.last_backup_label = MDLabel(
            text="Loading backup information...",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(30)
        )
        backup_layout.add_widget(self.last_backup_label)

        # Backup actions
        backup_actions = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['sm'],
            size_hint_y=None,
            height=dp(40)
        )

        create_backup_btn = ModernButton(
            text="Create Full Backup",
            on_release=self.create_full_backup
        )
        backup_actions.add_widget(create_backup_btn)

        export_data_btn = ModernButton(
            text="Export Data",
            on_release=self.export_data
        )
        backup_actions.add_widget(export_data_btn)

        restore_btn = ModernButton(
            text="Restore Backup",
            on_release=self.restore_backup
        )
        backup_actions.add_widget(restore_btn)

        backup_layout.add_widget(backup_actions)

        # Auto-backup settings
        auto_backup_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['md'],
            size_hint_y=None,
            height=dp(40)
        )

        auto_backup_label = MDLabel(
            text="Enable automatic daily backups",
            size_hint_x=0.7
        )
        auto_backup_layout.add_widget(auto_backup_label)

        self.auto_backup_switch = MDSwitch(
            size_hint_x=0.3,
            pos_hint={"center_y": 0.5}
        )
        auto_backup_layout.add_widget(self.auto_backup_switch)

        backup_layout.add_widget(auto_backup_layout)
        backup_card.add_widget(backup_layout)
        parent.add_widget(backup_card)

    def build_database_section(self, parent):
        """Build database settings section"""
        db_card = ModernCard(
            title="Database Management",
            elevation=2,
            padding=DesignTokens.SPACING['md']
        )

        db_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['sm']
        )

        # Database info
        self.db_info_label = MDLabel(
            text="Loading database information...",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(30)
        )
        db_layout.add_widget(self.db_info_label)

        # Database actions
        db_actions = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['sm'],
            size_hint_y=None,
            height=dp(40)
        )

        optimize_btn = ModernButton(
            text="Optimize Database",
            on_release=self.optimize_database
        )
        db_actions.add_widget(optimize_btn)

        repair_btn = ModernButton(
            text="Repair Database",
            on_release=self.repair_database
        )
        db_actions.add_widget(repair_btn)

        db_layout.add_widget(db_actions)
        db_card.add_widget(db_layout)
        parent.add_widget(db_card)

    def build_interface_section(self, parent):
        """Build interface settings section"""
        interface_card = ModernCard(
            title="Interface Settings",
            elevation=2,
            padding=DesignTokens.SPACING['md']
        )

        interface_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['sm']
        )

        # Language setting
        lang_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['md'],
            size_hint_y=None,
            height=dp(40)
        )

        lang_label = MDLabel(
            text="Default Language:",
            size_hint_x=0.5
        )
        lang_layout.add_widget(lang_label)

        self.language_field = MDTextField(
            text="Arabic",
            size_hint_x=0.5,
            readonly=True
        )
        lang_layout.add_widget(self.language_field)

        interface_layout.add_widget(lang_layout)

        # Theme setting
        theme_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['md'],
            size_hint_y=None,
            height=dp(40)
        )

        theme_label = MDLabel(
            text="Enable dark theme",
            size_hint_x=0.7
        )
        theme_layout.add_widget(theme_label)

        self.dark_theme_switch = MDSwitch(
            size_hint_x=0.3,
            pos_hint={"center_y": 0.5}
        )
        theme_layout.add_widget(self.dark_theme_switch)

        interface_layout.add_widget(theme_layout)
        interface_card.add_widget(interface_layout)
        parent.add_widget(interface_card)

    def build_advanced_section(self, parent):
        """Build advanced settings section"""
        advanced_card = ModernCard(
            title="Advanced Settings",
            elevation=2,
            padding=DesignTokens.SPACING['md']
        )

        advanced_layout = MDBoxLayout(
            orientation='vertical',
            spacing=DesignTokens.SPACING['sm']
        )

        # Debug mode
        debug_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['md'],
            size_hint_y=None,
            height=dp(40)
        )

        debug_label = MDLabel(
            text="Enable debug logging",
            size_hint_x=0.7
        )
        debug_layout.add_widget(debug_label)

        self.debug_switch = MDSwitch(
            size_hint_x=0.3,
            pos_hint={"center_y": 0.5}
        )
        debug_layout.add_widget(self.debug_switch)

        advanced_layout.add_widget(debug_layout)

        # Export/Import settings
        settings_actions = MDBoxLayout(
            orientation='horizontal',
            spacing=DesignTokens.SPACING['sm'],
            size_hint_y=None,
            height=dp(40)
        )

        export_settings_btn = ModernButton(
            text="Export Settings",
            on_release=self.export_settings
        )
        settings_actions.add_widget(export_settings_btn)

        import_settings_btn = ModernButton(
            text="Import Settings",
            on_release=self.import_settings
        )
        settings_actions.add_widget(import_settings_btn)

        reset_settings_btn = ModernButton(
            text="Reset to Defaults",
            on_release=self.reset_settings
        )
        settings_actions.add_widget(reset_settings_btn)

        advanced_layout.add_widget(settings_actions)
        advanced_card.add_widget(advanced_layout)
        parent.add_widget(advanced_card)

    def load_settings_data(self, dt=None):
        """Load current settings data"""
        try:
            if self.integration_layer:
                # Load settings via integration layer
                self.current_settings = self.integration_layer.get_application_settings()

                # Update system status
                health_status = self.integration_layer.get_system_health_status()
                self.update_system_status_display(health_status)

                # Update backup info
                self.update_backup_info_display()

                # Update database info
                self.update_database_info_display()

                # Update UI controls with current settings
                self.update_settings_controls()

                logger.info("Settings data loaded via integration layer")
            else:
                # Fallback to basic settings
                self.load_basic_settings()

        except Exception as e:
            logger.error(f"Error loading settings data: {e}")
            self.show_error_dialog(f"Failed to load settings: {str(e)}")

    def load_basic_settings(self):
        """Load basic settings when integration layer is not available"""
        self.current_settings = {
            'auto_backup': False,
            'dark_theme': False,
            'debug_mode': False,
            'language': 'Arabic'
        }

        self.system_status_label.text = "System status: Basic mode"
        self.last_backup_label.text = "Backup information not available"
        self.db_info_label.text = "Database information not available"

    def update_system_status_display(self, health_status):
        """Update system status display"""
        try:
            overall_health = health_status.get('overall_health', 'unknown')

            status_text = f"System Health: {overall_health.title()}"
            if health_status.get('database_status') == 'connected':
                status_text += " | Database: Connected"
            else:
                status_text += " | Database: Disconnected"

            disk_info = health_status.get('disk_space', {})
            if disk_info.get('free_gb'):
                status_text += f" | Free Space: {disk_info['free_gb']}GB"

            self.system_status_label.text = status_text

        except Exception as e:
            logger.error(f"Error updating system status display: {e}")
            self.system_status_label.text = "Error loading system status"

    def update_backup_info_display(self):
        """Update backup information display"""
        try:
            if self.integration_layer:
                health_status = self.integration_layer.get_system_health_status()
                last_backup = health_status.get('last_backup', {})

                if last_backup.get('exists'):
                    days_ago = last_backup.get('days_ago', 0)
                    backup_text = f"Last backup: {days_ago} days ago"
                    if days_ago > 7:
                        backup_text += " (Warning: Old backup)"
                else:
                    backup_text = "No backups found"

                self.last_backup_label.text = backup_text

        except Exception as e:
            logger.error(f"Error updating backup info: {e}")
            self.last_backup_label.text = "Error loading backup information"

    def update_database_info_display(self):
        """Update database information display"""
        try:
            if self.integration_layer:
                health_status = self.integration_layer.get_system_health_status()

                total_properties = health_status.get('total_properties', 0)
                total_owners = health_status.get('total_owners', 0)

                db_text = f"Properties: {total_properties} | Owners: {total_owners}"
                self.db_info_label.text = db_text

        except Exception as e:
            logger.error(f"Error updating database info: {e}")
            self.db_info_label.text = "Error loading database information"

    def update_settings_controls(self):
        """Update UI controls with current settings"""
        try:
            # Update switches and fields based on current settings
            self.auto_backup_switch.active = self.current_settings.get('auto_backup', False)
            self.dark_theme_switch.active = self.current_settings.get('dark_theme', False)
            self.debug_switch.active = self.current_settings.get('debug_mode', False)
            self.language_field.text = self.current_settings.get('language', 'Arabic')

        except Exception as e:
            logger.error(f"Error updating settings controls: {e}")

    # Action methods
    def check_system_health(self, instance):
        """Check and display system health"""
        try:
            if self.integration_layer:
                health_status = self.integration_layer.get_system_health_status()
                self.show_health_dialog(health_status)
            else:
                self.show_info_dialog("System health check not available in basic mode")

        except Exception as e:
            logger.error(f"Error checking system health: {e}")
            self.show_error_dialog(f"Health check failed: {str(e)}")

    def create_full_backup(self, instance):
        """Create a full system backup"""
        try:
            if self.integration_layer:
                result = self.integration_layer.create_backup_with_notification('full')

                if result.get('success'):
                    self.show_success_dialog(result.get('message', 'Backup created successfully'))
                    self.update_backup_info_display()
                else:
                    self.show_error_dialog(result.get('message', 'Backup failed'))
            else:
                self.show_info_dialog("Backup functionality not available in basic mode")

        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            self.show_error_dialog(f"Backup failed: {str(e)}")

    def export_data(self, instance):
        """Export application data"""
        try:
            if self.integration_layer:
                result = self.integration_layer.create_backup_with_notification('data')

                if result.get('success'):
                    self.show_success_dialog(f"Data exported successfully to {result.get('file_path', 'unknown location')}")
                else:
                    self.show_error_dialog(result.get('message', 'Export failed'))
            else:
                self.show_info_dialog("Export functionality not available in basic mode")

        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            self.show_error_dialog(f"Export failed: {str(e)}")

    def restore_backup(self, instance):
        """Restore from backup"""
        try:
            # Show file chooser for backup file
            if not self.file_manager:
                self.file_manager = MDFileManager(
                    exit_manager=self.exit_file_manager,
                    select_path=self.select_backup_file,
                    ext=['.sql', '.json', '.db']
                )

            self.file_manager.show(os.path.expanduser("~"))

        except Exception as e:
            logger.error(f"Error opening file manager: {e}")
            self.show_error_dialog(f"Failed to open file manager: {str(e)}")

    def select_backup_file(self, path):
        """Handle backup file selection"""
        try:
            self.exit_file_manager()

            if self.integration_layer:
                result = self.integration_layer.restore_backup_with_confirmation(path)

                if result.get('success'):
                    self.show_success_dialog("Backup restored successfully. Please restart the application.")
                else:
                    self.show_error_dialog(result.get('message', 'Restore failed'))
            else:
                self.show_info_dialog("Restore functionality not available in basic mode")

        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            self.show_error_dialog(f"Restore failed: {str(e)}")

    def exit_file_manager(self, *args):
        """Close file manager"""
        if self.file_manager:
            self.file_manager.close()

    def view_activity_logs(self, instance):
        """View activity logs"""
        try:
            if self.integration_layer:
                activities = self.integration_layer.get_activity_log_for_display(limit=100)
                self.show_activity_log_dialog(activities)
            else:
                self.show_info_dialog("Activity logs not available in basic mode")

        except Exception as e:
            logger.error(f"Error viewing activity logs: {e}")
            self.show_error_dialog(f"Failed to load activity logs: {str(e)}")

    def optimize_database(self, instance):
        """Optimize database"""
        try:
            if self.db:
                # Run database optimization
                self.db.execute_query("VACUUM")
                self.show_success_dialog("Database optimized successfully")
            else:
                self.show_error_dialog("Database not available")

        except Exception as e:
            logger.error(f"Error optimizing database: {e}")
            self.show_error_dialog(f"Database optimization failed: {str(e)}")

    def repair_database(self, instance):
        """Repair database"""
        try:
            if self.db:
                # Run database integrity check
                result = self.db.execute_query("PRAGMA integrity_check")
                if result and result[0].get('integrity_check') == 'ok':
                    self.show_success_dialog("Database integrity check passed")
                else:
                    self.show_error_dialog("Database integrity issues detected")
            else:
                self.show_error_dialog("Database not available")

        except Exception as e:
            logger.error(f"Error checking database: {e}")
            self.show_error_dialog(f"Database check failed: {str(e)}")

    def export_settings(self, instance):
        """Export current settings"""
        try:
            if self.integration_layer:
                settings = self.integration_layer.get_application_settings()

                # Save settings to file
                import json
                file_path = f"settings_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(settings, f, indent=2, ensure_ascii=False)

                self.show_success_dialog(f"Settings exported to {file_path}")
            else:
                self.show_info_dialog("Settings export not available in basic mode")

        except Exception as e:
            logger.error(f"Error exporting settings: {e}")
            self.show_error_dialog(f"Settings export failed: {str(e)}")

    def import_settings(self, instance):
        """Import settings from file"""
        try:
            # Show file chooser for settings file
            if not self.file_manager:
                self.file_manager = MDFileManager(
                    exit_manager=self.exit_file_manager,
                    select_path=self.select_settings_file,
                    ext=['.json']
                )

            self.file_manager.show(os.path.expanduser("~"))

        except Exception as e:
            logger.error(f"Error opening file manager: {e}")
            self.show_error_dialog(f"Failed to open file manager: {str(e)}")

    def select_settings_file(self, path):
        """Handle settings file selection"""
        try:
            self.exit_file_manager()

            # Load and apply settings
            import json
            with open(path, 'r', encoding='utf-8') as f:
                new_settings = json.load(f)

            if self.integration_layer:
                result = self.integration_layer.update_application_settings(new_settings)

                if result.get('success'):
                    self.show_success_dialog("Settings imported successfully")
                    self.load_settings_data()
                else:
                    self.show_error_dialog(result.get('message', 'Settings import failed'))
            else:
                self.show_info_dialog("Settings import not available in basic mode")

        except Exception as e:
            logger.error(f"Error importing settings: {e}")
            self.show_error_dialog(f"Settings import failed: {str(e)}")

    def reset_settings(self, instance):
        """Reset settings to defaults"""
        try:
            # Show confirmation dialog
            self.show_confirmation_dialog(
                "Reset Settings",
                "Are you sure you want to reset all settings to default values?",
                self.confirm_reset_settings
            )

        except Exception as e:
            logger.error(f"Error resetting settings: {e}")
            self.show_error_dialog(f"Settings reset failed: {str(e)}")

    def confirm_reset_settings(self, instance):
        """Confirm and execute settings reset"""
        try:
            if self.integration_layer:
                default_settings = {
                    'auto_backup': False,
                    'dark_theme': False,
                    'debug_mode': False,
                    'language': 'Arabic'
                }

                result = self.integration_layer.update_application_settings(default_settings)

                if result.get('success'):
                    self.show_success_dialog("Settings reset to defaults")
                    self.load_settings_data()
                else:
                    self.show_error_dialog(result.get('message', 'Settings reset failed'))
            else:
                self.show_info_dialog("Settings reset not available in basic mode")

        except Exception as e:
            logger.error(f"Error confirming settings reset: {e}")
            self.show_error_dialog(f"Settings reset failed: {str(e)}")

    def save_all_settings(self, instance):
        """Save all current settings"""
        try:
            if self.integration_layer:
                # Collect current settings from UI
                new_settings = {
                    'auto_backup': self.auto_backup_switch.active,
                    'dark_theme': self.dark_theme_switch.active,
                    'debug_mode': self.debug_switch.active,
                    'language': self.language_field.text
                }

                result = self.integration_layer.update_application_settings(new_settings)

                if result.get('success'):
                    self.show_success_dialog("Settings saved successfully")
                else:
                    self.show_error_dialog(result.get('message', 'Settings save failed'))
            else:
                self.show_info_dialog("Settings save not available in basic mode")

        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            self.show_error_dialog(f"Settings save failed: {str(e)}")

    def reload_settings(self, instance):
        """Reload settings from source"""
        self.load_settings_data()
        self.show_info_dialog("Settings reloaded")

    def go_back(self, instance):
        """Navigate back to dashboard"""
        try:
            if self.manager:
                self.manager.current = 'enhanced_dashboard'
        except Exception as e:
            logger.error(f"Error navigating back: {e}")

    # Dialog methods
    def show_success_dialog(self, message):
        """Show success message dialog"""
        self.show_dialog("Success", message, "check-circle")

    def show_error_dialog(self, message):
        """Show error message dialog"""
        self.show_dialog("Error", message, "alert-circle")

    def show_info_dialog(self, message):
        """Show information dialog"""
        self.show_dialog("Information", message, "information")

    def show_dialog(self, title, message, icon):
        """Show a general dialog"""
        if self.settings_dialog:
            self.settings_dialog.dismiss()

        self.settings_dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.settings_dialog.dismiss()
                )
            ]
        )
        self.settings_dialog.open()

    def show_confirmation_dialog(self, title, message, confirm_callback):
        """Show confirmation dialog"""
        if self.settings_dialog:
            self.settings_dialog.dismiss()

        self.settings_dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDRaisedButton(
                    text="Cancel",
                    on_release=lambda x: self.settings_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Confirm",
                    on_release=lambda x: (self.settings_dialog.dismiss(), confirm_callback(x))
                )
            ]
        )
        self.settings_dialog.open()

    def show_health_dialog(self, health_status):
        """Show system health status dialog"""
        health_text = f"""
Overall Health: {health_status.get('overall_health', 'Unknown').title()}
Database: {health_status.get('database_status', 'Unknown')}
Backup Status: {health_status.get('backup_status', 'Unknown')}
Free Disk Space: {health_status.get('disk_space', {}).get('free_gb', 'Unknown')} GB
Total Properties: {health_status.get('total_properties', 'Unknown')}
Total Owners: {health_status.get('total_owners', 'Unknown')}
        """.strip()

        self.show_dialog("System Health Status", health_text, "monitor")

    def show_activity_log_dialog(self, activities):
        """Show activity log dialog"""
        if not activities:
            self.show_info_dialog("No recent activities found")
            return

        activity_text = "Recent Activities:\n\n"
        for activity in activities[:10]:  # Show last 10 activities
            activity_text += f"• {activity.get('title', 'Unknown')}\n"
            activity_text += f"  {activity.get('formatted_time', 'Unknown time')}\n\n"

        self.show_dialog("Activity Log", activity_text, "history")
