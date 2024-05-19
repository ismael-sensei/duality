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
                description=f"""{character.community} {character.ancestry} {character.class_} {character.subclass} **Level {character.level}**"""
            )
            embed.set_author(
                name = 'Demiplane Sheet', 
                url= f'https://app.demiplane.com/nexus/daggerheart/character-sheet/{character.character_id}', 
                icon_url='https://yt3.googleusercontent.com/ytc/AIdro_kwVr8UI750Rhk1QRjBGtGvIHewJS1YZVhDGXUXk6j23w=s900-c-k-c0x00ffffff-no-rj'
            )

            embed.set_thumbnail(url=character.thumbnail)

            embed.add_field(name='Agility', value= f'{character.agility:+}')
            embed.add_field(name='Strength', value= f'{character.strength:+}')
            embed.add_field(name='Finesse', value= f'{character.finesse:+}')
            embed.add_field(name='Instinct', value= f'{character.instinct:+}')
            embed.add_field(name='Presence', value= f'{character.presence:+}')
            embed.add_field(name='Knowledge', value= f'{character.knowledge:+}')


            embed.add_field(name='Evasion', value= f'{character.evasion}')
            embed.add_field(name='Armor', value= f'{character.armor}')
            embed.add_field(name=f'Armor Slots (1/{character.armor_slots})', value= '⚪️⚫️⚫️⚫️⚫️⚫️')


            embed.add_field(name=f'HP (1/{character.hp_slots})', value = '⚪️⚫️⚫️⚫️⚫️⚫️')
            embed.add_field(name=f'Stress (1/{character.stress_slots}', value = '⚪️⚫️⚫️⚫️⚫️⚫️')
            embed.add_field(name = f"**Hope** (2/{character.hope_slots})", value="⚪️⚪️⚫️⚫️⚫️")

            embed.add_field(name='Thresholds', value=f'{character.minor_th} >= *minor* > {character.major_th} >= *major* > {character.severe_th} >= *severe*')


            await self.ctx.send(embed=embed)
        else:
            await self.ctx.send("Character not found")