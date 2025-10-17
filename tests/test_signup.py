"""
Tests for the signup functionality
"""
import pytest
from fastapi import status


class TestSignupEndpoint:
    """Test class for signup functionality"""
    
    def test_successful_signup(self, client, reset_activities, sample_email, sample_activity):
        """Test successful signup for an activity"""
        response = client.post(f"/activities/{sample_activity}/signup?email={sample_email}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "message" in data
        assert sample_email in data["message"]
        assert sample_activity in data["message"]
        
        # Verify the participant was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert sample_email in activities_data[sample_activity]["participants"]
    
    def test_signup_for_nonexistent_activity(self, client, reset_activities, sample_email):
        """Test signup for an activity that doesn't exist"""
        nonexistent_activity = "Nonexistent Activity"
        response = client.post(f"/activities/{nonexistent_activity}/signup?email={sample_email}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]
    
    def test_duplicate_signup_prevention(self, client, reset_activities):
        """Test that duplicate signups are prevented"""
        # Use an email that's already registered for Chess Club
        existing_email = "michael@mergington.edu"
        activity = "Chess Club"
        
        response = client.post(f"/activities/{activity}/signup?email={existing_email}")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]
    
    def test_signup_with_url_encoded_activity_name(self, client, reset_activities, sample_email):
        """Test signup with URL-encoded activity name (spaces)"""
        activity = "Chess Club"
        encoded_activity = "Chess%20Club"
        response = client.post(f"/activities/{encoded_activity}/signup?email={sample_email}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verify the participant was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert sample_email in activities_data[activity]["participants"]
    
    def test_signup_with_url_encoded_email(self, client, reset_activities):
        """Test signup with URL-encoded email"""
        email = "test+user@mergington.edu"
        encoded_email = "test%2Buser%40mergington.edu"
        activity = "Chess Club"
        
        response = client.post(f"/activities/{activity}/signup?email={encoded_email}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verify the participant was added with correct email
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity]["participants"]