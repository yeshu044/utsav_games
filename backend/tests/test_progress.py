"""
Tests for user progress and leaderboard endpoints
"""
import pytest
import json
from app.models.progress import UserLevelProgress


@pytest.mark.progress
class TestProgress:
    
    def test_get_user_progress_empty(self, client, auth_headers, test_event):
        """Test getting progress when user hasn't started"""
        response = client.get(
            f"/api/events/{test_event.event_id}/progress",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["completed_levels"] == 0
        assert data["current_level"] == 1
    
    def test_start_level(self, client, auth_headers, test_event, test_level):
        """Test starting a level"""
        response = client.post(
            f"/api/events/{test_event.event_id}/levels/{test_level.level_id}/start",
            json={"device_info": {"platform": "iOS"}},
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["level_id"] == test_level.level_id
        assert data["status"] == "in_progress"
    
    def test_complete_level(self, client, auth_headers, db, test_user, test_event, test_level):
        """Test completing a level"""
        # First start the level
        progress = UserLevelProgress(
            user_id=test_user.user_id,
            event_id=test_event.event_id,
            level_id=test_level.level_id,
            status="in_progress",
            attempts_count=1
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
        
        # Complete it
        response = client.post(
            f"/api/events/{test_event.event_id}/levels/{test_level.level_id}/complete",
            json={
                "progress_id": progress.progress_id,
                "result_data": json.dumps({"score": 100}),
                "is_passed": True
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["is_passed"] == True
        assert "celebration" in data


@pytest.mark.leaderboard
class TestLeaderboard:
    
    def test_get_leaderboard_empty(self, client, auth_headers, test_event):
        """Test getting leaderboard with no participants"""
        response = client.get(
            f"/api/events/{test_event.event_id}/leaderboard",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_participants"] == 0
        assert len(data["leaderboard"]) == 0
    
    def test_get_leaderboard_with_participants(self, client, auth_headers, db, test_event, test_level, multiple_users):
        """Test leaderboard with multiple users"""
        # Create progress for multiple users
        for i, user in enumerate(multiple_users):
            progress = UserLevelProgress(
                user_id=user.user_id,
                event_id=test_event.event_id,
                level_id=test_level.level_id,
                status="completed",
                attempts_count=1,
                time_taken_seconds=100 + (i * 10),
                is_passed=True
            )
            db.add(progress)
        db.commit()
        
        response = client.get(
            f"/api/events/{test_event.event_id}/leaderboard",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_participants"] == len(multiple_users)
        assert len(data["leaderboard"]) == len(multiple_users)
        
        # Check ranking (fastest first)
        leaderboard = data["leaderboard"]
        assert leaderboard[0]["rank"] == 1
        assert leaderboard[0]["total_time_seconds"] == 100
        assert leaderboard[-1]["total_time_seconds"] == 100 + ((len(multiple_users) - 1) * 10)
    
    def test_get_my_rank(self, client, auth_headers, db, test_user, test_event, test_level):
        """Test getting current user's rank"""
        # Create progress for current user
        progress = UserLevelProgress(
            user_id=test_user.user_id,
            event_id=test_event.event_id,
            level_id=test_level.level_id,
            status="completed",
            time_taken_seconds=150,
            is_passed=True
        )
        db.add(progress)
        db.commit()
        
        response = client.get(
            f"/api/events/{test_event.event_id}/leaderboard/me",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == test_user.user_id
        assert data["rank"] == 1
        assert data["levels_completed"] == 1
