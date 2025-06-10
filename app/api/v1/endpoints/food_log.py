from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from datetime import datetime, date
import logging
from sqlalchemy import cast, Date, func
from app.db.session import get_db
from app.models.food_log import FoodLog
from app.schemas.food_log import FoodLogUpdate, FoodLogSchema, FoodLogListResponse, DetailResponse
from app.crud import food_log as crud
from app.api import deps
from typing import Union

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/search", response_model=Union[FoodLogListResponse, DetailResponse])
def get_food_logs_by_schedule(
    registrationid: int,
    date_str: str,
    db: Session = Depends(deps.get_db)
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

        # Convert the food log to a FoodLogSchema and wrap it in a list
        food_log_schema = FoodLogSchema.from_orm(food_log)
        return FoodLogListResponse(data=[food_log_schema])

    except ValueError as e:
        logger.error(f"Invalid date format: {date_str}. Error: {e}")
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Please use YYYY-MM-DD"
        )
    except Exception as e:
        logger.error(f"Error searching food logs: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@router.post("/update", response_model=Union[FoodLogSchema, DetailResponse])
def update_food_log(
    response: Response,
    update_data: FoodLogUpdate,
    db: Session = Depends(get_db)
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