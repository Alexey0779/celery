# celery_app/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем код Celery
COPY . .

# Запуск worker для Celery
CMD ["celery", "-A", "my_project.celery", "worker", "--loglevel=info"]
