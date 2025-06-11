from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from datetime import datetime, date
import logging
from sqlalchemy import cast, Date, func
from app.db.session import get_db
from app.models.food_log import FoodLog
from app.models.user import User as UserModel
from app.schemas.food_log import FoodLogUpdate, FoodLogSchema, FoodLogListResponse, DetailResponse
from app.crud import food_log as crud
from app.api import deps
from app.core.security import get_current_user
from typing import Union

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/search", response_model=Union[FoodLogListResponse, DetailResponse])
def get_food_logs_by_schedule(
    registrationid: int,
    date_str: str,
    response: Response,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Get food logs by registration ID and date
    """
    try:
        logger.info(f"Attempting to parse date: {repr(date_str)} (type: {type(date_str)}). Bytes: {date_str.strip().encode('utf-8')}")
        search_date = date.fromisoformat(date_str.strip())

        food_log = db.query(FoodLog).filter(
            FoodLog.registration_id == registrationid,
            func.date(FoodLog.date) == search_date
        ).first()

        if not food_log:
            return DetailResponse(detail="No data found")

        # Convert the food log to a FoodLogSchema (which no longer includes userid) and wrap it in a list
        food_log_schema = FoodLogSchema.from_orm(food_log)
        return FoodLogListResponse(data=[food_log_schema])

    except ValueError as e:
        logger.error(f"Invalid date format: {date_str}. Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Please use YYYY-MM-DD"
        )
    except HTTPException as e:
        # Re-raise HTTP exceptions (including auth errors) without modification
        raise e
    except Exception as e:
        logger.error(f"Error searching food logs: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/update", response_model=Union[FoodLogSchema, DetailResponse])
def update_food_log(
    response: Response,
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
        return log
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