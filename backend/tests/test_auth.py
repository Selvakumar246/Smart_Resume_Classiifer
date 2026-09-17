from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import get_current_user
from app.db.models import User

client = TestClient(app)

def test_missing_auth_header_returns_401():
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    assert "detail" in response.json()

def test_invalid_auth_token_returns_401():
    response = client.get("/api/v1/users/me", headers={"Authorization": "Bearer invalidtokenhere"})
    assert response.status_code == 401
