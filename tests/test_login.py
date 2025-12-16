import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
login_route = "auth/login"

def test_login_success(client, test_user_data):
    response = client.post(login_route, json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure():
    response = client.post(
        login_route,
        json={"email": "bob@mail.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid credentials"
