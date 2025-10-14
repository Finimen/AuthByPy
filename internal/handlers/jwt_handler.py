from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
ALGORITM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class JWTHandler:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algoritm = ALGORITM
        self.access_token_expire = ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, data:dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire)

        to_encode.update({"exp" : expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algoritm)
        return encoded_jwt
    
    def verify_token(self, token:str)->Optional[dict]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algoritm])
            return payload
        except JWTError:
            return None
    