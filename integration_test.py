#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Integration Test
Test the integration between MainController and the UI components
"""

import sys
import os
import logging
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / 'app'
sys.path.insert(0, str(app_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_integration():
    """Test the integration layer and main controller system"""
    try:
        logger.info("Starting integration test...")

        # Test database connection
        from app.database import DatabaseManager
        from app.config import config

        db = DatabaseManager(config.db_file)
        logger.info("✓ Database connection successful")

        # Test MainController initialization
        from app.controllers.main_controller import MainController
        main_controller = MainController(db)
        logger.info("✓ MainController initialized successfully")

        # Test IntegrationLayer initialization
        from app.controllers.integration_layer import IntegrationLayer
        integration_layer = IntegrationLayer(main_controller)
        logger.info("✓ Integration layer initialized successfully")

        # Test dashboard statistics
        dashboard_stats = integration_layer.get_dashboard_stats()
        logger.info(f"✓ Dashboard stats loaded: {dashboard_stats.get('total_properties', 0)} properties")

        # Test system health
        health_status = integration_layer.get_system_health_status()
        logger.info(f"✓ System health check: {health_status.get('overall_health', 'unknown')}")

        # Test settings retrieval
        settings = integration_layer.get_application_settings()
        logger.info(f"✓ Settings loaded successfully")

        # Test activity log
        activities = integration_layer.get_activity_log_for_display(limit=5)
        logger.info(f"✓ Activity log loaded: {len(activities)} recent activities")

        # Test property search capabilities
        search_results = integration_layer.search_properties_advanced({
            'location': 'test'
        })
        logger.info(f"✓ Property search working: {len(search_results)} results")

        # Cleanup
        main_controller.shutdown()
        db.close_connection()

        logger.info("🎉 All integration tests passed successfully!")
        return True

    except Exception as e:
        logger.error(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ui_components():
    """Test UI component initialization"""
    try:
        logger.info("Testing UI components...")

        # Test enhanced dashboard import
        from app.views.enhanced_dashboard import EnhancedDashboardScreen
        logger.info("✓ Enhanced dashboard import successful")

        # Test enhanced settings import
        from app.views.enhanced_settings import EnhancedSettingsScreen
        logger.info("✓ Enhanced settings import successful")

        # Test enhanced properties import
        from app.views.enhanced_properties import EnhancedPropertiesScreen
        logger.info("✓ Enhanced properties import successful")

        # Test enhanced owners import
        from app.views.enhanced_owners import EnhancedOwnersScreen
        logger.info("✓ Enhanced owners import successful")

        logger.info("🎉 All UI component tests passed!")
        return True

    except Exception as e:
        logger.error(f"❌ UI component test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_controller_initialization():
    """Test all controller components"""
    try:
        logger.info("Testing controller initialization...")

        from app.database import DatabaseManager
        from app.config import config

        db = DatabaseManager(config.db_file)

        # Test all controllers
        from app.controllers.property_controller import PropertyController
        from app.controllers.backup_controller import BackupController
        from app.controllers.report_controller import ReportController
        from app.controllers.activity_controller import ActivityController
        from app.controllers.settings_controller import SettingsController

        # Test property controller
        from app.models.property_model import PropertyModel
        property_model = PropertyModel(db)
        property_controller = PropertyController(property_model)
        logger.info("✓ Property controller initialized")

        # Test backup controller
        backup_controller = BackupController(db)
        logger.info("✓ Backup controller initialized")        # Test report controller
        from app.models.owner_model import OwnerModel
        owner_model = OwnerModel(db)
        report_controller = ReportController(property_model, owner_model)
        logger.info("✓ Report controller initialized")        # Test activity controller
        from app.models.activity_model import ActivityModel
        activity_model = ActivityModel(db)
        activity_controller = ActivityController(activity_model)
        logger.info("✓ Activity controller initialized")

        # Test settings controller
        from app.models.settings_model import SettingsModel
        settings_model = SettingsModel(db)
        settings_controller = SettingsController(settings_model)
        logger.info("✓ Settings controller initialized")

        db.close_connection()
        logger.info("🎉 All controller tests passed!")
        return True

    except Exception as e:
        logger.error(f"❌ Controller test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all integration tests"""
    logger.info("=" * 60)
    logger.info("Real Estate Management System - Integration Test Suite")
    logger.info("=" * 60)

    tests = [
        ("Controller Initialization", test_controller_initialization),
        ("UI Components", test_ui_components),
        ("Integration Layer", test_integration)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        logger.info(f"\n--- Running {test_name} Test ---")
        if test_func():
            passed += 1
            logger.info(f"✅ {test_name} test PASSED")
        else:
            logger.error(f"❌ {test_name} test FAILED")

    logger.info(f"\n" + "=" * 60)
    logger.info(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        logger.info("🎉 ALL TESTS PASSED! Integration is working correctly.")
        return 0
    else:
        logger.error(f"❌ {total - passed} tests failed. Please check the errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
