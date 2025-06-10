from sqlalchemy import Column, Integer, String, DateTime
from app.db.base import Base

class FoodLog(Base):
    __tablename__ = "food_logs"
    __table_args__ = {"schema": "fnb"}

    userid = Column(Integer, primary_key=True)
    name = Column(String)
    registration_id = Column(Integer, index=True)
    date = Column(DateTime(timezone=True))
    lunch = Column(Integer)
    dinner = Column(Integer)
    lunch_takenon = Column(DateTime(timezone=True))
    dinner_takenon = Column(DateTime(timezone=True)) 