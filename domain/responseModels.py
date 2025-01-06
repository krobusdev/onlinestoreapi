from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from domain import gameModel
from typing import Optional



class ReturnOneGame(BaseModel):
    game_id: int
    game_name: str
    game_price: int
    game_is_in_stock: bool


    class Config:
        from_attributes = True  # Чтобы парсить атрибуты напрямую из GameModel

class AddedOneGame(BaseModel):
    game_id: int
    game_name: str
    game_price: int
    game_is_in_stock: bool

    class Config:
        from_attributes = True  # Чтобы парсить атрибуты напрямую из GameModel