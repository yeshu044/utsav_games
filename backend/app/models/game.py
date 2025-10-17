from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Game(Base):
    __tablename__ = "games"
    
    game_id = Column(Integer, primary_key=True, index=True)
    game_name = Column(String(255), nullable=False)
    game_type = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    component_name = Column(String(100), nullable=False)  # React component name
    default_config_schema = Column(Text, nullable=True)  # JSON string
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Game {self.game_name} ({self.game_type})>"
