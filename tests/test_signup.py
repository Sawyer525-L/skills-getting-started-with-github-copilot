import pytest


def test_signup_success(client):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Chess Club/signup?email=test@mergington.edu"
    )
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]


def test_signup_activity_not_found(client):
    """Test signup for non-existent activity"""
    response = client.post(
        "/activities/Nonexistent Club/signup?email=test@mergington.edu"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_duplicate_registration(client):
    """Test that same student cannot register twice"""
    email = "duplicate@mergington.edu"
    activity = "Programming Class"
    
    # First signup should succeed
    response1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response1.status_code == 200
    
    # Second signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]


def test_signup_updates_participant_list(client):
    """Test that signup updates the participant list"""
    email = "newstudent@mergington.edu"
    activity = "Art Studio"
    
    # Get initial count
    initial = client.get("/activities").json()
    initial_count = len(initial[activity]["participants"])
    
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    
    # Check updated count
    updated = client.get("/activities").json()
    assert len(updated[activity]["participants"]) == initial_count + 1
    assert email in updated[activity]["participants"]
