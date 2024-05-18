from discord import Embed
from domain.entities.character import Character
from discord.ext.commands.context import Context

class CharacterPresenter():
    ctx: Context

    def __init__(self, ctx: Context):
        self.ctx = ctx

    async def show(self, character: Character):
        if character:
            embed = Embed(
                title=f"{character.name}",
                description=f"{character.class_}",
                
            )
            embed.add_field(name='Level', value=character.level)
            embed.set_thumbnail(url=character.thumbnail)

            await self.ctx.send(embed=embed)
        else:
            await self.ctx.send("Character not found")