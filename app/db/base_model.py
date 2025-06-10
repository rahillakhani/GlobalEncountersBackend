# Import all models here for Alembic to detect them
from app.db.base import Base  # noqa
from app.models.user import User  # noqa
from app.models.food_log import FoodLog  # noqa
from app.models.audit_log import AuditLog  # noqa
from app.models.participant import Participant  # noqa
from app.models.error_log import ErrorLog  # noqa 