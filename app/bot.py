import discord
from discord.ext import commands
import os

class MyBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.load_cogs()

    def load_cogs(self):
        for filename in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if filename.endswith('.py'):
                try:
                    self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'Cog {filename} loaded successfully')
                except Exception as e:
                    print(f'Failed to load cog {filename}: {e}')

    async def on_ready(self):
        print(f'Bot conectado como {self.user}')

def run():
    intents = discord.Intents.default()
    intents.message_content = True 
    intents.messages = True

    bot = MyBot(command_prefix='!', intents=intents)

    # Corre el bot con tu token
    bot.run(os.getenv('DISCORD_TOKEN'))
