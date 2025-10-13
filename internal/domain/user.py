from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    email:EmailStr
    username:str
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str="bearer"

class HealthCheck(BaseModel):
    status:str
    timestamp:str
    database: Optional[str] = None
    redis: Optional[str] = None