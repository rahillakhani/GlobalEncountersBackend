from sqlalchemy.orm import Session
from sqlalchemy import func, text, cast
from sqlalchemy.types import String
from app.models.participant import Participant
from app.schemas.participant import ParticipantCreate, ParticipantUpdate
from datetime import date

def get_participant(db: Session, registrant_id: int):
    return db.query(Participant).filter(Participant.registrant_id == registrant_id).first()

def get_participants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Participant).offset(skip).limit(limit).all()

def create_participant(db: Session, participant: ParticipantCreate):
    db_participant = Participant(**participant.dict())
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant

def update_participant(db: Session, registrant_id: int, participant: ParticipantUpdate):
    db_participant = get_participant(db, registrant_id)
    if db_participant:
        for key, value in participant.dict(exclude_unset=True).items():
            setattr(db_participant, key, value)
        db.commit()
        db.refresh(db_participant)
    return db_participant

def delete_participant(db: Session, registrant_id: int):
    db_participant = get_participant(db, registrant_id)
    if db_participant:
        db.delete(db_participant)
        db.commit()
    return db_participant

def get_participant_by_schedule(db: Session, registrationid: int, date_str: str):
    """
    Get participant data by registration ID and date.
    """
    # Convert date string to date object
    search_date = date.fromisoformat(date_str.strip())
    
    # Build the main query - convert UTC to PKT by adding 5 hours
    query = db.query(Participant).filter(
        cast(Participant.registrant_id, String) == str(registrationid),
        func.date(Participant.date + text("INTERVAL '5 hours'")) == search_date
    )
    
    return query.first() 