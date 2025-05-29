from sqlalchemy.orm import Session
from datetime import datetime
from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogUpdate

def get_audit_logs_by_schedule(db: Session, registration_id: str, date_str: str):
    """
    Get audit logs for a specific registration ID and date.
    
    Args:
        db (Session): Database session
        registration_id (str): Registration ID to search for
        date_str (str): Date in YYYY-MM-DD format
        
    Returns:
        List[AuditLog]: List of audit logs matching the criteria
    """
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
    
    return db.query(AuditLog).filter(
        AuditLog.registration_id == registration_id,
        AuditLog.date == date
    ).all()

def update_audit_log(db: Session, update_data: AuditLogUpdate):
    """
    Update audit log data.
    
    Args:
        db (Session): Database session
        update_data (AuditLogUpdate): Data to update
        
    Returns:
        AuditLog: Updated audit log
    """
    try:
        date = datetime.strptime(update_data.date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
    
    audit_log = db.query(AuditLog).filter(
        AuditLog.registration_id == update_data.registrationid,
        AuditLog.date == date
    ).first()
    
    if not audit_log:
        # Create new audit log if it doesn't exist
        audit_log = AuditLog(
            registration_id=update_data.registrationid,
            date=date,
            lunch_status=update_data.lunch_status,
            dinner_status=update_data.dinner_status
        )
        db.add(audit_log)
    else:
        # Update existing audit log
        audit_log.lunch_status = update_data.lunch_status
        audit_log.dinner_status = update_data.dinner_status
    
    db.commit()
    db.refresh(audit_log)
    return audit_log 