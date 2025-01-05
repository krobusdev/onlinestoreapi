from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from domain import gameModel
from typing import Optional



class ReturnOneGame(BaseModel):
    id: int
    name: str
    price: int
    is_in_stock: bool

    class Config:
        from_attributes = True  # Чтобы парсить атрибуты напрямую из GameModel

class AddOneGameResponse(BaseModel):
    id: int
    name: str
    price: int
    is_in_stock: bool