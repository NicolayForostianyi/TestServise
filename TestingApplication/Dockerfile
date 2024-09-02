# Используем официальный образ Python как базовый
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app/

ENV PYTHONDONTWRITEBYTECODE 1

# Копируем файлы зависимостей
COPY . /app/
COPY TestingApplication/ /app/
COPY requirements.txt /app/
COPY entrypoint.sh /app/


# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Даем права на выполнение скриптов
RUN chmod +x /app/entrypoint.sh

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

# Устанавливаем команду для запуска контейнера
ENTRYPOINT ["TestingApplication/entrypoint.sh"]