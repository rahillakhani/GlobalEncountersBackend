from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = {"schema": "fnb"}

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    entitlement_type = Column(String)
    name = Column(String)
    registration_id = Column(Integer)
    lunch = Column(Integer, default=0)  # 0 for False, 1 for True
    dinner = Column(Integer, default=0)  # 0 for False, 1 for True
    lunch_takenon = Column(DateTime(timezone=True), nullable=True)
    dinner_takenon = Column(DateTime(timezone=True), nullable=True) 