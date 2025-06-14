from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from typing import Optional, Union, List
from datetime import datetime, timedelta
from sqlalchemy import func, Date
import logging

from app.api.deps import get_db
from app.crud import error_log as crud
from app.schemas.error_log import (
    ErrorLogCreate,
    ErrorLogSchema,
    ErrorLogResponse,
    ErrorLogListResponse,
    DetailResponse
)
from app.models.user import User as UserModel
from app.core.security import get_current_user, create_access_token
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=Union[ErrorLogResponse, DetailResponse])
def create_error_log(
    error_log_in: ErrorLogCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Create a new error log.
    """
    try:
        error_log = crud.create_error_log(db, error_log_in)
        # Generate new token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        new_token = create_access_token(
            data={"sub": current_user.username}, expires_delta=access_token_expires
        )
        return ErrorLogResponse(
            userid=error_log.user_id,
            registrant_id=str(error_log.registrant_id),
            error=error_log.error,
            scan_time=error_log.scan_time,
            detail=None,
            access_token=new_token
        )
    except Exception as e:
        logger.error(f"Error creating error log: {str(e)}", exc_info=True)
        return DetailResponse(detail=f"An error occurred: {str(e)}")

@router.get("/", response_model=Union[ErrorLogListResponse, DetailResponse])
def get_error_logs(
    response: Response,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    registrant_id: Optional[int] = None,
    start_date_str: Optional[str] = None,
    end_date_str: Optional[str] = None
) -> Union[ErrorLogListResponse, DetailResponse]:
    """
    Retrieve error logs with optional filtering.
    """
    try:
        start_date = None
        end_date = None

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            except ValueError:
                response.status_code = 400
                return DetailResponse(detail="Invalid start_date format. Please use YYYY-MM-DD.")

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            except ValueError:
                response.status_code = 400
                return DetailResponse(detail="Invalid end_date format. Please use YYYY-MM-DD.")

        error_logs = crud.get_error_logs(
            db=db,
            skip=skip,
            limit=limit,
            user_id=user_id,
            registrant_id=registrant_id,
            start_date=start_date,
            end_date=end_date
        )
        
        if not error_logs:
            response.status_code = 404
            return DetailResponse(detail="No error logs found matching the criteria.")

        return ErrorLogListResponse(data=error_logs)
    except Exception as e:
        logger.error(f"Error retrieving error logs: {str(e)}", exc_info=True)
        response.status_code = 500
        return DetailResponse(detail=f"An error occurred: {str(e)}") 