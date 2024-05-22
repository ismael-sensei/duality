from domain.entities import Tracker
from abc import ABC, abstractmethod

class TrackerRepository(ABC):
    @abstractmethod
    def set_tracker(self, id: str, tracker: Tracker):
        pass

    @abstractmethod
    def get_tracker(self, id: str) -> Tracker:
        pass

    @abstractmethod
    def del_tracker(self, id: str) -> Tracker:
        pass