from domain.interfaces.output import RollOutput
from discord.ext.commands.context import Context
from domain.entities import ActionRollResult
from d20.dice import RollResult
from discord import Color, Embed

class RollBotPresenter(RollOutput):
    ctx: Context

    def __init__(self, ctx: Context):
        self.ctx = ctx

    async def roll(self, roll_result: RollResult):
        await self.ctx.send(roll_result)

    async def action(self, action_roll: ActionRollResult):
        color_map = {
            ActionRollResult.HOPE: Color.blue(),
            ActionRollResult.FEAR: Color.red(),
            ActionRollResult.CRITIC: Color.green()
        }

        await self.ctx.send(embed=Embed(
            title=f"{action_roll.total} {action_roll.result}",
            description=f"Hope: {action_roll.hope} | Fear: {action_roll.fear} | Mod: {action_roll.mod}",
            color=color_map[action_roll.result]
        ))

    async def agility(self, action_roll: ActionRollResult):
        color_map = {
            ActionRollResult.HOPE: Color.blue(),
            ActionRollResult.FEAR: Color.red(),
            ActionRollResult.CRITIC: Color.green()
        }

        await self.ctx.send(embed=Embed(
            title=f"Agility roll: {action_roll.total} {action_roll.result}",
            description=f"Hope: {action_roll.hope} | Fear: {action_roll.fear} | Mod: {action_roll.mod}",
            color=color_map[action_roll.result]
        ))