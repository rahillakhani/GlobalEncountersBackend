from sqlalchemy.orm import Session, joinedload
from sqlalchemy import cast, Date, func, text
from sqlalchemy.types import String
from datetime import datetime, timezone, date
from app.models.food_log import FoodLog
from app.models.participant import Participant
from app.schemas.food_log import FoodLogUpdate, FoodLogCreate
from app.core.special_registrations import is_special_registration
import logging
import datetime
from typing import Union, Optional

# Set up logging
logger = logging.getLogger(__name__)

def get_food_logs_by_schedule(db: Session, registrationid: Union[str, int], date_str: str):
    """
    Get food log data by registration ID and date.
    
    Args:
        db (Session): Database session
        registrationid (Union[str, int]): Registration ID to search for
        date_str (str): Date in YYYY-MM-DD format
        
    Returns:
        List[FoodLog]: List of food log entries for the given registration ID and date
        
    Raises:
        ValueError: If user doesn't exist or if date format is invalid
    """
    try:
        search_date = date.fromisoformat(date_str.strip())
        
        # Convert registration_id to string if it's an integer
        if isinstance(registrationid, int):
            registrationid = str(registrationid)
        
        # For special registrations, return all entries for the day
        if is_special_registration(registrationid):
            food_logs = db.query(FoodLog).filter(
                FoodLog.registration_id == registrationid,
                func.date(FoodLog.date) == search_date
            ).all()
            return food_logs if food_logs else None
        
        # For regular registrations, return the first entry
        food_log = db.query(FoodLog).filter(
            FoodLog.registration_id == registrationid,
            func.date(FoodLog.date) == search_date
        ).first()

        return [food_log] if food_log else None
    except Exception as e:
        raise ValueError(f"Error searching food logs: {str(e)}")

def update_food_log(db: Session, update_data: FoodLogUpdate) -> Optional[FoodLog]:
    """
    Update food log data for a specific registration ID and date.
    For special registration IDs and the name "master", creates a new entry each time.
    
    Args:
        db (Session): Database session
        update_data (FoodLogUpdate): Data to update
        
    Returns:
        FoodLog: Updated or new food log entry
    """
    try:
        logger.info(f"Processing food log update for registration_id={update_data.registration_id} and date={update_data.date}")
        
        # Use registration_id as is, without conversion
        registration_id = update_data.registration_id

        # Check if it's a special registration or if the name is "master"
        if is_special_registration(registration_id) or (update_data.name and update_data.name.lower() == "master"):
            logger.info("Processing special registration or master")
            # For special registrations and master, always create a new entry
            food_log = FoodLog(
                registration_id=registration_id,
                date=update_data.date,
                name=update_data.name,
                lunch=update_data.lunch,
                dinner=update_data.dinner,
                lunch_takenon=update_data.lunch_takenon,
                dinner_takenon=update_data.dinner_takenon
            )
            db.add(food_log)
        else:
            logger.info("Processing regular registration")
            # Check for existing entry first
            food_log = db.query(FoodLog).filter(
                FoodLog.registration_id == registration_id,
                func.date(FoodLog.date) == update_data.date
            ).first()
            
            if food_log:
                logger.info("Updating existing entry for regular registration")
                # Update existing entry
                food_log.lunch = update_data.lunch
                food_log.dinner = update_data.dinner
                food_log.lunch_takenon = update_data.lunch_takenon
                food_log.dinner_takenon = update_data.dinner_takenon
                food_log.name = update_data.name
            else:
                logger.info("Creating new entry for regular registration")
                # Create new entry only if none exists
                food_log = FoodLog(
                    registration_id=registration_id,
                    date=update_data.date,
                    name=update_data.name,
                    lunch=update_data.lunch,
                    dinner=update_data.dinner,
                    lunch_takenon=update_data.lunch_takenon,
                    dinner_takenon=update_data.dinner_takenon
                )
                db.add(food_log)
        
        db.commit()
        db.refresh(food_log)
        return food_log
    except Exception as e:
        logger.error(f"Error in update_food_log: {str(e)}", exc_info=True)
        db.rollback()
        raise ValueError(f"Error updating food log: {str(e)}") 