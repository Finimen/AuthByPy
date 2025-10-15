from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from internal.infrastrucrure.repositories.user_repository import UserRepository
from internal.infrastrucrure.database.session import async_session
from internal.services.auth_service import AuthService
from internal.infrastrucrure.redis.client import RedisClient
from internal.infrastrucrure.repositories.token_blacklist import TokenBlacklist
from pkg.logger_config import get_logger
import logging

async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_user_repository(
        db: AsyncSession = Depends(get_db),
        logger: logging.Logger = Depends(get_logger),
        ) -> UserRepository:
    return UserRepository(db, logger)

async def get_redis_client() -> RedisClient:
    redis_client = RedisClient()
    await redis_client.connect()
    try:
        yield redis_client
    finally:
        await redis_client.disconnect()

async def get_token_blacklist(
        redis_client: RedisClient = Depends(get_redis_client),
        logger: logging.Logger = Depends(get_logger),
        ) -> TokenBlacklist:
    return TokenBlacklist(redis_client.get_client(), logger)

async def get_auth_service(
        repo: UserRepository = Depends(get_user_repository),
        blacklist: TokenBlacklist = Depends(get_token_blacklist),
        logger: logging.Logger = Depends(get_logger),
        ) -> AuthService:
    return AuthService(repo, blacklist, logger)
