"""
Tests for authentication endpoints
"""
import pytest
from app.models.otp import OTPVerification
from datetime import datetime, timedelta


@pytest.mark.auth
class TestAuthentication:
    
    def test_send_otp_success(self, client, db):
        """Test sending OTP to valid phone number"""
        response = client.post(
            "/api/auth/send-otp",
            json={"phone_number": "+919876543210"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "OTP sent successfully"
        assert data["expires_in"] == 300
        
        # Verify OTP was created in database
        otp = db.query(OTPVerification).filter(
            OTPVerification.phone_number == "+919876543210"
        ).first()
        assert otp is not None
        assert len(otp.otp_code) == 6
    
    def test_send_otp_invalid_phone(self, client):
        """Test sending OTP with invalid phone number"""
        response = client.post(
            "/api/auth/send-otp",
            json={"phone_number": "1234567890"}  # Missing +91
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_verify_otp_new_user(self, client, db):
        """Test OTP verification for new user"""
        # Create OTP
        otp = OTPVerification(
            phone_number="+919876543210",
            otp_code="123456",
            expires_at=datetime.utcnow() + timedelta(minutes=5),
            is_verified=False
        )
        db.add(otp)
        db.commit()
        
        # Verify OTP
        response = client.post(
            "/api/auth/verify-otp",
            json={
                "phone_number": "+919876543210",
                "otp_code": "123456",
                "name": "New User"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["name"] == "New User"
        assert data["user"]["phone_number"] == "+919876543210"
    
    def test_verify_otp_existing_user(self, client, db, test_user):
        """Test OTP verification for existing user"""
        # Create OTP
        otp = OTPVerification(
            phone_number=test_user.phone_number,
            otp_code="123456",
            expires_at=datetime.utcnow() + timedelta(minutes=5),
            is_verified=False
        )
        db.add(otp)
        db.commit()
        
        # Verify OTP (no name needed for existing user)
        response = client.post(
            "/api/auth/verify-otp",
            json={
                "phone_number": test_user.phone_number,
                "otp_code": "123456"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["user_id"] == test_user.user_id
    
    def test_verify_otp_invalid(self, client, db):
        """Test OTP verification with wrong code"""
        response = client.post(
            "/api/auth/verify-otp",
            json={
                "phone_number": "+919876543210",
                "otp_code": "999999",
                "name": "Test User"
            }
        )
        
        assert response.status_code == 401
        assert "Invalid or expired OTP" in response.json()["detail"]
    
    def test_verify_otp_expired(self, client, db):
        """Test OTP verification with expired OTP"""
        # Create expired OTP
        otp = OTPVerification(
            phone_number="+919876543210",
            otp_code="123456",
            expires_at=datetime.utcnow() - timedelta(minutes=1),  # Expired
            is_verified=False
        )
        db.add(otp)
        db.commit()
        
        response = client.post(
            "/api/auth/verify-otp",
            json={
                "phone_number": "+919876543210",
                "otp_code": "123456",
                "name": "Test User"
            }
        )
        
        assert response.status_code == 401
    
    def test_get_current_user(self, client, auth_headers, test_user):
        """Test getting current user profile"""
        response = client.get("/api/auth/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == test_user.user_id
        assert data["name"] == test_user.name
        assert data["phone_number"] == test_user.phone_number
    
    def test_get_current_user_no_token(self, client):
        """Test getting user without authentication"""
        response = client.get("/api/auth/me")
        
        assert response.status_code == 403  # Forbidden
    
    def test_update_user_profile(self, client, auth_headers, test_user):
        """Test updating user profile"""
        response = client.put(
            "/api/auth/me",
            headers=auth_headers,
            params={"name": "Updated Name", "email": "updated@example.com"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["email"] == "updated@example.com"
