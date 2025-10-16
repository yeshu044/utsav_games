from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import SendOTPRequest, VerifyOTPRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services.otp_service import create_otp, verify_otp, send_otp_sms
from app.services.auth_service import get_or_create_user, create_user_token
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/send-otp", status_code=200)
async def send_otp(request: SendOTPRequest, db: Session = Depends(get_db)):
    """Send OTP to phone number."""
    try:
        # Create OTP
        otp_record, otp_code = create_otp(db, request.phone_number)
        
        # Send OTP via SMS
        sms_sent = await send_otp_sms(request.phone_number, otp_code)
        
        if not sms_sent:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send OTP"
            )
        
        return {
            "message": "OTP sent successfully",
            "expires_in": 300,  # 5 minutes
            "phone_number": request.phone_number
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending OTP: {str(e)}"
        )


@router.post("/verify-otp", response_model=TokenResponse, status_code=200)
async def verify_otp_endpoint(
    request: VerifyOTPRequest,
    db: Session = Depends(get_db)
):
    """Verify OTP and login/register user."""
    
    # Verify OTP
    is_valid = verify_otp(db, request.phone_number, request.otp_code)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OTP"
        )
    
    # Check if user exists
    user = db.query(User).filter(User.phone_number == request.phone_number).first()
    
    # If new user, name is required
    if not user and not request.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name is required for new users"
        )
    
    # Get or create user
    user = get_or_create_user(db, request.phone_number, request.name)
    
    # Create token
    token_data = create_user_token(user)
    
    return token_data


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return current_user


@router.put("/me", response_model=UserResponse)
def update_me(
    name: str = None,
    email: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile."""
    if name:
        current_user.name = name
    if email:
        current_user.email = email
    
    db.commit()
    db.refresh(current_user)
    
    return current_user
