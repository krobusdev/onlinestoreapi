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
    id: Optional[int] = None
    name: str
    price: int
    is_in_stock: bool

    class Config:
        from_attributes = True  # Чтобы парсить атрибуты напрямую из GameModel

class UpdateOneGame(BaseModel):  # Класс чтобы при изменении указывать не все атрибуты, а только те, что поменять
    name: Optional[str] = None
    price: Optional[int] = None
    is_in_stock: Optional[bool] = None