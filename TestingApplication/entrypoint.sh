#!/bin/bash
# entrypoint.sh

# Выполнение миграций
python TestingApplication/manage.py migrate

# Создание суперпользователя с предопределенными данными
python TestingApplication/manage.py create_superuser


python TestingApplication/manage.py runserver 0.0.0.0:8000


