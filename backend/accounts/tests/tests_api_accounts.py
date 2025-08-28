import os
import random
import string

import requests
import tomli
from django.test import TestCase


class ApiAccountsTests(TestCase):
    def setUp(self):
        with open("settings.toml", "rb") as f:
            config = tomli.load(f)
        tests_config = config.get("tests", {})
        self.test_server_url = tests_config.get("test_server_url")
        self.accounts_endpoint = self.test_server_url + "/api/accounts/"
        self.group_endpoint = self.accounts_endpoint + "group/"
        self.register_endpoint = self.accounts_endpoint + "register/"
        self.systemapps_endpoint = self.accounts_endpoint + "systemapps/"
        self.upload_picture_endpoint = self.accounts_endpoint + "upload-profile-picture/"

        # 登入帳號
        self.superadmin = {
            "account": "superadmin",
            "password": "superadmin",
            "remember_me": True,
            "select_mode": "Standard",
        }
        self.headers = {"Content-Type": "application/json"}
        # 登入取得 token
        resp = requests.post(f"{self.test_server_url}/api/auth/login/", json=self.superadmin, headers=self.headers)
        self.access_token = resp.json().get("access_token")
        self.auth_headers = {**self.headers, "Authorization": self.access_token}

    # 正向測試: 取得使用者列表
    def test_get_user_list(self):
        response = requests.get(self.accounts_endpoint, headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.json())
        self.assertIsInstance(response.json()["results"], list)

    # 正向測試: 取得單一使用者詳細資訊
    def test_retrieve_user_detail(self):
        list_resp = requests.get(self.accounts_endpoint, headers=self.auth_headers)
        user_list = list_resp.json().get("results", [])
        if not user_list:
            self.skipTest("No users available to test.")
        user_id = user_list[0]["id"]
        detail_resp = requests.get(f"{self.accounts_endpoint}{user_id}/", headers=self.auth_headers)
        self.assertEqual(detail_resp.status_code, 200)
        self.assertEqual(detail_resp.json().get("id"), user_id)

    def test_update_user_detail(self):
        list_resp = requests.get(self.accounts_endpoint, headers=self.auth_headers)
        user_list = list_resp.json().get("results", [])
        if not user_list:
            self.skipTest("No users available to test.")
        user_id = user_list[0]["id"]
        payload = {"account": user_list[0]["account"], "first_name": "UpdatedFirst", "last_name": "UpdatedLast"}
        update_resp = requests.put(f"{self.accounts_endpoint}{user_id}/", headers=self.auth_headers, json=payload)
        self.assertEqual(update_resp.status_code, 200)
        self.assertEqual(update_resp.json().get("first_name"), payload["first_name"])
        self.assertEqual(update_resp.json().get("last_name"), payload["last_name"])

    # 正向測試: 部分更新使用者詳細資訊
    def test_partial_update_user_detail(self):
        list_resp = requests.get(self.accounts_endpoint, headers=self.auth_headers)
        user_list = list_resp.json().get("results", [])
        if not user_list:
            self.skipTest("No users available to test.")
        user_id = user_list[0]["id"]
        payload = {"first_name": "PartialFirst"}
        patch_resp = requests.patch(f"{self.accounts_endpoint}{user_id}/", headers=self.auth_headers, json=payload)
        self.assertEqual(patch_resp.status_code, 200)
        self.assertEqual(patch_resp.json().get("first_name"), payload["first_name"])

    # 正向測試: 刪除使用者
    def test_delete_user(self):
        username = "tempuser" + str(os.urandom(4).hex())
        payload = {
            "account": username,
            "password": "Password123!",
        }
        create_resp = requests.post(self.register_endpoint, headers=self.auth_headers, json=payload)
        user_id = create_resp.json().get("id")
        del_resp = requests.delete(f"{self.accounts_endpoint}{user_id}/", headers=self.auth_headers)
        self.assertIn(del_resp.status_code, [204, 200])

    # 正向測試: 不可刪除預設管理員帳號
    def test_delete_default_admin(self):
        list_resp = requests.get(self.accounts_endpoint, headers=self.auth_headers)
        user_list = list_resp.json().get("results", [])
        admin_user = next((u for u in user_list if u["account"] == "superadmin"), None)
        if not admin_user:
            self.skipTest("No superadmin user available to test.")
        user_id = admin_user["id"]
        del_resp = requests.delete(f"{self.accounts_endpoint}{user_id}/", headers=self.auth_headers)
        self.assertEqual(del_resp.status_code, 400)
        self.assertIn("Cannot delete", del_resp.text)

    # 正向測試: 取得用戶群組列表
    def test_list_user_groups(self):
        response = requests.get(self.group_endpoint, headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.json())

    # 正向測試: 用戶群組 CRUD
    def test_group_crud_operations(self):
        # 先建立一個 group
        payload = {"group_name": f"tempgroup-{random.randint(1000, 9999)}"}
        create_resp = requests.post(self.group_endpoint, headers=self.auth_headers, json=payload)
        group_id = create_resp.json()["id"]

        # retrieve
        retrieve_resp = requests.get(f"{self.group_endpoint}{group_id}/", headers=self.auth_headers)
        self.assertEqual(retrieve_resp.status_code, 200)
        self.assertEqual(retrieve_resp.json()["id"], group_id)

        # update PUT
        update_payload = {"group_name": f"updated-{random.randint(1000, 9999)}"}
        update_resp = requests.put(f"{self.group_endpoint}{group_id}/", headers=self.auth_headers, json=update_payload)
        self.assertEqual(update_resp.status_code, 200)
        self.assertEqual(update_resp.json()["group_name"], update_payload["group_name"])

        # partial update PATCH
        patch_payload = {"group_name": f"patched-{random.randint(1000, 9999)}"}
        patch_resp = requests.patch(f"{self.group_endpoint}{group_id}/", headers=self.auth_headers, json=patch_payload)
        self.assertEqual(patch_resp.status_code, 200)
        self.assertEqual(patch_resp.json()["group_name"], patch_payload["group_name"])

        # delete
        del_resp = requests.delete(f"{self.group_endpoint}{group_id}/", headers=self.auth_headers)
        self.assertIn(del_resp.status_code, [204, 200])

    # 正向測試: 使用者註冊
    def test_register_user(self):
        username = "user_" + "".join(random.choices(string.ascii_lowercase, k=5))
        payload = {"account": username, "password": "@Password123", "email": f"{username}@example.com", "group_id": 1}
        response = requests.post(self.register_endpoint, headers=self.auth_headers, json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())
        user_id = response.json().get("id")

        # delete
        del_resp = requests.delete(f"{self.accounts_endpoint}{user_id}/", headers=self.auth_headers)
        self.assertEqual(del_resp.status_code, 204)

    # 反向測試: 使用者註冊缺少必要欄位
    def test_register_user_missing_fields(self):
        payload = {
            "account": "incompleteuser",
            # Missing password
        }
        response = requests.post(self.register_endpoint, headers=self.auth_headers, json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.json())

    # 反向測試: 使用者註冊帳號重複
    def test_register_user_duplicate_account(self):
        payload = {
            "account": "superadmin",  # Assuming this account already exists
            "password": "@Password123",
        }
        response = requests.post(self.register_endpoint, headers=self.auth_headers, json=payload)
        self.assertEqual(response.status_code, 400)

    # 反向測試: 使用者註冊帳號不符合規範
    def test_register_user_invalid_password(self):
        payload = {
            "account": "aa",  # Invalid account (too short)
            "password": "@Password123",  # Invalid password (too short)
        }
        response = requests.post(self.register_endpoint, headers=self.auth_headers, json=payload)
        self.assertEqual(response.status_code, 400)

    # 反向測試: 使用者註冊密碼不符合規範
    def test_register_user_invalid_account(self):
        payload = {
            "account": "validuser",
            "password": "abc",  # Invalid password (too short)
        }
        response = requests.post(self.register_endpoint, headers=self.auth_headers, json=payload)
        self.assertEqual(response.status_code, 400)

    # 正向測試: 變更使用者密碼
    def test_change_user_password(self):
        # register a temp user first
        username = "tempuser" + str(os.urandom(4).hex())
        payload = {
            "account": username,
            "password": "OldPassword123!",
        }
        create_resp = requests.post(self.register_endpoint, headers=self.auth_headers, json=payload)
        user_id = create_resp.json().get("id")

        change_payload = {"old_password": "OldPassword123!", "new_password": "NewPassword123!"}
        change_resp = requests.post(
            f"{self.accounts_endpoint}change-password/{user_id}/", headers=self.auth_headers, json=change_payload
        )
        self.assertEqual(change_resp.status_code, 200)
        self.assertIn("Password changed successfully", change_resp.text)

        # delete
        del_resp = requests.delete(f"{self.accounts_endpoint}{user_id}/", headers=self.auth_headers)
        self.assertEqual(del_resp.status_code, 204)

    # 正向測試: 取得系統應用程式列表
    def test_list_system_apps(self):
        response = requests.get(self.systemapps_endpoint, headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json()["results"], list)

    # 正向測試: 上傳使用者大頭貼
    def test_upload_profile_picture(self):
        # 模擬上傳小檔案
        files = {"file": ("test.png", b"dummy_image_bytes", "image/png")}
        response = requests.post(
            self.upload_picture_endpoint, headers={"Authorization": self.access_token}, files=files
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("image_url", response.json())
