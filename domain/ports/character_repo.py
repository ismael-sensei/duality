from abc import ABC, abstractmethod


class CharacterRepository(ABC):
    @abstractmethod
    def find_character(self, user_id):
        pass

    @abstractmethod
    def set_character(self, character):
        pass