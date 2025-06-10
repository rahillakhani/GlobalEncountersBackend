import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.main import app
from app.db.session import get_db
from app.models.user import User
from app.models.audit_log import AuditLog

client = TestClient(app)

# Test data
TEST_USER = {
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "testpassword123"
}

TEST_AUDIT_LOG = {
    "registration_id": 123,
    "entitlement_type": "test_entitlement",
    "name": "Test Name",
    "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
    "lunch": 0,
    "dinner": 0
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

@pytest.fixture
def test_audit_log(test_db: Session):
    """Create a test audit log entry"""
    audit_log = AuditLog(
        registration_id=TEST_AUDIT_LOG["registration_id"],
        entitlement_type=TEST_AUDIT_LOG["entitlement_type"],
        name=TEST_AUDIT_LOG["name"],
        date=datetime.strptime(TEST_AUDIT_LOG["date"], "%Y-%m-%d"),
        lunch=TEST_AUDIT_LOG["lunch"],
        dinner=TEST_AUDIT_LOG["dinner"]
    )
    test_db.add(audit_log)
    test_db.commit()
    test_db.refresh(audit_log)
    return audit_log

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

# Audit Log endpoint tests
def test_get_audit_logs_by_registration(test_audit_log):
    """Test getting audit logs by registration ID"""
    response = client.get(f"/api/v1/audit-log/by-registration/{TEST_AUDIT_LOG['registration_id']}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["registration_id"] == TEST_AUDIT_LOG["registration_id"]

def test_search_audit_logs_by_schedule(test_audit_log):
    """Test searching audit logs by schedule"""
    response = client.get(
        f"/api/v1/audit-log/search?registrationid={TEST_AUDIT_LOG['registration_id']}&date={TEST_AUDIT_LOG['date']}"
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["registration_id"] == TEST_AUDIT_LOG["registration_id"]
    assert data[0]["date"] == TEST_AUDIT_LOG["date"]

def test_update_audit_log(test_audit_log):
    """Test updating audit log"""
    update_data = {
        "registrationid": TEST_AUDIT_LOG["registration_id"],
        "date": TEST_AUDIT_LOG["date"],
        "lunch_status": True,
        "dinner_status": True
    }
    response = client.post(
        "/api/v1/audit-log/update",
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["lunch"] == 1  # True is represented as 1
    assert data["dinner"] == 1  # True is represented as 1 