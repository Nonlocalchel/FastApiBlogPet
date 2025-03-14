#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

set -e

echo "Применение миграций..."
poetry run alembic upgrade head

echo "Запуск приложения..."
exec poetry run python main.py && "$@"