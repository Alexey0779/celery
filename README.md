![Celery Logo](https://st.timeweb.com/cloud-static/apps-logo/celery.svg)

# Celery

Пример приложения Celery, которое можно развернуть в **Timeweb Cloud Apps** без настройки.

:rocket: [Создать свой Apps](https://timeweb.cloud/my/apps/create)

:books: [Документация Timeweb Cloud Apps](https://timeweb.cloud/docs/apps)

## <a name="rabbit"></a>Подключение к RabbitMQ

Для корректного запуска приложения требуется указать переменные окружения для подключения к RabbitMQ.

Вы можете переименовать файл `.env.example` в `.env` и заполнить его своими значениями.

RabbitMQ можно запустить локально в [Docker](https://hub.docker.com/_/rabbitmq) или подключить как сервис в [Timeweb Cloud](https://timeweb.cloud/my/database/create?type=rabbitmq).

## <a name="dev"></a>Локальный запуск проекта

```bash
# установка зависимостей
pip3 install -r requirements.txt --break-system-packages

# запуск приложения
celery -A tasks worker --loglevel=INFO
```
