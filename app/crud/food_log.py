from sqlalchemy.orm import Session, joinedload
from sqlalchemy import cast, Date, func
from datetime import datetime
from app.models.food_log import FoodLog
from app.models.participant import Participant
from app.schemas.food_log import FoodLogUpdate

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
        
        # Format response with all fields
        return [
            {
                "userid": log.userid,
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
        # Find existing food log by registration_id and date
        food_log = db.query(FoodLog).filter(
            FoodLog.registration_id == update_data.registration_id,
            func.date(FoodLog.date) == update_data.date.date()
        ).first()
        
        if not food_log:
            # If no existing food log, only create if userid is provided
            if update_data.userid is None:
                # Cannot create a new log without userid due to unique constraint
                return None # Return None to indicate creation was not possible
            
            # Create a new food log entry
            food_log = FoodLog(
                userid=update_data.userid,
                name=update_data.name,
                registration_id=update_data.registration_id,
                date=update_data.date,
                lunch=update_data.lunch,
                dinner=update_data.dinner,
                lunch_takenon=update_data.lunch_takenon if update_data.lunch_takenon is not None else (datetime.now() if update_data.lunch is not None else None),
                dinner_takenon=update_data.dinner_takenon if update_data.dinner_takenon is not None else (datetime.now() if update_data.dinner is not None else None)
            )
            db.add(food_log)
        else:
            # Update existing food log fields
            # Only update fields that are explicitly provided in update_data and are different
            if update_data.userid is not None and food_log.userid != update_data.userid:
                food_log.userid = update_data.userid
            if update_data.name is not None and food_log.name != update_data.name:
                food_log.name = update_data.name
            if update_data.lunch is not None and food_log.lunch != update_data.lunch:
                food_log.lunch = update_data.lunch
                if update_data.lunch_takenon is not None:
                    food_log.lunch_takenon = update_data.lunch_takenon
                else:
                    food_log.lunch_takenon = datetime.now()
            if update_data.dinner is not None and food_log.dinner != update_data.dinner:
                food_log.dinner = update_data.dinner
                if update_data.dinner_takenon is not None:
                    food_log.dinner_takenon = update_data.dinner_takenon
                else:
                    food_log.dinner_takenon = datetime.now()

        db.commit()
        db.refresh(food_log)
        return food_log
        
    except Exception as e:
        raise ValueError(f"Error updating food log: {str(e)}") 