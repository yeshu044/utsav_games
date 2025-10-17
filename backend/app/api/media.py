from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.media import MediaUploadResponse, MediaAssetResponse
from app.models.media import MediaAsset
from app.models.event import Event
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/events/{event_id}/media", response_model=MediaUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_media(
    event_id: int,
    level_id: Optional[int] = Form(None),
    asset_type: str = Form(...),
    file_url: str = Form(...),  # For now, accept URL directly (Cloudinary URL)
    thumbnail_url: Optional[str] = Form(None),
    display_order: int = Form(0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload media asset for an event.
    For now, accepts pre-uploaded file URL (from Cloudinary, etc.)
    TODO: Implement actual file upload
    """
    
    # Verify event exists
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Create media record
    media = MediaAsset(
        event_id=event_id,
        level_id=level_id,
        asset_type=asset_type,
        file_url=file_url,
        thumbnail_url=thumbnail_url,
        display_order=display_order
    )
    
    db.add(media)
    db.commit()
    db.refresh(media)
    
    return media


@router.get("/events/{event_id}/media", response_model=List[MediaAssetResponse])
def get_event_media(
    event_id: int,
    level_id: Optional[int] = None,
    asset_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all media assets for an event."""
    
    query = db.query(MediaAsset).filter(MediaAsset.event_id == event_id)
    
    if level_id:
        query = query.filter(MediaAsset.level_id == level_id)
    
    if asset_type:
        query = query.filter(MediaAsset.asset_type == asset_type)
    
    media = query.order_by(MediaAsset.display_order).all()
    return media


@router.delete("/media/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_media(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete media asset."""
    
    media = db.query(MediaAsset).filter(MediaAsset.asset_id == asset_id).first()
    
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )
    
    db.delete(media)
    db.commit()
    
    return None
