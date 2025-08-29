import logging
import os
import unittest
from dataclasses import dataclass

import requests
import tomli
from accounts.tests.tests_api_accounts import ApiAccountsTests
from accounts.tests.tests_api_auth import ApiAuthTests
from activity_logs.tests.face_recognition import ApiFaceRecognitionActivityLogsTests
from activity_logs.tests.retention import ApiActivityLogsRetentionTests
from activity_logs.tests.system import ApiSystemActivtityLogsTests
from alarm_logs.tests import ApiAlarmLogsTests
from system.tests.debug_config import ApiFaceRecognitionConfigDebugTests
from system.tests.preview_config import ApiFaceRecognitionConfigPreviewTests
from system.tests.recoginiton_config import ApiFaceRecognitionConfigRecoginitonTests
from system.tests.video_config import ApiFaceRecognitionConfigVideoTests
from user_registration.tests.group import ApiUserRegistrationGroupTests
from user_registration.tests.user import ApiUserRegistrationTests

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
file_handler = logging.FileHandler("test_run.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])


@dataclass
class TestConfig:
    test_server_url: str


def initial_system_config(server_url: str = None) -> bool:
    logging.info("Initial system configuration...")
    test_server_url = server_url
    superadmin = {
        "account": "superadmin",
        "password": "superadmin",
        "remember_me": True,
        "select_mode": "Advanced",
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(f"{test_server_url}/api/auth/login/", json=superadmin, headers=headers)
    access_token = resp.json().get("access_token")
    auth_headers = {**headers, "Authorization": access_token}

    update_reco_data = {
        "enable_blink_detection": True,
        "dlib_predictor_path": "models/dlib/shape_predictor_68_face_landmarks.dat",
        "dlib_recognition_model_path": "models/dlib/dlib_face_recognition_resnet_model_v1.dat",
        "face_model": "models/face_recognition/model.csv",
        "minimum_bounding_box_height": 0.4,
        "minimum_face_detection_score": 0.6,
        "eyes_detection_brightness_threshold": 120,
        "eyes_detection_brightness_value_min": 50,
        "eyes_detection_brightness_value_max": 20,
        "sensitivity": 0.4,
        "consecutive_prediction_intervals_frame": 90,
    }
    face_recognition_url = test_server_url + "/api/face-recognition-config/recognition/"
    response = requests.put(
        face_recognition_url + "1/",
        json=update_reco_data,
        headers=auth_headers,
    )
    if response.status_code == 200:
        logging.info("Initial system configuration completed successfully.")
    else:
        logging.error(
            f"Failed to initial system configuration. Status code: {response.status_code}, Response: {response.text}"
        )
        return False

    update_video_data = {
        "rtsp": "",
        "web_camera": 0,
        "image_height": 720,
        "image_width": 1280,
        "detection_range_start_point_x": 420,
        "detection_range_start_point_y": 160,
        "detection_range_end_point_x": 820,
        "detection_range_end_point_y": 560,
    }
    video_config_url = test_server_url + "/api/face-recognition-config/video/"
    response = requests.put(
        video_config_url + "1/",
        json=update_video_data,
        headers=auth_headers,
    )
    if response.status_code == 200:
        logging.info("Initial video configuration completed successfully.")
    else:
        logging.error(
            f"Failed to initial video configuration. Status code: {response.status_code}, Response: {response.text}"
        )
        return False
    return True


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_server.settings")
    with open("settings.toml", "rb") as f:
        config = tomli.load(f)
    test_config = TestConfig(**config.get("tests", {}))
    if not initial_system_config(test_config.test_server_url):
        logging.error("Initial system configuration failed. Exiting tests.")
        os._exit(1)
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
            loader.loadTestsFromTestCase(ApiUserRegistrationGroupTests),
            loader.loadTestsFromTestCase(ApiUserRegistrationTests),
            loader.loadTestsFromTestCase(ApiFaceRecognitionConfigPreviewTests),
            loader.loadTestsFromTestCase(
                ApiFaceRecognitionConfigDebugTests
            ),  # System testing must be done last because it changes the actual available system parameters
            loader.loadTestsFromTestCase(ApiFaceRecognitionConfigVideoTests),
            loader.loadTestsFromTestCase(ApiFaceRecognitionConfigRecoginitonTests),
        ]
    )
    test_result = runner.run(suite_test)
