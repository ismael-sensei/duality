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
        self.character_repo = CachedCharacterRepository(cache_repo=RedisCacheRepository(), character_repo=SQLAlchemyCharacterRepository())

    @commands.command(name='import')
    async def import_(self, ctx: commands.context.Context, character_id: str = None):
        message = await ctx.send("Loading...")

        await CharacterPresenter(ctx).show(
            CharacterInteractor(
                repo=self.character_repo,
                game_id=ctx.guild.id,
                user_id=ctx.author.id
            ).import_sheet(character_id)
        )

        await message.delete()

    @commands.command(aliases=['s'])
    async def show(self, ctx: commands.context.Context):
        await CharacterPresenter(ctx).show(
            CharacterInteractor(
                repo=self.character_repo,
                game_id=ctx.guild.id,
                user_id=ctx.author.id
            ).character
        )

    @commands.command(aliases=['agi'])
    async def agility(self, ctx: commands.context.Context, mod: str = '0'):
        interactor = CharacterInteractor(
            repo=self.character_repo,
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
            repo=self.character_repo,
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
            repo=self.character_repo,
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
            repo=self.character_repo,
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
            repo=self.character_repo,
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
            repo=self.character_repo,
            game_id=ctx.guild.id,
            user_id=ctx.author.id
        )

        await RollPresenter(ctx).action(
            interactor.knowledge(mod), 
            title='Knowledge',
            character=interactor.character
        )

    # Comando para actualizar el hope
    @commands.command(name='hope')
    async def hope(self, ctx: commands.context.Context, mod: str):
        await self.update_character_attribute(ctx, 'hope', mod)

    # Comando para actualizar el armor slots
    @commands.command(name='armor')
    async def armor(self, ctx: commands.context.Context, mod: str):
        await self.update_character_attribute(ctx, 'armor_slots', mod)

    # Comando para actualizar el hope
    @commands.command(name='hp')
    async def hp(self, ctx: commands.context.Context, mod: str):
        await self.update_character_attribute(ctx, 'hp', mod)

    # Comando para actualizar el hope
    @commands.command(name='stress')
    async def stress(self, ctx: commands.context.Context, mod: str):
        await self.update_character_attribute(ctx, 'stress', mod)

    # Método genérico para actualizar cualquier atributo
    async def update_character_attribute(self, ctx: commands.context.Context, attribute: str, mod: str):
        interactor = CharacterInteractor(
            repo=self.character_repo,
            game_id=ctx.guild.id,
            user_id=ctx.author.id
        )

        updated_character = interactor.update_attribute(attribute, mod)
        if updated_character:
            await CharacterPresenter(ctx).show(updated_character)
        else:
            await ctx.send("Character not found or error updating attribute.")

    # Comando para actualizar el hope
    @commands.command(name='hopeset')
    async def set_hope(self, ctx: commands.context.Context, mod: str):
        await self.set_character_attribute(ctx, 'hope', mod)

    # Comando para actualizar el armor slots
    @commands.command(name='armorset')
    async def set_armor(self, ctx: commands.context.Context, mod: str):
        await self.set_character_attribute(ctx, 'armor_slots', mod)

    # Comando para actualizar el hope
    @commands.command(name='hpset')
    async def set_hp(self, ctx: commands.context.Context, mod: str):
        await self.set_character_attribute(ctx, 'hp', mod)

    # Comando para actualizar el hope
    @commands.command(name='stressset')
    async def set_stress(self, ctx: commands.context.Context, mod: str):
        await self.set_character_attribute(ctx, 'stress', mod)

    # Método genérico para actualizar cualquier atributo
    async def set_character_attribute(self, ctx: commands.context.Context, attribute: str, mod: str):
        interactor = CharacterInteractor(
            repo=self.character_repo,
            game_id=ctx.guild.id,
            user_id=ctx.author.id
        )

        updated_character = interactor.set_attribute(attribute, mod)
        if updated_character:
            await CharacterPresenter(ctx).show(updated_character)
        else:
            await ctx.send("Character not found or error updating attribute.")
        
        

async def setup(bot):
    await bot.add_cog(CharacterCog(bot))
