import datetime
import mimetypes
import os
import ssl
from io import BytesIO

import urllib3
from django.conf import settings
from minio import Minio, error
from urllib3.util.timeout import Timeout

TIMEOUT_CONFIG = Timeout(
    connect=settings.MINIO.get("CONNECT_TIMEOUT", 1.0),
    read=settings.MINIO.get("READ_TIMEOUT", 3.0),
    total=settings.MINIO.get("TOTAL_TIMEOUT", 3.0),
)

POOL_KWARGS = {
    "timeout": TIMEOUT_CONFIG,
    "retries": urllib3.Retry(
        total=settings.MINIO.get("MAX_RETRIES", 1),
        backoff_factor=settings.MINIO.get("BACKOFF_FACTOR", 0.3),
        status_forcelist=[500, 502, 503, 504],
    ),
    "maxsize": settings.MINIO.get("POOL_MAXSIZE", 10),
    "block": settings.MINIO.get("POOL_BLOCK", False),
}


class MinioClient:
    _client = None

    @classmethod
    def get_client(cls):
        """Get MinIO client instance with timeout configuration."""
        try:
            if not cls._client:
                if settings.MINIO["ENABLE_SSL"]:
                    context = ssl.create_default_context(cafile=settings.MINIO["CA_PATH"])
                    context.check_hostname = False
                    POOL_KWARGS["ssl_context"] = context
                    http_client = urllib3.PoolManager(**POOL_KWARGS)
                    cls._client = Minio(
                        endpoint=settings.MINIO["ENDPOINT"],
                        access_key=settings.MINIO["ACCESS_KEY"],
                        secret_key=settings.MINIO["SECRET_KEY"],
                        secure=True,
                        http_client=http_client,
                    )
                else:
                    http_client = urllib3.PoolManager(**POOL_KWARGS)
                    cls._client = Minio(
                        endpoint=settings.MINIO["ENDPOINT"],
                        access_key=settings.MINIO["ACCESS_KEY"],
                        secret_key=settings.MINIO["SECRET_KEY"],
                        secure=False,
                        http_client=http_client,
                    )
        except error.S3Error as e:
            return {"status": False, "error": str(e)}

        return cls._client

    @classmethod
    def create_bucket(cls, bucket_name: str) -> tuple[bool, str]:
        """Create a bucket."""
        try:
            client = cls.get_client()
            if not client.bucket_exists(bucket_name):
                client.make_bucket(bucket_name)
                return True, f"Bucket '{bucket_name}' created successfully."
            else:
                return False, f"Bucket '{bucket_name}' already exists."
        except error.S3Error as e:
            return False, {"status": False, "error": str(e)}

    @classmethod
    def upload_object(
        cls, bucket_name: str, absolute_path_or_binary: str, saved_object_name: str, is_binary: bool = False
    ) -> tuple[bool, dict]:
        """
        If `is_content` is True, pass the binary content of the file.
        """
        try:
            client = cls.get_client()
            if is_binary:
                try:
                    mime_type = mimetypes.guess_type(saved_object_name)[0]
                    if mime_type is None:
                        mime_type = "application/octet-stream"
                    file_size = len(absolute_path_or_binary)
                    file_data_io = BytesIO(absolute_path_or_binary)
                    client.put_object(
                        bucket_name,
                        saved_object_name,
                        file_data_io,
                        length=file_size,
                        content_type=mime_type,
                    )
                except Exception as e:
                    return False, {"status": False, "error": str(e)}

            if not is_binary and os.path.exists(absolute_path_or_binary):
                mime_type, _ = mimetypes.guess_type(absolute_path_or_binary)
                if mime_type is None:
                    mime_type = "application/octet-stream"
                try:
                    with open(absolute_path_or_binary, "rb") as file_data:
                        file_size = os.path.getsize(absolute_path_or_binary)
                        client.put_object(
                            bucket_name,
                            saved_object_name,
                            file_data,
                            length=file_size,
                            content_type=mime_type,
                        )
                except FileNotFoundError:
                    return False, {"status": False, "error": f"File '{absolute_path_or_binary}' not found."}

            return True, {"status": True, "object_name": saved_object_name, "bucket_name": bucket_name}
        except error.S3Error as e:
            return False, {"status": False, "error": str(e)}

    @classmethod
    def get_object_url(cls, bucket_name: str, object_name: str, expires_in_sec: int = 300) -> tuple[bool, dict]:
        """Get a pre-signed URL for a file."""
        try:
            client = cls.get_client()
            client.stat_object(bucket_name, object_name)
            url = client.presigned_get_object(
                bucket_name,
                object_name,
                expires=datetime.timedelta(seconds=expires_in_sec),
                response_headers={"response-cache-control": f"max-age={expires_in_sec}, public"},
            )
            return True, {"status": True, "url": url}
        except error.S3Error as e:
            return False, {"status": False, "error": str(e)}

    @classmethod
    def download_object(cls, bucket_name: str, object_name: str, download_path: str) -> tuple[bool, dict]:
        """Download a file from MinIO."""
        try:
            client = cls.get_client()
            response = client.get_object(bucket_name, object_name)
            with open(download_path, "wb") as file_data:
                for d in response.stream(64 * 1024):
                    file_data.write(d)
            response.close()
            response.release_conn()
            return True, {"status": True, "object_name": object_name, "download_path": download_path}
        except error.S3Error as e:
            return False, {"status": False, "error": str(e)}

    @classmethod
    def delete_object(cls, bucket_name: str, object_name: str) -> tuple[bool, dict]:
        """Delete a file from MinIO."""
        try:
            client = cls.get_client()
            client.remove_object(bucket_name, object_name)
            return True, {"status": True, "object_name": object_name}
        except error.S3Error as e:
            return False, {"status": False, "error": str(e)}


# if __name__ == "__main__":
# Example usage
# absolute_path = "/Users/xiu/Desktop/side-project/FaceRecoSystem/backend/cat.jpg"
# print("1. ", MinioClient.upload_object("accounts", absolute_path, "cat.jpg"))
# print("2. ", MinioClient.get_object_url("accounts", "cat.jpg", expires_in_sec=300))
# binary_image = ""
# with open("../cat.jpg", "rb") as f:
#     content = f.read()
#     binary_image = content
# print("1. ", MinioClient.upload_object("accounts", binary_image, "cat1.jpg", is_binary=True))
# print("2. ", MinioClient.get_object_url("accounts", "cat1.jpg", expires_in_sec=300))
