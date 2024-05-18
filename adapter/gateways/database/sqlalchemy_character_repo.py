from typing import Optional

from adapter.gateways.database.model import BaseModel, CharacterModel
from domain.entities.character import Character
from domain.interfaces import CharacterRepository

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from adapter import config


engine = create_engine(config.DB_URI)
Session = scoped_session(sessionmaker(bind=engine))
#BaseModel.metadata.drop_all(engine)
BaseModel.metadata.create_all(engine)

class SQLAlchemyCharacterRepository(CharacterRepository):
    def __init__(self):
        self.session = Session

    def add_character(self, character: Character):
        """Add a new character to the database."""
        db_character = CharacterModel(**character.__dict__)
        self.session.add(db_character)
        self.session.commit()

    def get_character(self, user_id: str, game_id: str) -> Optional[Character]:
        """Retrieve a character by their user ID."""
        db_character = self.session.query(CharacterModel).filter_by(user_id = user_id, game_id = game_id).one_or_none()
        if db_character is not None:
            return Character(**{column.name: getattr(db_character, column.name) for column in db_character.__table__.columns})
        return None
