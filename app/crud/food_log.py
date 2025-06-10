from sqlalchemy.orm import Session, joinedload
from sqlalchemy import cast, Date, func
from datetime import datetime, timezone
from app.models.food_log import FoodLog
from app.models.participant import Participant
from app.schemas.food_log import FoodLogUpdate, FoodLogCreate
import logging
import datetime

def get_food_logs_by_schedule(db: Session, registrationid: str, date_str: str):
    """
    Get food log data for a specific registration ID and date.
    
    Args:
        db (Session): Database session
        registrationid (str): Registration ID to search for
        date_str (str): Date in YYYY-MM-DD format
        
    Returns:
        List[dict]: List of food logs with all fields
        
    Raises:
        ValueError: If user doesn't exist or if date format is invalid
    """
    try:
        # Convert registration ID to integer for participant check
        try:
            registration_id_int = int(registrationid)
        except ValueError:
            raise ValueError("Invalid registration ID format. Please provide a valid number.")
        
        # Check if registration ID exists in participants table
        participant_exists = db.query(Participant.registrant_id).filter(
            Participant.registrant_id == registration_id_int
        ).first() is not None
        
        if not participant_exists:
            raise ValueError("User not found")
        
        # Convert date string to datetime
        search_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Query food logs for the given registration ID and date
        food_logs = db.query(FoodLog).filter(
            FoodLog.registration_id == registrationid,  # Keep as string for food_logs table
            cast(FoodLog.date, Date) == search_date
        ).all()
        
        if not food_logs:
            return []
        
        # Format response with all fields (removed userid)
        return [
            {
                "name": log.name,
                "registration_id": log.registration_id,
                "lunch": log.lunch,
                "dinner": log.dinner,
                "date": log.date,
                "lunch_takenon": log.lunch_takenon,
                "dinner_takenon": log.dinner_takenon
            }
            for log in food_logs
        ]
    except ValueError as e:
        if "time data" in str(e):
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError(f"Error searching food logs: {str(e)}")

def update_food_log(db: Session, update_data: FoodLogUpdate):
    """
    Update food log data for a specific registration ID and date.
    
    Args:
        db (Session): Database session
        update_data (FoodLogUpdate): Data to update
        
    Returns:
        FoodLog: Updated food log or None if creation not possible
    """
    try:
        if not update_data.registration_id or not update_data.date:
            raise ValueError("Registration ID and date are required for updating food logs")

        logger = logging.getLogger(__name__)
        logger.info(f"Searching for food log with registration_id={update_data.registration_id} and date={update_data.date}")

        input_date = update_data.date
        # Use datetime.timezone.utc if available, else skip conversion
        tz_utc = getattr(datetime, 'timezone', None)
        if tz_utc is not None and input_date.tzinfo is not None:
            input_date = input_date.astimezone(tz_utc.utc)

        # First try to find an existing entry for this registration_id and date
        existing_log = db.query(FoodLog).filter(
            FoodLog.registration_id == update_data.registration_id,
            func.date(FoodLog.date) == input_date.date()
        ).first()

        if existing_log:
            logger.info(f"Found existing food log entry: {existing_log}")
            # Update the existing entry
            if update_data.name is not None:
                existing_log.name = update_data.name
            if update_data.lunch is not None:
                existing_log.lunch = update_data.lunch
            if update_data.dinner is not None:
                existing_log.dinner = update_data.dinner
            if update_data.lunch_takenon is not None:
                existing_log.lunch_takenon = update_data.lunch_takenon
            if update_data.dinner_takenon is not None:
                existing_log.dinner_takenon = update_data.dinner_takenon
            food_log = existing_log
        else:
            logger.info("No existing food log found, creating new entry")
            food_log = FoodLog(
                name=update_data.name,
                registration_id=update_data.registration_id,
                date=input_date,
                lunch=update_data.lunch,
                dinner=update_data.dinner,
                lunch_takenon=update_data.lunch_takenon,
                dinner_takenon=update_data.dinner_takenon
            )
            db.add(food_log)

        db.commit()
        db.refresh(food_log)
        logger.info(f"Final food log state: {food_log}")
        return food_log

    except Exception as e:
        db.rollback()
        logger.error(f"Error in update_food_log: {str(e)}", exc_info=True)
        raise ValueError(f"Error updating food log: {str(e)}") 