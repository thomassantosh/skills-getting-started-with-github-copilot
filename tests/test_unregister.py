"""
Tests for the unregister functionality
"""
import pytest
from fastapi import status


class TestUnregisterEndpoint:
    """Test class for unregister functionality"""
    
    def test_successful_unregister(self, client, reset_activities):
        """Test successful unregistration from an activity"""
        # Use an existing participant
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # Verify participant is initially registered
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity]["participants"]
        
        # Unregister
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]
        
        # Verify the participant was removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email not in activities_data[activity]["participants"]
    
    def test_unregister_from_nonexistent_activity(self, client, reset_activities):
        """Test unregistration from an activity that doesn't exist"""
        email = "test@mergington.edu"
        nonexistent_activity = "Nonexistent Activity"
        
        response = client.delete(f"/activities/{nonexistent_activity}/unregister?email={email}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]
    
    def test_unregister_non_registered_participant(self, client, reset_activities):
        """Test unregistration of a participant who isn't registered"""
        email = "notregistered@mergington.edu"
        activity = "Chess Club"
        
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        data = response.json()
        assert "detail" in data
        assert "not registered" in data["detail"]
    
    def test_unregister_with_url_encoded_activity_name(self, client, reset_activities):
        """Test unregistration with URL-encoded activity name"""
        email = "michael@mergington.edu"
        activity = "Chess Club"
        encoded_activity = "Chess%20Club"
        
        response = client.delete(f"/activities/{encoded_activity}/unregister?email={email}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verify the participant was removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email not in activities_data[activity]["participants"]
    
    def test_signup_then_unregister_workflow(self, client, reset_activities):
        """Test complete workflow of signup followed by unregister"""
        email = "test@mergington.edu"
        activity = "Chess Club"
        
        # First signup
        signup_response = client.post(f"/activities/{activity}/signup?email={email}")
        assert signup_response.status_code == status.HTTP_200_OK
        
        # Verify registration
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity]["participants"]
        
        # Then unregister
        unregister_response = client.delete(f"/activities/{activity}/unregister?email={email}")
        assert unregister_response.status_code == status.HTTP_200_OK
        
        # Verify unregistration
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email not in activities_data[activity]["participants"]