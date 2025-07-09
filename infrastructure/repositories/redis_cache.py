import redis.asyncio as redis
import os
import json

class RedisCache:
    def __init__(self):
        self.client = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379)

    async def get(self, user_id: str):
        data = await self.client.get(user_id)
        return json.loads(data) if data else None

    async def set(self, user_id: str, data: dict, ttl: int):
        await self.client.set(user_id, json.dumps(data), ex=ttl)
