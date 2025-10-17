"""
Tests for game catalog endpoints
"""
import pytest
import json


@pytest.mark.games
class TestGames:
    
    def test_create_game(self, client, auth_headers):
        """Test creating a new game type"""
        game_data = {
            "game_name": "Word Scramble",
            "game_type": "WORD_SCRAMBLE",
            "description": "Unscramble words",
            "component_name": "WordScrambleGame",
            "default_config_schema": json.dumps({"word_count": 5})
        }
        
        response = client.post(
            "/api/games",
            json=game_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["game_name"] == "Word Scramble"
        assert data["game_type"] == "WORD_SCRAMBLE"
        assert data["is_active"] == True
    
    def test_create_duplicate_game_type(self, client, auth_headers, test_game):
        """Test creating game with duplicate game_type"""
        game_data = {
            "game_name": "Duplicate",
            "game_type": test_game.game_type,  # Same as existing
            "component_name": "DuplicateGame"
        }
        
        response = client.post(
            "/api/games",
            json=game_data,
            headers=auth_headers
        )
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]
    
    def test_list_games(self, client, test_game):
        """Test listing all games (public endpoint)"""
        response = client.get("/api/games")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(g["game_id"] == test_game.game_id for g in data)
    
    def test_list_games_exclude_inactive(self, client, db, test_game):
        """Test listing only active games"""
        # Create inactive game
        inactive_game = test_game
        inactive_game.is_active = False
        db.commit()
        
        response = client.get("/api/games?include_inactive=false")
        
        assert response.status_code == 200
        data = response.json()
        assert not any(g["game_id"] == test_game.game_id for g in data)
    
    def test_get_game_by_id(self, client, test_game):
        """Test getting specific game"""
        response = client.get(f"/api/games/{test_game.game_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["game_id"] == test_game.game_id
        assert data["game_name"] == test_game.game_name
    
    def test_update_game(self, client, auth_headers, test_game):
        """Test updating game"""
        response = client.put(
            f"/api/games/{test_game.game_id}",
            json={"description": "Updated description"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Updated description"
    
    def test_delete_game(self, client, auth_headers, test_game):
        """Test deleting game"""
        response = client.delete(
            f"/api/games/{test_game.game_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
