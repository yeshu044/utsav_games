from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProgressStart(BaseModel):
    device_info: Optional[dict] = None


class ProgressUpdate(BaseModel):
    progress_id: int
    game_state: str  # JSON string


class ProgressComplete(BaseModel):
    progress_id: int
    result_data: str  # JSON string
    is_passed: bool


class ProgressResponse(BaseModel):
    progress_id: int
    level_id: int
    status: str
    attempts_count: int
    start_time: Optional[datetime]
    completion_time: Optional[datetime]
    time_taken_seconds: Optional[int]
    is_passed: bool
    
    class Config:
        from_attributes = True


class UserProgressSummary(BaseModel):
    event_id: int
    user_id: int
    total_levels: int
    completed_levels: int
    current_level: int
    total_time_seconds: int
    started_at: Optional[datetime]
    last_activity: Optional[datetime]
    level_progress: list
