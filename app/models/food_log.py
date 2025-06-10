from sqlalchemy import Column, Integer, String, DateTime, PrimaryKeyConstraint
from app.db.base import Base

class FoodLog(Base):
    __tablename__ = "food_logs"
    __table_args__ = (
        PrimaryKeyConstraint('registration_id', 'date', name='food_logs_pkey'),
        {"schema": "fnb"}
    )

    name = Column(String)
    registration_id = Column(Integer, nullable=False, index=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    lunch = Column(Integer)
    dinner = Column(Integer)
    lunch_takenon = Column(DateTime(timezone=True))
    dinner_takenon = Column(DateTime(timezone=True)) 