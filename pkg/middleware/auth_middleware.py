from internal.services.auth_service import AuthService
async def get_auth_service() -> AuthService:
    """DI for AuthService"""
    return AuthService()

