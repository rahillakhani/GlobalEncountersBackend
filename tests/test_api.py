import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.main import app
from app.db.session import get_db
from app.models.user import User

client = TestClient(app)

# Test data
TEST_USER = {
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "testpassword123"
}

@pytest.fixture
def test_db():
    """Create a test database session"""
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def test_user(test_db: Session):
    """Create a test user"""
    user = User(
        email=TEST_USER["email"],
        full_name=TEST_USER["full_name"],
        hashed_password=TEST_USER["password"]
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

# User endpoint tests
def test_create_user():
    """Test creating a new user"""
    response = client.post("/api/v1/users/", json=TEST_USER)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == TEST_USER["email"]
    assert data["full_name"] == TEST_USER["full_name"]

def test_get_users(test_user):
    """Test getting all users"""
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(user["email"] == TEST_USER["email"] for user in data)

def test_get_user(test_user):
    """Test getting a specific user"""
    response = client.get(f"/api/v1/users/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == TEST_USER["email"]
    assert data["full_name"] == TEST_USER["full_name"]

# Remove all audit log related test functions 