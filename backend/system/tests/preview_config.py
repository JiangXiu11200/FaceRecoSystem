import requests
import tomli
from django.test import TestCase


class ApiFaceRecognitionConfigPreviewTests(TestCase):
    """Test cases for the /api/face-recognition-config/preview/ endpoint."""
    def setUp(self):
        with open("settings.toml", "rb") as f:
            config = tomli.load(f)
        tests_config = config.get("tests", {})
        self.test_server_url = tests_config.get("test_server_url")
        self.activity_logs_url = self.test_server_url + "/api/face-recognition-config/preview/"
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

    # 正向測試: 取得 Preview Configuration
    def test_get_preview_configuration(self):
        response = requests.get(
            self.activity_logs_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)

    # 反向測試: 不允許的方法
    def test_method_not_allowed(self):
        method = ["POST", "PUT", "PATCH", "DELETE"]
        for m in method:
            response = requests.request(
                m,
                self.activity_logs_url,
                headers=self.auth_headers,
            )
            self.assertEqual(response.status_code, 405)

