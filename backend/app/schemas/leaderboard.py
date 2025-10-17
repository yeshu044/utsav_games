from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: int
    name: str
    levels_completed: int
    total_time_seconds: int
    all_levels_completed: bool
    correct_name_guess: Optional[bool] = None
    completed_at: Optional[datetime]
    badge: Optional[str] = None


class LeaderboardResponse(BaseModel):
    event_id: int
    total_participants: int
    leaderboard: List[LeaderboardEntry]
    current_user_rank: Optional[int] = None
