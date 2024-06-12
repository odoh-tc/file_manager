from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
import re
from enum import Enum

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class UserBase(BaseModel):
    username: str = Field(..., max_length=100)
    email: EmailStr
    role: Optional[UserRole] = UserRole.user  # Default role is 'user'

class UserPasswordBase(BaseModel):
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator('password', pre=True, always=True)
    def validate_password(cls, v):
        if v is None:
            return v
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])', v):
            raise ValueError(
                "Password must be at least 8 characters long, contain an uppercase letter, "
                "a lowercase letter, a digit, and a special character."
            )
        return v

class UserCreate(UserBase, UserPasswordBase):
    pass

class UserUpdate(UserPasswordBase):
    username: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None

class UserIn(UserBase):
    id: int
    joined_date: datetime

    class Config:
        orm_mode = True

class UserDeleteResponse(BaseModel):
    user: UserIn
    message: str