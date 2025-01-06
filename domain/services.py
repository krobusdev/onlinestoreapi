
from fastapi import HTTPException
from domain import responseModels
from domain import requestModels
from pydantic import BaseModel
from domain import gameModel



def get_games(db):
    games = db.query(gameModel.GameModel).all()  # Создаем запрос с помощью SQLAlchemy

    return [responseModels.ReturnOneGame.model_validate(game) for game in games]

def add_game(game_data: dict, db):  # В скобках - берем данные из запроса и обозначаем что это словарь

    try:
        game = requestModels.AddOneGame(**game_data)  # запихиваем словарь в класс
    except:
        raise HTTPException(detail="Invalid request. JSON provides wrong request structure.")

    game_data_dict = {key: value for key, value in game.model_dump().items() if not key.startswith('_')}
    new_game = gameModel.GameModel(**game_data_dict)

    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    return responseModels.AddedOneGame.model_validate(new_game)

def update_game(game_id: int, game_data: dict, db):  # В скобках - берем данные из запроса и обозначаем что это словарь

    try:
        game = requestModels.UpdateOneGame(**game_data)  # запихиваем словарь в класс
    except:
        raise HTTPException(detail="Invalid request. JSON provides wrong request structure.")

    existing_game = db.query(gameModel.GameModel).filter(gameModel.GameModel.game_id == game_id).first()  # .first это берем первое попавшееся совпадение. .filter это как WHERE в SQL.
    if not existing_game:
        raise HTTPException(status_code=404, detail="Game not found")

    for key, value in game.model_dump().items():
        if value is not None:
            setattr(existing_game, key, value)

    db.commit()
    db.refresh(existing_game)

    return responseModels.ReturnOneGame.model_validate(existing_game)

def delete_game(game_id: int, db):
    existing_game = db.query(gameModel.GameModel).filter(gameModel.GameModel.game_id == game_id).first()
    if not existing_game:
        raise HTTPException(status_code=404, detail="Game not found")

    db.delete(existing_game)
    db.commit()

    return {"message": f"Game with id {game_id} deleted successfully"}