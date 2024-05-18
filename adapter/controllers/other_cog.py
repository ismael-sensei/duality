from discord.ext import commands

from adapter.presenters.message_presenter import MessagePresenter
from domain.interactors import other_interactor

class OtherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.context.Context):
        await MessagePresenter(ctx).send(other_interactor.ping(ctx.author.mention))

async def setup(bot):
    await bot.add_cog(OtherCog(bot))