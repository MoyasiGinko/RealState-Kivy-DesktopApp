#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Integration Layer
Bridges the existing UI components with the new MainController system
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class IntegrationLayer:
    """Integration layer that connects UI components with the MainController system"""

    def __init__(self, main_controller):
        """Initialize the integration layer"""
        self.main_controller = main_controller
        self.activity_controller = main_controller.controllers['activity']
        self.settings_controller = main_controller.controllers['settings']
        self.backup_controller = main_controller.controllers['backup']
        self.report_controller = main_controller.controllers['report']
        self.property_controller = main_controller.controllers['property']

        logger.info("Integration layer initialized")

    # Dashboard Integration Methods
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get comprehensive dashboard statistics"""
        try:
            # Get system status
            system_status = self.main_controller.get_system_status()

            # Get property statistics
            property_stats = self.property_controller.get_property_statistics()

            # Get activity summary
            activities = self.activity_controller.get_recent_activities(limit=5)

            # Combine all statistics
            dashboard_data = {
                'system_status': system_status,
                'property_stats': property_stats,
                'recent_activities': activities,
                'total_properties': property_stats.get('total_properties', 0),
                'total_owners': property_stats.get('total_owners', 0),
                'total_regions': len(property_stats.get('regions', [])),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            # Log activity
            self.activity_controller.log_activity(
                'system', 'dashboard_viewed',
                f"Dashboard statistics accessed with {dashboard_data['total_properties']} properties"
            )

            return dashboard_data

        except Exception as e:
            logger.error(f"Error getting dashboard stats: {e}")
            return {
                'error': str(e),
                'total_properties': 0,
                'total_owners': 0,
                'total_regions': 0,
                'system_status': 'error'
            }

    # Property Integration Methods
    def search_properties_advanced(self, criteria: Dict[str, Any]) -> List[Dict]:
        """Advanced property search with activity logging"""
        try:
            results = self.property_controller.advanced_search(criteria)

            # Log search activity
            search_description = f"Advanced search with {len(criteria)} criteria returned {len(results)} results"
            self.activity_controller.log_activity(
                'property', 'advanced_search', search_description
            )

            return results

        except Exception as e:
            logger.error(f"Error in advanced search: {e}")
            self.activity_controller.log_activity(
                'property', 'search_error', f"Advanced search failed: {str(e)}"
            )
            return []

    def export_properties_with_tracking(self, criteria: Dict[str, Any],
                                       format_type: str = 'csv') -> Optional[str]:
        """Export properties with activity tracking"""
        try:
            if format_type == 'csv':
                result = self.property_controller.export_properties_csv(criteria)
            elif format_type == 'json':
                result = self.property_controller.export_properties_json(criteria)
            else:
                raise ValueError(f"Unsupported export format: {format_type}")

            if result:
                # Log export activity
                self.activity_controller.log_activity(
                    'property', 'export',
                    f"Properties exported to {format_type.upper()} format"
                )

            return result

        except Exception as e:
            logger.error(f"Error exporting properties: {e}")
            self.activity_controller.log_activity(
                'property', 'export_error', f"Export failed: {str(e)}"
            )
            return None

    def get_property_summary_report(self) -> Dict[str, Any]:
        """Get comprehensive property summary report"""
        try:
            report = self.report_controller.generate_property_summary_report()

            # Log report generation
            self.activity_controller.log_activity(
                'report', 'property_summary',
                "Property summary report generated"
            )

            return report

        except Exception as e:
            logger.error(f"Error generating property summary: {e}")
            return {'error': str(e)}

    # Backup Integration Methods
    def create_backup_with_notification(self, backup_type: str = 'full') -> Dict[str, Any]:
        """Create backup with user notification and activity tracking"""
        try:
            if backup_type == 'full':
                result = self.backup_controller.create_full_backup()
            elif backup_type == 'data':
                result = self.backup_controller.export_data_json()
            else:
                raise ValueError(f"Unsupported backup type: {backup_type}")

            if result.get('success'):
                # Log successful backup
                self.activity_controller.log_activity(
                    'backup', 'created',
                    f"{backup_type.title()} backup created successfully"
                )

                return {
                    'success': True,
                    'message': f"{backup_type.title()} backup created successfully",
                    'file_path': result.get('file_path'),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                # Log backup failure
                self.activity_controller.log_activity(
                    'backup', 'error',
                    f"{backup_type.title()} backup failed: {result.get('error', 'Unknown error')}"
                )

                return {
                    'success': False,
                    'message': f"Backup failed: {result.get('error', 'Unknown error')}"
                }

        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            self.activity_controller.log_activity(
                'backup', 'error', f"Backup creation failed: {str(e)}"
            )

            return {
                'success': False,
                'message': f"Backup failed: {str(e)}"
            }

    def restore_backup_with_confirmation(self, backup_path: str) -> Dict[str, Any]:
        """Restore backup with confirmation and activity tracking"""
        try:
            result = self.backup_controller.restore_backup(backup_path)

            if result.get('success'):
                # Log successful restore
                self.activity_controller.log_activity(
                    'backup', 'restored',
                    f"Data restored from backup: {backup_path}"
                )

                return {
                    'success': True,
                    'message': "Data restored successfully",
                    'backup_path': backup_path,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                # Log restore failure
                self.activity_controller.log_activity(
                    'backup', 'restore_error',
                    f"Restore failed from {backup_path}: {result.get('error', 'Unknown error')}"
                )

                return {
                    'success': False,
                    'message': f"Restore failed: {result.get('error', 'Unknown error')}"
                }

        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            self.activity_controller.log_activity(
                'backup', 'restore_error', f"Restore failed: {str(e)}"
            )

            return {
                'success': False,
                'message': f"Restore failed: {str(e)}"
            }

    # Settings Integration Methods
    def get_application_settings(self) -> Dict[str, Any]:
        """Get current application settings"""
        try:
            settings = self.settings_controller.get_settings()

            # Add system information
            system_status = self.main_controller.get_system_status()
            settings['system_info'] = system_status

            return settings

        except Exception as e:
            logger.error(f"Error getting settings: {e}")
            return {'error': str(e)}

    def update_application_settings(self, new_settings: Dict[str, Any]) -> Dict[str, Any]:
        """Update application settings with validation"""
        try:
            result = self.settings_controller.update_settings(new_settings)

            if result.get('success'):
                # Log settings update
                self.activity_controller.log_activity(
                    'settings', 'updated',
                    f"Application settings updated: {', '.join(new_settings.keys())}"
                )

                return {
                    'success': True,
                    'message': "Settings updated successfully",
                    'updated_settings': list(new_settings.keys())
                }
            else:
                return {
                    'success': False,
                    'message': f"Settings update failed: {result.get('error', 'Unknown error')}"
                }

        except Exception as e:
            logger.error(f"Error updating settings: {e}")
            return {
                'success': False,
                'message': f"Settings update failed: {str(e)}"
            }

    # Activity Integration Methods
    def get_activity_log_for_display(self, limit: int = 50,
                                    activity_type: Optional[str] = None) -> List[Dict]:
        """Get formatted activity log for UI display"""
        try:
            activities = self.activity_controller.get_activities(
                limit=limit,
                activity_type=activity_type
            )

            # Format activities for display
            formatted_activities = []
            for activity in activities:
                formatted_activity = {
                    'id': activity.get('id'),
                    'icon': self._get_activity_icon(activity.get('activity_type')),
                    'title': self._format_activity_title(activity),
                    'description': activity.get('description', ''),
                    'timestamp': activity.get('timestamp', ''),
                    'formatted_time': self._format_timestamp(activity.get('timestamp')),
                    'category': activity.get('activity_type', 'general'),
                    'object_type': activity.get('object_type', 'system')
                }
                formatted_activities.append(formatted_activity)

            return formatted_activities

        except Exception as e:
            logger.error(f"Error getting activity log: {e}")
            return []

    # Reporting Integration Methods
    def generate_custom_report(self, report_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate custom report based on configuration"""
        try:
            report_type = report_config.get('type', 'property_summary')

            if report_type == 'property_summary':
                report = self.report_controller.generate_property_summary_report()
            elif report_type == 'owner_properties':
                report = self.report_controller.generate_owner_properties_report()
            elif report_type == 'market_analysis':
                report = self.report_controller.generate_market_analysis_report()
            elif report_type == 'custom':
                filters = report_config.get('filters', {})
                report = self.report_controller.generate_custom_report(filters)
            else:
                raise ValueError(f"Unsupported report type: {report_type}")

            # Log report generation
            self.activity_controller.log_activity(
                'report', 'generated',
                f"{report_type.replace('_', ' ').title()} report generated"
            )

            return {
                'success': True,
                'report': report,
                'generated_at': datetime.now().isoformat(),
                'report_type': report_type
            }

        except Exception as e:
            logger.error(f"Error generating custom report: {e}")
            self.activity_controller.log_activity(
                'report', 'error', f"Report generation failed: {str(e)}"
            )

            return {
                'success': False,
                'error': str(e)
            }

    # Owner Integration Methods
    def export_owners_data(self, search_criteria: Dict[str, Any] = None, include_properties: bool = False) -> bool:
        """Export owners data with activity tracking"""
        try:
            if not self.main_controller:
                logger.error("Main controller not available for owners export")
                return False

            # Get export file path
            export_path = self.main_controller.backup_controller.get_export_path("owners")

            # Get owners data
            owners_data = self.db_manager.get_owners()

            # Prepare export data
            export_data = {
                'export_metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'total_owners': len(owners_data),
                    'search_criteria': search_criteria or {},
                    'include_properties': include_properties,
                    'exported_by': 'integration_layer'
                },
                'owners': []
            }

            # Format owners data
            for owner in owners_data:
                owner_code, owner_name, owner_phone, note = owner
                owner_data = {
                    'owner_code': owner_code,
                    'owner_name': owner_name,
                    'owner_phone': owner_phone,
                    'note': note
                }

                # Include properties if requested
                if include_properties:
                    try:
                        properties = self.db_manager.get_properties_by_owner(owner_code)
                        owner_data['properties'] = [
                            {
                                'property_code': prop[0],
                                'property_area': prop[1],
                                'property_type': prop[2],
                                'bedrooms': prop[3],
                                'bathrooms': prop[4]
                            } for prop in properties
                        ]
                        owner_data['property_count'] = len(properties)
                    except Exception as e:
                        logger.warning(f"Could not load properties for owner {owner_code}: {e}")
                        owner_data['properties'] = []
                        owner_data['property_count'] = 0

                export_data['owners'].append(owner_data)

            # Save to file
            import json
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)

            # Log activity
            self.log_activity(
                action="export_owners",
                details=f"Exported {len(owners_data)} owners to {export_path}",
                category="data_management"
            )

            logger.info(f"Owners data exported successfully to {export_path}")
            return True

        except Exception as e:
            logger.error(f"Error exporting owners data: {e}")
            self.log_activity(
                action="export_owners_error",
                details=f"Failed to export owners: {str(e)}",
                category="data_management"
            )
            return False

    def import_owners_data(self, file_path: str = None) -> bool:
        """Import owners data with validation and activity tracking"""
        try:
            if not self.main_controller:
                logger.error("Main controller not available for owners import")
                return False

            # Get import file path (would normally open file dialog)
            if not file_path:
                # For now, look for the most recent export file
                import os
                import glob
                export_dir = os.path.dirname(self.main_controller.backup_controller.get_export_path("owners"))
                pattern = os.path.join(export_dir, "owners_export_*.json")
                files = glob.glob(pattern)
                if not files:
                    logger.error("No owners export files found for import")
                    return False
                file_path = max(files, key=os.path.getctime)  # Get most recent

            # Load and validate import data
            import json
            with open(file_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)

            if 'owners' not in import_data:
                logger.error("Invalid import file format - missing owners data")
                return False

            # Import owners
            imported_count = 0
            updated_count = 0
            error_count = 0

            for owner_data in import_data['owners']:
                try:
                    owner_code = owner_data.get('owner_code')
                    owner_name = owner_data.get('owner_name', '')
                    owner_phone = owner_data.get('owner_phone', '')
                    note = owner_data.get('note', '')

                    # Check if owner exists
                    existing_owner = self.db_manager.get_owner_by_code(owner_code)

                    if existing_owner:
                        # Update existing owner
                        if self.db_manager.update_owner(owner_code, owner_name, owner_phone, note):
                            updated_count += 1
                        else:
                            error_count += 1
                    else:
                        # Add new owner (might get new code if exists)
                        new_code = self.db_manager.add_owner(owner_name, owner_phone, note)
                        if new_code:
                            imported_count += 1
                        else:
                            error_count += 1

                except Exception as e:
                    logger.error(f"Error importing owner {owner_data}: {e}")
                    error_count += 1

            # Log activity
            self.log_activity(
                action="import_owners",
                details=f"Imported {imported_count} new, updated {updated_count}, errors {error_count} from {file_path}",
                category="data_management"
            )

            logger.info(f"Owners import completed: {imported_count} new, {updated_count} updated, {error_count} errors")
            return error_count == 0  # Success if no errors

        except Exception as e:
            logger.error(f"Error importing owners data: {e}")
            self.log_activity(
                action="import_owners_error",
                details=f"Failed to import owners: {str(e)}",
                category="data_management"
            )
            return False

    # Helper Methods
    def _get_activity_icon(self, activity_type: str) -> str:
        """Get icon name for activity type"""
        icon_map = {
            'property': 'home',
            'owner': 'account',
            'backup': 'backup-restore',
            'restore': 'restore',
            'export': 'export',
            'import': 'import',
            'search': 'magnify',
            'report': 'file-chart',
            'settings': 'cog',
            'system': 'monitor',
            'error': 'alert-circle',
            'delete': 'delete'
        }
        return icon_map.get(activity_type, 'information')

    def _format_activity_title(self, activity: Dict[str, Any]) -> str:
        """Format activity title for display"""
        object_type = activity.get('object_type', 'system')
        activity_type = activity.get('activity_type', 'action')

        title_map = {
            ('property', 'created'): 'Property Added',
            ('property', 'updated'): 'Property Updated',
            ('property', 'deleted'): 'Property Deleted',
            ('property', 'search'): 'Property Search',
            ('property', 'export'): 'Properties Exported',
            ('owner', 'created'): 'Owner Added',
            ('owner', 'updated'): 'Owner Updated',
            ('owner', 'deleted'): 'Owner Deleted',
            ('backup', 'created'): 'Backup Created',
            ('backup', 'restored'): 'Data Restored',
            ('report', 'generated'): 'Report Generated',
            ('settings', 'updated'): 'Settings Updated',
            ('system', 'startup'): 'System Started',
            ('system', 'shutdown'): 'System Shutdown'
        }

        key = (object_type, activity_type)
        return title_map.get(key, f"{object_type.title()} {activity_type.title()}")

    def _format_timestamp(self, timestamp: str) -> str:
        """Format timestamp for display"""
        try:
            if not timestamp:
                return "Unknown"

            # Parse the timestamp
            if 'T' in timestamp:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

            # Calculate time difference
            now = datetime.now()
            diff = now - dt

            if diff.days > 0:
                return f"{diff.days} days ago"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"{hours} hours ago"
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"{minutes} minutes ago"
            else:
                return "Just now"

        except Exception as e:
            logger.error(f"Error formatting timestamp {timestamp}: {e}")
            return "Unknown"

    def get_system_health_status(self) -> Dict[str, Any]:
        """Get comprehensive system health status"""
        try:
            system_status = self.main_controller.get_system_status()

            # Add health indicators
            health_status = {
                'overall_health': 'good',  # good, warning, critical
                'database_status': 'connected' if system_status.get('database_connected') else 'disconnected',
                'backup_status': self._check_backup_health(),
                'activity_log_status': self._check_activity_log_health(),
                'disk_space': self._check_disk_space(),
                'last_backup': self._get_last_backup_info(),
                'system_uptime': system_status.get('uptime', 0),
                'total_properties': system_status.get('total_properties', 0),
                'total_owners': system_status.get('total_owners', 0)
            }

            # Determine overall health
            if health_status['database_status'] == 'disconnected':
                health_status['overall_health'] = 'critical'
            elif health_status['backup_status'] == 'warning':
                health_status['overall_health'] = 'warning'

            return health_status

        except Exception as e:
            logger.error(f"Error getting system health: {e}")
            return {
                'overall_health': 'critical',
                'error': str(e)
            }

    def _check_backup_health(self) -> str:
        """Check backup system health"""
        try:
            backups = self.backup_controller.list_backups()
            if not backups:
                return 'warning'  # No backups exist

            # Check if there's a recent backup (within 7 days)
            latest_backup = max(backups, key=lambda x: x.get('created_at', ''))
            backup_date = datetime.fromisoformat(latest_backup.get('created_at', ''))
            days_since_backup = (datetime.now() - backup_date).days

            if days_since_backup > 7:
                return 'warning'
            else:
                return 'good'

        except Exception as e:
            logger.error(f"Error checking backup health: {e}")
            return 'unknown'

    def _check_activity_log_health(self) -> str:
        """Check activity log health"""
        try:
            activities = self.activity_controller.get_recent_activities(limit=1)
            if activities:
                return 'good'
            else:
                return 'warning'

        except Exception as e:
            logger.error(f"Error checking activity log health: {e}")
            return 'unknown'

    def _check_disk_space(self) -> Dict[str, Any]:
        """Check available disk space"""
        try:
            import shutil

            # Check main application directory
            total, used, free = shutil.disk_usage('.')

            free_gb = free // (1024**3)
            total_gb = total // (1024**3)
            used_percentage = (used / total) * 100

            return {
                'free_gb': free_gb,
                'total_gb': total_gb,
                'used_percentage': round(used_percentage, 1),
                'status': 'critical' if free_gb < 1 else 'warning' if free_gb < 5 else 'good'
            }

        except Exception as e:
            logger.error(f"Error checking disk space: {e}")
            return {
                'status': 'unknown',
                'error': str(e)
            }

    def _get_last_backup_info(self) -> Dict[str, Any]:
        """Get information about the last backup"""
        try:
            backups = self.backup_controller.list_backups()
            if not backups:
                return {
                    'exists': False,
                    'message': 'No backups found'
                }

            latest_backup = max(backups, key=lambda x: x.get('created_at', ''))
            backup_date = datetime.fromisoformat(latest_backup.get('created_at', ''))
            days_ago = (datetime.now() - backup_date).days

            return {
                'exists': True,
                'date': latest_backup.get('created_at'),
                'days_ago': days_ago,
                'file_path': latest_backup.get('file_path'),
                'size': latest_backup.get('file_size', 'Unknown')
            }

        except Exception as e:
            logger.error(f"Error getting last backup info: {e}")
            return {
                'exists': False,
                'error': str(e)
            }
