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
            embed.add_field(
                name='Stats', 
                value=f"""
                    **Agility**: {character.agility}{"\u3000" * 3}**Strength**: {character.strength}{"\u3000" * 3}**Finesse**: {character.finesse}
                    **Instinct**: {character.instinct}{"\u3000" * 3}**Presence**: {character.presence}{"\u3000" * 3}**Knowledge**: {character.knowledge}
                """,
                inline=False
            )

            embed.add_field(
                name = f"**Hope** (2/{character.hope_slots})",
                value="⚪️⚪️⚫️⚫️⚫️",
                inline=False
            )

            embed.add_field(
                name="Defense", 
                value=f"""
                    **Evasion**: {character.evasion}
                    **Armor**: {character.armor}
                    **Armor Slots** (1/{character.armor_slots}): ⚪️⚫️⚫️⚫️⚫️⚫️
                """,
                inline=False
            )

            embed.add_field(
                name="Damage", 
                value=f"""
                    **Thresholds**: **{character.minor_th}** >= minor > **{character.major_th}** >= major > **{character.severe_th}** >= severe
                    **HP** (1/{character.hp_slots}): ⚪️⚫️⚫️⚫️⚫️⚫️
                    **Stress** (1/{character.stress_slots}): ⚪️⚫️⚫️⚫️⚫️⚫️
                """,
                inline=False
            )

            embed.add_field(
                name="Character Sheet",
                value=f"https://app.demiplane.com/nexus/daggerheart/character-sheet/{character.character_id}",
                inline=False
            )
            embed.set_thumbnail(url=character.thumbnail)

            await self.ctx.send(embed=embed)
        else:
            await self.ctx.send("Character not found")