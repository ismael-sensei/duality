from abc import ABC, abstractmethod
from domain.entities.character import Character

class ImportSheetOutput(ABC):
    @abstractmethod
    async def present(character: Character):
        pass