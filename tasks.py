from celery import Celery
from dotenv import load_dotenv
from celery import shared_task
import os
# from django.contrib.auth.models import User
# from shop.get_data_from_wb.get_fin_report import zapros_finreport
# from shop.get_data_from_wb.get_product import zapros_product, zapros_product_deleted
# from shop.get_data_from_wb.get_sales import zapros_sale, initial_load_sales
# from shop.models import user_tarif, Apisales, ApiToken
# from shop.set_data_to_db.set_products import acreate_products
import logging

# from shop.set_data_to_db.set_sales import save_sales_data

load_dotenv()

REDIS_USERNAME = os.getenv('REDIS_USERNAME')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

# Создаем строку подключения для Redis
redis_url = f'redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'  # Здесь 0 — это номер базы данных Redis (по умолчанию)

# Инициализация объекта Celery с использованием Redis как брокера
app = Celery('tasks', broker=redis_url)

logger = logging.getLogger(__name__)

@app.task
def add(x, y):
    return x + y

# celery_app/tasks.py


@shared_task
def my_task():
    print("Задача выполнена!")
    return "Задача завершена"


@shared_task
def update_data_from_api(user_id):
    # Получите пользователя
    user = User.objects.get(pk=user_id)
    user_status_data = user_tarif.objects.get(user_id=user_id)
    try:
        user_api_token_status = ApiToken.objects.get(user=user.pk)

        if user_status_data.user_status:
            # Здесь выполните логику для скачивания и обновления данных по API
            zapros_product(user)
            zapros_product_deleted(user)
            zapros_finreport(user)
            initial_load_sales(user)

            print(f"Обновление данных для пользователя {user}")
            # Пример: вызов API и обновление данных
    except Exception as e:
        print(f'токена нет, пропускаем {e}')


@shared_task
def periodic_update_data_from_api():
    list_users = User.objects.all().filter()
    print(list_users)
    for user in list_users:
        user_status_data = user_tarif.objects.get(user_id=user.pk)
        try:
            user_api_token_status = ApiToken.objects.get(user=user.pk)
            print(user)
            if user_status_data.user_status and user_api_token_status.is_active:
                # Здесь выполните логику для скачивания и обновления данных по API
                zapros_product(user)
                zapros_product_deleted(user)
                zapros_finreport(user)
                print(f"Периодическое обновление данных для пользователя {user} завершено")
        except Exception as e:
            print(f'токена нет, пропускаем {e}')
    print(f"Периодическое обновление данных для пользователей завершено")


@shared_task
def update_sales_data():
    # Получаем пользователя (или пользователей)
    users = User.objects.all()  # Здесь можно сделать фильтрацию по нужному пользователю

    # Для каждого пользователя получаем последнее обновление и загружаем новые данные
    for user in users:
        last_sale = Apisales.objects.filter(user=user).order_by('-lastChangeDate').first()
        if last_sale:
            date_from = last_sale.lastChangeDate.isoformat()
        else:
            # Если данных нет, начинаем с 01.03.2024
            date_from = "2024-03-01T00:00:00"

        # Загружаем данные с последнего обновления
        sales_data = zapros_sale(user, date_from)
        if sales_data:
            save_sales_data(sales_data, user)
