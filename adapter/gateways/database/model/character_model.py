from sqlalchemy import Column, Integer, String, BigInteger
from .base_model import BaseModel

class CharacterModel(BaseModel):
    __tablename__ = 'characters'

    character_id = Column(String)
    name = Column(String)
    community = Column(String)
    ancestry = Column(String)
    class_ = Column(String)
    subclass = Column(String)
    level = Column(Integer)
    agility = Column(Integer)
    strength = Column(Integer)
    finesse = Column(Integer)
    instinct = Column(Integer)
    presence = Column(Integer)
    knowledge = Column(Integer)
    evasion = Column(Integer)
    armor = Column(Integer)
    minor_th = Column(Integer)
    major_th = Column(Integer)
    severe_th = Column(Integer)
    armor_slots = Column(Integer)
    hp_slots = Column(Integer)
    stress_slots = Column(Integer)
    hope_slots = Column(Integer)
    thumbnail = Column(String)
    user_id = Column(BigInteger, primary_key=True)
    game_id = Column(BigInteger, primary_key=True)