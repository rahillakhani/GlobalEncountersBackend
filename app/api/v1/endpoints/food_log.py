from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from sqlalchemy.orm import Session
from sqlalchemy.types import String
from datetime import datetime, date
import logging
from sqlalchemy import cast, Date, func, text
from app.db.session import get_db
from app.models.food_log import FoodLog
from app.models.user import User as UserModel
from app.schemas.food_log import FoodLogUpdate, FoodLogSchema, FoodLogListResponse, DetailResponse
from app.crud import food_log as crud
from app.api import deps
from app.core.security import get_current_user, create_access_token
from typing import Union
from app.core.config import settings
from datetime import timedelta

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/search", response_model=Union[FoodLogListResponse, DetailResponse])
def get_food_logs_by_schedule(
    response: Response,
    registrationid: str,
    date_str: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Get food logs by registration ID and date.
    """
    try:
        food_logs = crud.get_food_logs_by_schedule(db, registrationid, date_str)
        if not food_logs:
            response.status_code = 200
            return DetailResponse(detail="No data found")

        # Generate new token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        new_token = create_access_token(
            data={"sub": current_user.username}, expires_delta=access_token_expires
        )

        # Convert food logs to schema format
        food_log_schemas = []
        for log in food_logs:
            food_log_schemas.append(FoodLogSchema(
                name=log.name,
                registration_id=log.registration_id,
                date=log.date,
                lunch=log.lunch,
                dinner=log.dinner,
                lunch_takenon=log.lunch_takenon,
                dinner_takenon=log.dinner_takenon
            ))

        return FoodLogListResponse(
            food_logs=food_log_schemas,
            detail=None,
            access_token=new_token
        )
    except Exception as e:
        logger.error(f"Error searching food logs: {str(e)}", exc_info=True)
        response.status_code = 500
        return DetailResponse(detail=f"An error occurred: {str(e)}")

@router.post("/update", response_model=Union[FoodLogSchema, DetailResponse])
def update_food_log(
    response: Response,
    request: Request,
    update_data: FoodLogUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Update food log data for a specific registration ID and date.
    
    Args:
        update_data (FoodLogUpdate): The data to update including registrationid and date
        
    Returns:
        FoodLogResponse: Updated food log data
        
    Raises:
        HTTPException: If no food log is found or if update fails
    """
    try:
        log = crud.update_food_log(db, update_data)
        if log is None:
            response.status_code = 400
            return DetailResponse(detail="Cannot create new food log: 'userid' is required for new entries.")
        
        # Generate new token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        new_token = create_access_token(
            data={"sub": current_user.username}, expires_delta=access_token_expires
        )
        
        # Convert log to dict and add new token
        log_dict = {
            "name": log.name,
            "registration_id": log.registration_id,
            "date": log.date,
            "lunch": log.lunch,
            "dinner": log.dinner,
            "lunch_takenon": log.lunch_takenon,
            "dinner_takenon": log.dinner_takenon,
            "access_token": new_token
        }
        return log_dict
    except ValueError as e:
        response.status_code = 400
        return DetailResponse(detail=str(e))
    except Exception as e:
        logger.error(f"Error updating food log: {str(e)}", exc_info=True)
        response.status_code = 500
        return DetailResponse(detail=f"An error occurred: {str(e)}")

@router.delete("/{registration_id}/{date_str}", response_model=DetailResponse)
def delete_food_log(
    registration_id: int,
    date_str: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Delete a food log entry for a specific registration ID and date.
    
    Args:
        registration_id (int): The registration ID of the food log to delete
        date_str (str): The date of the food log to delete in YYYY-MM-DD format
        
    Returns:
        DetailResponse: Success or error message
    """
    try:
        # Convert date string to datetime
        search_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Find the food log entry
        food_log = db.query(FoodLog).filter(
            FoodLog.registration_id == registration_id,
            func.date(FoodLog.date) == search_date
        ).first()
        
        if not food_log:
            raise HTTPException(
                status_code=404,
                detail="Food log not found"
            )
        
        # Delete the entry
        db.delete(food_log)
        db.commit()
        
        return DetailResponse(detail="Food log deleted successfully")
        
    except ValueError as e:
        if "time data" in str(e):
            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Please use YYYY-MM-DD"
            )
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting food log: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting food log: {str(e)}"
        )

@router.get("/some-endpoint")
def some_endpoint(current_user: UserModel = Depends(get_current_user)):
    # This endpoint is only accessible if the user is authenticated
    return {"message": f"Hello, {current_user.username}!"} 