from domain.interfaces.output.other_output import OtherOutput
from abc import ABC, abstractmethod

class OtherInput(ABC):
    presenter: OtherOutput

    def __init__(self, presenter: OtherOutput):
        self.presenter = presenter

    async def ping(self):
        self.ping_logic()
        await self.presenter.pong()

    @abstractmethod
    def ping_logic(self):
        pass