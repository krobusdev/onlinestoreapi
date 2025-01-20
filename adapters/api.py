from fastapi import APIRouter, Depends, HTTPException
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
    try:
        return service.get_games()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/games/{name}", response_model=List[GameReadSchema])
def read_games(name : str, service: GameService = Depends(get_game_service)):
    try:
        return service.search_games_by_name(name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/games/{id}", response_model=GameReadSchema)
def read_game(id: int, service: GameService = Depends(get_game_service)):
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
    try:
        service.delete_game(id)
        return {"detail": "Game deleted"}
    except GameNotFoundError:
        raise HTTPException(status_code=404, detail="Game not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))