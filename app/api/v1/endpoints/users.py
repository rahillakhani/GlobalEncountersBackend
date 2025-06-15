from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
import bcrypt
from pydantic import BaseModel
import logging
import os
from typing import Union, Optional
from datetime import date, datetime, timedelta
from sqlalchemy import func

from app.db.session import get_db
from app.schemas.user import User, UserCreate, UserUpdate
from app.models.user import User as UserModel
from app.schemas.food_log import FoodLogListResponse, DetailResponse
from app.core.security import create_access_token, create_tokens, refresh_access_token
from app.core.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str
    device_id: Optional[str] = None

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: User

@router.post("/", response_model=User)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate
):
    # Check if username already exists
    user = db.query(UserModel).filter(UserModel.username == user_in.username).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    
    # Hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user_in.password.encode('utf-8'), salt)
    
    user = UserModel(
        username=user_in.username,
        password=hashed_password.decode('utf-8'),  # Store the hashed password
        device_id=user_in.device_id,
        email=user_in.email
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{user_id}", response_model=User)
def read_user(
    *,
    db: Session = Depends(get_db),
    user_id: int
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user

@router.get("/by-username/{username}", response_model=User)
def get_user_by_username(
    *,
    db: Session = Depends(get_db),
    username: str
):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user

@router.post("/login", response_model=LoginResponse)
async def login(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Login endpoint that accepts username, password, and device_id and returns JWT tokens
    """
    try:
        # Parse the request body
        body = await request.json()
        username = body.get("username")
        password = body.get("password")
        device_id = body.get("device_id")
        
        logger.info(f"Login attempt for username: {username}")
        
        if not username or not password:
            logger.error("Missing username or password")
            raise HTTPException(
                status_code=400,
                detail="Username and password are required"
            )
        
        # Find user by username
        user = db.query(UserModel).filter(UserModel.username == username).first()
        if not user:
            logger.error(f"User not found: {username}")
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password"
            )
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            logger.error(f"Invalid password for user: {username}")
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password"
            )
        
        # Update device_id if provided
        if device_id:
            user.device_id = device_id
            db.commit()
        
        # Create access and refresh tokens
        access_token, refresh_token = create_tokens(data={"sub": user.username})
        
        logger.info(f"Successful login for user: {username}")
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": User.from_orm(user)
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@router.post("/refresh", response_model=dict)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    """
    try:
        new_access_token = await refresh_access_token(refresh_token, db)
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@router.get("/search", response_model=Union[FoodLogListResponse, DetailResponse])
def get_food_logs_by_schedule(
    registrationid: int,
    date_str: str,
    db: Session = Depends(get_db)
):
    try:
        search_date = date.fromisoformat(date_str.strip())
        food_log = db.query(FoodLog).filter(
            FoodLog.registration_id == registrationid,
            func.date(FoodLog.date) == search_date
        ).first()

        if not food_log:
            response.status_code = 404
            return DetailResponse(detail="No data found")

        return FoodLogListResponse(
            userid=food_log.userid,
            name=food_log.name,
            registration_id=food_log.registration_id,
            lunch=food_log.lunch,
            dinner=food_log.dinner,
            date=food_log.date,
            lunch_takenon=food_log.lunch_takenon,
            dinner_takenon=food_log.dinner_takenon
        )

    except ValueError as e:
        # This is only for date parsing errors
        logger.error(f"Invalid date format: {date_str}. Error: {e}")
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Please use YYYY-MM-DD"
        )
    except Exception as e:
        logger.error(f"Error searching food logs: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        ) 