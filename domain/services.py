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

    def search_games(
    self,
    name: str = None,
    skip: int = 0,
    limit: int = 10,
    min_price: int = None,
    max_price: int = None,
    is_in_stock: bool = None
    ):
        """
        Поиск игр c поддержкой фильтров и пагинации.
        - name: поиск по имени
        - skip: количество пропускаемых элементов
        - limit: количество возвращаемых элементов
        - min_price: минимальная цена
        - max_price: максимальная цена
        - is_in_stock: фильтрация по наличию
        """
        # Формируем базовый bool-запрос
        must_queries = []
        if name:
            must_queries.append({
                "wildcard": {
                    "name": {
                        "value": f"*{name.lower()}*",
                        "boost": 1.0,
                        "rewrite": "constant_score"
                    }
                }
            })

        # Опциональные фильтры
        filters = []
        if min_price is not None:
            filters.append({"range": {"price": {"gte": min_price}}})
        if max_price is not None:
            filters.append({"range": {"price": {"lte": max_price}}})
        if is_in_stock is not None:
            filters.append({"term": {"is_in_stock": is_in_stock}})

        # Финальный запрос
        body = {
            "from": skip,
            "size": limit,
            "query": {
                "bool": {
                    "must": must_queries,
                    "filter": filters
                }
            }
        }

        response = self.es_client.search(index="games", body=body)
        results = response["hits"]["hits"]
        return [{"id": hit["_id"], **hit["_source"]} for hit in results]

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
            new_game = models.GameModel(**game_data.dict())   # Добавляем игру в бд
            self.db_session.add(new_game)
            self.db_session.commit()
            self.db_session.refresh(new_game)

            es.index(      # Добавляем игру в Elasticsearch
                index="games",
                id=new_game.id,
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

        es.update(index="games", id=game_id, body={"doc": game_data.dict()})  # Обновляем игру в Elasticsearch

        self.db_session.commit()   # Обновляем игру в бд
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

        self.db_session.delete(game)   # Удаляем игру в бд
        self.db_session.commit()

        es.delete(index="games", id=game_id)   # Удаляем игру в Elasticsearch


def get_game_service(
        db: Session = Depends(get_db),
        es_client: Elasticsearch = Depends(get_es)
        ):
    return GameService(db, es_client)