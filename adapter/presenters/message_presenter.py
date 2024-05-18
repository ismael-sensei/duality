from discord.ext.commands.context import Context

class MessagePresenter():
    ctx: Context

    def __init__(self, ctx: Context):
        self.ctx = ctx

    async def send(self, message: str):
        await self.ctx.send(message)