from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List
from app.database import get_db
from app.schemas.progress import (
    ProgressStart, ProgressUpdate, ProgressComplete,
    ProgressResponse, UserProgressSummary
)
from app.models.progress import UserLevelProgress
from app.models.level import EventLevel
from app.models.event import Event
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/events/{event_id}/progress", response_model=UserProgressSummary)
def get_user_progress(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's overall progress in an event."""
    
    # Verify event exists
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Get all levels for this event
    levels = db.query(EventLevel).filter(
        EventLevel.event_id == event_id,
        EventLevel.is_enabled == True
    ).order_by(EventLevel.level_number).all()
    
    # Get user's progress for each level
    progress_records = db.query(UserLevelProgress).filter(
        UserLevelProgress.event_id == event_id,
        UserLevelProgress.user_id == current_user.user_id
    ).all()
    
    # Create progress map
    progress_map = {p.level_id: p for p in progress_records}
    
    # Build level progress
    level_progress = []
    completed_levels = 0
    total_time = 0
    current_level = 1
    
    for level in levels:
        progress = progress_map.get(level.level_id)
        
        if progress:
            level_data = {
                "level_id": level.level_id,
                "level_number": level.level_number,
                "status": progress.status,
                "attempts_count": progress.attempts_count,
                "time_taken_seconds": progress.time_taken_seconds,
                "completed_at": progress.completion_time
            }
            
            if progress.status == "completed":
                completed_levels += 1
                if progress.time_taken_seconds:
                    total_time += progress.time_taken_seconds
            else:
                current_level = level.level_number
        else:
            level_data = {
                "level_id": level.level_id,
                "level_number": level.level_number,
                "status": "locked" if level.level_number > current_level else "not_started"
            }
        
        level_progress.append(level_data)
    
    # Get first and last activity
    first_progress = min(progress_records, key=lambda x: x.created_at) if progress_records else None
    last_progress = max(progress_records, key=lambda x: x.updated_at) if progress_records else None
    
    return {
        "event_id": event_id,
        "user_id": current_user.user_id,
        "total_levels": len(levels),
        "completed_levels": completed_levels,
        "current_level": current_level,
        "total_time_seconds": total_time,
        "started_at": first_progress.created_at if first_progress else None,
        "last_activity": last_progress.updated_at if last_progress else None,
        "level_progress": level_progress
    }


@router.post("/events/{event_id}/levels/{level_id}/start", response_model=ProgressResponse, status_code=status.HTTP_201_CREATED)
def start_level(
    event_id: int,
    level_id: int,
    request: ProgressStart,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start playing a level."""
    
    # Verify level exists
    level = db.query(EventLevel).filter(
        EventLevel.level_id == level_id,
        EventLevel.event_id == event_id
    ).first()
    
    if not level:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Level not found"
        )
    
    # Check if previous level is completed (except for level 1)
    if level.level_number > 1:
        prev_level = db.query(EventLevel).filter(
            EventLevel.event_id == event_id,
            EventLevel.level_number == level.level_number - 1
        ).first()
        
        if prev_level:
            prev_progress = db.query(UserLevelProgress).filter(
                UserLevelProgress.user_id == current_user.user_id,
                UserLevelProgress.level_id == prev_level.level_id,
                UserLevelProgress.status == "completed"
            ).first()
            
            if not prev_progress:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Previous level not completed"
                )
    
    # Create or update progress record
    existing_progress = db.query(UserLevelProgress).filter(
        UserLevelProgress.user_id == current_user.user_id,
        UserLevelProgress.level_id == level_id,
        UserLevelProgress.status == "in_progress"
    ).first()
    
    if existing_progress:
        return existing_progress
    
    # Create new progress record
    progress = UserLevelProgress(
        user_id=current_user.user_id,
        event_id=event_id,
        level_id=level_id,
        status="in_progress",
        attempts_count=1,
        start_time=datetime.utcnow()
    )
    
    db.add(progress)
    db.commit()
    db.refresh(progress)
    
    return progress


@router.put("/events/{event_id}/levels/{level_id}/progress")
def update_progress(
    event_id: int,
    level_id: int,
    update: ProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update game state during gameplay (for resume)."""
    
    progress = db.query(UserLevelProgress).filter(
        UserLevelProgress.progress_id == update.progress_id,
        UserLevelProgress.user_id == current_user.user_id,
        UserLevelProgress.level_id == level_id
    ).first()
    
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress not found"
        )
    
    progress.game_state = update.game_state
    db.commit()
    
    return {"message": "Progress saved", "progress_id": progress.progress_id}


@router.post("/events/{event_id}/levels/{level_id}/complete", response_model=dict)
def complete_level(
    event_id: int,
    level_id: int,
    completion: ProgressComplete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit level completion."""
    
    progress = db.query(UserLevelProgress).filter(
        UserLevelProgress.progress_id == completion.progress_id,
        UserLevelProgress.user_id == current_user.user_id,
        UserLevelProgress.level_id == level_id
    ).first()
    
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress not found"
        )
    
    # Calculate time taken
    if progress.start_time:
        time_taken = int((datetime.utcnow() - progress.start_time).total_seconds())
    else:
        time_taken = 0
    
    # Update progress
    progress.status = "completed" if completion.is_passed else "failed"
    progress.completion_time = datetime.utcnow()
    progress.time_taken_seconds = time_taken
    progress.result_data = completion.result_data
    progress.is_passed = completion.is_passed
    
    db.commit()
    db.refresh(progress)
    
    # Get next level info
    level = db.query(EventLevel).filter(EventLevel.level_id == level_id).first()
    next_level = db.query(EventLevel).filter(
        EventLevel.event_id == event_id,
        EventLevel.level_number == level.level_number + 1
    ).first()
    
    # Calculate leaderboard rank
    rank = db.query(func.count(UserLevelProgress.user_id.distinct())).filter(
        UserLevelProgress.event_id == event_id,
        UserLevelProgress.status == "completed"
    ).scalar()
    
    response = {
        "progress_id": progress.progress_id,
        "level_id": level_id,
        "status": progress.status,
        "time_taken_seconds": time_taken,
        "is_passed": completion.is_passed,
        "completed_at": progress.completion_time,
        "leaderboard_rank": rank or 1,
        "celebration": {
            "message": "🎉 Great job! Level completed!" if completion.is_passed else "Try again!",
            "stars": 3 if completion.is_passed else 0,
            "is_personal_best": True
        }
    }
    
    if next_level:
        response["next_level"] = {
            "level_id": next_level.level_id,
            "level_number": next_level.level_number,
            "is_unlocked": True
        }
    
    return response


@router.get("/events/{event_id}/levels/{level_id}/attempts", response_model=List[ProgressResponse])
def get_attempt_history(
    event_id: int,
    level_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get attempt history for a level."""
    
    attempts = db.query(UserLevelProgress).filter(
        UserLevelProgress.user_id == current_user.user_id,
        UserLevelProgress.event_id == event_id,
        UserLevelProgress.level_id == level_id
    ).order_by(UserLevelProgress.created_at).all()
    
    return attempts
