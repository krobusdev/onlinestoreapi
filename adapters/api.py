# set PYTHONPATH=%PYTHONPATH%;Z:\projects\onlinestoreAPI
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from adapters.database import get_db
from domain.services import get_games, add_game, update_game, delete_game
router = APIRouter()

@router.get("/games/")
def get(db: Session = Depends(get_db)):
    return get_games(db)

@router.post("/games/")
def add(game: dict, db: Session = Depends(get_db)): # В скобках - берем данные из запроса и обозначаем что это словарь. Создаем сессию
    return add_game(game, db)

@router.put("/games/{game_id}")
def update(game_id: int, game: dict, db: Session = Depends(get_db)):  # В скобках - берем данные из запроса и обозначаем что это словарь. Создаем сессию. Создаем сессию.
    return update_game(game_id, game, db)

@router.delete("/games/{game_id}")
def delete(game_id: int, db: Session = Depends(get_db)):  # Создаем сессию.
    return delete_game(game_id, db)