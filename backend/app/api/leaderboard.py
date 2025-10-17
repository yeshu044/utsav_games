from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional
from app.database import get_db
from app.schemas.leaderboard import LeaderboardResponse, LeaderboardEntry
from app.models.progress import UserLevelProgress
from app.models.user import User
from app.models.event import Event
from app.models.level import EventLevel  # ← Added this import
from app.utils.dependencies import get_current_user
import json

router = APIRouter()


@router.get("/events/{event_id}/leaderboard", response_model=LeaderboardResponse)
def get_leaderboard(
    event_id: int,
    filter: str = "all",  # all, completed, correct_guess
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get event leaderboard.
    Simple API that can be polled every 10-15 seconds by frontend.
    """
    
    # Verify event exists
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Get all users who participated
    participants = db.query(
        UserLevelProgress.user_id
    ).filter(
        UserLevelProgress.event_id == event_id
    ).distinct().count()
    
    # Build leaderboard query
    # Get users with their completion stats
    subquery = db.query(
        UserLevelProgress.user_id,
        func.count(UserLevelProgress.progress_id).label('levels_completed'),
        func.sum(UserLevelProgress.time_taken_seconds).label('total_time'),
        func.max(UserLevelProgress.completion_time).label('last_completed')
    ).filter(
        UserLevelProgress.event_id == event_id,
        UserLevelProgress.status == "completed"
    ).group_by(UserLevelProgress.user_id).subquery()
    
    # Join with User table
    leaderboard_query = db.query(
        User.user_id,
        User.name,
        subquery.c.levels_completed,
        subquery.c.total_time,
        subquery.c.last_completed
    ).join(
        subquery, User.user_id == subquery.c.user_id
    ).order_by(
        subquery.c.levels_completed.desc(),
        subquery.c.total_time.asc()
    )
    
    # Apply filters
    if filter == "completed":
        leaderboard_query = leaderboard_query.filter(
            subquery.c.levels_completed == event.total_levels
        )
    
    # Get results
    results = leaderboard_query.offset(offset).limit(limit).all()
    
    # Build leaderboard entries
    leaderboard = []
    for rank, (user_id, name, levels_completed, total_time, last_completed) in enumerate(results, start=offset + 1):
        # Check if name guess was correct (for final level)
        final_progress = db.query(UserLevelProgress).join(
            EventLevel
        ).filter(
            UserLevelProgress.user_id == user_id,
            UserLevelProgress.event_id == event_id,
            EventLevel.is_final_level == True,
            UserLevelProgress.status == "completed"
        ).first()
        
        correct_guess = None
        if final_progress and final_progress.result_data:
            try:
                result = json.loads(final_progress.result_data)
                correct_guess = result.get("is_correct", False)
            except:
                pass
        
        # Assign badges
        badge = None
        if rank == 1:
            badge = "🥇"
        elif rank == 2:
            badge = "🥈"
        elif rank == 3:
            badge = "🥉"
        
        entry = LeaderboardEntry(
            rank=rank,
            user_id=user_id,
            name=name,
            levels_completed=levels_completed,
            total_time_seconds=total_time or 0,
            all_levels_completed=levels_completed == event.total_levels,
            correct_name_guess=correct_guess,
            completed_at=last_completed,
            badge=badge
        )
        
        leaderboard.append(entry)
    
    # Find current user's rank
    current_user_rank = None
    for entry in leaderboard:
        if entry.user_id == current_user.user_id:
            current_user_rank = entry.rank
            break
    
    return LeaderboardResponse(
        event_id=event_id,
        total_participants=participants,
        leaderboard=leaderboard,
        current_user_rank=current_user_rank
    )


@router.get("/events/{event_id}/leaderboard/me")
def get_my_rank(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's rank in leaderboard."""
    
    # Get all completed users ordered by completion
    all_users = db.query(
        UserLevelProgress.user_id,
        func.count(UserLevelProgress.progress_id).label('levels_completed'),
        func.sum(UserLevelProgress.time_taken_seconds).label('total_time')
    ).filter(
        UserLevelProgress.event_id == event_id,
        UserLevelProgress.status == "completed"
    ).group_by(
        UserLevelProgress.user_id
    ).order_by(
        func.count(UserLevelProgress.progress_id).desc(),
        func.sum(UserLevelProgress.time_taken_seconds).asc()
    ).all()
    
    # Find current user's rank
    for rank, (user_id, levels, time) in enumerate(all_users, start=1):
        if user_id == current_user.user_id:
            return {
                "user_id": current_user.user_id,
                "rank": rank,
                "levels_completed": levels,
                "total_time_seconds": time or 0,
                "total_participants": len(all_users)
            }
    
    # User hasn't completed any levels
    return {
        "user_id": current_user.user_id,
        "rank": None,
        "levels_completed": 0,
        "total_time_seconds": 0,
        "total_participants": len(all_users)
    }
