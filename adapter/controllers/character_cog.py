from discord.ext import commands
from adapter.gateways.cache.cached_character_repo import CachedCharacterRepository
from adapter.gateways.cache.redis_cache_repo import RedisCacheRepository
from adapter.gateways.database.sqlalchemy_character_repo import SQLAlchemyCharacterRepository
from adapter.presenters import CharacterPresenter, RollPresenter
from domain.interactors.character_interactor import CharacterInteractor

class CharacterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.imported_ids = []
        self.__cog_name__ = 'Character'

    @commands.command(name='import')
    async def import_(self, ctx: commands.context.Context, character_id: str = None):
        message = await ctx.send("Loading...")

        await CharacterPresenter(ctx).show(
            CharacterInteractor(
                repo=CachedCharacterRepository(cache_repo=RedisCacheRepository(), character_repo=SQLAlchemyCharacterRepository()),
                game_id=ctx.guild.id,
                user_id=ctx.author.id
            ).import_sheet(character_id)
        )

        await message.delete()

    @commands.command(aliases=['s'])
    async def show(self, ctx: commands.context.Context):
        await CharacterPresenter(ctx).show(
            CharacterInteractor(
                repo=CachedCharacterRepository(cache_repo=RedisCacheRepository(), character_repo=SQLAlchemyCharacterRepository()),
                game_id=ctx.guild.id,
                user_id=ctx.author.id
            ).character
        )

    @commands.command(aliases=['agi'])
    async def agility(self, ctx: commands.context.Context, mod: str = '0'):
        interactor = CharacterInteractor(
            repo=CachedCharacterRepository(cache_repo=RedisCacheRepository(), character_repo=SQLAlchemyCharacterRepository()),
            game_id=ctx.guild.id,
            user_id=ctx.author.id
        )

        await RollPresenter(ctx).action(
            interactor.agility(mod), 
            title='Agility',
            character=interactor.character
        )
        
    @commands.command(aliases=['str'])
    async def strength(self, ctx: commands.context.Context, mod: str = '0'):
        interactor = CharacterInteractor(
            repo=CachedCharacterRepository(cache_repo=RedisCacheRepository(), character_repo=SQLAlchemyCharacterRepository()),
            game_id=ctx.guild.id,
            user_id=ctx.author.id
        )

        await RollPresenter(ctx).action(
            interactor.strength(mod), 
            title='Strength',
            character=interactor.character
        )
        
    @commands.command(aliases=['fin'])
    async def finesse(self, ctx: commands.context.Context, mod: str = '0'):
        interactor = CharacterInteractor(
            repo=CachedCharacterRepository(cache_repo=RedisCacheRepository(), character_repo=SQLAlchemyCharacterRepository()),
            game_id=ctx.guild.id,
            user_id=ctx.author.id
        )

        await RollPresenter(ctx).action(
            interactor.finesse(mod), 
            title='Finesse',
            character=interactor.character
        )
        
    @commands.command(aliases=['ins'])
    async def instinct(self, ctx: commands.context.Context, mod: str = '0'):
        interactor = CharacterInteractor(
            repo=CachedCharacterRepository(cache_repo=RedisCacheRepository(), character_repo=SQLAlchemyCharacterRepository()),
            game_id=ctx.guild.id,
            user_id=ctx.author.id
        )

        await RollPresenter(ctx).action(
            interactor.instinct(mod), 
            title='Instinct',
            character=interactor.character
        )
        
    @commands.command(aliases=['pre'])
    async def presence(self, ctx: commands.context.Context, mod: str = '0'):
        interactor = CharacterInteractor(
            repo=CachedCharacterRepository(cache_repo=RedisCacheRepository(), character_repo=SQLAlchemyCharacterRepository()),
            game_id=ctx.guild.id,
            user_id=ctx.author.id
        )

        await RollPresenter(ctx).action(
            interactor.presence(mod), 
            title='Presence',
            character=interactor.character
        )
        
    @commands.command(aliases=['kno'])
    async def knowledge(self, ctx: commands.context.Context, mod: str = '0'):
        interactor = CharacterInteractor(
            repo=CachedCharacterRepository(cache_repo=RedisCacheRepository(), character_repo=SQLAlchemyCharacterRepository()),
            game_id=ctx.guild.id,
            user_id=ctx.author.id
        )

        await RollPresenter(ctx).action(
            interactor.knowledge(mod), 
            title='Knowledge',
            character=interactor.character
        )
        
        

async def setup(bot):
    await bot.add_cog(CharacterCog(bot))
