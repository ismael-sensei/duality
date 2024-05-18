from domain.entities.character import Character
from domain.interfaces.output import ImportSheetOutput
from domain.interfaces.gateway.cache_repo import CacheRepository
from abc import ABC, abstractmethod

class ImportSheetInput(ABC):
    output: ImportSheetOutput

    def __init__(self, output: ImportSheetOutput, cache: CacheRepository):
        self.output = output
        self.cache = cache

    async def run(self, sheet_id: str, user_id: str):
        character = self.logic(sheet_id, user_id)
        self.cache.set(user_id, character)
        await self.output.present(character)
        
    @abstractmethod
    def logic(self, sheet_id: str, user_id: str) -> Character:
        pass
