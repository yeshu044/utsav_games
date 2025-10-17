from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class EventBase(BaseModel):
    event_name: str
    event_date: datetime
    organizer_name: str
    organizer_contact: str
    description: Optional[str] = None


class EventCreate(EventBase):
    baby_name: str  # Will be encrypted before storage
    total_levels: int = 5
    event_start_time: Optional[datetime] = None
    event_end_time: Optional[datetime] = None
    theme_config: Optional[str] = None


class EventUpdate(BaseModel):
    event_name: Optional[str] = None
    event_date: Optional[datetime] = None
    is_active: Optional[bool] = None
    event_end_time: Optional[datetime] = None
    description: Optional[str] = None


class EventResponse(BaseModel):
    event_id: int
    event_name: str
    event_date: datetime
    organizer_name: str
    qr_code_token: str
    total_levels: int
    is_active: bool
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class EventDetailResponse(EventResponse):
    organizer_contact: str
    event_start_time: Optional[datetime]
    event_end_time: Optional[datetime]
    theme_config: Optional[str]
    stats: Optional[dict] = None


class EventPublicResponse(BaseModel):
    """Public event info (accessed via QR code)"""
    event_id: int
    event_name: str
    event_date: datetime
    is_active: bool
    total_levels: int
    description: Optional[str]
    theme_config: Optional[str]
    
    class Config:
        from_attributes = True
