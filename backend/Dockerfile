FROM python:3.11-slim-bookworm

# Use the official uv image to quickly build the environment
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /backend

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
  netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock* ./

RUN uv sync --locked

COPY backend ./
COPY backend/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["uv", "run", "uvicorn", "app_server.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
