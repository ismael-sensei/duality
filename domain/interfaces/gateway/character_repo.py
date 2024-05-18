from abc import ABC, abstractmethod

from entities.character import Character

class CharacterRepository(ABC):
    @abstractmethod
    def add_character(self, character: Character):
        pass

    @abstractmethod
    def get_character(self, id: str) -> Character:
        pass

    @abstractmethod
    def update_character(self, character: Character):
        pass

    @abstractmethod
    def delete_character(self, id: str):
        pass