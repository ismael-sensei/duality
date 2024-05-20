from abc import ABC, abstractmethod

from domain.entities.character import Character

class CharacterRepository(ABC):
    @abstractmethod
    def add_character(self, character: Character):
        pass

    @abstractmethod
    def get_character(self, user_id: str, game_id: str) -> Character:
        pass
