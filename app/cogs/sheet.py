import discord
from discord.ext import commands

class Sheet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.imported_ids = []

    @commands.command(name='import')
    async def import_(self, interaction: discord.Interaction, user: discord.User):
        self.imported_ids.append(id)
        await interaction.send(f'ID {id} importado!')

    @commands.command()
    async def show(self, interaction: discord.Interaction, user: discord.User):
        if self.imported_ids:
            await interaction.send(f'IDs importados: {", ".join(self.imported_ids)}')
        else:
            await interaction.send('No hay IDs importados.')

def setup(bot):
    bot.add_cog(Sheet(bot))
