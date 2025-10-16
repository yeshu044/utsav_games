from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    name: str
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    @field_validator('phone_number')
    @classmethod
    def validate_phone(cls, v):
        if v and not v.startswith('+91'):
            raise ValueError('Phone number must start with +91')
        if v and len(v) != 13:
            raise ValueError('Invalid Indian phone number format')
        return v


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(BaseModel):
    user_id: int
    name: str
    phone_number: Optional[str]
    email: Optional[str]
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
