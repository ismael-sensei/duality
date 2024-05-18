from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
# Setup de SQLAlchemy
engine = create_engine('postgresql://user:password@localhost/mydatabase')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    level = Column(Integer)

class SQLAlchemyCharacterRepository(CharacterRepository):
    def __init__(self):
        self.session = Session()

    def add_character(self, character):
        self.session.add(character)
        self.session.commit()

    def get_character(self, character_id: int):
        return self.session.query(Character).filter_by(id=character_id).first()

    def update_character(self, character):
        db_character = self.session.query(Character).filter_by(id=character.id).first()
        if db_character:
            db_character.name = character.name
            db_character.level = character.level
            self.session.commit()

    def delete_character(self, character_id: int):
        character = self.session.query(Character).filter_by(id=character_id).first()
        if character:
            self.session.delete(character)
            self.session.commit()
