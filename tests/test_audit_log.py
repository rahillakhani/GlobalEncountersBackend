import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.main import app
from app.db.session import get_db
from app.models.audit_log import AuditLog
from app.core.security import create_access_token

client = TestClient(app)

# Test data
TEST_REGISTRATION_ID = 123
TEST_ENTITY_ID = 456
TEST_DATE = "2024-03-20"

def get_test_token():
    """Create a test token for authentication"""
    return create_access_token({"sub": "testuser"})

@pytest.fixture
def test_db():
    """Create a test database session"""
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def test_audit_log(test_db: Session):
    """Create a test audit log entry"""
    audit_log = AuditLog(
        registration_id=TEST_REGISTRATION_ID,
        entity_id=TEST_ENTITY_ID,
        date=datetime.strptime(TEST_DATE, "%Y-%m-%d").date(),
        lunch_status=False,
        dinner_status=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    test_db.add(audit_log)
    test_db.commit()
    test_db.refresh(audit_log)
    return audit_log

def test_get_audit_logs_by_registration(test_audit_log):
    """Test getting audit logs by registration ID"""
    response = client.get(f"/api/v1/audit-log/by-registration/{TEST_REGISTRATION_ID}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["registration_id"] == TEST_REGISTRATION_ID

def test_get_audit_logs_by_entity(test_audit_log):
    """Test getting audit logs by entity ID"""
    response = client.get(f"/api/v1/audit-log/by-entity/{TEST_ENTITY_ID}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["entity_id"] == TEST_ENTITY_ID

def test_search_audit_logs_by_schedule(test_audit_log):
    """Test searching audit logs by schedule"""
    token = get_test_token()
    response = client.get(
        f"/api/v1/audit-log/search?registrationid={TEST_REGISTRATION_ID}&date={TEST_DATE}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["registration_id"] == TEST_REGISTRATION_ID
    assert data[0]["date"] == TEST_DATE

def test_update_audit_log(test_audit_log):
    """Test updating audit log"""
    token = get_test_token()
    update_data = {
        "registrationid": TEST_REGISTRATION_ID,
        "date": TEST_DATE,
        "lunch_status": True,
        "dinner_status": True
    }
    response = client.post(
        "/api/v1/audit-log/update",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["lunch_status"] == True
    assert data["dinner_status"] == True

def test_unauthorized_access():
    """Test unauthorized access to protected endpoints"""
    # Test search endpoint without token
    response = client.get(
        f"/api/v1/audit-log/search?registrationid={TEST_REGISTRATION_ID}&date={TEST_DATE}"
    )
    assert response.status_code == 401

    # Test update endpoint without token
    update_data = {
        "registrationid": TEST_REGISTRATION_ID,
        "date": TEST_DATE,
        "lunch_status": True,
        "dinner_status": True
    }
    response = client.post("/api/v1/audit-log/update", json=update_data)
    assert response.status_code == 401

def test_invalid_token():
    """Test access with invalid token"""
    response = client.get(
        f"/api/v1/audit-log/search?registrationid={TEST_REGISTRATION_ID}&date={TEST_DATE}",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401 