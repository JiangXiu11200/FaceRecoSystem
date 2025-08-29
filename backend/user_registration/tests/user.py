import base64
import hashlib
import random
import string
import time

import requests
import tomli
from django.test import TestCase

with open("./user_registration/tests/test_face.jpg", "rb") as img_file:
    image_data = img_file.read()
BASE64_TEST_IMAGE = base64.b64encode(image_data).decode("utf-8")


class ApiUserRegistrationTests(TestCase):
    """Test cases for the /api/user-registration/group/ endpoint."""

    def setUp(self):
        # 讀取測試設定
        with open("settings.toml", "rb") as f:
            config = tomli.load(f)
        tests_config = config.get("tests", {})
        self.test_server_url = tests_config.get("test_server_url")
        self.user_registration_url = f"{self.test_server_url}/api/user-registration/"
        self.user_registration_group_url = f"{self.test_server_url}/api/user-registration/group/"

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

    # 正向測試: 取得使用者註冊列表
    def test_get_user_registration_list(self):
        response = requests.get(
            self.user_registration_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)

    # 正向測試: 使用者註冊 CRUD
    def test_user_registration_crud(self):
        # 註冊群組
        text = (hashlib.sha256(str(time.time()).encode()).hexdigest())[:10]
        group_data = {"group_name": text}
        group_response = requests.post(
            self.user_registration_group_url,
            json=group_data,
            headers=self.auth_headers,
        )
        self.assertEqual(group_response.status_code, 201)
        group_id = group_response.json().get("id")
        name = "".join(random.choices(string.ascii_letters, k=8))
        user_data = {
            "name": name,
            "s3_object_key": "test_key",
            "register_group": group_id,
            "image": BASE64_TEST_IMAGE,
        }
        # Create
        response = requests.post(
            self.user_registration_url,
            json=user_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 201)
        created_user = response.json()
        self.assertEqual(created_user["name"], user_data["name"])
        user_id = created_user["id"]

        # Retrieve
        response = requests.get(
            f"{self.user_registration_url}{user_id}/",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        retrieved_user = response.json()
        self.assertEqual(retrieved_user["id"], user_id)

        # Update
        updated_data = {
            "name": name,
            "register_group": group_id,
            "is_active": False,
        }
        response = requests.put(
            f"{self.user_registration_url}{user_id}/",
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)

        # Partial Update
        partial_data = {"is_active": True}
        response = requests.patch(
            f"{self.user_registration_url}{user_id}/",
            json=partial_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        patched_user = response.json()
        self.assertEqual(patched_user["is_active"], partial_data["is_active"])

        # Delete
        response = requests.delete(
            f"{self.user_registration_url}{user_id}/",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 204)

        # Confirm Deletion
        response = requests.get(
            f"{self.user_registration_url}{user_id}/",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 404)

    # 正向測試: 使用者名稱過濾
    def test_user_registration_username_filter(self):
        # 註冊群組
        text = (hashlib.sha256(str(time.time()).encode()).hexdigest())[:10]
        group_data = {"group_name": text}
        group_response = requests.post(
            self.user_registration_group_url,
            json=group_data,
            headers=self.auth_headers,
        )
        self.assertEqual(group_response.status_code, 201)
        group_id = group_response.json().get("id")
        names = [(hashlib.sha256(str(time.time()).encode()).hexdigest())[:5] for _ in range(3)]
        for name in names:
            user_data = {
                "name": name,
                "s3_object_key": "test_key",
                "register_group": group_id,
                "image": BASE64_TEST_IMAGE,
            }
            requests.post(
                self.user_registration_url,
                json=user_data,
                headers=self.auth_headers,
            )

        response = requests.get(
            self.user_registration_url,
            params={"name": names[0][:3]},
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["name"], names[0])

    # 正向測試: 建立只包含必要欄位的使用者
    def test_create_minimal_user_registration(self):
        # 註冊群組
        text = (hashlib.sha256(str(time.time()).encode()).hexdigest())[:10]
        group_data = {"group_name": text}
        group_response = requests.post(
            self.user_registration_group_url,
            json=group_data,
            headers=self.auth_headers,
        )
        self.assertEqual(group_response.status_code, 201)
        group_id = group_response.json().get("id")
        names = "".join(random.choices(string.ascii_letters + string.digits, k=12))
        minimal_user = {
            "name": names,
            "s3_object_key": "test_key",
            "register_group": group_id,
            "image": BASE64_TEST_IMAGE,
        }
        response = requests.post(
            self.user_registration_url,
            json=minimal_user,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 201)
        created_user = response.json()
        self.assertEqual(created_user["name"], minimal_user["name"])
        self.assertIn("id", created_user)

    # 反向測試: 重複使用者名稱
    def test_create_duplicate_username(self):
        # 註冊群組
        text = (hashlib.sha256(str(time.time()).encode()).hexdigest())[:10]
        group_data = {"group_name": text}
        group_response = requests.post(
            self.user_registration_group_url,
            json=group_data,
            headers=self.auth_headers,
        )
        self.assertEqual(group_response.status_code, 201)
        group_id = group_response.json().get("id")
        name = "".join(random.choices(string.ascii_letters + string.digits, k=10))
        user_data = {
            "name": name,
            "s3_object_key": "test_key",
            "register_group": group_id,
            "image": BASE64_TEST_IMAGE,
        }
        response1 = requests.post(
            self.user_registration_url,
            json=user_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response1.status_code, 201)

        # Try to create another user with the same username
        response2 = requests.post(
            self.user_registration_url,
            json=user_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response2.status_code, 400)

    # 反向測試: 取得不存在的使用者
    def test_retrieve_nonexistent_user(self):
        response = requests.get(
            f"{self.user_registration_url}99999/",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 404)

    # 反向測試: 更新不存在的使用者
    def test_update_nonexistent_user(self):
        updated_data = {"is_active": False}
        response = requests.put(
            f"{self.user_registration_url}99999/",
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 404)

    # 反向測試: 刪除不存在的使用者
    def test_delete_nonexistent_user(self):
        response = requests.delete(
            f"{self.user_registration_url}99999/",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 404)

    # 反向測試: 不存在的群組ID
    def test_create_user_with_nonexistent_group(self):
        name = "".join(random.choices(string.ascii_letters + string.digits, k=4))
        user_data = {
            "name": name,
            "s3_object_key": "test_key",
            "register_group": 99998,
            "image": BASE64_TEST_IMAGE,
        }
        response = requests.post(
            self.user_registration_url,
            json=user_data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 400)

    # 邊界測試: 使用者名稱長度邊界測試
    def test_username_length_boundary(self):
        # 註冊群組
        text = (hashlib.sha256(str(time.time()).encode()).hexdigest())[:10]
        group_data = {"group_name": text}
        group_response = requests.post(
            self.user_registration_group_url,
            json=group_data,
            headers=self.auth_headers,
        )
        self.assertEqual(group_response.status_code, 201)
        group_id = group_response.json().get("id")
        # 測試最短使用者名稱
        min_username = "".join(random.choices(string.ascii_letters, k=1))
        min_user = {
            "name": min_username,
            "s3_object_key": "test_key",
            "register_group": group_id,
            "image": BASE64_TEST_IMAGE,
        }
        response = requests.post(
            self.user_registration_url,
            json=min_user,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 201)

    # 邊界測試: 使用者名稱長度邊界測試
    def test_username_length_limits(self):
        # 註冊群組
        text = (hashlib.sha256(str(time.time()).encode()).hexdigest())[:10]
        group_data = {"group_name": text}
        group_response = requests.post(
            self.user_registration_group_url,
            json=group_data,
            headers=self.auth_headers,
        )
        self.assertEqual(group_response.status_code, 201)
        group_id = group_response.json().get("id")
        max_username = "".join(random.choices(string.ascii_letters, k=64))
        max_user = {
            "name": max_username,
            "s3_object_key": "test_key",
            "register_group": group_id,
            "image": BASE64_TEST_IMAGE,
        }
        response = requests.post(
            self.user_registration_url,
            json=max_user,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 201)

    # 邊界測試: 使用者名稱長度超出限制
    def test_username_too_long(self):
        too_long_username = "".join(random.choices(string.ascii_letters + string.digits, k=65))
        too_long_user = {"name": too_long_username, "s3_object_key": "test_key", "image": "test_base64_image"}
        response = requests.post(
            self.user_registration_url,
            json=too_long_user,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 400)
