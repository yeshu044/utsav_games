from pydantic import BaseModel, field_validator
from typing import Optional


class SendOTPRequest(BaseModel):
    phone_number: str
    
    @field_validator('phone_number')
    @classmethod
    def validate_phone(cls, v):
        if not v.startswith('+91'):
            raise ValueError('Phone number must start with +91')
        if len(v) != 13:
            raise ValueError('Invalid Indian phone number format')
        return v


class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp_code: str
    name: Optional[str] = None  # Required for new users
    
    @field_validator('otp_code')
    @classmethod
    def validate_otp(cls, v):
        if len(v) != 6 or not v.isdigit():
            raise ValueError('OTP must be 6 digits')
        return v


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict


class GoogleAuthRequest(BaseModel):
    id_token: str
