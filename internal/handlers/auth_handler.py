from fastapi import APIRouter, Depends
from internal.domain.user import UserRegister, UserLogin, Token
from internal.services.auth_service import AuthService
from logging import Logger
from cmd.di.dependencies import get_auth_service, get_logger

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=dict)
async def register(
    user_data: UserRegister,
    auth_service: AuthService = Depends(get_auth_service),
    logger: Logger = Depends(get_logger),
):
    logger.info(f"register attemt for email: {user_data.email}")
    result = await auth_service.register_user(user_data)
    logger.info(f"user registered: {result}")
    return {"message" : "user registered successfully", "data" : result}


@router.post("/login", response_model=Token)
async def login(
    user_data:UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
    logger: Logger = Depends(get_logger),
):
    logger.info(f"login attemt for username: {user_data.username}")
    token = await auth_service.login_user(user_data)
    logger.info(f"user logged in : {user_data.username}")
    return token


@router.post("/logout")
async def logout(
    auth_service: AuthService = Depends(get_auth_service),
    logger: Logger = Depends(get_logger),
):
    result = await auth_service.logout_user("token")
    logger.info("user logged out")
    return result