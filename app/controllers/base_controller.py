#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Base Controller
Base class for all controllers with common functionality
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class BaseController(ABC):
    """Base controller class with common functionality"""

    def __init__(self, model=None, view=None):
        self.model = model
        self.view = view
        self._setup_model_observers()
        self._setup_view_handlers()

    def _setup_model_observers(self):
        """Setup observers for model changes"""
        if self.model:
            self.model.add_observer(self)

    def _setup_view_handlers(self):
        """Setup event handlers for view"""
        if self.view:
            # Override in subclasses to setup specific handlers
            pass

    def on_model_changed(self, event_type: str, data: Any = None):
        """Handle model change notifications"""
        # Override in subclasses to handle specific events
        if self.view and hasattr(self.view, 'refresh_data'):
            self.view.refresh_data()

    def handle_error(self, error_message: str, title: str = "Error"):
        """Handle and display errors"""
        logger.error(error_message)
        if self.view and hasattr(self.view, 'show_error'):
            self.view.show_error(error_message, title)

    def handle_success(self, message: str, title: str = "Success"):
        """Handle and display success messages"""
        logger.info(message)
        if self.view and hasattr(self.view, 'show_success'):
            self.view.show_success(message, title)

    def validate_input(self, data: Dict) -> tuple[bool, str]:
        """Validate input data"""
        if self.model and hasattr(self.model, 'validate_data'):
            return self.model.validate_data(data)
        return True, ""
