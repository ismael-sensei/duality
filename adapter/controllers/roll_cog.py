from discord.ext import commands
from discord.ext.commands import context
from adapter.presenters import RollPresenter
from domain.interactors import roll_interactor
from domain.interactors.character_interactor import CharacterInteractor
from adapter.gateways.cache.cached_character_repo import CachedCharacterRepository
from adapter.gateways.cache.redis_cache_repo import RedisCacheRepository
from adapter.gateways.database.sqlalchemy_character_repo import SQLAlchemyCharacterRepository

class RollCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__cog_name__ = 'Roll'

    @commands.command(aliases=['r'])
    async def roll(self, ctx: context.Context, arg):
        await RollPresenter(ctx).roll(roll_interactor.roll(arg))

    @commands.command(aliases=['a'])
    async def action(self, ctx : context.Context, mod: str = '0'):
        interactor = CharacterInteractor(
            repo=CachedCharacterRepository(cache_repo=RedisCacheRepository(), character_repo=SQLAlchemyCharacterRepository()),
            game_id=ctx.guild.id,
            user_id=ctx.author.id
        )

        await RollPresenter(ctx).action(roll_interactor.action(mod), character=interactor.character)

async def setup(bot):
    await bot.add_cog(RollCog(bot))
