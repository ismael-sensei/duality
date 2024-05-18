import d20

from domain.entities import ActionRoll

def roll(expr: str):
    return d20.roll(expr)


def action(mod: str = 0):
    return ActionRoll(hope = d20.roll("1d12").total, fear = d20.roll("1d12").total, mod = d20.roll(mod))
    
