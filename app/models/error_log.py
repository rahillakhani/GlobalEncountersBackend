from sqlalchemy import Column, Integer, DateTime, Text
from app.db.base_class import Base

class ErrorLog(Base):
    __tablename__ = "error_logs"
    __table_args__ = {"schema": "fnb"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    registrant_id = Column(Integer, index=True)
    scan_time = Column(DateTime(timezone=True), index=True)
    error = Column(Text) 