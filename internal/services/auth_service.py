from fastapi import HTTPException, status
from domain.user import UserRegister, UserLogin, Token

class AuthService:
    def __init__(self):
        self.user_db = {}
        self.current_id = 1

    async def register_user(self, user_data: UserRegister) -> dict:
        if user_data.email in self.user_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        user_id = self.current_id
        self.user_db[user_data.email] = {
            "id":user_id,
            "email":user_data.email,
            "username":user_data.username,
            "password":user_data.password,
        }
        self.current_id+=1

        return {"user_id" : user_id, "email" : user_data.email}
    
    async def login_user(self, user_data: UserLogin) -> Token:
        user = self.user_db.get(user_data.email)
        if not user or user["password"] != user_data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credits"
            )
        return Token(access_token=f"fake-jwt-token-{user["id"]}")
    
    async def logout_user(self, token: str) -> dict:
        return {"messege" : "succesfully logged out"}
