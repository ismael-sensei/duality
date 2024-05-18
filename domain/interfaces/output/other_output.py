from abc import ABC, abstractmethod

from domain.entities.character import Character

class OtherOutput(ABC):
    @abstractmethod
    async def present(character: Character):
        pass