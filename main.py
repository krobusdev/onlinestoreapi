from fastapi import FastAPI
from adapters.api import router
from adapters.database.database import init_db
from adapters.elasticsearch.connection import sync_data_to_elasticsearch
from settings import get_settings
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Действия при запуске приложения
    settings = next(get_settings())  # Получаем настройки
    print(f"DATABASE_URL:\t{settings.DATABASE_URL}")
    print(f"SECRET_KEY:\t{settings.SECRET_KEY}")
    print(f"DEBUG:\t\t{settings.DEBUG}")

    # Инициализация базы данных перед стартом приложения
    init_db()
    # Переносим данные с БД в Elasticsearch
    sync_data_to_elasticsearch()
    yield  # Запускаем приложение

    # Действия при остановке приложения
    print("Application is shutting down...")

app = FastAPI(lifespan=lifespan)
app.include_router(router)