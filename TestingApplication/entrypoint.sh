#!/bin/bash
# entrypoint.sh

# Выполнение миграций
python manage.py migrate

# Создание суперпользователя с предопределенными данными
python manage.py create_superuser

# Запуск приложения
exec gunicorn TestingApplication.wsgi:application --bind localhost:8000