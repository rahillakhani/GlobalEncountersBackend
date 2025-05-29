from app.db.base import Base
from app.models.user import User
from app.models.encounter import Encounter
from app.models.location import Location
from app.models.category import Category
from app.models.entitlement import Entitlement
from app.models.audit_log import AuditLog
from app.models.registration_type import RegistrationType
from app.models.food_data import FoodData
from sqlalchemy import create_engine
from app.core.config import settings

# Create engine
engine = create_engine(settings.get_database_url)

# Create all tables
Base.metadata.create_all(bind=engine)

print("Tables created successfully!") 