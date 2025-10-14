from internal.infrastrucrure.database.models import UserModel
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import logging

class UserRepository:
    def __init__(self, db_session: AsyncSession, logger: logging.Logger):
        self.db = db_session
        self.logger = logger

    async def create_tables(self):
        self.logger.info(f"migrations not used yet")

    async def get_user_by_username(self, username:str)-> Optional[UserModel]:
        self.logger.info(f"getting user by username: {username}")

        try:
            query = select(UserModel).where(UserModel.username==username)
            result = await self.db.execute(query)
            user_model = result.scalar_one_or_none()
            if user_model:
                self.logger.info(f"User found: {username}")
            else:
                self.logger.info(f"User not found: {username}")
            
            return user_model
        except Exception as e:
            self.logger.error(f"error getting user by username: {e}")
            raise
        
    async def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        self.logger.info(f"getting user by id: {user_id}")

        try:
            query = select(UserModel).where(UserModel.id == user_id)
            result = await self.db.execute(query)
            user_model = result.scalar_one_or_none()
            if user_model:
                self.logger.info(f"User found: {id}")
            else:
                self.logger.info(f"User not found: {id}")
            
            return user_model
        
        except Exception as e:
            self.logger.error(f"error getting user by id: {e}")
            raise

    async def get_user_by_token(self, token: str) -> Optional[UserModel]:
        self.logger.info(f"getting user by token: {token}")

        try:
            query = select(UserModel).where(UserModel.verify_token == token)
            result = await self.db.execute(query)
            user_model = result.scalar_one_or_none()
            if user_model:
                self.logger.info(f"User found: {token}")
            else:
                self.logger.info(f"User not found: {token}")
            
            return user_model
        
        except NoResultFound:
            self.logger.info(f"user not found: {token}")
            return None
        
        except Exception as e:
            self.logger.error(f"error getting user by id: {e}")
            raise

    async def create_user(self, user:UserModel) -> UserModel:
        self.logger.info(f"creating user: {user.username}")

        try:
            user_model = UserModel(
                username=user.username,
                email=user.email,
                password=user.password,
                is_verified=user.is_verified,
                is_banned=user.is_banned,
                verify_token=user.verify_token
            )

            self.db.add(user_model)
            await self.db.commit()
            await self.db.refresh(user_model)

            user.id = user_model.id
            user.created_at = user_model.created_at

            self.logger.info(f"user created successfully: {user.username}, ID: {user.id}")
            return user
        
        except Exception as e:
            await self.db.rollback()
            self.logger.error(f"error creating user: {e}")
            raise

    async def delete_user(self, user_id:int)-> bool:
        self.logger.info(f"deleting user: {user_id}")

        try:
            query = delete(UserModel).where(UserModel.id == user_id)
            result = await self.db.execute(query)
            await self.db.commit()

            deleted = result.rowcount > 0

            if deleted:
                self.logger.info(f"User deleted: {user_id}")
            else:
                self.logger.warning(f"User not found for deletion: {user_id}")

            return deleted
        
        except Exception as e:
            await self.db.rollback()
            self.logger.error(f"Error deleting user: {e}")
            raise

    async def mark_user_as_verified(self, user_id:int) -> bool:
        self.logger.info(f"marking user as verified: {user_id}")

        try:
            query = update(UserModel).where(UserModel.id==user_id).values(is_verified = True, verify_token=None)
            result = await self.db.execute(query)
            await self.db.commit()

            updated = result.rowcount > 0
            if updated:
                self.logger.info(f"User verified: {user_id}")
            else:
                self.logger.warning(f"User not found for verification: {user_id}")
                
            return updated

        except Exception as e:
            await self.db.rollback()
            self.logger.error(f"Error verifying user: {e}")
            raise
