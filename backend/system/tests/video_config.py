import random
import string
import time

import requests
import tomli
from django.test import TestCase


class ApiFaceRecognitionConfigVideoTests(TestCase):
    """Test cases for the /api/face-recognition-config/video/ endpoint."""

    def setUp(self):
        with open("settings.toml", "rb") as f:
            config = tomli.load(f)
        tests_config = config.get("tests", {})
        self.test_server_url = tests_config.get("test_server_url")
        self.activity_logs_url = self.test_server_url + "/api/face-recognition-config/video/"
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

    # 正向測試: 取得 Video Configuration
    def test_get_video_configuration(self):
        response = requests.get(
            self.activity_logs_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)

    # 正向測試: 更新 Video Configuration
    def test_update_video_configuration(self):
        update_data = {
            "rtsp": "rtsp://example.com/stream",
            "web_camera": 0,
            "image_height": 720,
            "image_width": 1280,
            "detection_range_start_point_x": 100,
            "detection_range_start_point_y": 100,
            "detection_range_end_point_x": 600,
            "detection_range_end_point_y": 400,
        }
        response = requests.put(
            self.activity_logs_url + "1/",
            json=update_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("rtsp", data)
        self.assertEqual(data["rtsp"], update_data["rtsp"])
        self.assertIn("web_camera", data)
        self.assertEqual(data["web_camera"], update_data["web_camera"])
        self.assertIn("image_height", data)
        self.assertEqual(data["image_height"], update_data["image_height"])
        self.assertIn("image_width", data)
        self.assertEqual(data["image_width"], update_data["image_width"])
        self.assertIn("detection_range_start_point_x", data)
        self.assertEqual(data["detection_range_start_point_x"], update_data["detection_range_start_point_x"])
        self.assertIn("detection_range_start_point_y", data)
        self.assertEqual(data["detection_range_start_point_y"], update_data["detection_range_start_point_y"])
        self.assertIn("detection_range_end_point_x", data)
        self.assertEqual(data["detection_range_end_point_x"], update_data["detection_range_end_point_x"])
        self.assertIn("detection_range_end_point_y", data)
        self.assertEqual(data["detection_range_end_point_y"], update_data["detection_range_end_point_y"])

    # 正向測試: 部分更新 Video Configuration
    def test_partial_update_video_configuration(self):
        partial_update_data = {
            "image_height": 1080,
            "image_width": 1920,
        }
        response = requests.patch(
            self.activity_logs_url + "1/",
            json=partial_update_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("image_height", data)
        self.assertEqual(data["image_height"], partial_update_data["image_height"])
        self.assertIn("image_width", data)
        self.assertEqual(data["image_width"], partial_update_data["image_width"])

    # 反向測試: 欄位類型錯誤
    def test_invalid_field_type(self):
        invalid_data = {
            "web_camera": "not_an_integer",  # 應為整數或 null
            "image_height": "not_an_integer",  # 應為整數
            "image_width": -1920,  # 應為正整數
            "detection_range_start_point_x": "not_an_integer",  # 應為整數
            "detection_range_start_point_y": "not_an_integer",  # 應為整數
            "detection_range_end_point_x": "not_an_integer",  # 應為整數
            "detection_range_end_point_y": "not_an_integer",  # 應為整數
        }
        for field, value in invalid_data.items():
            response = requests.put(
                self.activity_logs_url + "1/",
                json={field: value},
                headers=self.auth_headers,
            )
            self.assertEqual(response.status_code, 400)

    # 反向測試: 不允許的方法
    def test_method_not_allowed(self):
        response = requests.post(
            self.activity_logs_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 405)

    # 反向測試: ID 不存在
    def test_id_not_found(self):
        response = requests.get(
            self.activity_logs_url + "999/",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 404)

    # 反向測試: 無效的 ID 格式
    def test_invalid_id_format(self):
        response = requests.get(
            self.activity_logs_url + "invalid_id/",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 404)

    # 邊界測試: 每個欄位的最大長度
    def test_max_length_rtsp_url(self):
        max_length_rtsp = "r" * 64
        update_data = {
            "rtsp": max_length_rtsp,
            "web_camera": 0,
            "image_height": 2160,
            "image_width": 3840,
            "detection_range_start_point_x": 3840,
            "detection_range_start_point_y": 2160,
            "detection_range_end_point_x": 3840,
            "detection_range_end_point_y": 2160,
        }
        for field, value in update_data.items():
            response = requests.put(
                self.activity_logs_url + "1/",
                json={field: value},
                headers=self.auth_headers,
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn(field, data)
            self.assertEqual(data[field], value)

    # 邊界測試: 每個欄位的最小長度
    def test_min_length_field(self):
        min_length_rtsp = ""
        update_data = {
            "rtsp": min_length_rtsp,
            "web_camera": 0,
            "image_height": 0,
            "image_width": 0,
            "detection_range_start_point_x": 0,
            "detection_range_start_point_y": 0,
            "detection_range_end_point_x": 0,
            "detection_range_end_point_y": 0,
        }
        for field, value in update_data.items():
            response = requests.put(
                self.activity_logs_url + "1/",
                json={field: value},
                headers=self.auth_headers,
            )
            self.assertEqual(response.status_code, 200)

    # Monkey 測試: 大量隨機請求
    def test_monkey_requests(self):
        def random_string(length):
            return "".join(random.choices(string.ascii_letters + string.digits, k=length))

        def random_int(min_value, max_value):
            return random.randint(min_value, max_value)

        for _ in range(50):
            method = random.choice(["GET", "PUT", "PATCH"])
            if method == "GET":
                response = requests.get(
                    self.activity_logs_url,
                    headers=self.auth_headers,
                )
                self.assertIn(response.status_code, [200, 404])
            else:
                data = {
                    "rtsp": random_string(random.randint(0, 64)),
                    "web_camera": random.choice([None, random_int(0, 10)]),
                    "image_height": random_int(0, 2160),
                    "image_width": random_int(0, 3840),
                    "detection_range_start_point_x": random_int(0, 3840),
                    "detection_range_start_point_y": random_int(0, 2160),
                    "detection_range_end_point_x": random_int(0, 3840),
                    "detection_range_end_point_y": random_int(0, 2160),
                }
                if method == "PUT":
                    response = requests.put(
                        self.activity_logs_url + "1/",
                        json=data,
                        headers=self.auth_headers,
                    )
                else:
                    response = requests.patch(
                        self.activity_logs_url + "1/",
                        json=data,
                        headers=self.auth_headers,
                    )
                self.assertIn(response.status_code, [200, 400, 404])
            time.sleep(0.1)  # 避免過快請求導致伺服器過載

    # Monkey 測試: 大量無效請求
    def test_monkey_invalid_requests(self):
        def random_string(length):
            return "".join(random.choices(string.ascii_letters + string.digits, k=length))

        def random_invalid_value():
            choices = [
                12345,  # 整數
                12.345,  # 浮點數
                [],  # 空列表
                {},  # 空字典
                None,  # 空值
                random_string(100),  # 過長字串
                -1,  # 負數
            ]
            return random.choice(choices)

        for _ in range(50):
            method = random.choice(["PUT", "PATCH"])
            data = {
                "rtsp": random_invalid_value(),
                "web_camera": random_invalid_value(),
                "image_height": random_invalid_value(),
                "image_width": random_invalid_value(),
                "detection_range_start_point_x": random_invalid_value(),
                "detection_range_start_point_y": random_invalid_value(),
                "detection_range_end_point_x": random_invalid_value(),
                "detection_range_end_point_y": random_invalid_value(),
            }
            if method == "PUT":
                response = requests.put(
                    self.activity_logs_url + "1/",
                    json=data,
                    headers=self.auth_headers,
                )
            else:
                response = requests.patch(
                    self.activity_logs_url + "1/",
                    json=data,
                    headers=self.auth_headers,
                )
            self.assertIn(response.status_code, [400, 404])
            time.sleep(0.1)
