from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class FoodData(Base):
    __tablename__ = "food_data"
    __table_args__ = {"schema": "fnb"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    category = Column(String, index=True)  # e.g., "main course", "dessert", "beverage"
    price = Column(Float)
    currency = Column(String, default="USD")
    is_vegetarian = Column(Boolean, default=False)
    is_vegan = Column(Boolean, default=False)
    is_gluten_free = Column(Boolean, default=False)
    allergens = Column(String)  # Comma-separated list of allergens
    nutritional_info = Column(Text)  # JSON string of nutritional information
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    food_orders = relationship("FoodOrder", back_populates="food_item") 