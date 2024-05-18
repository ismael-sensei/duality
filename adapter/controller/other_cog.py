from discord.ext import commands

from adapter.presenter.bot.other_bot_presenter import OtherBotPresenter
from domain.use_cases.other_use_case import OtherUseCase

class OtherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.context.Context):
        await OtherUseCase(OtherBotPresenter(ctx)).ping()

async def setup(bot):
    await bot.add_cog(OtherCog(bot))