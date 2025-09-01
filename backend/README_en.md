# Face Recognition System (Backend)

Readme Languages: <a href="./README.md">English 🇺🇸</a> / <a href="./README_zh-tw.md">繁體中文版 🇹🇼</a>


## Install the development environment

Before getting started, please install Python 3.10 and the uv package management tool and docker environment.

#### Install uv environment tools

Install uv (You can refer to [GitHub: astral/uv](https://github.com/astral-sh/uv))
```
pip install uv
```

Though uv and pyproject to build virtual environment
```
uv sync
```

#### Startup PostgreSQ、MinIO S3 and Redis

#### MinIO S3

Pull Minio S3 image

```bash
docker pull quay.io/minio/minio:RELEASE.2025-07-23T15-54-02Z
```

Create a MinIO S3 local static directory

```bash
mkdir ./docker-volumes/minio
```

Startup MinIO S3

```bash
docker run -d \
  --name facereco-minio \
  --restart always \
  -p 9000:9000 \
  -p 9001:9001 \
  -v $(pwd)/docker-volumes/minio/certs:/root/.minio/certs:ro \
  -v $(pwd)/docker-volumes/minio/cors.json:/root/.minio/config/cors.json \
  -v $(pwd)/docker-volumes/minio:/data \
  --network server_network \
  -e MINIO_ROOT_USER=<SET_USER_ACCOUNT> \
  -e MINIO_ROOT_PASSWORD=<SET_USER_PASSWORD> \
  -e MINIO_SERVER_URL="http://127.0.0.1:9000" \
  -e MINIO_BROWSER_REDIRECT_URL="http://127.0.0.1:9001" \
  quay.io/minio/minio server /data --console-address ":9001"
```

#### MinIO Web UI

If successful startup, you can access MinIO S3 Web through `MINIO_BROWSER_REDIRECT_URL` and log in through the configured `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD`.

![Images](../assets/backend/minios3.png)


#### PostgreSQL

Pull PostgreSQL image

```bash
sudo docker pull postgres:16
```

Create a Postgres local static directory

```bash
mkdir ./docker-volumes/postgres
```

Startup PostgreSQL

```bash
docker run -d \
  --name facereco-postgres \
  --restart always \
  --network server_network \
  -e POSTGRES_USER=<SET_USER_ACCOUNT> \
  -e POSTGRES_PASSWORD=<SET_USER_PASSWORD> \
  -e POSTGRES_DB=facereco \
  -p 5432:5432 \
  -v $(pwd)/docker-volumes/postgre:/var/lib/postgresql/data \
  postgres:16
```

#### Redis

Pull redis image

```bash
pull redis:8.0.3
```

Create a Redis local static directory

```bash
./docker-volumes/redis
```

Startup Redis

```bash
docker run -d \
  --name facereco-redis \
  --restart always \
  -p 6379:6379 \
  --network server_network \
  -v $(pwd)//docker-volumes/redis:/data \
  redis:8.0.3 \
  redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
```

#### Backend configurations

Go to the ./backend directory, edit the `settings.toml` configuration file, and set the parameters according to the MinIO and Postgres startup details.

```toml
[postgres]
host= PostgreSQL IP
port = PostgreSQL Port
name = DB Name
user = user name
password = user password

[minios3]
enable_ssl = Enable SSL (SSL is not currently supported)
ca_path = CA Path
endpoint = MiniO S3 endpoint (IP:PORT)
external_endpoint = External endpoint (Used when deploying nginx, development mode is set to "")
access_key = user account
secret_key = user password
connect_timeout = Try to connect timeout (sec.)
read_timeout = S3 wait time for response (sec.)
total_timeout = Overall waiting time (including connection, request, and response)
max_retries = Number of failed reconnections (sec.)
backoff_factor = Retry interval (sec.)
pool_maxsize = Maximum number of connections
pool_block = Behavior when the connection pool is full (True: waiting / False: return fail)

[microservice]
endpoint = microservice endpoint
internal_token = Manually generated internal token

[tests]
test_server_url = server endpoint

[celery]
broker = redis broker endpoint
```

#### Startup Django

Database migration and initialization settings

```bash
uv run python3 manage.py create_apps
uv run python3 manage.py create_user
uv run python3 manage.py create_retention
uv run python3 manage.py create_default_config
uv run python3 manage.py create_minio_buckets
```

Startup Django server

```bash
uv run uvicorn app_server.asgi:application --host 0.0.0.0 --port 8000 --reload
```

#### Startup Celery

- Flower：
```bash
uv run celery -A app_server flower --port=5555
```

- Celery beat:
```bash
uv run celery -A app_server beat --loglevel=info
```

- Celery worker:
```bash
uv run celery -A app_server worker --loglevel=info
```

## Run Tests

Set tests.test_server_url in `settings.toml` to localhost:8000 or YOUR_IP:8000

```bash
uv run python3 run_test.py
```
