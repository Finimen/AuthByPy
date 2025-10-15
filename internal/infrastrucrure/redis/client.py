import redis.asyncio as redis
import os
from typing import Optional

class RedisClient:
    def __init__(self, url: Optional[str]=None):
        self.url = url or os.getenv("REDIS_URL", "redis://localhost:6379")
        self._client: Optional[redis.Client] = None

    async def connect(self):
        self._client = redis.from_url(self.url, decode_responses=True)
        return self
    
    async def disconnect(self):
        if self._client:
            await self._client.aclose()

    def get_client(self) -> redis.Redis:
        if not self._client:
            raise RuntimeError("Redis client not connected")
        return self._client
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.disconnect()
