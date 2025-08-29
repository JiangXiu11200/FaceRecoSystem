import random
import string

import requests
import tomli
from django.test import TestCase


class ApiActivityLogsRetentionTests(TestCase):
    def setUp(self):
        with open("settings.toml", "rb") as f:
            config = tomli.load(f)
        tests_config = config.get("tests", {})
        self.test_server_url = tests_config.get("test_server_url")
        self.activity_logs_retention_url = self.test_server_url + "/api/activity-logs/system/retention/"
        self.face_recognition_retention_url = self.test_server_url + "/api/activity-logs/face-recognition/retention/"
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

    # 正向測試: 取得 System activity logs retention 列表
    def test_get_activity_logs_retention_list(self):
        response = requests.get(
            self.activity_logs_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)

    # 正向測試: 取得 Face Recognition activity logs retention 列表
    def test_get_face_recognition_activity_logs_retention_list(self):
        response = requests.get(
            self.face_recognition_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)

    # 正向測試: 更新 System activity logs retention
    def test_update_activity_logs_retention(self):
        response = requests.get(
            self.activity_logs_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.activity_logs_retention_url}{retention_id}/"
        updated_data = {"retention_days": 60}
        update_response = requests.put(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 200)
        updated_response_data = update_response.json()
        self.assertEqual(updated_response_data["retention_days"], updated_data["retention_days"])

    # 正向測試: 更新 Face Recognition activity logs retention
    def test_update_face_recognition_activity_logs_retention(self):
        response = requests.get(
            self.face_recognition_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.face_recognition_retention_url}{retention_id}/"
        updated_data = {"retention_days": 60}
        update_response = requests.put(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 200)
        updated_response_data = update_response.json()
        self.assertEqual(updated_response_data["retention_days"], updated_data["retention_days"])

    # 正向測試: 部分更新 System activity logs retention (PATCH, 功能同 PUT)
    def test_partial_update_activity_logs_retention(self):
        response = requests.get(
            self.activity_logs_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.activity_logs_retention_url}{retention_id}/"
        updated_data = {"retention_days": 90}
        update_response = requests.patch(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 200)
        updated_response_data = update_response.json()
        self.assertEqual(updated_response_data["retention_days"], updated_data["retention_days"])

    # 正向測試: 部分更新 Face Recognition activity logs retention (PATCH, 功能同 PUT)
    def test_partial_update_face_recognition_activity_logs_retention(self):
        response = requests.get(
            self.face_recognition_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.face_recognition_retention_url}{retention_id}/"
        updated_data = {"retention_days": 90}
        update_response = requests.patch(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 200)
        updated_response_data = update_response.json()
        self.assertEqual(updated_response_data["retention_days"], updated_data["retention_days"])

    # 反向測試: 更新 System activity logs retention，輸入 retention_days 非數字
    def test_update_activity_logs_retention_invalid_retention_days(self):
        response = requests.get(
            self.activity_logs_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.activity_logs_retention_url}{retention_id}/"
        updated_data = {"retention_days": "invalid_number"}
        update_response = requests.put(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 400)
        updated_response_data = update_response.json()
        self.assertIn("retention_days", updated_response_data)

    # 反向測試: 更新 Face Recognition activity logs retention，輸入 retention_days 非數字
    def test_update_face_recognition_activity_logs_retention_invalid_retention_days(self):
        response = requests.get(
            self.face_recognition_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.face_recognition_retention_url}{retention_id}/"
        updated_data = {"retention_days": "invalid_number"}
        update_response = requests.put(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 400)
        updated_response_data = update_response.json()
        self.assertIn("retention_days", updated_response_data)

    # 反向測試: 更新 System activity logs retention，輸入 retention_days 小於 1
    def test_update_activity_logs_retention_retention_days_too_small(self):
        response = requests.get(
            self.activity_logs_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.activity_logs_retention_url}{retention_id}/"
        updated_data = {"retention_days": 0}
        update_response = requests.put(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 400)
        updated_response_data = update_response.json()
        self.assertIn("retention_days", updated_response_data)

    # 反向測試: 更新 Face Recognition activity logs retention，輸入 retention_days 小於 1
    def test_update_face_recognition_activity_logs_retention_retention_days_too_small(self):
        response = requests.get(
            self.face_recognition_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.face_recognition_retention_url}{retention_id}/"
        updated_data = {"retention_days": 0}
        update_response = requests.put(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 400)
        updated_response_data = update_response.json()
        self.assertIn("retention_days", updated_response_data)

    # 反向測試: 更新 System activity logs retention，輸入 retention_days 大於 365
    def test_update_activity_logs_retention_retention_days_too_large(self):
        response = requests.get(
            self.activity_logs_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.activity_logs_retention_url}{retention_id}/"
        updated_data = {"retention_days": 999}
        update_response = requests.put(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 400)
        updated_response_data = update_response.json()
        self.assertIn("retention_days", updated_response_data)

    # 反向測試: 更新 Face Recognition activity logs retention，輸入 retention_days 大於 365
    def test_update_face_recognition_activity_logs_retention_retention_days_too_large(self):
        response = requests.get(
            self.face_recognition_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.face_recognition_retention_url}{retention_id}/"
        updated_data = {"retention_days": 999}
        update_response = requests.put(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 400)
        updated_response_data = update_response.json()
        self.assertIn("retention_days", updated_response_data)

    # 反向測試: 更新 System activity logs retention，輸入 retention_days 為空
    def test_update_activity_logs_retention_retention_days_empty(self):
        response = requests.get(
            self.activity_logs_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.activity_logs_retention_url}{retention_id}/"
        updated_data = {"retention_days": ""}
        update_response = requests.put(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 400)
        updated_response_data = update_response.json()
        self.assertIn("retention_days", updated_response_data)

    # 反向測試: 更新 Face Recognition activity logs retention，輸入 retention_days 為空
    def test_update_face_recognition_activity_logs_retention_retention_days_empty(self):
        response = requests.get(
            self.face_recognition_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.face_recognition_retention_url}{retention_id}/"
        updated_data = {"retention_days": ""}
        update_response = requests.put(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 400)
        updated_response_data = update_response.json()
        self.assertIn("retention_days", updated_response_data)

    # 反向測試: 不允許 POST 新增 System activity logs retention (應回傳 405)
    def test_post_activity_logs_retention_not_allowed(self):
        new_data = {"retention_days": 90}
        post_response = requests.post(
            self.activity_logs_retention_url,
            json=new_data,
            headers=self.auth_headers,
        )
        self.assertEqual(post_response.status_code, 405)

    # 反向測試: 不允許 POST 新增 Face Recognition activity logs retention (應回傳 405)
    def test_post_face_recognition_activity_logs_retention_not_allowed(self):
        new_data = {"retention_days": 90}
        post_response = requests.post(
            self.face_recognition_retention_url,
            json=new_data,
            headers=self.auth_headers,
        )
        self.assertEqual(post_response.status_code, 405)

    # 邊界值測試: 更新 System activity logs retention，輸入 retention_days 為 1
    def test_update_activity_logs_retention_retention_days_boundary_1(self):
        response = requests.get(
            self.activity_logs_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.activity_logs_retention_url}{retention_id}/"
        updated_data = {"retention_days": 1}
        update_response = requests.put(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 200)
        updated_response_data = update_response.json()
        self.assertEqual(updated_response_data["retention_days"], updated_data["retention_days"])

    # 邊界值測試: 更新 Face Recognition activity logs retention，輸入 retention_days 為 1
    def test_update_face_recognition_activity_logs_retention_retention_days_boundary_1(self):
        response = requests.get(
            self.face_recognition_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.face_recognition_retention_url}{retention_id}/"
        updated_data = {"retention_days": 1}
        update_response = requests.put(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 200)
        updated_response_data = update_response.json()
        self.assertEqual(updated_response_data["retention_days"], updated_data["retention_days"])

    # 邊界值測試: 更新 System activity logs retention，輸入 retention_days 為 365
    def test_update_activity_logs_retention_retention_days_boundary_365(self):
        response = requests.get(
            self.activity_logs_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.activity_logs_retention_url}{retention_id}/"
        updated_data = {"retention_days": 365}
        update_response = requests.put(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 200)
        updated_response_data = update_response.json()
        self.assertEqual(updated_response_data["retention_days"], updated_data["retention_days"])

    # 邊界值測試: 更新 Face Recognition activity logs retention，輸入 retention_days 為 365
    def test_update_face_recognition_activity_logs_retention_retention_days_boundary_365(self):
        response = requests.get(
            self.face_recognition_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.face_recognition_retention_url}{retention_id}/"
        updated_data = {"retention_days": 365}
        update_response = requests.put(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 200)
        updated_response_data = update_response.json()
        self.assertEqual(updated_response_data["retention_days"], updated_data["retention_days"])

    # Monkey 測試: 更新 System activity logs retention，輸入 retention_days 為隨機字串
    def test_update_activity_logs_retention_retention_days_random_string(self):
        response = requests.get(
            self.activity_logs_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.activity_logs_retention_url}{retention_id}/"
        random_string = "".join(random.choices(string.ascii_letters + string.digits, k=10))
        updated_data = {"retention_days": random_string}
        update_response = requests.put(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 400)
        updated_response_data = update_response.json()
        self.assertIn("retention_days", updated_response_data)

    # Monkey 測試: 更新 Face Recognition activity logs retention，輸入 retention_days 為隨機字串
    def test_update_face_recognition_activity_logs_retention_retention_days_random_string(self):
        response = requests.get(
            self.face_recognition_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.face_recognition_retention_url}{retention_id}/"
        random_string = "".join(random.choices(string.ascii_letters + string.digits, k=10))
        updated_data = {"retention_days": random_string}
        update_response = requests.put(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 400)
        updated_response_data = update_response.json()
        self.assertIn("retention_days", updated_response_data)

    # Monkey 測試: 更新 System activity logs retention，輸入 retention_days 為負數
    def test_update_activity_logs_retention_retention_days_negative(self):
        response = requests.get(
            self.activity_logs_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.activity_logs_retention_url}{retention_id}/"
        updated_data = {"retention_days": -10}
        update_response = requests.put(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 400)
        updated_response_data = update_response.json()
        self.assertIn("retention_days", updated_response_data)

    # Monkey 測試: 更新 Face Recognition activity logs retention，輸入 retention_days 為負數
    def test_update_face_recognition_activity_logs_retention_retention_days_negative(self):
        response = requests.get(
            self.face_recognition_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.face_recognition_retention_url}{retention_id}/"
        updated_data = {"retention_days": -10}
        update_response = requests.put(
            update_url,
            json=updated_data,
            headers=self.auth_headers,
        )
        self.assertEqual(update_response.status_code, 400)
        updated_response_data = update_response.json()
        self.assertIn("retention_days", updated_response_data)

    # Monkey 測試: 刪除 System activity logs retention (不允許刪除，應回傳 405)
    def test_delete_activity_logs_retention_not_allowed(self):
        response = requests.get(
            self.activity_logs_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        delete_url = f"{self.activity_logs_retention_url}{retention_id}/"
        delete_response = requests.delete(
            delete_url,
            headers=self.auth_headers,
        )
        self.assertEqual(delete_response.status_code, 405)

    # Monkey 測試: 刪除 Face Recognition activity logs retention (不允許刪除，應回傳 405)
    def test_delete_face_recognition_activity_logs_retention_not_allowed(self):
        response = requests.get(
            self.face_recognition_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        delete_url = f"{self.face_recognition_retention_url}{retention_id}/"
        delete_response = requests.delete(
            delete_url,
            headers=self.auth_headers,
        )
        self.assertEqual(delete_response.status_code, 405)

    # Monkey: 測試並發操作
    def test_concurrent_updates_activity_logs_retention(self):
        response = requests.get(
            self.activity_logs_retention_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        retention_id = data["results"][0]["id"]
        update_url = f"{self.activity_logs_retention_url}{retention_id}/"

        updated_data_1 = {"retention_days": 30}
        updated_data_2 = {"retention_days": 120}

        from concurrent.futures import ThreadPoolExecutor

        def update_retention(data):
            return requests.put(update_url, json=data, headers=self.auth_headers)

        with ThreadPoolExecutor(max_workers=2) as executor:
            future1 = executor.submit(update_retention, updated_data_1)
            future2 = executor.submit(update_retention, updated_data_2)

            response1 = future1.result()
            response2 = future2.result()

            self.assertIn(response1.status_code, [200, 400])
            self.assertIn(response2.status_code, [200, 400])
