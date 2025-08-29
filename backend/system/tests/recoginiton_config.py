import random
import string

import requests
import tomli
from django.test import TestCase


class ApiFaceRecognitionConfigRecoginitonTests(TestCase):
    """Test cases for the /api/face-recognition-config/recoginiton/ endpoint."""
    def setUp(self):
        with open("settings.toml", "rb") as f:
            config = tomli.load(f)
        tests_config = config.get("tests", {})
        self.test_server_url = tests_config.get("test_server_url")
        self.face_recognition_url = self.test_server_url + "/api/face-recognition-config/recognition/"
        # 登入帳號
        self.superadmin = {
            "account": "superadmin",
            "password": "superadmin",
            "remember_me": True,
            "select_mode": "Advanced",
        }
        self.headers = {"Content-Type": "application/json"}
        # 登入取得 token
        resp = requests.post(f"{self.test_server_url}/api/auth/login/", json=self.superadmin, headers=self.headers)
        self.access_token = resp.json().get("access_token")
        self.auth_headers = {**self.headers, "Authorization": self.access_token}

    # 正向測試: 取得 Recoginition Configuration
    def test_get_recoginition_configuration(self):
        response = requests.get(
            self.face_recognition_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)

    # 正向測試: 更新 Recoginition Configuration
    def test_update_recoginition_configuration(self):
        update_data = {
            "dlib_predictor_path": "/path/to/predictor.dat",
            "dlib_recognition_model_path": "/path/to/recognition.dat",
            "face_model": "/path/to/face_model.csv",
            "minimum_bounding_box_height": 0.3,
            "minimum_face_detection_score": 0.5,
            "eyes_detection_brightness_threshold": 100,
            "eyes_detection_brightness_value_min": 50,
            "eyes_detection_brightness_value_max": 200,
            "sensitivity": 0.7,
            "consecutive_prediction_intervals_frame": 120,
        }
        response = requests.put(
            self.face_recognition_url + "1/",
            json=update_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for field, value in update_data.items():
            self.assertIn(field, data)
            self.assertEqual(data[field], value)

    # 正向測試: 部分更新 Recoginition Configuration
    def test_partial_update_recoginition_configuration(self):
        partial_update_data = {
            "sensitivity": 0.9,
            "consecutive_prediction_intervals_frame": 100,
        }
        response = requests.patch(
            self.face_recognition_url + "1/",
            json=partial_update_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for field, value in partial_update_data.items():
            self.assertIn(field, data)
            self.assertEqual(data[field], value)

    # 反向測試: 欄位類型錯誤
    def test_invalid_field_type(self):
        invalid_data = {
            "dlib_predictor_path": 123,  # 應為字串
            "minimum_bounding_box_height": "not_a_float",  # 應為浮點數
            "sensitivity": "not_a_float",  # 應為浮點數
            "consecutive_prediction_intervals_frame": "not_an_integer",  # 應為整數
        }
        response = requests.put(
            self.face_recognition_url + "1/",
            json=invalid_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 400)

    # 反向測試: 不允許的方法
    def test_method_not_allowed(self):
        response = requests.post(
            self.face_recognition_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 405)

    # 反向測試: ID 不存在
    def test_get_nonexistent_id(self):
        response = requests.get(
            self.face_recognition_url + "999/",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 404)

    # 反向測試: 更新不存在的 ID
    def test_update_nonexistent_id(self):
        update_data = {
            "dlib_predictor_path": "/path/to/predictor.dat",
            "dlib_recognition_model_path": "/path/to/recognition.dat",
            "face_model": "/path/to/face_model.csv",
            "minimum_bounding_box_height": 0.3,
            "minimum_face_detection_score": 0.5,
            "eyes_detection_brightness_threshold": 100,
            "eyes_detection_brightness_value_min": 50,
        }
        response = requests.put(
            self.face_recognition_url + "999/",
            json=update_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 404)

    # 邊界測試: 每個欄位的最大長度
    def test_max_length_rtsp_url(self):
        # Test with maximum allowed values for each field
        max_length_path = "a" * 256  # Max length for path fields
        update_data = {
            "dlib_predictor_path": max_length_path,
            "dlib_recognition_model_path": max_length_path,
            "face_model": max_length_path,
            "minimum_bounding_box_height": 1.0,  # max value
            "minimum_face_detection_score": 1.0,  # max value
            "eyes_detection_brightness_threshold": 255,  # max value
            "eyes_detection_brightness_value_min": 255,  # max value
            "eyes_detection_brightness_value_max": 255,  # max value
            "sensitivity": 1.0,  # max value
            "consecutive_prediction_intervals_frame": 150,  # max value
        }
        response = requests.put(
            self.face_recognition_url + "1/",
            json=update_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)

    # 邊界測試: 每個欄位的最小長度
    def test_min_length_field(self):
        update_data = {
            "dlib_predictor_path": "",
            "dlib_recognition_model_path": "",
            "face_model": "",
            "minimum_bounding_box_height": 0.0,  # min value
            "minimum_face_detection_score": 0.0,  # min value
            "eyes_detection_brightness_threshold": 0,  # min value
            "eyes_detection_brightness_value_min": 0,  # min value
            "eyes_detection_brightness_value_max": 0,  # min value
            "sensitivity": 0.0,  # min value
            "consecutive_prediction_intervals_frame": 10,  # min value
        }
        response = requests.put(
            self.face_recognition_url + "1/",
            json=update_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)

    # Monkey 測試: 大量隨機請求
    def test_monkey_requests(self):
        def random_string(length):
            return "".join(random.choices(string.ascii_letters + string.digits, k=length))

        for _ in range(50):
            update_data = {
                "dlib_predictor_path": random_string(random.randint(0, 256)),
                "dlib_recognition_model_path": random_string(random.randint(0, 256)),
                "face_model": random_string(random.randint(0, 256)),
                "minimum_bounding_box_height": round(random.uniform(0.0, 1.0), 2),
                "minimum_face_detection_score": round(random.uniform(0.0, 1.0), 2),
                "eyes_detection_brightness_threshold": random.randint(0, 255),
                "eyes_detection_brightness_value_min": random.randint(0, 255),
                "eyes_detection_brightness_value_max": random.randint(0, 255),
                "sensitivity": round(random.uniform(0.0, 1.0), 2),
                "consecutive_prediction_intervals_frame": random.randint(10, 150),
            }
            response = requests.put(
                self.face_recognition_url + "1/",
                json=update_data,
                headers=self.auth_headers,
            )
            self.assertEqual(response.status_code, 200)

    # Monkey 測試: 大量無效請求
    def test_monkey_invalid_requests(self):
        def random_string(length):
            return "".join(random.choices(string.ascii_letters + string.digits, k=length))

        for _ in range(20):
            invalid_data = {
                "dlib_predictor_path": random.randint(0, 1000),  # 應為字串
                "minimum_bounding_box_height": random_string(5),  # 應為浮點數
                "sensitivity": random_string(5),  # 應為浮點數
                "consecutive_prediction_intervals_frame": random_string(5),  # 應為整數
            }
            response = requests.put(
                self.face_recognition_url + "1/",
                json=invalid_data,
                headers=self.auth_headers,
            )
            self.assertEqual(response.status_code, 400)
