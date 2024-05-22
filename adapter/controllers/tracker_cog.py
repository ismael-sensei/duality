from discord.ext import commands
from adapter.gateways.cache import CachedTrackerRepository
from adapter.gateways.cache.redis_cache_repo import RedisCacheRepository
from adapter.gateways.database.sqlalchemy_character_repo import SQLAlchemyCharacterRepository
from adapter.presenters import CharacterPresenter, RollPresenter, TrackerPresenter, MessagePresenter
from domain.interactors.tracker_interactor import TrackerInteractor

class TrackerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.imported_ids = []
        self.__cog_name__ = 'Tracker'
        self.tracker_repo = CachedTrackerRepository(cache_repo=RedisCacheRepository())

    @commands.group(aliases=['t'])
    async def tracker(self, ctx: commands.context.Context):
        if ctx.invoked_subcommand is None:
            self.show(ctx)

            
    @tracker.command()
    async def init(self, ctx: commands.context.Context):
        TrackerInteractor(
            game_id=ctx.guild.id,
            tracker_id=ctx.channel.id,
            repo=self.tracker_repo
        ).create_tracker()
        await MessagePresenter(ctx).send('Tracker initialized!')
        await self.show(ctx)

    @tracker.command()
    async def set(self, ctx: commands.context.Context, tokens: int = 0):
        TrackerInteractor(
            game_id=ctx.guild.id,
            tracker_id=ctx.channel.id,
            repo=self.tracker_repo
        ).set_tokens(tokens)
        await self.show(ctx)

    @tracker.command()
    async def add(self, ctx: commands.context.Context, tokens: int = 1):
        TrackerInteractor(
            game_id=ctx.guild.id,
            tracker_id=ctx.channel.id,
            repo=self.tracker_repo
        ).add_tokens(tokens)
        await self.show(ctx)

    @tracker.command()
    async def show(self, ctx: commands.context.Context):
        await TrackerPresenter(ctx).show(
            TrackerInteractor(
                game_id=ctx.guild.id,
                tracker_id=ctx.channel.id,
                repo=self.tracker_repo
            ).tracker
        )

    @tracker.command()
    async def end(self, ctx: commands.context.Context):
        TrackerInteractor(
            game_id=ctx.guild.id,
            tracker_id=ctx.channel.id,
            repo=self.tracker_repo
        ).del_tracker()
        await MessagePresenter(ctx).send('Tracker ended!')
    


async def setup(bot):
    await bot.add_cog(TrackerCog(bot))
