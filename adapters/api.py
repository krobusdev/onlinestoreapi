from fastapi import APIRouter, Depends, HTTPException, Query
from domain.services import (
    GameService,
    GameNotFoundError,
    InvalidGameDataError,
)
from domain.schemas import GameCreateSchema, GameUpdateSchema, GameReadSchema
from typing import List
from domain.services import get_game_service

router = APIRouter()


@router.get("/games/", response_model=List[GameReadSchema])
def read_games(service: GameService = Depends(get_game_service)):
    """
    Получить все игры.
    """
    try:
        return service.get_games()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/games_filters/", response_model=List[GameReadSchema])
def read_games(
    name: str = Query(None, description="Строка для поиска имени игры (опционально)"),
    skip: int = Query(0, ge=0, description="Сколько элементов пропустить"),
    limit: int = Query(10, gt=0, description="Сколько элементов вернуть"),
    min_price: int = Query(None, ge=0, description="Минимальная цена"),
    max_price: int = Query(None, ge=0, description="Максимальная цена"),
    is_in_stock: bool = Query(None, description="Наличие на складе (true/false)"),
    service: GameService = Depends(get_game_service)
):
    """
    Ручка для поиска игр c поддержкой фильтрации и пагинации.
    - name: поиск по имени
    - skip: количество пропускаемых элементов
    - limit: количество возвращаемых элементов
    - min_price: минимальная цена
    - max_price: максимальная цена
    - is_in_stock: фильтрация по наличию на складе
    """
    try:
        return service.search_games(
            name=name,
            skip=skip,
            limit=limit,
            min_price=min_price,
            max_price=max_price,
            is_in_stock=is_in_stock
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/games/{id}", response_model=GameReadSchema)
def read_game(id: int, service: GameService = Depends(get_game_service)):
    """
    Получить игру по её ID.
    """
    try:
        return service.get_game_by_id(id)
    except GameNotFoundError:
        raise HTTPException(status_code=404, detail="Game not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/games/", response_model=GameReadSchema)
def create_game(
    game: GameCreateSchema, service: GameService = Depends(get_game_service)
):
    """
    Добавить новую игру.
    """
    try:
        return service.add_game(game)
    except InvalidGameDataError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/games/{id}", response_model=GameReadSchema)
def update_game(
    id: int,
    game: GameUpdateSchema,
    service: GameService = Depends(get_game_service),
):
    """
    Обновить данные игры по её ID.
    """
    try:
        return service.update_game(id, game)
    except GameNotFoundError:
        raise HTTPException(status_code=404, detail="Game not found")
    except InvalidGameDataError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/games/{id}")
def delete_game(id: int, service: GameService = Depends(get_game_service)):
    """
    Удалить игру по её ID.
    """
    try:
        service.delete_game(id)
        return {"detail": "Game deleted"}
    except GameNotFoundError:
        raise HTTPException(status_code=404, detail="Game not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))