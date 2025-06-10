from sqlalchemy.orm import Session
from app.models.participant import Participant
from app.schemas.participant import ParticipantCreate, ParticipantUpdate

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