from abc import ABC, abstractmethod

from domain.entities.action import ActionRoll
from d20.dice import RollResult

class RollOutput(ABC):
    @abstractmethod
    async def roll(roll_result: RollResult):
        pass

    @abstractmethod
    async def action(action_roll: ActionRoll):
        pass

    @abstractmethod
    async def agility(action_roll: ActionRoll):
        pass