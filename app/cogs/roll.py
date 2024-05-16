import discord
from discord.ext import commands

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def agility(self, interaction: discord.Interaction, user: discord.User):
        await interaction.send('Mostrando información de agilidad...')

def setup(bot):
    bot.add_cog(Roll(bot))
