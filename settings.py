from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env файла
load_dotenv()


class Settings:
    def __init__(self):
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.DEBUG = os.getenv("DEBUG", "False").lower() in (
            "true",
            "1",
            "yes",
        )  # Значение по умолчанию


def get_settings():
    """
    Генератор, который создает экземпляр Settings только один раз,
    а затем возвращает тот же экземпляр.
    """
    settings = Settings()  # Инициализация объекта
    yield settings
