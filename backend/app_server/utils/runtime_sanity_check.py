import requests
from django.conf import settings
from django.db import connections
from minio import Minio


def check_services():
    # DB
    try:
        connections["default"].cursor()
    except Exception as e:
        raise RuntimeError(f"Database connection failed: {e}")

    # MinIO
    try:
        client = Minio(
            settings.MINIOS3["endpoint"],
            access_key=settings.MINIOS3["access_key"],
            secret_key=settings.MINIOS3["secret_key"],
            secure=settings.MINIO["enable_ssl"],
        )
        client.list_buckets()
    except Exception as e:
        raise RuntimeError(f"MinIO connection failed: {e}")

    # Microservice
    try:
        resp = requests.get(settings.MICROSERVICE["endpoint"] + "/health", timeout=5)
        resp.raise_for_status()
    except Exception as e:
        raise RuntimeError(f"Microservice health check failed: {e}")
