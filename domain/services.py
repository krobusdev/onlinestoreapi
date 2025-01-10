from domain import schemas
from adapters.database import models
from sqlalchemy.orm import Session
from adapters.database.database import get_db
from fastapi import Depends


class GameNotFoundError(Exception):
    """Исключение, выбрасываемое, если игра не найдена."""

    pass


class InvalidGameDataError(Exception):
    """Исключение, выбрасываемое, если данные игры некорректны."""

    pass


class GameService:
    def __init__(self, db_session):
        self.db_session = db_session

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


def get_game_service(db: Session = Depends(get_db)):
    return GameService(db)
