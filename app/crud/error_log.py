from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Optional
from app.models.error_log import ErrorLog
from app.schemas.error_log import ErrorLogCreate
from sqlalchemy import func

def create_error_log(db: Session, error_log: ErrorLogCreate) -> ErrorLog:
    """
    Create a new error log entry in the database.
    """
    db_error_log = ErrorLog(
        user_id=error_log.user_id,
        registrant_id=error_log.registrant_id,
        scan_time=error_log.scan_time,
        error=error_log.error,
        error_code=error_log.error_code
    )
    db.add(db_error_log)
    db.commit()
    db.refresh(db_error_log)
    return db_error_log

def get_error_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    registrant_id: Optional[int] = None,
    error_code: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> list[ErrorLog]:
    """
    Retrieve error logs with optional filtering.
    
    Args:
        db (Session): Database session
        skip (int): Number of records to skip
        limit (int): Maximum number of records to return
        user_id (int, optional): Filter by user ID
        registrant_id (int, optional): Filter by registrant ID
        error_code (str, optional): Filter by error code (e.g., "01", "02", "03")
        start_date (date, optional): Filter by start date
        end_date (date, optional): Filter by end date
        
    Returns:
        list[ErrorLog]: List of error log entries
    """
    query = db.query(ErrorLog)
    
    if user_id is not None:
        query = query.filter(ErrorLog.user_id == user_id)
    if registrant_id is not None:
        query = query.filter(ErrorLog.registrant_id == registrant_id)
    if error_code is not None:
        query = query.filter(ErrorLog.error_code == error_code)
    if start_date is not None:
        query = query.filter(func.date(ErrorLog.scan_time) >= start_date)
    if end_date is not None:
        query = query.filter(func.date(ErrorLog.scan_time) <= end_date)
        
    return query.order_by(ErrorLog.scan_time.desc()).offset(skip).limit(limit).all() 