import redis
import os
from fastapi import HTTPException
from time import time

r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True)
RATE_LIMIT = 10
WINDOW = 60  # seconds

def enforce_rate_limit(user_id: str):
    key = f"rate_limit:{user_id}"
    current = r.get(key)

    if current and int(current) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    pipe = r.pipeline()
    pipe.incr(key, 1)
    pipe.expire(key, WINDOW)
    pipe.execute()
