from dataclasses import dataclass
from d20.dice import RollResult

class ActionRollResult:
    HOPE = "Hope"
    FEAR = "Fear"
    CRITIC = 'CRITIC'

@dataclass
class ActionRoll:
    hope: int
    fear: int
    mod: RollResult
    
    @property
    def total(self):
        return self.hope+self.fear+self.mod.total
    
    @property
    def result(self):
        if self.hope > self.fear:
            return ActionRollResult.HOPE
        elif self.fear > self.hope:
            return ActionRollResult.FEAR
        else:
            return ActionRollResult.CRITIC
    
    @property
    def is_hope(self):
        return self.hope > self.fear
    
    @property
    def is_hope(self):
        return self.fear > self.hope
    
    @property
    def is_crit(self):
        return self.fear == self.hope
    
    def __str__(self):
        return f"{self.result} ({self.total} = {self.hope} hope + {self.fear} fear)"