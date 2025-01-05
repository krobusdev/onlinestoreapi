from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GameModel(Base):  # Создаем ОРМ модель, чтобы вместо SQL запросов обращаться через объекты и классы
    __tablename__ = "games"

    game_id = Column(Integer, primary_key=True, index=True)
    game_name = Column(String, nullable=False)
    game_price = Column(Integer, nullable=False)
    game_is_in_stock = Column(Boolean, nullable=False)