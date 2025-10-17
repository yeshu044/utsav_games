from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from app.database import Base
import secrets


class Event(Base):
    __tablename__ = "events"
    
    event_id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String(255), nullable=False)
    event_date = Column(DateTime(timezone=True), nullable=False)
    organizer_name = Column(String(255), nullable=False)
    organizer_contact = Column(String(20), nullable=False)
    baby_name_encrypted = Column(String(255), nullable=False)  # The correct answer
    qr_code_token = Column(String(100), unique=True, index=True, nullable=False)
    total_levels = Column(Integer, default=5)
    is_active = Column(Boolean, default=True)
    event_start_time = Column(DateTime(timezone=True), nullable=True)
    event_end_time = Column(DateTime(timezone=True), nullable=True)
    description = Column(Text, nullable=True)
    theme_config = Column(Text, nullable=True)  # JSON string for theme colors
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    @staticmethod
    def generate_qr_token():
        """Generate unique QR code token."""
        return secrets.token_urlsafe(16)
    
    def __repr__(self):
        return f"<Event {self.event_name} ({self.event_id})>"
