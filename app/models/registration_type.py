from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class RegistrationType(Base):
    __tablename__ = "registration_types"
    __table_args__ = {"schema": "fnb"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    requires_approval = Column(Boolean, default=False)
    max_participants = Column(Integer)
    registration_fee = Column(Integer)  # Amount in cents
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    registrations = relationship("Registration", back_populates="registration_type") 