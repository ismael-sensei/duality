from discord.ext import commands
from discord.ext.commands import context
from adapter.gateway.cache.in_memory_character_repo import InMemoryCacheRepository
from adapter.presenter.bot.roll_bot_presenter import RollBotPresenter
from domain.use_cases import RollUseCase

class RollCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['r'])
    async def roll(self, ctx: context.Context, arg):
        await RollUseCase(RollBotPresenter(ctx)).roll(arg)

    @commands.command(aliases=['a'])
    async def action(self, ctx : context.Context, mod: str = '0'):
        await RollUseCase(RollBotPresenter(ctx)).action(mod)

    @commands.command(aliases=['agi'])
    async def agility(self, ctx : context.Context, mod: str = '0'):
        await RollUseCase(RollBotPresenter(ctx), cache=InMemoryCacheRepository()).agility(mod, ctx.author.id)

async def setup(bot):
    await bot.add_cog(RollCog(bot))
