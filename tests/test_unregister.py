import pytest


def test_unregister_success(client):
    """Test successful unregistration from an activity"""
    activity = "Soccer Team"
    email = "alex@mergington.edu"  # Existing participant
    
    response = client.delete(
        f"/activities/{activity}/unregister?email={email}"
    )
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]


def test_unregister_activity_not_found(client):
    """Test unregister from non-existent activity"""
    response = client.delete(
        "/activities/Nonexistent Club/unregister?email=test@mergington.edu"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_not_registered(client):
    """Test unregister when student is not registered"""
    response = client.delete(
        "/activities/Gym Class/unregister?email=notregistered@mergington.edu"
    )
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_unregister_updates_participant_list(client):
    """Test that unregister updates the participant list"""
    activity = "Basketball Club"
    email = "chris@mergington.edu"  # Existing participant
    
    # Get initial count
    initial = client.get("/activities").json()
    initial_count = len(initial[activity]["participants"])
    
    # Unregister
    response = client.delete(
        f"/activities/{activity}/unregister?email={email}"
    )
    assert response.status_code == 200
    
    # Check updated count
    updated = client.get("/activities").json()
    assert len(updated[activity]["participants"]) == initial_count - 1
    assert email not in updated[activity]["participants"]
