from discord import Embed
from domain.entities.character import Character
from domain.interfaces.output import ImportSheetOutput
from discord.ext.commands.context import Context

class ImportSheetBotPresenter(ImportSheetOutput):
    ctx: Context

    def __init__(self, ctx: Context):
        self.ctx = ctx

    async def present(self, character: Character):
        await self.ctx.send(embed=Embed(
            title=f"{character.name}",
            description=f"{character.class_}",
        ))