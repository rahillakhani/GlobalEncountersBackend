from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
import logging
from sqlalchemy import cast, Date, text, func, String, literal
from app.db.session import get_db
from app.models.participant import Participant
from app.schemas.participant import ParticipantBase, ParticipantUpdate, ParticipantResponse, ParticipantListResponse, DetailResponse, ParticipantCreate
from app.crud import participant as crud
from typing import Union
from app.core.security import get_current_user, create_access_token
from app.models.user import User as UserModel
from app.core.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/search", response_model=Union[ParticipantListResponse, DetailResponse])
def get_participant_by_schedule(
    response: Response,
    registrationid: str,
    date: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Get participant data by registration ID and date.
    """
    try:
        participant = crud.get_participant_by_schedule(db, registrationid, date)
        if not participant:
            response.status_code = 200
            return DetailResponse(detail="No data found")

        # Generate new token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        new_token = create_access_token(
            data={"sub": current_user.username}, expires_delta=access_token_expires
        )

        return ParticipantListResponse(
            userid=participant.id,
            name=participant.participant_type,
            registration_id=participant.registrant_id,
            date=participant.date,
            detail=None,
            access_token=new_token
        )
    except Exception as e:
        logger.error(f"Error getting participants: {str(e)}", exc_info=True)
        response.status_code = 500
        return DetailResponse(detail=f"An error occurred: {str(e)}")

@router.post("/", response_model=ParticipantListResponse)
def create_participant(
    *,
    db: Session = Depends(get_db),
    participant_in: ParticipantCreate
):
    """
    Create a new participant.
    
    Args:
        participant_in (ParticipantCreate): The participant data to create
        
    Returns:
        ParticipantListResponse: Created participant data
    """
    try:
        participant = crud.create_participant(db, participant_in)
        return ParticipantListResponse(
            userid=participant.id,
            name=participant.participant_type,
            registration_id=participant.registrant_id,
            date=participant.date,
            detail=None
        )
    except Exception as e:
        logger.error(f"Error creating participant: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating participant: {str(e)}"
        ) 