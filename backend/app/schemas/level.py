from pydantic import BaseModel
from typing import Optional


class LevelBase(BaseModel):
    game_id: int
    level_number: int
    level_config: Optional[str] = None
    passing_criteria: Optional[str] = None


class LevelCreate(LevelBase):
    max_retries: int = -1
    is_final_level: bool = False


class LevelUpdate(BaseModel):
    level_config: Optional[str] = None
    passing_criteria: Optional[str] = None
    max_retries: Optional[int] = None
    is_enabled: Optional[bool] = None


class LevelResponse(BaseModel):
    level_id: int
    event_id: int
    game_id: int
    level_number: int
    level_config: Optional[str]
    passing_criteria: Optional[str]
    max_retries: int
    is_final_level: bool
    is_enabled: bool
    
    class Config:
        from_attributes = True


class LevelDetailResponse(LevelResponse):
    game_name: str
    game_type: str
    component_name: str
    is_unlocked: bool = False
    user_status: str = "locked"  # locked, not_started, in_progress, completed
    user_best_time: Optional[int] = None
    global_best_time: Optional[int] = None
