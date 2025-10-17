from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.level import LevelCreate, LevelUpdate, LevelResponse, LevelDetailResponse
from app.models.level import EventLevel
from app.models.game import Game
from app.models.event import Event
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/events/{event_id}/levels", response_model=LevelResponse, status_code=status.HTTP_201_CREATED)
def add_level_to_event(
    event_id: int,
    level: LevelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a game level to an event (admin)."""
    
    # Verify event exists
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Verify game exists
    game = db.query(Game).filter(Game.game_id == level.game_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    # Check if level number already exists for this event
    existing = db.query(EventLevel).filter(
        EventLevel.event_id == event_id,
        EventLevel.level_number == level.level_number
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Level {level.level_number} already exists for this event"
        )
    
    # Create level
    db_level = EventLevel(
        event_id=event_id,
        **level.model_dump()
    )
    
    db.add(db_level)
    db.commit()
    db.refresh(db_level)
    
    return db_level


@router.get("/events/{event_id}/levels", response_model=List[LevelDetailResponse])
def get_event_levels(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Get all levels for an event."""
    
    # Verify event exists
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Get levels with game info
    levels = db.query(EventLevel, Game).join(
        Game, EventLevel.game_id == Game.game_id
    ).filter(
        EventLevel.event_id == event_id,
        EventLevel.is_enabled == True
    ).order_by(EventLevel.level_number).all()
    
    result = []
    for level, game in levels:
        level_dict = {
            **level.__dict__,
            "game_name": game.game_name,
            "game_type": game.game_type,
            "component_name": game.component_name,
            "is_unlocked": level.level_number == 1,  # TODO: Check user progress
            "user_status": "not_started",  # TODO: Get from user progress
        }
        result.append(level_dict)
    
    return result


@router.get("/events/{event_id}/levels/{level_id}", response_model=LevelDetailResponse)
def get_level(
    event_id: int,
    level_id: int,
    db: Session = Depends(get_db)
):
    """Get specific level details."""
    
    level = db.query(EventLevel, Game).join(
        Game, EventLevel.game_id == Game.game_id
    ).filter(
        EventLevel.level_id == level_id,
        EventLevel.event_id == event_id
    ).first()
    
    if not level:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Level not found"
        )
    
    event_level, game = level
    
    level_dict = {
        **event_level.__dict__,
        "game_name": game.game_name,
        "game_type": game.game_type,
        "component_name": game.component_name,
        "is_unlocked": True,  # TODO: Check user progress
        "user_status": "not_started",  # TODO: Get from user progress
    }
    
    return level_dict


@router.put("/events/{event_id}/levels/{level_id}", response_model=LevelResponse)
def update_level(
    event_id: int,
    level_id: int,
    level_update: LevelUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update level configuration (admin)."""
    
    level = db.query(EventLevel).filter(
        EventLevel.level_id == level_id,
        EventLevel.event_id == event_id
    ).first()
    
    if not level:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Level not found"
        )
    
    update_data = level_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(level, field, value)
    
    db.commit()
    db.refresh(level)
    
    return level


@router.delete("/events/{event_id}/levels/{level_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_level(
    event_id: int,
    level_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove level from event (admin)."""
    
    level = db.query(EventLevel).filter(
        EventLevel.level_id == level_id,
        EventLevel.event_id == event_id
    ).first()
    
    if not level:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Level not found"
        )
    
    db.delete(level)
    db.commit()
    
    return None