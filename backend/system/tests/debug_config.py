import requests
import tomli
from django.test import TestCase


class ApiFaceRecognitionConfigDebugTests(TestCase):
    """Test cases for the /api/face-recognition-config/debug/ endpoint."""
    def setUp(self):
        with open("settings.toml", "rb") as f:
            config = tomli.load(f)
        tests_config = config.get("tests", {})
        self.test_server_url = tests_config.get("test_server_url")
        self.activity_logs_url = self.test_server_url + "/api/face-recognition-config/debug/"
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

    # 正向測試: 取得 Debug Configuration
    def test_get_debug_configuration(self):
        response = requests.get(
            self.activity_logs_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        self.assertGreaterEqual(len(data["results"]), 1)
        self.assertIn("debug", data["results"][0])

    # 正向測試: 更新 Debug Configuration
    def test_update_debug_configuration(self):
        update_data = {"debug": True}
        response = requests.put(
            self.activity_logs_url + "1/",
            json=update_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("debug", data)
        self.assertTrue(data["debug"])

    # 正向測試: 部分更新 Debug Configuration
    def test_partial_update_debug_configuration(self):
        partial_update_data = {"debug": False}
        response = requests.patch(
            self.activity_logs_url + "1/",
            json=partial_update_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("debug", data)
        self.assertFalse(data["debug"])

    # 反向測試: 欄位類型錯誤
    def test_invalid_field_type(self):
        invalid_data = {"debug": "not_a_boolean"}
        response = requests.put(
            self.activity_logs_url + "1/",
            json=invalid_data,
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
