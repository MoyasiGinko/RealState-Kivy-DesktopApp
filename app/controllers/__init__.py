#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Controllers Module
Exports all controller classes for easy importing
"""

from .main_controller import MainController
from .property_controller import PropertyController
from .owner_controller import OwnerController
from .settings_controller import SettingsController
from .activity_controller import ActivityController
from .backup_controller import BackupController
from .report_controller import ReportController
from .base_controller import BaseController

__all__ = [
    'MainController',
    'PropertyController',
    'OwnerController',
    'SettingsController',
    'ActivityController',
    'BackupController',
    'ReportController',
    'BaseController'
]

# Version information
__version__ = '1.0.0'
__author__ = 'Real Estate Management System'

# Controller factory function
def create_main_controller(db_manager):
    """Factory function to create a fully configured MainController"""
    return MainController(db_manager)

# Utility function to get controller dependencies
def get_controller_dependencies():
    """Get information about controller dependencies"""
    return {
        'MainController': {
            'requires': ['database_manager'],
            'manages': ['property', 'owner', 'settings', 'activity', 'backup', 'report']
        },
        'PropertyController': {
            'requires': ['property_model'],
            'provides': ['property_management', 'search', 'export']
        },
        'OwnerController': {
            'requires': ['owner_model'],
            'provides': ['owner_management', 'search']
        },
        'SettingsController': {
            'requires': [],
            'provides': ['settings_management', 'configuration']
        },
        'ActivityController': {
            'requires': [],
            'provides': ['activity_logging', 'statistics']
        },
        'BackupController': {
            'requires': ['database_manager'],
            'provides': ['backup', 'restore', 'data_export']
        },
        'ReportController': {
            'requires': ['property_model', 'owner_model'],
            'provides': ['reporting', 'analysis', 'export']
        }
    }
