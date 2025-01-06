from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from domain import gameModel
from typing import Optional



class GetOneGame(BaseModel):
    id: int
    name: str
    price: int
    is_in_stock: bool

    class Config:
        from_attributes = True  # Чтобы парсить атрибуты напрямую из GameModel

class AddOneGame(BaseModel):
    game_id: Optional[int] = None
    game_name: str
    game_price: int
    game_is_in_stock: bool

    class Config:
        from_attributes = True  # Чтобы парсить атрибуты напрямую из GameModel

class UpdateOneGame(BaseModel):  # Класс чтобы при изменении указывать не все атрибуты, а только те, что поменять
    game_name: Optional[str] = None
    game_price: Optional[int] = None
    game_is_in_stock: Optional[bool] = None