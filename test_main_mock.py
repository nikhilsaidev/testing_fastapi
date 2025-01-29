import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main_mock import app, Database

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_db():
    """Mock Database instance"""
    mock = MagicMock()
    mock.get_user.return_value = {"name": "Mocked User", "email": "mock@example.com"}
    mock.create_user.return_value = {"id": 99, "name": "Mocked User", "email": "mock@example.com"}
    return mock

def test_mock_get_user(client, mock_db, monkeypatch):
    """Test retrieving a user using mock"""
    monkeypatch.setattr(Database, "get_user", mock_db.get_user)

    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Mocked User"

def test_mock_create_user(client, mock_db, monkeypatch):
    """Test creating a user using mock"""
    monkeypatch.setattr(Database, "create_user", mock_db.create_user)

    new_user = {"name": "Charlie", "email": "charlie@example.com"}
    response = client.post("/users", json=new_user)

    assert response.status_code == 200
    assert response.json()["id"] == 99
    assert response.json()["name"] == "Mocked User"

####################################
# How This Works
# Mocking the Database:
#       MagicMock() creates a fake database instance.
#       .get_user.return_value sets what the mock should return.
# Monkeypatching (monkeypatch.setattr):
#       Replaces Database.get_user and Database.create_user with mocked versions.
# Mocked Responses:
#       test_mock_get_user: Fetches a mocked user.
#       test_mock_create_user: Mocks creating a user.