from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.game import GameCreate, GameUpdate, GameResponse
from app.models.game import Game
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
def create_game(
    game: GameCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add new game type to catalog (admin)."""
    
    # Check if game_type already exists
    existing = db.query(Game).filter(Game.game_type == game.game_type).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game type already exists"
        )
    
    db_game = Game(**game.model_dump())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    
    return db_game


@router.get("", response_model=List[GameResponse])
def list_games(
    include_inactive: bool = False,
    db: Session = Depends(get_db)
):
    """List all available game types."""
    query = db.query(Game)
    
    if not include_inactive:
        query = query.filter(Game.is_active == True)
    
    games = query.all()
    return games


@router.get("/{game_id}", response_model=GameResponse)
def get_game(game_id: int, db: Session = Depends(get_db)):
    """Get specific game details."""
    game = db.query(Game).filter(Game.game_id == game_id).first()
    
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    return game


@router.put("/{game_id}", response_model=GameResponse)
def update_game(
    game_id: int,
    game_update: GameUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update game type (admin)."""
    game = db.query(Game).filter(Game.game_id == game_id).first()
    
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    update_data = game_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(game, field, value)
    
    db.commit()
    db.refresh(game)
    
    return game


@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game(
    game_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete game type (admin)."""
    game = db.query(Game).filter(Game.game_id == game_id).first()
    
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    db.delete(game)
    db.commit()
    
    return None
