#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Base Model
Base class for all models with common functionality
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class BaseModel(ABC):
    """Base model class with common functionality"""

    def __init__(self, db_manager=None):
        self.db_manager = db_manager
        self._observers = []

    def add_observer(self, observer):
        """Add observer for model changes"""
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        """Remove observer"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, event_type: str, data: Any = None):
        """Notify all observers of model changes"""
        for observer in self._observers:
            if hasattr(observer, 'on_model_changed'):
                observer.on_model_changed(event_type, data)

    @abstractmethod
    def get_all(self) -> List[Dict]:
        """Get all records"""
        pass

    @abstractmethod
    def get_by_id(self, record_id: str) -> Optional[Dict]:
        """Get record by ID"""
        pass

    @abstractmethod
    def create(self, data: Dict) -> bool:
        """Create new record"""
        pass

    @abstractmethod
    def update(self, record_id: str, data: Dict) -> bool:
        """Update existing record"""
        pass

    @abstractmethod
    def delete(self, record_id: str) -> bool:
        """Delete record"""
        pass

    def validate_data(self, data: Dict) -> tuple[bool, str]:
        """Validate data before operations"""
        return True, ""
