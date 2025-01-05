
from fastapi import HTTPException
from domain import responseModels
from domain import requestModels
from domain import gameModel



def get_games(db):
    games = db.query(gameModel.GameModel).all()  # Создаем запрос с помощью SQLAlchemy
    return [
        responseModels.ReturnOneGame(
            id=game.game_id,
            name=game.game_name,
            price=game.game_price,
            is_in_stock=game.game_is_in_stock
        )
        for game in games
    ]

def add_game(game_data: dict, db):  # В скобках - берем данные из запроса и обозначаем что это словарь

    game = requestModels.AddOneGame(**game_data)  # запихиваем словарь в класс

    new_game = gameModel.GameModel(
        game_name=game.name,
        game_price=game.price,
        game_is_in_stock=game.is_in_stock
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    return responseModels.AddOneGameResponse(
        id=new_game.game_id,
        name=new_game.game_name,
        price=new_game.game_price,
        is_in_stock=new_game.game_is_in_stock
    )

def update_game(game_id: int, game_data: dict, db):  # В скобках - берем данные из запроса и обозначаем что это словарь

    try:
        game = requestModels.UpdateOneGame(**game_data)  # запихиваем словарь в класс
    except:
        raise HTTPException(detail="Invalid request. JSON provides wrong request structure.")

    existing_game = db.query(gameModel.GameModel).filter(gameModel.GameModel.game_id == game_id).first()  # .first это берем первое попавшееся совпадение. .filter это как WHERE в SQL.
    if not existing_game:
        raise HTTPException(status_code=404, detail="Game not found")

    if game.name is not None:  # Проверяем какие данные меняем
        existing_game.game_name = game.name
    if game.price is not None:
        existing_game.game_price = game.price
    if game.is_in_stock is not None:
        existing_game.game_is_in_stock = game.is_in_stock

    db.commit()
    db.refresh(existing_game)

    return responseModels.ReturnOneGame(
        id=existing_game.game_id,
        name=existing_game.game_name,
        price=existing_game.game_price,
        is_in_stock=existing_game.game_is_in_stock
    )

def delete_game(game_id: int, db):
    existing_game = db.query(gameModel.GameModel).filter(gameModel.GameModel.game_id == game_id).first()
    if not existing_game:
        raise HTTPException(status_code=404, detail="Game not found")

    db.delete(existing_game)
    db.commit()

    return {"message": f"Game with id {game_id} deleted successfully"}