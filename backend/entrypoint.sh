#!/bin/bash
set -e

echo "Postgres is up! Running migrations and initial setup..."

uv run python3 manage.py migrate
uv run python3 manage.py create_apps
uv run python3 manage.py create_user
uv run python3 manage.py create_retention
uv run python3 manage.py create_default_config
uv run python3 manage.py create_minio_buckets

exec "$@"
