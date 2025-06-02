#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Backup Controller
Handles database backup, export, and import operations
"""

from typing import Dict, List, Optional
import logging
import os
import json
import sqlite3
import shutil
from datetime import datetime

from .base_controller import BaseController

logger = logging.getLogger(__name__)


class BackupController(BaseController):
    """Controller for backup and data management operations"""

    def __init__(self, db_manager, view=None):
        super().__init__(None, view)
        self.db_manager = db_manager
        self.backup_directory = "backups"
        self._ensure_backup_directory()

    def _ensure_backup_directory(self):
        """Ensure backup directory exists"""
        if not os.path.exists(self.backup_directory):
            os.makedirs(self.backup_directory)

    def create_full_backup(self) -> Optional[str]:
        """Create a full database backup"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"realestate_backup_{timestamp}.db"
            backup_path = os.path.join(self.backup_directory, backup_filename)

            # Get current database path
            db_path = self.db_manager.db_path

            # Copy database file
            shutil.copy2(db_path, backup_path)

            # Create backup metadata
            metadata = {
                "backup_date": datetime.now().isoformat(),
                "original_db": db_path,
                "backup_size": os.path.getsize(backup_path),
                "tables_included": self._get_table_list()
            }

            metadata_path = backup_path.replace('.db', '_metadata.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)

            self.handle_success(f"Full backup created: {backup_filename}")
            logger.info(f"Full backup created: {backup_path}")
            return backup_path

        except Exception as e:
            self.handle_error(f"Error creating backup: {str(e)}")
            return None

    def create_data_export(self, tables: List[str] = None, format_type: str = 'json') -> Optional[str]:
        """Export specific tables or all data"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            if tables is None:
                tables = ['Realstatspecification', 'Owners', 'realstatephotos', 'Maincode']

            export_data = {}

            for table in tables:
                export_data[table] = self._export_table_data(table)

            if format_type.lower() == 'json':
                filename = f"data_export_{timestamp}.json"
                export_path = os.path.join(self.backup_directory, filename)

                with open(export_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)

            elif format_type.lower() == 'sql':
                filename = f"data_export_{timestamp}.sql"
                export_path = os.path.join(self.backup_directory, filename)

                with open(export_path, 'w', encoding='utf-8') as f:
                    for table, data in export_data.items():
                        f.write(f"-- Data for table {table}\n")
                        f.write(self._generate_sql_inserts(table, data))
                        f.write("\n\n")

            else:
                self.handle_error(f"Unsupported export format: {format_type}")
                return None

            self.handle_success(f"Data export created: {filename}")
            logger.info(f"Data export created: {export_path}")
            return export_path

        except Exception as e:
            self.handle_error(f"Error creating data export: {str(e)}")
            return None

    def restore_from_backup(self, backup_path: str) -> bool:
        """Restore database from backup"""
        try:
            if not os.path.exists(backup_path):
                self.handle_error("Backup file not found")
                return False

            # Create a backup of current database before restore
            current_backup = self.create_full_backup()
            if not current_backup:
                self.handle_error("Failed to create current database backup")
                return False

            # Close current database connection
            self.db_manager.close_connection()

            # Replace current database with backup
            db_path = self.db_manager.db_path
            shutil.copy2(backup_path, db_path)

            # Reconnect to restored database
            self.db_manager.get_connection()

            self.handle_success("Database restored from backup successfully")
            logger.info(f"Database restored from: {backup_path}")
            return True

        except Exception as e:
            self.handle_error(f"Error restoring from backup: {str(e)}")
            return False

    def import_data(self, import_path: str, table_mapping: Dict = None) -> bool:
        """Import data from exported file"""
        try:
            if not os.path.exists(import_path):
                self.handle_error("Import file not found")
                return False

            # Determine file type and import accordingly
            if import_path.endswith('.json'):
                return self._import_from_json(import_path, table_mapping)
            elif import_path.endswith('.sql'):
                return self._import_from_sql(import_path)
            else:
                self.handle_error("Unsupported import file format")
                return False

        except Exception as e:
            self.handle_error(f"Error importing data: {str(e)}")
            return False

    def list_backups(self) -> List[Dict]:
        """List all available backups"""
        try:
            backups = []

            for filename in os.listdir(self.backup_directory):
                if filename.endswith('.db'):
                    filepath = os.path.join(self.backup_directory, filename)
                    metadata_path = filepath.replace('.db', '_metadata.json')

                    backup_info = {
                        'filename': filename,
                        'filepath': filepath,
                        'size': os.path.getsize(filepath),
                        'created': datetime.fromtimestamp(os.path.getctime(filepath)).isoformat(),
                        'modified': datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
                    }

                    # Load metadata if available
                    if os.path.exists(metadata_path):
                        try:
                            with open(metadata_path, 'r', encoding='utf-8') as f:
                                metadata = json.load(f)
                                backup_info.update(metadata)
                        except:
                            pass

                    backups.append(backup_info)

            # Sort by creation date, newest first
            backups.sort(key=lambda x: x['created'], reverse=True)
            return backups

        except Exception as e:
            logger.error(f"Error listing backups: {e}")
            return []

    def cleanup_old_backups(self, keep_count: int = 10) -> int:
        """Clean up old backup files, keeping only the specified number"""
        try:
            backups = self.list_backups()

            if len(backups) <= keep_count:
                return 0

            deleted_count = 0
            backups_to_delete = backups[keep_count:]

            for backup in backups_to_delete:
                try:
                    os.remove(backup['filepath'])

                    # Remove metadata file if exists
                    metadata_path = backup['filepath'].replace('.db', '_metadata.json')
                    if os.path.exists(metadata_path):
                        os.remove(metadata_path)

                    deleted_count += 1
                    logger.info(f"Deleted old backup: {backup['filename']}")

                except Exception as e:
                    logger.error(f"Error deleting backup {backup['filename']}: {e}")

            if deleted_count > 0:
                self.handle_success(f"Cleaned up {deleted_count} old backup(s)")

            return deleted_count

        except Exception as e:
            self.handle_error(f"Error cleaning up backups: {str(e)}")
            return 0

    def _get_table_list(self) -> List[str]:
        """Get list of all tables in database"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]

            return tables

        except Exception as e:
            logger.error(f"Error getting table list: {e}")
            return []

    def _export_table_data(self, table_name: str) -> List[Dict]:
        """Export data from a specific table"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            cursor.execute(f"SELECT * FROM {table_name}")
            columns = [description[0] for description in cursor.description]

            rows = []
            for row in cursor.fetchall():
                row_dict = dict(zip(columns, row))
                rows.append(row_dict)

            return rows

        except Exception as e:
            logger.error(f"Error exporting table {table_name}: {e}")
            return []

    def _generate_sql_inserts(self, table_name: str, data: List[Dict]) -> str:
        """Generate SQL INSERT statements for table data"""
        if not data:
            return ""

        sql_statements = []

        for row in data:
            columns = list(row.keys())
            values = list(row.values())
              # Format values for SQL
            formatted_values = []
            for value in values:
                if value is None:
                    formatted_values.append('NULL')
                elif isinstance(value, str):
                    escaped_value = value.replace("'", "''")
                    formatted_values.append(f"'{escaped_value}'")
                else:
                    formatted_values.append(str(value))

            columns_str = ', '.join(f'"{col}"' for col in columns)
            values_str = ', '.join(formatted_values)

            sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});"
            sql_statements.append(sql)

        return '\n'.join(sql_statements)

    def _import_from_json(self, import_path: str, table_mapping: Dict = None) -> bool:
        """Import data from JSON file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            conn = self.db_manager.get_connection()

            for table_name, table_data in data.items():
                if table_mapping and table_name in table_mapping:
                    target_table = table_mapping[table_name]
                else:
                    target_table = table_name

                # Insert data into table
                for row in table_data:
                    columns = list(row.keys())
                    values = list(row.values())

                    placeholders = ', '.join(['?' for _ in values])
                    columns_str = ', '.join(f'"{col}"' for col in columns)

                    query = f"INSERT OR REPLACE INTO {target_table} ({columns_str}) VALUES ({placeholders})"

                    try:
                        conn.execute(query, values)
                    except sqlite3.Error as e:
                        logger.error(f"Error inserting row into {target_table}: {e}")

            conn.commit()
            self.handle_success("Data imported from JSON successfully")
            return True

        except Exception as e:
            self.handle_error(f"Error importing from JSON: {str(e)}")
            return False

    def _import_from_sql(self, import_path: str) -> bool:
        """Import data from SQL file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                sql_content = f.read()

            conn = self.db_manager.get_connection()
            conn.executescript(sql_content)
            conn.commit()

            self.handle_success("Data imported from SQL successfully")
            return True

        except Exception as e:
            self.handle_error(f"Error importing from SQL: {str(e)}")
            return False
