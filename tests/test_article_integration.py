import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

article_route = "/v1/articles"

def test_article_integration(auth_header):
    # 1. CREATE article
    files = {
        "cover_image": ("cover.jpg", b"dummy_cover_content", "image/jpeg"),
    }
    data = {
        "title": "Test Article Integration",
        "content": "This is a test article content",
    }
    response = client.post(article_route, data=data, files=files, headers=auth_header)
    assert response.status_code == 200
    article = response.json()
    assert article["title"] == data["title"]
    article_id = article["id"]

    # 2. READ the created article
    response = client.get(f"{article_route}/{article_id}", headers=auth_header)
    assert response.status_code == 200
    article_data = response.json()
    assert article_data["id"] == article_id

    # 3. DELETE article
    response = client.delete(f"{article_route}/{article_id}", headers=auth_header)
    assert response.status_code == 200 or response.status_code == 204
    result = response.json()
    assert result["message"] == "Article deleted" or result.get("success") is True

    # 4. CONFIRM deletion
    response = client.get(f"{article_route}/{article_id}", headers=auth_header)
    assert response.status_code == 404
