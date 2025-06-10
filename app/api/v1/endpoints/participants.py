from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from datetime import datetime
import logging
from sqlalchemy import cast, Date, text, func
from app.db.session import get_db
from app.models.participant import Participant
from app.schemas.participant import ParticipantBase, ParticipantUpdate, ParticipantResponse, ParticipantListResponse, DetailResponse
from app.crud import participant as crud
from typing import Union

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/search", response_model=Union[ParticipantListResponse, DetailResponse])
def get_participant_by_schedule(
    registrationid: int,
    date: str,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Get participant data for a specific registration ID and date.
    
    Args:
        registrationid (int): The registration ID to search for
        date (str): The date in YYYY-MM-DD format
        
    Returns:
        Union[ParticipantListResponse, DetailResponse]: Participant data with registration_id and date, or a detail message if not found.
    """
    try:
        # Convert date string to datetime
        search_date = datetime.strptime(date, "%Y-%m-%d").date()
        
        # Log the search parameters
        logger.info(f"Searching for registration_id: {registrationid}, date: {search_date}")
        
        # Query using func.date() to properly handle timezone-aware dates
        query = db.query(Participant).filter(
            Participant.registrant_id == registrationid,
            func.date(Participant.date) == search_date
        )
        
        # Log the SQL query
        logger.info(f"SQL Query: {query}")
        
        # Execute query
        participant = query.first()
        
        # Log the results
        if participant:
            logger.info(f"Found participant: registration_id={participant.registrant_id}, date={participant.date}")
            return ParticipantListResponse(
                userid=participant.id,
                name=participant.participant_type,
                registration_id=participant.registrant_id,
                date=participant.date,
                detail=None
            )
        else:
            logger.info("No participant found")
            response.status_code = 404
            return DetailResponse(detail="Data not found")
            
    except ValueError as e:
        if "time data" in str(e):
            response.status_code = 400
            return DetailResponse(detail="Invalid date format. Please use YYYY-MM-DD format.")
        response.status_code = 400
        return DetailResponse(detail=str(e))
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        response.status_code = 500
        return DetailResponse(detail=f"An error occurred: {str(e)}") 