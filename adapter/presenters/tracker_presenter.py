from discord import Embed
from domain.entities import Tracker
from discord.ext.commands.context import Context

class TrackerPresenter():
    ctx: Context

    def __init__(self, ctx: Context):
        self.ctx = ctx

    async def show(self, tracker: Tracker):
        if tracker is not None:
            if tracker.max_tokens < 100:
                embed = Embed(
                    title=f"Tracker",
                    description=''.join(['⚪️' for slot in range(tracker.tokens)]) + ''.join(['⚫️' for slot in range(tracker.max_tokens - tracker.tokens)])
                )

                await self.ctx.send(embed=embed)
            else:
                embed = Embed(
                    title=f"Tracker",
                    description=''.join(['⚪️' for slot in range(tracker.tokens)])
                )

                await self.ctx.send(embed=embed)
        else:
            await self.ctx.send("Tracker not found.")
