from domain.entities.character import Character
from domain.interfaces.character_repo import CharacterRepository


class DummyCharacterRepository(CharacterRepository):
    def add_character(self, character: Character):
        pass

    def get_character(self, id: int) -> Character:
        return None

    def update_character(self, character: Character):
        pass

    def delete_character(self, id: int):
        pass