from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GameBase(BaseModel):
    game_name: str
    game_type: str
    description: Optional[str] = None
    component_name: str


class GameCreate(GameBase):
    default_config_schema: Optional[str] = None


class GameUpdate(BaseModel):
    game_name: Optional[str] = None
    description: Optional[str] = None
    default_config_schema: Optional[str] = None
    is_active: Optional[bool] = None


class GameResponse(BaseModel):
    game_id: int
    game_name: str
    game_type: str
    description: Optional[str]
    component_name: str
    default_config_schema: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
