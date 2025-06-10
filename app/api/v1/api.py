from fastapi import APIRouter
from app.api.v1.endpoints import food_log, audit_log, participants, error_logs, users

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(food_log.router, prefix="/food-log", tags=["food-log"])
api_router.include_router(audit_log.router, prefix="/audit-log", tags=["audit-log"])
api_router.include_router(participants.router, prefix="/participants", tags=["participants"])
api_router.include_router(error_logs.router, prefix="/error-logs", tags=["error-logs"]) 