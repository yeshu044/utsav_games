import random
import requests
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.otp import OTPVerification
from app.core.config import settings


def generate_otp() -> str:
    """Generate a 6-digit OTP."""
    return str(random.randint(100000, 999999))


async def send_otp_sms(phone_number: str, otp_code: str) -> bool:
    """
    Send OTP via MSG91 SMS service.
    For development, just print to console.
    """
    if settings.ENVIRONMENT == "development" or not settings.MSG91_AUTH_KEY:
        # Development mode - just print OTP
        print(f"\n{'='*50}")
        print(f"📱 OTP for {phone_number}: {otp_code}")
        print(f"{'='*50}\n")
        return True
    
    # Production - Send via MSG91
    try:
        url = "https://api.msg91.com/api/v5/otp"
        
        payload = {
            "template_id": settings.MSG91_TEMPLATE_ID,
            "mobile": phone_number,
            "authkey": settings.MSG91_AUTH_KEY,
            "otp": otp_code
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return False


def create_otp(db: Session, phone_number: str) -> tuple[OTPVerification, str]:
    """
    Create and store OTP in database.
    Returns (OTPVerification object, otp_code)
    """
    # Invalidate any existing OTPs for this phone number
    db.query(OTPVerification).filter(
        OTPVerification.phone_number == phone_number,
        OTPVerification.is_verified == False
    ).update({"is_verified": True})
    
    # Generate new OTP
    otp_code = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
    
    # Create OTP record
    otp_record = OTPVerification(
        phone_number=phone_number,
        otp_code=otp_code,
        expires_at=expires_at
    )
    
    db.add(otp_record)
    db.commit()
    db.refresh(otp_record)
    
    return otp_record, otp_code


def verify_otp(db: Session, phone_number: str, otp_code: str) -> bool:
    """Verify OTP code."""
    otp_record = db.query(OTPVerification).filter(
        OTPVerification.phone_number == phone_number,
        OTPVerification.otp_code == otp_code,
        OTPVerification.is_verified == False
    ).first()
    
    if not otp_record:
        return False
    
    if otp_record.is_expired():
        return False
    
    # Mark as verified
    otp_record.is_verified = True
    db.commit()
    
    return True
