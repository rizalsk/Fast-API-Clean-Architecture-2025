import pytest
from fastapi.testclient import TestClient
from app.main import app

# TestClient global untuk semua test
@pytest.fixture(scope="session")
def client():
    return TestClient(app)

# Fixture for user login data
@pytest.fixture
def test_user_data():
    return {
        "email": "bob@mail.com",
        "password": "password"
    }

@pytest.fixture
def login_route():
    return "/auth/login"

# Fixture untuk login user
@pytest.fixture
def login_test(client, test_user_data):
    """
    Fixture untuk login user.
    Mengembalikan function yang menerima username dan password,
    lalu mengembalikan response JSON termasuk access token.
    """
    def _login(email=None, password=None):
        email = email or test_user_data["email"]
        password = password or test_user_data["password"]
        response = client.post(
            "/auth/login",
            json={"email": email, "password": password}
        )
        assert response.status_code == 200
        return response.json()
    return _login

@pytest.fixture
def auth_header(login_test):
    token_data = login_test()
    return {"Authorization": f"Bearer {token_data['access_token']}"}