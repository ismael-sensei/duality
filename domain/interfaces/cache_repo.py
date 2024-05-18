from abc import ABC, abstractmethod

class CacheRepository(ABC):
    @abstractmethod
    def get(self, key, class_):
        pass

    @abstractmethod
    def set(self, key, value):
        pass