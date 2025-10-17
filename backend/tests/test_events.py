"""
Tests for event management endpoints
"""
import pytest
from datetime import datetime, timedelta


@pytest.mark.events
class TestEvents:
    
    def test_create_event(self, client, auth_headers):
        """Test creating a new event"""
        event_data = {
            "event_name": "New Baby Event",
            "event_date": (datetime.now() + timedelta(days=10)).isoformat(),
            "organizer_name": "John Doe",
            "organizer_contact": "+919876543210",
            "baby_name": "NewBaby",
            "total_levels": 5,
            "description": "A wonderful celebration"
        }
        
        response = client.post(
            "/api/events",
            json=event_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["event_name"] == "New Baby Event"
        assert "qr_code_token" in data
        assert len(data["qr_code_token"]) > 0
    
    def test_create_event_unauthorized(self, client):
        """Test creating event without authentication"""
        event_data = {
            "event_name": "Test",
            "event_date": datetime.now().isoformat(),
            "organizer_name": "Test",
            "organizer_contact": "+919999999999",
            "baby_name": "Test"
        }
        
        response = client.post("/api/events", json=event_data)
        assert response.status_code == 403
    
    def test_list_events(self, client, auth_headers, test_event):
        """Test listing all events"""
        response = client.get("/api/events", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["event_name"] == test_event.event_name
    
    def test_get_event_by_id(self, client, auth_headers, test_event):
        """Test getting event by ID"""
        response = client.get(
            f"/api/events/{test_event.event_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["event_id"] == test_event.event_id
        assert data["event_name"] == test_event.event_name
        assert "stats" in data
    
    def test_get_event_by_qr(self, client, test_event):
        """Test getting event by QR token (public endpoint)"""
        response = client.get(f"/api/events/qr/{test_event.qr_code_token}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["event_id"] == test_event.event_id
        assert data["is_active"] == True
    
    def test_get_event_by_invalid_qr(self, client):
        """Test getting event with invalid QR token"""
        response = client.get("/api/events/qr/invalid_token_xyz")
        
        assert response.status_code == 404
    
    def test_update_event(self, client, auth_headers, test_event):
        """Test updating an event"""
        response = client.put(
            f"/api/events/{test_event.event_id}",
            json={"event_name": "Updated Event Name"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["event_name"] == "Updated Event Name"
    
    def test_toggle_event_status(self, client, auth_headers, test_event):
        """Test activating/deactivating event"""
        response = client.patch(
            f"/api/events/{test_event.event_id}/activate",
            params={"is_active": False},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] == False
    
    def test_delete_event(self, client, auth_headers, test_event):
        """Test deleting an event"""
        response = client.delete(
            f"/api/events/{test_event.event_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify event is deleted
        get_response = client.get(
            f"/api/events/{test_event.event_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404
