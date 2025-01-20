from pydantic import BaseModel
from typing import Optional


class GameReadSchema(BaseModel):
    """
    Схема для чтения данных об игре.
    """
    id: int
    name: str
    price: int
    is_in_stock: bool

    class Config:
        from_attributes = True  # Чтобы парсить атрибуты напрямую из GameModel


class GameCreateSchema(BaseModel):
    """
    Схема для создания новой игры.
    """
    # id: Optional[int] = None
    name: str
    price: int
    is_in_stock: bool

    class Config:
        from_attributes = True  # Чтобы парсить атрибуты напрямую из GameModel


class GameUpdateSchema(BaseModel):
    """
    Схема для обновления существующей игры.
    """
    name: Optional[str] = None
    price: Optional[int] = None
    is_in_stock: Optional[bool] = None