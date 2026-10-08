#!/bin/sh

set -e

KEYS_DIR="/app/keys"

mkdir -p "$KEYS_DIR"

if [ ! -f "$KEYS_DIR/private.pem" ]; then
    openssl genrsa -out "$KEYS_DIR/private.pem" 2048
    chmod 600 "$KEYS_DIR/private.pem"
fi

if [ ! -f "$KEYS_DIR/public.pem" ]; then
    openssl rsa \
        -in "$KEYS_DIR/private.pem" \
        -pubout \
        -out "$KEYS_DIR/public.pem"

    chmod 644 "$KEYS_DIR/public.pem"
fi

uv run alembic upgrade head

exec uv run --no-dev uvicorn main:app --host 0.0.0.0 --port 8000
