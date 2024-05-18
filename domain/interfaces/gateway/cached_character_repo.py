import json

from entities.character import Character
from .character_repo import CharacterRepository
from threading import Thread

class CachedCharacterRepository(CharacterRepository):
    def __init__(self, character_repo, cache_repo):
        self.character_repo = character_repo
        self.cache_repo = cache_repo

    def add_character(self, character):
        self.cache_repo.set(f"character_{character.id}", json.dumps(character.__dict__))
        
        thread = Thread(target=self.character_repo.add_character, args=(character,))
        thread.start()

    def get_character(self, id: str) -> Character:
        character_data = self.cache_repo.get(id)

        if character_data:
            character_dict = json.loads(character_data)
            character = Character(**character_dict)
            return character
        else:
            character = self.character_repo.get_character(id)
            if character:
                self.cache_repo.set(f"character_{character.id}", json.dumps(character.__dict__))
            return character

    def update_character(self, character):
        # Update cache and asynchronously update database
        self.cache_repo.set(f"character_{character.id}", json.dumps(character.__dict__))
        from threading import Thread
        thread = Thread(target=self.character_repo.update_character, args=(character,))
        thread.start()

    def delete_character(self, character_id: int):
        # Delete from cache and asynchronously delete from database
        self.cache_repo.delete(f"character_{character_id}")
        from threading import Thread
        thread = Thread(target=self.character_repo.delete_character, args=(character_id,))
        thread.start()