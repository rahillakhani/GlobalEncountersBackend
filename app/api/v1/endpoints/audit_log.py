from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.session import get_db
from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogSchema, AuditLogUpdate
from app.crud import audit_log as crud

router = APIRouter()

@router.get("/by-registration/{registration_id}", response_model=List[AuditLogSchema])
def get_audit_logs_by_registration(
    registration_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all audit logs for a specific registration ID.
    
    Args:
        registration_id (int): The registration ID to search for
        
    Returns:
        List[AuditLogSchema]: List of audit logs matching the registration ID
        
    Raises:
        HTTPException: If no audit logs are found
    """
    audit_logs = db.query(AuditLog).filter(
        AuditLog.registration_id == registration_id
    ).all()
    
    if not audit_logs:
        raise HTTPException(
            status_code=404,
            detail=f"No audit logs found for registration ID: {registration_id}"
        )
    
    return audit_logs

@router.get("/search", response_model=List[AuditLogSchema])
def get_audit_logs_by_schedule(
    registrationid: str,
    date: str,
    db: Session = Depends(get_db)
):
    """
    Get audit logs for a specific registration ID and date.
    
    Args:
        registrationid (str): The registration ID to search for
        date (str): The date in YYYY-MM-DD format
        
    Returns:
        List[AuditLogSchema]: List of audit logs matching the registration ID and date
        
    Raises:
        HTTPException: If no audit logs are found or if date format is invalid
    """
    try:
        logs = crud.get_audit_logs_by_schedule(db, registrationid, date)
        if not logs:
            raise HTTPException(status_code=404, detail="No audit logs found")
        return logs
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update", response_model=AuditLogSchema)
def update_audit_log(
    update_data: AuditLogUpdate,
    db: Session = Depends(get_db)
):
    """
    Update audit log data for a specific registration ID and date.
    
    Args:
        update_data (AuditLogUpdate): The data to update including registrationid and date
        
    Returns:
        AuditLogSchema: Updated audit log data
        
    Raises:
        HTTPException: If no audit log is found or if update fails
    """
    try:
        log = crud.update_audit_log(db, update_data)
        if not log:
            raise HTTPException(status_code=404, detail="Audit log not found")
        return log
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 