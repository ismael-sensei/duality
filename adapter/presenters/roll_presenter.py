from discord.ext.commands.context import Context
from domain.entities import ActionRollResult, Character
from d20.dice import RollResult
from discord import Color, Embed

class RollPresenter():
    ctx: Context

    def __init__(self, ctx: Context):
        self.ctx = ctx

    async def roll(self, roll_result: RollResult):
        await self.ctx.send(roll_result)

    async def action(self, action_roll: ActionRollResult, title: str = 'Roll', character: Character = None):
        color_map = {
            ActionRollResult.HOPE: Color.blue(),
            ActionRollResult.FEAR: Color.red(),
            ActionRollResult.CRITIC: Color.green()
        }

        embed=Embed(
            title=f"{title}: {action_roll.total} {action_roll.result}",
            description=f"Hope: {action_roll.hope} | Fear: {action_roll.fear} | Mod: {action_roll.mod}",
            color=color_map[action_roll.result],
        )

        if character:
            embed.set_author(name = character.name, icon_url= character.thumbnail)
        else:
            embed.set_author(name=self.ctx.author.name, icon_url=self.ctx.author.avatar.url)

        await self.ctx.send(embed=embed)