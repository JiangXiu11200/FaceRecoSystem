# config.py
import socket
from pathlib import Path

import tomli

# from minio import Minio
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class PostgresConfig(BaseModel):
    name: str
    user: str
    password: str
    host: str
    port: int


class MinioConfig(BaseModel):
    endpoint: str
    access_key: str
    secret_key: str
    connect_timeout: int = 5
    read_timeout: int = 5
    total_timeout: int = 15
    max_retries: int = 3
    backoff_factor: float = 0.5
    pool_maxsize: int = 10
    pool_block: bool = True
    enable_ssl: bool = False


class MicroserviceConfig(BaseModel):
    endpoint: str
    internal_token: str


class Settings(BaseModel):
    postgres: PostgresConfig
    minios3: MinioConfig
    microservice: MicroserviceConfig


def load_settings(path: Path = BASE_DIR / "settings.toml") -> Settings:
    with open(path, "rb") as f:
        config_dict = tomli.load(f)
    return Settings(**config_dict)


def runtime_check(settings: Settings) -> None:
    errors = []

    # Check Postgres connection
    try:
        print("Checking Postgres connection... host:", settings.postgres.host, "port:", settings.postgres.port)
        with socket.create_connection((settings.postgres.host, settings.postgres.port), timeout=3):
            pass
    except Exception as e:
        errors.append(f"Postgres connection failed: {e}")

    # Check MinIO connection
    # try:
    #     print("Checking MinIO connection... endpoint:", settings.minios3.endpoint)
    #     client = Minio(
    #         settings.minios3.endpoint,
    #         access_key=settings.minios3.access_key,
    #         secret_key=settings.minios3.secret_key,
    #         secure=False,
    #     )
    #     client.list_buckets()
    # except Exception as e:
    #     errors.append(f"MinIO endpoint failed: {e}")

    if errors:
        raise RuntimeError("Runtime config checks failed: ", errors)
