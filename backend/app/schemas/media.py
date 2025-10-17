from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MediaUploadResponse(BaseModel):
    asset_id: int
    event_id: int
    level_id: Optional[int]
    asset_type: str
    file_url: str
    thumbnail_url: Optional[str]
    uploaded_at: datetime
    
    class Config:
        from_attributes = True


class MediaAssetResponse(BaseModel):
    asset_id: int
    level_id: Optional[int]
    asset_type: str
    file_url: str
    thumbnail_url: Optional[str]
    display_order: int
    uploaded_at: datetime
    
    class Config:
        from_attributes = True
