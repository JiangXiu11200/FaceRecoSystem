import logging
import os
import unittest

import django
from accounts.tests.tests_api_accounts import ApiAccountsTests
from accounts.tests.tests_api_auth import ApiAuthTests
from activity_logs.tests.face_recognition import ApiFaceRecognitionActivityLogsTests
from activity_logs.tests.retention import ApiActivityLogsRetentionTests
from activity_logs.tests.system import ApiSystemActivtityLogsTests
from alarm_logs.tests import ApiAlarmLogsTests
from django.core.management import call_command


def setup_database():
    logging.info("Setting up the database...")
    call_command("migrate")


def setup_initial_data():
    logging.info("Setting up initial data...")
    call_command("create_apps")
    call_command("create_user")


def setup_minios3():
    logging.info("Setting up MinIO S3...")
    call_command("create_minio_buckets")


def setup_activity_log():
    logging.info("Setting up activity log...")
    call_command("create_retention")


def setup_system_config():
    logging.info("Setting up system configuration...")
    call_command("create_default_config")


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_server.settings")
    django.setup()
    setup_database()
    setup_initial_data()
    setup_minios3()
    setup_activity_log()
    setup_system_config()
    logging.basicConfig(
        filename="test_run.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner(verbosity=2)
    suite_test = unittest.TestSuite()
    suite_test.addTests(
        [
            loader.loadTestsFromTestCase(ApiAuthTests),
            loader.loadTestsFromTestCase(ApiAccountsTests),
            loader.loadTestsFromTestCase(ApiAlarmLogsTests),
            loader.loadTestsFromTestCase(ApiSystemActivtityLogsTests),
            loader.loadTestsFromTestCase(ApiFaceRecognitionActivityLogsTests),
            loader.loadTestsFromTestCase(ApiActivityLogsRetentionTests),
        ]
    )
    test_result = runner.run(suite_test)
