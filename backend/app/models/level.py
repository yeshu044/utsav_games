from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class EventLevel(Base):
    __tablename__ = "event_levels"
    
    level_id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.event_id", ondelete="CASCADE"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.game_id"), nullable=False)
    level_number = Column(Integer, nullable=False)  # 1, 2, 3, 4, 5
    level_config = Column(Text, nullable=True)  # JSON string with game-specific config
    passing_criteria = Column(Text, nullable=True)  # JSON string
    max_retries = Column(Integer, default=-1)  # -1 = unlimited
    is_final_level = Column(Boolean, default=False)
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<EventLevel event_id={self.event_id} level={self.level_number}>"
