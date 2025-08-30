#!/bin/bash
set -e

# 最大等待時間 (秒)
TIMEOUT=30
SLEEP_INTERVAL=1
ELAPSED=0

echo "Waiting for Postgres to be ready..."

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
    sleep $SLEEP_INTERVAL
    ELAPSED=$((ELAPSED + SLEEP_INTERVAL))
    if [ $ELAPSED -ge $TIMEOUT ]; then
        echo "Timeout waiting for Postgres after $TIMEOUT seconds"
        exit 1
    fi
done

echo "Postgres is up! Running migrations and initial setup..."

# 執行 Django 初始化指令
uv run python3 manage.py migrate
uv run python3 manage.py create_apps
uv run python3 manage.py create_user
uv run python3 manage.py create_retention
uv run python3 manage.py create_default_config
uv run python3 manage.py create_minio_buckets

exec "$@"
