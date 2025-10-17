"""
Tests for the main application endpoints
"""
import pytest
from fastapi import status


class TestMainEndpoints:
    """Test class for main application endpoints"""
    
    def test_root_endpoint_redirects_to_static(self, client):
        """Test that root endpoint redirects to static index.html"""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        # Check if it's serving the HTML content
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """Test that /activities endpoint returns all activities"""
        response = client.get("/activities")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, dict)
        
        # Check that we have the expected activities
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Soccer Team",
            "Basketball Club", "Art Workshop", "Drama Club", "Math Olympiad", "Science Club"
        ]
        
        for activity in expected_activities:
            assert activity in data
            
        # Check structure of an activity
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)
    
    def test_activities_have_correct_structure(self, client, reset_activities):
        """Test that each activity has the correct data structure"""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_name, str)
            assert isinstance(activity_data, dict)
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)
            assert activity_data["max_participants"] > 0