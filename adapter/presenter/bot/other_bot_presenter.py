from domain.interfaces.output import OtherOutput
from discord.ext.commands.context import Context

class OtherBotPresenter(OtherOutput):
    ctx: Context

    def __init__(self, ctx: Context):
        self.ctx = ctx

    async def pong(self):
        await self.ctx.send(f'Pong @{self.ctx.author}!')