#!/bin/sh

echo "waiting for postgres..."

while ! nc -z web-db 5432; do
  sleep 0.1
done

echo "PostgresSQL started"

exec "$@"