import json

from domain.entities.character import Character
from domain.interfaces import CharacterRepository
from threading import Thread

class CachedCharacterRepository(CharacterRepository):
    def __init__(self, character_repo, cache_repo):
        self.character_repo = character_repo
        self.cache_repo = cache_repo

    def add_character(self, character):
        self.cache_repo.set(f"{character.user_id}-{character.game_id}", character)
        
        thread = Thread(target=self.character_repo.add_character, args=(character,))
        thread.start()

    def get_character(self, user_id: str, game_id: str) -> Character:
        character: Character = self.cache_repo.get(f"{user_id}-{game_id}", Character)

        if character:
            return character
        else:
            character = self.character_repo.get_character(user_id, game_id)
            if character:
                self.cache_repo.set(f"{character.id}-{character.game_id}", character)
            return character

