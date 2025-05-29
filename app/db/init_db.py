from sqlalchemy import create_engine
from app.core.config import settings
from app.db.base import Base
from app.models.audit_log import AuditLog
from app.models.food_data import FoodData
from app.models.registration_type import RegistrationType
from app.models.entitlement import Entitlement
from app.models.user import User

def init_db():
    engine = create_engine(settings.get_database_url)
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db() 