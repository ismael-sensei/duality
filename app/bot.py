import discord
from discord.ext import commands
import os
from adapter import config

class MyBot(commands.Bot):
    
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self):
        extensions = [f"adapter.controller.{filename[:-3]}" for filename in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/../adapter/controller") if filename.endswith("_cog.py")]

        # Carga todas las extensiones
        for extension in extensions:
            try:
                await self.load_extension(extension)
                print(f'Cog {extension} loaded successfully')
            except Exception as e:
                print(f'Failed to load cog {extension}: {e}')

    async def on_ready(self):
        print(f'Bot conectado como {self.user}')

def run():
    intents = discord.Intents.default()
    intents.message_content = True 
    intents.messages = True

    bot = MyBot(command_prefix='!', intents=intents)

    # Corre el bot con tu token
    bot.run(config.DISCORD_TOKEN)
