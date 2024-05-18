import redis

class RedisCacheRepository(CacheRepository):
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def get(self, key: str):
        return self.client.get(key)

    def set(self, key: str, value, expiry: int = None):
        if expiry:
            self.client.setex(key, expiry, value)
        else:
            self.client.set(key, value)