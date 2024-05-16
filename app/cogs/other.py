import discord
from discord.ext import commands

class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, interaction: discord.Interaction, user: discord.User):
        await interaction.send('Pong!')

async def setup(bot):
    bot.add_cog(Other(bot))