import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_remove_participant():
    # Signup
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400

    # Remove participant
    response = client.post(f"/activities/{activity}/remove?email={email}")
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]

    # Remove again should fail
    response = client.post(f"/activities/{activity}/remove?email={email}")
    assert response.status_code == 404
