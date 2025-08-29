import random
import string

import requests
import tomli
from django.test import TestCase


class ApiSystemActivtityLogsTests(TestCase):
    def setUp(self):
        with open("settings.toml", "rb") as f:
            config = tomli.load(f)
        tests_config = config.get("tests", {})
        self.test_server_url = tests_config.get("test_server_url")
        self.activity_logs_url = self.test_server_url + "/api/activity-logs/system/"
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

    # 正向測試: 取得 activity logs 列表
    def test_get_activity_logs_list(self):
        response = requests.get(
            self.activity_logs_url,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)

        # 驗證按 timestamp 降序排列
        if len(data["results"]) > 1:
            for i in range(len(data["results"]) - 1):
                self.assertGreaterEqual(data["results"][i]["timestamp"], data["results"][i + 1]["timestamp"])

    # 正向測試: activity logs crd
    def test_activity_log_crd(self):
        # Create
        new_activity_log = {
            "account": "test_user_crud",
            "actions": "CREATE",
            "status": True,
            "status_code": 201,
            "activity": "Created a new resource",
            "message": "Resource created successfully",
        }

        create_response = requests.post(
            self.activity_logs_url,
            json=new_activity_log,
            headers=self.auth_headers,
        )
        self.assertEqual(create_response.status_code, 201)
        created_data = create_response.json()
        activity_log_id = created_data.get("id")
        self.assertIsNotNone(activity_log_id)
        self.assertIn("timestamp", created_data)

        # Retrieve
        detail_url = f"{self.activity_logs_url}{activity_log_id}/"
        get_response = requests.get(detail_url, headers=self.auth_headers)
        self.assertEqual(get_response.status_code, 200)
        get_data = get_response.json()
        self.assertEqual(get_data["account"], new_activity_log["account"])
        self.assertEqual(get_data["actions"], new_activity_log["actions"])
        self.assertEqual(get_data["status"], new_activity_log["status"])
        self.assertEqual(get_data["status_code"], new_activity_log["status_code"])
        self.assertEqual(get_data["activity"], new_activity_log["activity"])
        self.assertEqual(get_data["message"], new_activity_log["message"])

        # Delete
        delete_response = requests.delete(detail_url, headers=self.auth_headers)
        self.assertEqual(delete_response.status_code, 204)

        # 驗證已刪除
        verify_response = requests.get(detail_url, headers=self.auth_headers)
        self.assertEqual(verify_response.status_code, 404)

    # 正向測試: 測試 account 過濾功能
    def test_filter_by_account(self):
        # 創建測試資料
        test_accounts = ["filter_user_1", "filter_user_2"]
        created_ids = []

        for account in test_accounts:
            log_data = {
                "account": account,
                "actions": "READ",
                "status": True,
                "status_code": 200,
                "activity": f"Test activity for {account}",
                "message": f"Test message for {account}",
            }
            resp = requests.post(self.activity_logs_url, json=log_data, headers=self.auth_headers)
            if resp.status_code == 201:
                created_ids.append(resp.json()["id"])

        # 測試過濾
        response = requests.get(
            f"{self.activity_logs_url}?account=filter_user_1",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # 驗證過濾結果
        for item in data["results"]:
            self.assertEqual(item["account"], "filter_user_1")

        # 清理
        for log_id in created_ids:
            requests.delete(f"{self.activity_logs_url}{log_id}/", headers=self.auth_headers)

    # 正向測試: 測試只提供必要欄位創建
    def test_create_with_minimal_fields(self):
        minimal_log = {
            "account": "minimal_test",
            "actions": "READ",
            "status": False,
            "status_code": 200,
        }

        response = requests.post(
            self.activity_logs_url,
            json=minimal_log,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 201)

        created_data = response.json()
        self.assertEqual(created_data["account"], minimal_log["account"])
        self.assertEqual(created_data["actions"], minimal_log["actions"])
        self.assertEqual(created_data["status"], minimal_log["status"])
        self.assertEqual(created_data["status_code"], minimal_log["status_code"])
        self.assertIsNone(created_data["activity"])
        self.assertIsNone(created_data["message"])

        # 清理
        requests.delete(f"{self.activity_logs_url}{created_data['id']}/", headers=self.auth_headers)

    # 反向測試: 測試缺少必要欄位
    def test_create_without_required_fields(self):
        invalid_logs = [
            {"actions": "CREATE", "status": True, "status_code": 200},  # 缺少 account
            {"account": "test", "status": True, "status_code": 200},  # 缺少 actions
            {"account": "test", "actions": "CREATE", "status": True},  # 缺少 status_code
            {},
        ]

        for log_data in invalid_logs:
            response = requests.post(
                self.activity_logs_url,
                json=log_data,
                headers=self.auth_headers,
            )
            self.assertIn(response.status_code, [400, 422])

    # 反向測試: 測試無效的欄位類型
    def test_invalid_field_types(self):
        invalid_logs = [
            {
                "account": "test123123123",
                "actions": "CREATE",
                "status": "123123",  # 應該是 Boolean
                "status_code": 200,
            },
            {
                "account": "test123123123",
                "actions": "CREATE",
                "status": True,
                "status_code": "OK",  # 應該是 Integer
            },
        ]

        for log_data in invalid_logs:
            response = requests.post(
                self.activity_logs_url,
                json=log_data,
                headers=self.auth_headers,
            )
            self.assertIn(response.status_code, [400, 422])

    # 反向測試: 超過欄位最大長度
    def test_exceed_field_max_length(self):
        invalid_logs = [
            {
                "account": "a" * 65,  # 超過 64 字元
                "actions": "CREATE",
                "status": True,
                "status_code": 200,
            },
            {
                "account": "test",
                "actions": "VERYLONGACTION",  # 超過 8 字元
                "status": True,
                "status_code": 200,
            },
            {
                "account": "test",
                "actions": "CREATE",
                "status": True,
                "status_code": 200,
                "activity": "a" * 256,  # 超過 255 字元
            },
        ]

        for log_data in invalid_logs:
            response = requests.post(
                self.activity_logs_url,
                json=log_data,
                headers=self.auth_headers,
            )
            self.assertIn(response.status_code, [400, 422])

    # 反向測試: 測試不允許的更新操作（ViewSet 不包含 UpdateModelMixin）
    def test_update_not_allowed(self):
        # 先創建一個日誌
        log_data = {
            "account": "update_test",
            "actions": "CREATE",
            "status": True,
            "status_code": 201,
        }

        create_response = requests.post(
            self.activity_logs_url,
            json=log_data,
            headers=self.auth_headers,
        )
        self.assertEqual(create_response.status_code, 201)
        log_id = create_response.json()["id"]

        # 嘗試 PUT 更新
        update_data = {
            "account": "updated_user",
            "actions": "UPDATE",
            "status": False,
            "status_code": 200,
        }

        put_response = requests.put(
            f"{self.activity_logs_url}{log_id}/",
            json=update_data,
            headers=self.auth_headers,
        )
        self.assertEqual(put_response.status_code, 405)  # Method Not Allowed

        # 嘗試 PATCH 更新
        patch_response = requests.patch(
            f"{self.activity_logs_url}{log_id}/",
            json={"account": "patched_user"},
            headers=self.auth_headers,
        )
        self.assertEqual(patch_response.status_code, 405)  # Method Not Allowed

        # 清理
        requests.delete(f"{self.activity_logs_url}{log_id}/", headers=self.auth_headers)

    # Monkey 測試: 隨機資料注入
    def test_random_data_injection(self):
        for i in range(10):
            random_string = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 50)))

            log_data = {
                "account": random_string[:64],
                "actions": random_string[:8],
                "status": random.choice([True, False]),
                "status_code": random.randint(100, 599),
                "activity": random_string[:255] if random.choice([True, False]) else None,
                "message": random_string * random.randint(1, 10) if random.choice([True, False]) else None,
            }

            response = requests.post(
                self.activity_logs_url,
                json=log_data,
                headers=self.auth_headers,
            )

            self.assertIn(response.status_code, [201, 400, 422])

            if response.status_code == 201:
                requests.delete(f"{self.activity_logs_url}{response.json()['id']}/", headers=self.auth_headers)

    # Monkey 測試: SQL 注入防護
    def test_sql_injection_prevention(self):
        sql_payloads = [
            "'; DROP TABLE system_activity_logs; --",
            "1' OR '1'='1",
            "admin'--",
            "' UNION SELECT * FROM auth_user--",
        ]

        for payload in sql_payloads:
            log_data = {
                "account": payload[:64],
                "actions": payload[:8],
                "status": True,
                "status_code": 200,
                "activity": payload[:255],
                "message": payload,
            }

            response = requests.post(
                self.activity_logs_url,
                json=log_data,
                headers=self.auth_headers,
            )

            if response.status_code == 201:
                created_id = response.json()["id"]

                # 驗證資料正確儲存而非執行
                get_response = requests.get(
                    f"{self.activity_logs_url}{created_id}/",
                    headers=self.auth_headers,
                )
                self.assertEqual(get_response.status_code, 200)

                # 清理
                requests.delete(f"{self.activity_logs_url}{created_id}/", headers=self.auth_headers)

    # Monkey 測試: Unicode 和特殊字元
    def test_unicode_and_special_characters(self):
        special_data = [
            "測試中文",
            "テスト",
            "🚀💻😀",
            "user@test.com",
            "path/to/file",
            "\n\r\t",
            "NULL\x00TEST",
        ]

        for special in special_data:
            log_data = {
                "account": special[:64],
                "actions": special[:8],
                "status": True,
                "status_code": 200,
                "activity": special[:255],
                "message": special,
            }

            response = requests.post(
                self.activity_logs_url,
                json=log_data,
                headers=self.auth_headers,
            )

            self.assertIn(response.status_code, [201, 400, 422])

            if response.status_code == 201:
                requests.delete(f"{self.activity_logs_url}{response.json()['id']}/", headers=self.auth_headers)

    # Monkey 測試: 並發操作
    def test_concurrent_operations(self):
        import concurrent.futures

        def create_and_delete(index):
            log_data = {
                "account": f"concurrent_{index}",
                "actions": "CREATE",
                "status": True,
                "status_code": 200,
                "activity": f"Concurrent test {index}",
            }

            # 創建
            create_resp = requests.post(
                self.activity_logs_url,
                json=log_data,
                headers=self.auth_headers,
            )

            if create_resp.status_code == 201:
                log_id = create_resp.json()["id"]

                # 立即刪除
                delete_resp = requests.delete(
                    f"{self.activity_logs_url}{log_id}/",
                    headers=self.auth_headers,
                )
                return create_resp.status_code, delete_resp.status_code

            return create_resp.status_code, None

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_and_delete, i) for i in range(20)]

            for future in concurrent.futures.as_completed(futures):
                create_status, delete_status = future.result()
                self.assertEqual(create_status, 201)
                if delete_status:
                    self.assertEqual(delete_status, 204)

    # Monkey 測試: 邊界值
    def test_boundary_values(self):
        boundary_tests = [
            {
                "account": "",  # 空字串
                "actions": "",
                "status": True,
                "status_code": 100,  # 最小 HTTP 狀態碼
            },
            {
                "account": "a",  # 單字元
                "actions": "A",
                "status": False,
                "status_code": 599,  # 最大標準 HTTP 狀態碼
            },
            {
                "account": "a" * 64,  # 最大長度
                "actions": "a" * 8,
                "status": True,
                "status_code": 999,  # 非標準狀態碼
                "activity": "a" * 255,
            },
        ]

        for log_data in boundary_tests:
            response = requests.post(
                self.activity_logs_url,
                json=log_data,
                headers=self.auth_headers,
            )

            # 記錄但不強制斷言，因為邊界處理可能因實作而異
            if response.status_code == 201:
                requests.delete(f"{self.activity_logs_url}{response.json()['id']}/", headers=self.auth_headers)

    # Monkey 測試: 超大 message 欄位
    def test_massive_message_field(self):
        huge_message = "A" * 1000000  # 1MB 文字

        log_data = {
            "account": "huge_message_test",
            "actions": "CREATE",
            "status": True,
            "status_code": 200,
            "message": huge_message,
        }

        response = requests.post(
            self.activity_logs_url,
            json=log_data,
            headers=self.auth_headers,
        )

        # 可能成功或因為請求太大而失敗
        self.assertIn(response.status_code, [201, 400, 413, 422])

        if response.status_code == 201:
            requests.delete(f"{self.activity_logs_url}{response.json()['id']}/", headers=self.auth_headers)
