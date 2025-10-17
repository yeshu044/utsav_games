from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class MediaAsset(Base):
    __tablename__ = "media_assets"
    
    asset_id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.event_id", ondelete="CASCADE"), nullable=False)
    level_id = Column(Integer, ForeignKey("event_levels.level_id", ondelete="CASCADE"), nullable=True)
    
    asset_type = Column(String(100), nullable=False)  # MEMORY_CARD_IMAGE, PUZZLE_IMAGE, etc.
    file_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    display_order = Column(Integer, default=0)
    
    asset_metadata = Column(String(1000), nullable=True)  # Changed from 'metadata' to 'asset_metadata'
    
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<MediaAsset {self.asset_type} event={self.event_id}>"
