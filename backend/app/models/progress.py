from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from app.database import Base


class UserLevelProgress(Base):
    __tablename__ = "user_level_progress"
    
    progress_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    event_id = Column(Integer, ForeignKey("events.event_id", ondelete="CASCADE"), nullable=False, index=True)
    level_id = Column(Integer, ForeignKey("event_levels.level_id", ondelete="CASCADE"), nullable=False)
    
    # Progress tracking
    status = Column(String(50), default="not_started")  # not_started, in_progress, completed, failed
    attempts_count = Column(Integer, default=0)
    
    # Timing
    start_time = Column(DateTime(timezone=True), nullable=True)
    completion_time = Column(DateTime(timezone=True), nullable=True)
    time_taken_seconds = Column(Integer, nullable=True)
    
    # Game state (for resume functionality)
    game_state = Column(Text, nullable=True)  # JSON string
    
    # Results
    result_data = Column(Text, nullable=True)  # JSON string with game-specific results
    is_passed = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Progress user={self.user_id} level={self.level_id} status={self.status}>"
