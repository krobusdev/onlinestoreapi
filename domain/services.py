from domain import schemas
from adapters.database import models
from sqlalchemy.orm import Session
from adapters.database.database import get_db
from adapters.elasticsearch.connection import get_es, es
from fastapi import Depends
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class GameNotFoundError(Exception):
    """Исключение, выбрасываемое, если игра не найдена."""

    pass


class InvalidGameDataError(Exception):
    """Исключение, выбрасываемое, если данные игры некорректны."""

    pass


class GameService:

    def __init__(self, db_session, es_client):
        self.db_session = db_session
        self.es_client = es_client

    def get_games(self):
        """
        Получить все игры.
        """
        games = self.db_session.query(models.GameModel).all()
        return [schemas.GameReadSchema.model_validate(game) for game in games]

    def get_game_by_id(self, game_id: int):
        """
        Получить игру по её ID.
        """
        game = (
            self.db_session.query(models.GameModel)
            .filter(models.GameModel.id == game_id)
            .first()
        )
        if not game:
            raise GameNotFoundError(f"Game with ID {game_id} not found")
        return schemas.GameReadSchema.model_validate(game)

    def add_game(self, game_data: schemas.GameCreateSchema):
        """
        Добавить новую игру.
        """
        try:
            new_game = models.GameModel(**game_data.dict())
            self.db_session.add(new_game)
            self.db_session.commit()
            self.db_session.refresh(new_game)

            es.index(
                index="games",  # Elasticsearch index name
                id=new_game.id,      # The ID of the document in Elasticsearch
                body={
                    "name": new_game.name,
                    "price": new_game.price,
                    "is_in_stock": new_game.is_in_stock
                }
            )

            return schemas.GameReadSchema.model_validate(new_game)
        except Exception as e:
            self.db_session.rollback()
            raise InvalidGameDataError(f"Invalid game data: {e}")

    def update_game(self, game_id: int, game_data: schemas.GameUpdateSchema):
        """
        Обновить данные игры по её ID.
        """
        game = (
            self.db_session.query(models.GameModel)
            .filter(models.GameModel.id == game_id)
            .first()
        )
        if not game:
            raise GameNotFoundError(f"Game with ID {game_id} not found")

        for key, value in game_data.dict(exclude_unset=True).items():
            setattr(game, key, value)

        self.db_session.commit()
        self.db_session.refresh(game)
        return schemas.GameReadSchema.model_validate(game)

    def delete_game(self, game_id: int):
        """
        Удалить игру по её ID.
        """
        game = (
            self.db_session.query(models.GameModel)
            .filter(models.GameModel.id == game_id)
            .first()
        )
        if not game:
            raise GameNotFoundError(f"Game with ID {game_id} not found")

        self.db_session.delete(game)
        self.db_session.commit()

    def search_games_by_name(self, query: str):
        """
        Поиск игр по имени.
        """
        body = {
            "query": {
                "wildcard": {
                    "name": {
                        "value": f"*{query.lower()}*",
                        "boost": 1.0,
                        "rewrite": "constant_score"
                    }
                }
            }
        }
        response = self.es_client.search(index="games", body=body)
        results = response["hits"]["hits"]
        return [{"id": hit["_id"], **hit["_source"]} for hit in results]


def get_game_service(
        db: Session = Depends(get_db),
        es_client: Elasticsearch = Depends(get_es)
        ):
    return GameService(db, es_client)