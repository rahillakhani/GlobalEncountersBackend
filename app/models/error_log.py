from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey, String
from app.db.base_class import Base
from datetime import datetime

class ErrorLog(Base):
    __tablename__ = "error_logs"
    __table_args__ = {"schema": "fnb"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    registrant_id = Column(String, index=True)
    scan_time = Column(DateTime(timezone=True), index=True)
    error = Column(Text)
    error_code = Column(String(10), index=True) 