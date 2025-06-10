from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base_class import Base

class Participant(Base):
    __tablename__ = "participants"
    __table_args__ = {"schema": "fnb"}

    id = Column(Integer, primary_key=True, index=True)
    registrant_id = Column(Integer, index=True)
    date = Column(DateTime(timezone=True), index=True)
    participant_type = Column(String(50), index=True)