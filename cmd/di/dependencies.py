from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from internal.infrastrucrure.repositories.user_repository import UserRepository
from internal.infrastrucrure.database.session import async_session
from internal.services.auth_service import AuthService
from pkg.logger_config import logger

async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db, logger)

async def get_auth_service(repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(repo)