import d20

from domain.entities.character import Character
from domain.interfaces.input.roll_input import RollInput
from domain.entities import ActionRoll


class RollUseCase(RollInput):

    def roll_logic(self, expr: str):
        return d20.roll(expr)

    def action_logic(self, mod: str = 0):
        return ActionRoll(hope = d20.roll("1d12").total, fear = d20.roll("1d12").total, mod = d20.roll(mod))
    
    def agility_logic(self, mod: str = 0, character: Character = None):
        if character is not None:
            mod = f"{mod}+{character.agility}"

        return ActionRoll(hope = d20.roll("1d12").total, fear = d20.roll("1d12").total, mod = d20.roll(mod))