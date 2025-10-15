from typing import Optional
import redis.asyncio as redis
from logging import Logger

class TokenBlacklist:
    def __init__(self, redis_client: redis.Redis, logger: Logger):
        self.redis_client = redis_client
        self.logger = logger

    async def add_token(self, token: str, expiration_seconds:int)->bool:
        try:
            self.logger.info(f"added token to blacklist {token[:10]}...")

            key = self._format_token_key(token)
            result = await self.redis_client.setex(key, expiration_seconds, "1")

            self.logger.info(f"token added to blacklist {token[:10]}...")

            return result
        
        except Exception as e:
            self.logger.error(f"error adding token to blacklist {e}")
            raise

    async def is_token_blacklisted(self, token:str)->bool:
        try:
            self.logger.info(f"cheking token in blacklist {token[:10]}...")
            key = self._format_token_key(token)
            exists = await self.redis_client.exists(key)

            result = exists == 1
            return result
        
        except Exception as e:
            self.logger.error(f"error cheking token blacklist {e}")

    def _format_token_key(self, token:str)->str:
        return f"bl:{token}"