from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import get_settings
from adapters.database.models import Base  # Убедитесь, что Base импортируется из вашей модели


settings = next(get_settings())  # Получаем настройки

# Создаем движок для подключения к БД
engine = create_engine(settings.DATABASE_URL)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Функция инициализации базы данных.
    Создает таблицы, если они отсутствуют.
    """
    try:
        print("Initializing database...")
        Base.metadata.create_all(bind=engine)
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")


def get_db():
    """
    Генератор для получения сессии базы данных.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
