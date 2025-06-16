from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import engine, SessionLocal
from app.db.base import Base

# Load environment variables
load_dotenv()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for Global Encounters application",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins,  # Allow both HTTP and HTTPS origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicitly specify allowed methods
    allow_headers=["Authorization", "Content-Type", "Accept"],  # Explicitly specify allowed headers
    expose_headers=["Content-Type"]
)

# Custom exception handler
@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    response = JSONResponse(
        status_code=401 if isinstance(exc, Exception) else 500,
        content={"detail": str(exc) if not isinstance(exc, Exception) else "Data not found"}
    )
    # Add CORS headers to error responses
    origin = request.headers.get("origin", settings.FRONTEND_URL)
    if origin in settings.get_allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, Accept"
    response.headers["Access-Control-Expose-Headers"] = "Content-Type"
    return response

# Password verification function
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

logging.basicConfig(level=logging.INFO)

@app.get("/")
async def root():
    return {"message": "Welcome to Global Encounters API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 