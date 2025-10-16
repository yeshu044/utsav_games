from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import create_access_token
from datetime import timedelta
from app.core.config import settings


def get_or_create_user(db: Session, phone_number: str, name: str = None) -> User:
    """Get existing user or create new one."""
    user = db.query(User).filter(User.phone_number == phone_number).first()
    
    if user:
        return user
    
    # Create new user
    user = User(
        name=name or "User",
        phone_number=phone_number,
        is_verified=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


def create_user_token(user: User) -> dict:
    """Create access token for user."""
    access_token = create_access_token(
        data={"sub": str(user.user_id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": {
            "user_id": user.user_id,
            "name": user.name,
            "phone_number": user.phone_number,
            "email": user.email
        }
    }
