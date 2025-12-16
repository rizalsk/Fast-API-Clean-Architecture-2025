
def test_login_success(client, test_user_data, login_route):
    response = client.post(login_route, json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_fail_wrong_password(client, test_user_data, login_route):
    wrong_data = test_user_data.copy()
    wrong_data["password"] = "wrongpassword"
    response = client.post(login_route, json=wrong_data)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Incorrect email or password"

def test_login_fail_nonexistent_user(client, login_route):
    response = client.post(login_route, json={"email": "nouser", "password": "123"})
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Incorrect email or password"
