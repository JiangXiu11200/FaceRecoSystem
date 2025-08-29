import random
import string

import requests
import tomli
from django.test import TestCase


class ApiAlarmLogsTests(TestCase):
    """Test cases for the /api/alarm-logs/ endpoint."""

    def setUp(self):
        with open("settings.toml", "rb") as f:
            config = tomli.load(f)
        tests_config = config.get("tests", {})
        self.test_server_url = tests_config.get("test_server_url")
        self.alarm_logs_url = self.test_server_url + "/api/alarm-logs/"
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

    # # 正向測試: 取得 alarm logs 列表
    def test_get_alarm_logs_list(self):
        response = requests.get(
            self.alarm_logs_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)

    # 正向測試: Alarm logs crd
    def test_alarm_log_crd(self):
        new_alarm_log = {
            "name": "test_user_crud",
            "s3_object_key": "test_key_crud",
        }
        create_response = requests.post(
            self.alarm_logs_url,
            json=new_alarm_log,
            headers=self.auth_headers,
        )
        self.assertEqual(create_response.status_code, 201)
        created_data = create_response.json()
        alarm_log_id = created_data.get("id")
        self.assertIsNotNone(alarm_log_id)

        detail_url = f"{self.alarm_logs_url}{alarm_log_id}/"
        get_response = requests.get(detail_url, headers=self.auth_headers)
        self.assertEqual(get_response.status_code, 200)
        get_data = get_response.json()
        self.assertEqual(get_data["name"], new_alarm_log["name"])
        self.assertEqual(get_data["s3_object_key"], new_alarm_log["s3_object_key"])

        delete_response = requests.delete(detail_url, headers=self.auth_headers)
        self.assertEqual(delete_response.status_code, 204)

        get_after_delete_response = requests.get(detail_url, headers=self.auth_headers)
        self.assertEqual(get_after_delete_response.status_code, 404)

    # 正向測試: alarm logs acknowledge
    def test_acknowledge_alarm_log(self):
        new_alarm_log = {
            "name": "test_user_ack",
            "s3_object_key": "test_key_ack",
        }
        create_response = requests.post(
            self.alarm_logs_url,
            json=new_alarm_log,
            headers=self.auth_headers,
        )
        self.assertEqual(create_response.status_code, 201)
        alarm_log_id = create_response.json().get("id")
        ack_url = f"{self.alarm_logs_url}acknowledge/{alarm_log_id}/"
        request_data = {"acknowledged": True}
        ack_response = requests.put(ack_url, json=request_data, headers=self.auth_headers)
        self.assertEqual(ack_response.status_code, 200)
        delete_response = requests.delete(f"{self.alarm_logs_url}{alarm_log_id}/", headers=self.auth_headers)
        self.assertEqual(delete_response.status_code, 204)

    # 反向測試: alarm logs acknowledge 不存在的 id
    def test_acknowledge_alarm_log_invalid_id(self):
        invalid_id = 99999
        ack_url = f"{self.alarm_logs_url}acknowledge/{invalid_id}/"
        request_data = {"acknowledged": True}
        ack_response = requests.put(ack_url, json=request_data, headers=self.auth_headers)
        self.assertEqual(ack_response.status_code, 404)

    # 反向測試: alarm logs acknowledge 無效的資料
    def test_acknowledge_alarm_log_invalid_data(self):
        new_alarm_log = {
            "name": "test_user_invalid_data",
            "s3_object_key": "test_key_invalid_data",
        }
        create_response = requests.post(
            self.alarm_logs_url,
            json=new_alarm_log,
            headers=self.auth_headers,
        )
        self.assertEqual(create_response.status_code, 201)
        alarm_log_id = create_response.json().get("id")
        ack_url = f"{self.alarm_logs_url}acknowledge/{alarm_log_id}/"
        request_data = {"acknowledged": "not_a_boolean"}
        ack_response = requests.put(ack_url, json=request_data, headers=self.auth_headers)
        self.assertEqual(ack_response.status_code, 400)
        delete_response = requests.delete(f"{self.alarm_logs_url}{alarm_log_id}/", headers=self.auth_headers)
        self.assertEqual(delete_response.status_code, 204)

    # 反向測試: 創建 alarm log 缺少必要欄位
    def test_create_alarm_log_missing_fields(self):
        incomplete_alarm_log = {}
        create_response = requests.post(
            self.alarm_logs_url,
            json=incomplete_alarm_log,
            headers=self.auth_headers,
        )
        self.assertEqual(create_response.status_code, 400)

    # Monkey Test: 傳入超長字串
    def test_create_alarm_log_with_long_strings(self):
        long_string = "".join(random.choices(string.ascii_letters + string.digits, k=5000))
        payload = {
            "name": long_string,
            "s3_object_key": long_string,
        }
        response = requests.post(self.alarm_logs_url, json=payload, headers=self.auth_headers)
        self.assertIn(response.status_code, [400, 413])

    # Monkey Test: 傳入隨機亂數/特殊字元
    def test_create_alarm_log_with_random_garbage(self):
        garbage_data = {
            "name": "".join(chr(random.randint(0, 255)) for _ in range(50)),
            "s3_object_key": "".join(chr(random.randint(0, 255)) for _ in range(50)),
        }
        response = requests.post(self.alarm_logs_url, json=garbage_data, headers=self.auth_headers)
        self.assertIn(response.status_code, [400, 201])

    # Monkey Test: 隨機呼叫不存在的 endpoint
    def test_random_invalid_endpoints(self):
        random_url = self.alarm_logs_url + "".join(random.choices(string.ascii_lowercase, k=10)) + "/"
        response = requests.get(random_url, headers=self.auth_headers)
        self.assertEqual(response.status_code, 404)
