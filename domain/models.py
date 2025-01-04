from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

class GameModel(Base):  # Создаем ОРМ модель, чтобы вместо SQL запросов обращаться через объекты и классы
    __tablename__ = "games"

    game_id = Column(Integer, primary_key=True, index=True)
    game_name = Column(String, nullable=False)
    game_price = Column(Integer, nullable=False)
    game_is_in_stock = Column(Boolean, nullable=False)

class Game(BaseModel):
    id: Optional[int] = None
    name: str
    price: int
    is_in_stock: bool

    class Config:
        from_attributes = True  # Чтобы парсить атрибуты напрямую из GameModel

class GameUpdate(BaseModel):  # Класс чтобы при изменении указывать не все атрибуты, а только те, что поменять
    name: Optional[str] = None
    price: Optional[int] = None
    is_in_stock: Optional[bool] = None