import os
import json
import redis.asyncio as redis

class RedisCache:
    def __init__(self):
        self.client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=6379,
            decode_responses=True
        )

    async def get(self, key: str):
        value = await self.client.get(key)
        if value is None:
            return None
        return json.loads(value)

    async def set(self, key: str, value: dict, ttl: int = 60):
        serialized = json.dumps(value)
        await self.client.set(key, serialized, ex=ttl)
