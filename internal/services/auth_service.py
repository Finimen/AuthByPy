from fastapi import HTTPException, Depends, status
from internal.domain.user import UserRegister, UserLogin, Token
from internal.infrastrucrure.repositories.user_repository import UserRepository
from internal.infrastrucrure.repositories.token_blacklist import TokenBlacklist
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from internal.infrastrucrure.database.models import UserModel
from passlib.context import CryptContext
from internal.handlers.jwt_handler import JWTHandler
from logging import Logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
jwt_handler = JWTHandler()

class AuthService:
    def __init__(self, repository: UserRepository, blacklist: TokenBlacklist, logger: Logger):
        self.user_db = repository
        self.token_blacklist = blacklist
        self.logger = logger

    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def _verify_password(self, plain_password:str, hashed_password:str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def register_user(self, user_data: UserRegister) -> dict:
        existing_user = await self.user_db.get_user_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )

        hashed_password = self._hash_password(user_data.password)

        user_model = UserModel(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password,
            is_verified=True
        )

        created_user = await self.user_db.create_user(user_model)

        return {"user_id" : created_user.id, "email" : created_user.email}
    
    async def login_user(self, user_data: UserLogin) -> Token:
        user = await self.user_db.get_user_by_username(user_data.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid credentials"
            )
        
        if not self._verify_password(user_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email not verified"
            )
        
        access_token = jwt_handler.create_access_token(
            {"sub": user.username, "user_id" : user.id}
        )

        if await self.token_blacklist.is_token_blacklisted(access_token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        return Token(access_token=access_token, token_type="bearer")
    
    async def logout_user(self, token: str) -> dict:
        await self.token_blacklist.add_token(token, 1800)
        return {"messege" : "Succesfully logged out"}
    
    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserModel:
        token = credentials.credentials
        payload = jwt_handler.verify_token(token)

        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid or expired token"
            )
        
        username: str = payload.get("sub")
        user_id: str = payload.get("user_id")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        user = await self.user_db.get_user_by_username(username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return user
