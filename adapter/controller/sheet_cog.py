from discord.ext import commands
from adapter.gateway.cache.in_memory_character_repo import InMemoryCacheRepository
from adapter.presenter.bot.import_sheet_presenter import ImportSheetBotPresenter
from domain.use_cases import ImportSheet

class Sheet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.imported_ids = []

    @commands.command(name='import')
    async def import_(self, ctx: commands.context.Context, character_id: str = None):
        message = await ctx.send("Loading...")
        await ImportSheet(
            output=ImportSheetBotPresenter(ctx), 
            cache=InMemoryCacheRepository()
        ).run(character_id, ctx.author.id)
        await message.delete()

async def setup(bot):
    await bot.add_cog(Sheet(bot))
