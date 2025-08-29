import random
import string

import requests
import tomli
from django.test import TestCase


class ApiUserRegistrationGroupTests(TestCase):
    def setUp(self):
        # 讀取測試設定
        with open("settings.toml", "rb") as f:
            config = tomli.load(f)
        tests_config = config.get("tests", {})
        self.test_server_url = tests_config.get("test_server_url")
        self.user_registration_url = f"{self.test_server_url}/api/user-registration/group/"
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

    # 正向測試: 取得 user registration group 列表
    def test_get_user_registration_group_list(self):
        response = requests.get(
            self.user_registration_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)

    # 正向測試: user registration group crud
    def test_user_registration_group_crud(self):
        # Create
        new_group = {"group_name": "".join(random.choices(string.ascii_letters, k=16))}
        response = requests.post(
            self.user_registration_url,
            json=new_group,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 201)
        created_group = response.json()
        self.assertEqual(created_group["group_name"], new_group["group_name"])
        group_id = created_group["id"]

        # Retrieve
        response = requests.get(
            f"{self.user_registration_url}{group_id}/",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        retrieved_group = response.json()
        self.assertEqual(retrieved_group["id"], group_id)

        # Update
        updated_data = {"group_name": "Updated Test Group", "is_active": False}
        response = requests.put(
            f"{self.user_registration_url}{group_id}/",
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        updated_group = response.json()
        self.assertEqual(updated_group["group_name"], updated_data["group_name"])
        self.assertEqual(updated_group["is_active"], updated_data["is_active"])

        # Partial Update
        partial_data = {"is_active": True}
        response = requests.patch(
            f"{self.user_registration_url}{group_id}/",
            json=partial_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        patched_group = response.json()
        self.assertEqual(patched_group["is_active"], partial_data["is_active"])

        # Delete
        response = requests.delete(
            f"{self.user_registration_url}{group_id}/",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 204)

        # Confirm Deletion
        response = requests.get(
            f"{self.user_registration_url}{group_id}/",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 404)

    # 正向測試: group name 過濾
    def test_user_registration_group_name_filter(self):
        group_names = ["Alpha Group", "Beta Group", "Gamma Group"]
        for name in group_names:
            requests.post(
                self.user_registration_url,
                json={"group_name": name},
                headers=self.auth_headers,
            )

        response = requests.get(
            self.user_registration_url,
            params={"group_name": "Alpha"},
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["group_name"], "Alpha Group")

    # 正向測試: 建立只包含必要欄位的 group
    def test_create_minimal_user_registration_group(self):
        text = "".join(random.choices(string.ascii_letters, k=10))
        minimal_group = {"group_name": text}
        response = requests.post(
            self.user_registration_url,
            json=minimal_group,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 201)
        created_group = response.json()
        self.assertEqual(created_group["group_name"], minimal_group["group_name"])
        self.assertIn("id", created_group)
        self.assertIn("user_count", created_group)
        self.assertIn("is_active", created_group)
        self.assertIn("create_time", created_group)
        self.assertIn("update_time", created_group)

    # 正向測試: 建立無效的 group (重複名稱)
    def test_create_invalid_user_registration_group(self):
        text = "".join(random.choices(string.ascii_letters, k=10))
        group_data = {"group_name": text}
        response1 = requests.post(
            self.user_registration_url,
            json=group_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response1.status_code, 201)

        response2 = requests.post(
            self.user_registration_url,
            json=group_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response2.status_code, 400)

    # 反向測試: 超過長的 group name
    def test_create_user_registration_group_exceeding_name_length(self):
        long_name = "G" * 65  # 65 characters, exceeding max length of 64
        group_data = {"group_name": long_name}
        response = requests.post(
            self.user_registration_url,
            json=group_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 400)

    # 反向測試: 取得不存在的 group
    def test_retrieve_nonexistent_user_registration_group(self):
        response = requests.get(
            f"{self.user_registration_url}99999/",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 404)

    # 反向測試: 更新不存在的 group
    def test_update_nonexistent_user_registration_group(self):
        updated_data = {"group_name": "Nonexistent Group", "is_active": False}
        response = requests.put(
            f"{self.user_registration_url}99999/",
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 404)

    # 反向測試: 刪除不存在的 group
    def test_delete_nonexistent_user_registration_group(self):
        response = requests.delete(
            f"{self.user_registration_url}99999/",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 404)

    # 反向測試: 非法字元輸入
    def test_create_user_registration_group_with_illegal_characters(self):
        illegal_name = "Invalid@Group#Name!"
        group_data = {"group_name": illegal_name}
        response = requests.post(
            self.user_registration_url,
            json=group_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 400)

    # 反向測試: 特殊字元輸入
    def test_create_user_registration_group_with_special_characters(self):
        special_name = "特殊字符组!@#$%^&*()"
        group_data = {"group_name": special_name}
        response = requests.post(
            self.user_registration_url,
            json=group_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 400)
        error_data = response.json()
        self.assertIn("group_name", error_data)

    # 邊界測試: 建立名稱長度為 1 的 group
    def test_create_user_registration_group_min_name_length(self):
        min_length_name = random.choice(string.ascii_letters)
        group_data = {"group_name": min_length_name}
        response = requests.post(
            self.user_registration_url,
            json=group_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 201)

    # 邊界測試: 建立名稱長度為 64 的 group
    def test_create_user_registration_group_max_name_length(self):
        text = "".join(random.choices(string.ascii_letters + string.digits + " _", k=64))  # 64 characters
        max_length_name = text
        group_data = {"group_name": max_length_name}
        response = requests.post(
            self.user_registration_url,
            json=group_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 201)
