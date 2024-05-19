import redis
from adapter import config
import json
from dataclasses import asdict

from domain.interfaces import CacheRepository

pool = redis.ConnectionPool.from_url(
    url=config.REDIS_URI,
    max_connections=10,
    socket_connect_timeout=5,  # Tiempo en segundos para intentar conectar antes de fallar
    socket_timeout=5,          # Tiempo en segundos para operaciones de lectura/escritura antes de fallar
    retry_on_timeout=True      # Intentar reconectar si una operación falla por timeout
)

class RedisAdapter:
    @staticmethod
    def to_json(entity):
        """ Convierte la entidad a JSON. """
        print(asdict(entity))
        return json.dumps(asdict(entity))
    
    @staticmethod
    def from_json(json_data, entity_class):
        """ Convierte JSON a una instancia de entidad. """
        data = json.loads(json_data)
        return entity_class(**data)


class RedisCacheRepository(CacheRepository):
    def __init__(self):
        self.client = redis.Redis.from_pool(connection_pool=pool)

    def get(self, key: str, class_):
        value = self.client.get(key)
        if value is not None:
            return RedisAdapter.from_json(self.client.get(key), class_)
        else:
            return None

    def set(self, key: str, value):
        self.client.set(key, RedisAdapter.to_json(value))