from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict
from datetime import datetime
import logging

from app.db.session import get_db
from app.core.meal_timings import MealTimings
from app.models.user import User as UserModel
from app.core.security import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/timings", response_model=Dict)
@router.post("/timings", response_model=Dict)
async def get_meal_timings(
    current_user: UserModel = Depends(get_current_user)
):
    """
    Get meal timings for lunch and dinner.
    Returns the start and end times for both meals.
    Accepts both GET and POST methods.
    """
    try:
        meal_timings = MealTimings()
        
        # Get timings for both meals
        lunch_start, lunch_end = meal_timings.get_meal_timings('lunch')
        dinner_start, dinner_end = meal_timings.get_meal_timings('dinner')
        
        return {
            "lunch": {
                "start_time": lunch_start.strftime("%I:%M %p"),
                "end_time": lunch_end.strftime("%I:%M %p")
            },
            "dinner": {
                "start_time": dinner_start.strftime("%I:%M %p"),
                "end_time": dinner_end.strftime("%I:%M %p")
            }
        }
    except Exception as e:
        logger.error(f"Error getting meal timings: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error retrieving meal timings"
        ) 