from abc import ABCMeta
from domain.interfaces.gateway.cache_repo import CacheRepository

class Singleton(ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class InMemoryCacheRepository(CacheRepository, metaclass=Singleton):
    cache: dict

    def __init__(self):
        self.cache = {}

    def get(self, key: str):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value