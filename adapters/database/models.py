from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GameModel(Base):
    """
    ORM модель для таблицы 'games'.
    """
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    is_in_stock = Column(Boolean, nullable=False)
