# Используем официальный образ Python как базовый
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY TestingApplication/requirements.txt /app/
COPY TestingApplication/entrypoint.sh /app/
COPY TestingApplication/create_superuser.py /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY TestingApplication/ /app/

# Даем права на выполнение скриптов
RUN chmod +x /app/entrypoint.sh

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

# Устанавливаем команду для запуска контейнера
ENTRYPOINT ["/app/TestingApplication/entrypoint.sh"]