from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.event import (
    EventCreate, EventUpdate, EventResponse, 
    EventDetailResponse, EventPublicResponse
)
from app.models.event import Event
from app.utils.dependencies import get_current_user
from app.models.user import User
import base64

router = APIRouter()


def encrypt_name(name: str) -> str:
    """Simple base64 encoding (use proper encryption in production)."""
    return base64.b64encode(name.encode()).decode()


def decrypt_name(encrypted: str) -> str:
    """Simple base64 decoding."""
    return base64.b64decode(encrypted.encode()).decode()


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new event (admin only for now)."""
    
    # Encrypt baby name
    encrypted_name = encrypt_name(event.baby_name)
    
    # Generate QR token
    qr_token = Event.generate_qr_token()
    
    # Create event
    db_event = Event(
        event_name=event.event_name,
        event_date=event.event_date,
        organizer_name=event.organizer_name,
        organizer_contact=event.organizer_contact,
        baby_name_encrypted=encrypted_name,
        qr_code_token=qr_token,
        total_levels=event.total_levels,
        event_start_time=event.event_start_time,
        event_end_time=event.event_end_time,
        description=event.description,
        theme_config=event.theme_config
    )
    
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return db_event


@router.get("", response_model=List[EventResponse])
def list_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all events (admin)."""
    events = db.query(Event).offset(skip).limit(limit).all()
    return events


@router.get("/qr/{qr_token}", response_model=EventPublicResponse)
def get_event_by_qr(qr_token: str, db: Session = Depends(get_db)):
    """Get event details by QR code token (public endpoint)."""
    event = db.query(Event).filter(Event.qr_code_token == qr_token).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    if not event.is_active:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Event has ended"
        )
    
    return event


@router.get("/{event_id}", response_model=EventDetailResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get event details by ID (admin)."""
    event = db.query(Event).filter(Event.event_id == event_id).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Add stats (you can implement this later)
    event_dict = {
        **event.__dict__,
        "stats": {
            "total_participants": 0,
            "completed_all_levels": 0,
            "correct_name_guesses": 0
        }
    }
    
    return event_dict


@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    event_update: EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update event (admin)."""
    event = db.query(Event).filter(Event.event_id == event_id).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Update fields
    update_data = event_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)
    
    db.commit()
    db.refresh(event)
    
    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete event (admin)."""
    event = db.query(Event).filter(Event.event_id == event_id).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    db.delete(event)
    db.commit()
    
    return None


@router.patch("/{event_id}/activate", response_model=EventResponse)
def toggle_event_status(
    event_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Activate or deactivate event (admin)."""
    event = db.query(Event).filter(Event.event_id == event_id).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    event.is_active = is_active
    db.commit()
    db.refresh(event)
    
    return event
