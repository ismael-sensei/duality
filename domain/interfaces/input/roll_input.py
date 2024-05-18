from domain.entities.character import Character
from domain.interfaces.gateway.cache_repo import CacheRepository
from domain.interfaces.output import RollOutput
from abc import ABC, abstractmethod

class RollInput(ABC):
    output: RollOutput
    cache: CacheRepository

    def __init__(self, output: RollOutput, cache: CacheRepository = None):
        self.output = output
        self.cache = cache

    async def roll(self, expr: str):
        await self.output.roll(self.roll_logic(expr))
        

    @abstractmethod
    def roll_logic(self, expr: str):
        pass

    async def action(self, mod: str = 0):
        await self.output.action(self.action_logic(mod))
        
    @abstractmethod
    def action_logic(self, mod: str = 0):
        pass
    
    async def agility(self, mod: str = 0, user_id: str = None):
        await self.output.agility(self.agility_logic(mod, self.cache.get(user_id)))
        
    @abstractmethod
    def agility_logic(self, mod: str = 0, character: Character = None):
        pass
