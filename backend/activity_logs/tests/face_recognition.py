import concurrent.futures
import random
import string
import time

import requests
import tomli
from django.test import TestCase


class ApiFaceRecognitionActivityLogsTests(TestCase):
    def setUp(self):
        with open("settings.toml", "rb") as f:
            config = tomli.load(f)
        tests_config = config.get("tests", {})
        self.test_server_url = tests_config.get("test_server_url")
        self.activity_logs_url = self.test_server_url + "/api/activity-logs/face-recognition/"
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

    # 正向測試: activity log crd
    def test_activity_log_crd(self):
        new_activity_log = {
            "name": "test_user_crud",
            "group": "test_group",
            "s3_object_key": "test_key/image.jpg",
            "detection_results": True,
        }

        # Create
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
        self.assertEqual(get_data["name"], new_activity_log["name"])
        self.assertEqual(get_data["group"], new_activity_log["group"])
        self.assertEqual(get_data["s3_object_key"], new_activity_log["s3_object_key"])
        self.assertEqual(get_data["detection_results"], new_activity_log["detection_results"])

        # Delete
        delete_response = requests.delete(detail_url, headers=self.auth_headers)
        self.assertEqual(delete_response.status_code, 204)

        # Verify deletion
        get_response_after_delete = requests.get(detail_url, headers=self.auth_headers)
        self.assertEqual(get_response_after_delete.status_code, 404)

    # 正向測試: 取得列表包含 MinIO URLs、過濾、排序等
    def test_list_with_minio_urls(self):
        # 創建測試資料
        test_log = {
            "name": "minio_test_user",
            "group": "minio_group",
            "s3_object_key": "test/minio_image.jpg",
            "detection_results": True,
        }

        create_resp = requests.post(
            self.activity_logs_url,
            json=test_log,
            headers=self.auth_headers,
        )
        self.assertEqual(create_resp.status_code, 201)
        log_id = create_resp.json()["id"]

        # 取得列表
        list_response = requests.get(
            self.activity_logs_url,
            headers=self.auth_headers,
        )
        self.assertEqual(list_response.status_code, 200)
        data = list_response.json()

        # 檢查是否包含 minio_urls（如果 MinIO 服務可用）
        for item in data["results"]:
            if item["s3_object_key"] == "test/minio_image.jpg":
                # minio_urls 可能存在或不存在，取決於 MinIO 服務
                if "minio_urls" in item:
                    self.assertIsInstance(item["minio_urls"], str)

        # 清理
        requests.delete(f"{self.activity_logs_url}{log_id}/", headers=self.auth_headers)

    # 正向測試: name 過濾
    def test_filter_by_name(self):
        test_names = ["filter_user_1", "filter_user_2", "another_user"]
        created_ids = []

        for name in test_names:
            log_data = {
                "name": name,
                "group": "test_group",
                "detection_results": True,
            }
            resp = requests.post(self.activity_logs_url, json=log_data, headers=self.auth_headers)
            if resp.status_code == 201:
                created_ids.append(resp.json()["id"])

        # 測試過濾
        response = requests.get(
            f"{self.activity_logs_url}?name=filter_user_1",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # 驗證過濾結果
        for item in data["results"]:
            self.assertEqual(item["name"], "filter_user_1")

        # 清理
        for log_id in created_ids:
            requests.delete(f"{self.activity_logs_url}{log_id}/", headers=self.auth_headers)

    # 正向測試: group 過濾
    def test_filter_by_group(self):
        test_groups = ["group_a", "group_b", None]
        created_ids = []

        for i, group in enumerate(test_groups):
            log_data = {
                "name": f"group_test_user_{i}",
                "detection_results": False,
            }
            if group:
                log_data["group"] = group

            resp = requests.post(self.activity_logs_url, json=log_data, headers=self.auth_headers)
            if resp.status_code == 201:
                created_ids.append(resp.json()["id"])

        # 測試過濾特定 group
        response = requests.get(
            f"{self.activity_logs_url}?group=group_a",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        for item in data["results"]:
            self.assertEqual(item["group"], "group_a")

        # 清理
        for log_id in created_ids:
            requests.delete(f"{self.activity_logs_url}{log_id}/", headers=self.auth_headers)

    # 正向測試: 建立只含必要欄位的日誌
    def test_create_with_minimal_fields(self):
        minimal_log = {
            "name": "minimal_test",
            "detection_results": False,
        }

        response = requests.post(
            self.activity_logs_url,
            json=minimal_log,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 201)

        created_data = response.json()
        self.assertEqual(created_data["name"], minimal_log["name"])
        self.assertEqual(created_data["detection_results"], minimal_log["detection_results"])
        self.assertIsNone(created_data["group"])
        self.assertIsNone(created_data["s3_object_key"])

        # 清理
        requests.delete(f"{self.activity_logs_url}{created_data['id']}/", headers=self.auth_headers)

    # 正向測試: 按 timestamp 排序
    def test_ordering_by_timestamp(self):
        # 創建多筆資料
        created_ids = []
        for i in range(3):
            log_data = {
                "name": f"order_test_{i}",
                "detection_results": True,
            }
            resp = requests.post(self.activity_logs_url, json=log_data, headers=self.auth_headers)
            if resp.status_code == 201:
                created_ids.append(resp.json()["id"])
            time.sleep(0.1)  # 確保時間戳不同

        # 取得列表
        response = requests.get(self.activity_logs_url, headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # 驗證降序排列
        timestamps = []
        for item in data["results"]:
            if item["name"].startswith("order_test_"):
                timestamps.append(item["timestamp"])

        for i in range(len(timestamps) - 1):
            self.assertGreaterEqual(timestamps[i], timestamps[i + 1])

        # 清理
        for log_id in created_ids:
            requests.delete(f"{self.activity_logs_url}{log_id}/", headers=self.auth_headers)

    # 正向測試: 建立無效資料
    def test_create_without_required_fields(self):
        invalid_logs = [
            {"detection_results": True},  # 缺少 name
            {"name": "test"},  # 缺少 detection_results（可能有預設值）
            {},  # 完全空白
        ]

        for log_data in invalid_logs:
            response = requests.post(
                self.activity_logs_url,
                json=log_data,
                headers=self.auth_headers,
            )
            # name 是必要欄位，detection_results 有預設值
            if "name" not in log_data:
                self.assertIn(response.status_code, [400, 422])

    # 反向測試: 超過欄位最大長度
    def test_exceed_field_max_length(self):
        invalid_logs = [
            {
                "name": "a" * 65,  # 超過 64 字元
                "detection_results": True,
            },
            {
                "name": "test",
                "group": "b" * 65,  # 超過 64 字元
                "detection_results": True,
            },
            {
                "name": "test",
                "s3_object_key": "c" * 129,  # 超過 128 字元
                "detection_results": True,
            },
        ]

        for log_data in invalid_logs:
            response = requests.post(
                self.activity_logs_url,
                json=log_data,
                headers=self.auth_headers,
            )
            self.assertIn(response.status_code, [400, 422])

    # 反向測試: 獲取不存在的日誌
    def test_get_nonexistent_log(self):
        response = requests.get(
            f"{self.activity_logs_url}999999999/",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 404)

    # 反向測試: 刪除不存在的日誌
    def test_delete_nonexistent_log(self):
        response = requests.delete(
            f"{self.activity_logs_url}999999999/",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 404)

    # 反向測試: 不允許的更新操作
    def test_update_not_allowed(self):
        # 先創建一個日誌
        log_data = {
            "name": "update_test",
            "detection_results": True,
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
            "name": "updated_name",
            "detection_results": False,
        }

        put_response = requests.put(
            f"{self.activity_logs_url}{log_id}/",
            json=update_data,
            headers=self.auth_headers,
        )
        self.assertEqual(put_response.status_code, 405)

        # 嘗試 PATCH 更新
        patch_response = requests.patch(
            f"{self.activity_logs_url}{log_id}/",
            json={"name": "patched_name"},
            headers=self.auth_headers,
        )
        self.assertEqual(patch_response.status_code, 405)

        # 清理
        requests.delete(f"{self.activity_logs_url}{log_id}/", headers=self.auth_headers)

    # 反向測試: 非法字元注入
    def test_random_data_injection(self):
        for _ in range(10):
            random_string = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 50)))

            log_data = {
                "name": random_string[:64],
                "group": random_string[:64] if random.choice([True, False]) else None,
                "s3_object_key": f"{random_string[:50]}/{random_string[:50]}.jpg"
                if random.choice([True, False])
                else None,
                "detection_results": random.choice([True, False]),
            }

            response = requests.post(
                self.activity_logs_url,
                json=log_data,
                headers=self.auth_headers,
            )

            self.assertIn(response.status_code, [201, 400, 422])

            if response.status_code == 201:
                requests.delete(f"{self.activity_logs_url}{response.json()['id']}/", headers=self.auth_headers)

    # 反向測試: SQL 注入防護
    def test_sql_injection_prevention(self):
        sql_payloads = [
            "'; DROP TABLE face_recognition_activity_logs; --",
            "1' OR '1'='1",
            "admin'--",
            "' UNION SELECT * FROM auth_user--",
        ]

        for payload in sql_payloads:
            log_data = {
                "name": payload[:64],
                "group": payload[:64],
                "s3_object_key": payload[:128],
                "detection_results": True,
            }

            response = requests.post(
                self.activity_logs_url,
                json=log_data,
                headers=self.auth_headers,
            )

            if response.status_code == 201:
                created_id = response.json()["id"]

                # 驗證資料正確儲存
                get_response = requests.get(
                    f"{self.activity_logs_url}{created_id}/",
                    headers=self.auth_headers,
                )
                self.assertEqual(get_response.status_code, 200)

                # 清理
                requests.delete(f"{self.activity_logs_url}{created_id}/", headers=self.auth_headers)

    # 反向測試: 特殊字元處理
    def test_special_characters_handling(self):
        special_data = [
            "測試中文",
            "テスト日本語",
            "🚀💻😀",
            "user@test.com",
            "path/to/file.jpg",
            "key=value&param=test",
            "\n\r\t",
        ]

        for special in special_data:
            log_data = {
                "name": special[:64],
                "group": special[:64],
                "s3_object_key": f"{special[:50]}/image.jpg",
                "detection_results": True,
            }

            response = requests.post(
                self.activity_logs_url,
                json=log_data,
                headers=self.auth_headers,
            )

            self.assertIn(response.status_code, [201, 400, 422])

            if response.status_code == 201:
                requests.delete(f"{self.activity_logs_url}{response.json()['id']}/", headers=self.auth_headers)

    # 反向測試: 並發操作
    def test_concurrent_operations(self):
        def create_and_delete(index):
            log_data = {
                "name": f"concurrent_{index}",
                "group": f"group_{index % 3}",
                "detection_results": index % 2 == 0,
            }

            create_resp = requests.post(
                self.activity_logs_url,
                json=log_data,
                headers=self.auth_headers,
            )

            if create_resp.status_code == 201:
                log_id = create_resp.json()["id"]

                # 獲取
                get_resp = requests.get(
                    f"{self.activity_logs_url}{log_id}/",
                    headers=self.auth_headers,
                )

                # 刪除
                delete_resp = requests.delete(
                    f"{self.activity_logs_url}{log_id}/",
                    headers=self.auth_headers,
                )

                return create_resp.status_code, get_resp.status_code, delete_resp.status_code

            return create_resp.status_code, None, None

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_and_delete, i) for i in range(20)]

            for future in concurrent.futures.as_completed(futures):
                create_status, get_status, delete_status = future.result()
                self.assertEqual(create_status, 201)
                if get_status:
                    self.assertEqual(get_status, 200)
                if delete_status:
                    self.assertEqual(delete_status, 204)

    # 反向測試: 畸形 JSON
    def test_malformed_json(self):
        malformed_payloads = [
            '{"name": "test", "detection_results": }',  # 缺少值
            '{"name": "test" "detection_results": true}',  # 缺少逗號
            '[{"name": "test"}]',  # 陣列而非物件
            "null",
            "true",
        ]

        for payload in malformed_payloads:
            response = requests.post(
                self.activity_logs_url,
                data=payload,
                headers=self.auth_headers,
            )

            self.assertIn(response.status_code, [400, 422])

    # 反向測試: 無效的 S3 object key 格式
    def test_invalid_s3_object_key_format(self):
        invalid_keys = [
            "../../../etc/passwd",  # 路徑遍歷
            "//double/slash",
            "key with spaces.jpg",
            "key\x00with\x00null.jpg",
        ]

        for key in invalid_keys:
            log_data = {
                "name": "s3_key_test",
                "s3_object_key": key[:128],
                "detection_results": True,
            }

            response = requests.post(
                self.activity_logs_url,
                json=log_data,
                headers=self.auth_headers,
            )

            # API 可能接受或拒絕，取決於驗證規則
            if response.status_code == 201:
                requests.delete(f"{self.activity_logs_url}{response.json()['id']}/", headers=self.auth_headers)

    # 邊界測試: 欄位長度邊界值
    def test_boundary_values(self):
        boundary_tests = [
            {
                "name": "",  # 空字串
                "detection_results": True,
            },
            {
                "name": "a",  # 單字元
                "group": "",  # 空 group
                "detection_results": False,
            },
            {
                "name": "a" * 64,  # 最大長度
                "group": "b" * 64,
                "s3_object_key": "c" * 128,
                "detection_results": True,
            },
        ]

        for log_data in boundary_tests:
            response = requests.post(
                self.activity_logs_url,
                json=log_data,
                headers=self.auth_headers,
            )

            if response.status_code == 201:
                requests.delete(f"{self.activity_logs_url}{response.json()['id']}/", headers=self.auth_headers)
