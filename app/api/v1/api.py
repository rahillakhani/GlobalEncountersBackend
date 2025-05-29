from fastapi import APIRouter
from app.api.v1.endpoints import users, audit_log

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(audit_log.router, prefix="/user", tags=["user"]) 