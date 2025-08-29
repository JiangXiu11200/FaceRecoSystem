import random
import string

import requests
import tomli
from django.test import TestCase


class ApiAuthTests(TestCase):
    """Test cases for the /api/auth/ endpoint."""

    def setUp(self):
        with open("settings.toml", "rb") as f:
            config = tomli.load(f)
        tests_config = config.get("tests", {})
        self.test_server_url = tests_config.get("test_server_url")
        self.login_endpoint = self.test_server_url + "/api/auth/login/"
        self.logout_endpoint = self.test_server_url + "/api/auth/logout/"
        self.refresh_endpoint = self.test_server_url + "/api/token/refresh/"
        self.superadmin = {
            "account": "superadmin",
            "password": "superadmin",
            "remember_me": True,
            "select_mode": "Standard",
        }
        self.headers = {"Content-Type": "application/json"}

    # 正向測試： Standard 模式登入/登出
    def test_login_success(self):
        response = requests.post(
            self.login_endpoint,
            json=self.superadmin,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertIsNotNone(response.cookies.get("refresh_token"))

        access_token = response.json().get("access_token")
        auth_headers = {**self.headers, "Authorization": access_token}
        logout_resp = requests.post(self.logout_endpoint, headers=auth_headers)
        self.assertEqual(logout_resp.status_code, 200)

    # 正向測試： Advanced 模式登入
    def test_login_admin_mode(self):
        payload = self.superadmin.copy()
        payload["select_mode"] = "Advanced"
        response = requests.post(
            self.login_endpoint,
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    # 反向測試：沒有此使用者
    def test_login_invalid_account(self):
        payload = self.superadmin.copy()
        payload["account"] = "wronguser"
        response = requests.post(
            self.login_endpoint,
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid", response.text)

    # 反向測試：密碼錯誤
    def test_login_invalid_password(self):
        payload = self.superadmin.copy()
        payload["password"] = "wrongpassword"
        response = requests.post(
            self.login_endpoint,
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 400)

    # 反向測試：缺少必要欄位
    def test_login_missing_field(self):
        payload = {"account": "superadmin"}
        response = requests.post(
            self.login_endpoint,
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 400)

    # 反向測試：錯誤的模式
    def test_login_invalid_select_mode(self):
        payload = self.superadmin.copy()
        payload["select_mode"] = "InvalidMode"
        response = requests.post(
            self.login_endpoint,
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid", response.text)

    # Monkey Test：隨機亂數輸入
    def test_login_monkey(self):
        payload = {
            "account": "".join(random.choices(string.printable, k=100)),
            "password": "".join(random.choices(string.printable, k=100)),
            "remember_me": random.choice([True, False, None]),
            "select_mode": random.choice(["Standard", "Advanced"]),
        }
        response = requests.post(
            self.login_endpoint,
            json=payload,
            headers=self.headers,
        )
        self.assertNotEqual(response.status_code, 500)
        self.assertIn(response.status_code, [400, 401])

    # 正向測試: refresh token 換取新的 access token
    def test_refresh_token_success(self):
        # 先登入取得 refresh token
        login_resp = requests.post(self.login_endpoint, json=self.superadmin, headers=self.headers)
        self.assertEqual(login_resp.status_code, 200)
        refresh_token = login_resp.cookies.get("refresh_token")
        self.assertIsNotNone(refresh_token)

        # 使用 refresh token 換取新的 access token
        refresh_resp = requests.post(
            f"{self.test_server_url}/api/token/refresh/",
            cookies={"refresh_token": refresh_token},
            headers=self.headers,
        )
        self.assertEqual(refresh_resp.status_code, 200)
        self.assertIn("access_token", refresh_resp.json())

    # 反向測試: 缺少 refresh token
    def test_refresh_token_missing(self):
        refresh_resp = requests.post(
            f"{self.test_server_url}/api/token/refresh/",
            headers=self.headers,
        )
        self.assertEqual(refresh_resp.status_code, 401)

    # 反向測試: 使用無效的 refresh token
    def test_refresh_token_invalid(self):
        refresh_resp = requests.post(
            f"{self.test_server_url}/api/token/refresh/",
            cookies={"refresh_token": "invalidtoken"},
            headers=self.headers,
        )
        self.assertEqual(refresh_resp.status_code, 401)
