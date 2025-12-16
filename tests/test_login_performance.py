import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_performance(benchmark, test_user_data, login_route):
    def do_login():
        response = client.post(login_route, json=test_user_data)
        assert response.status_code == 200
        json_data = response.json()
        assert "access_token" in json_data
        assert "token_type" in json_data

    benchmark(do_login)
