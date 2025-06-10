from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import bcrypt
from pydantic import BaseModel
import logging
import os
from typing import Union
from datetime import date
from sqlalchemy import func

from app.db.session import get_db
from app.schemas.user import User, UserCreate, UserUpdate
from app.models.user import User as UserModel
from app.schemas.food_log import FoodLogListResponse, DetailResponse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    user: User

@router.post("/", response_model=User)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate
):
    user = db.query(UserModel).filter(UserModel.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    # Hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user_in.password.encode('utf-8'), salt)
    
    user = UserModel(
        email=user_in.email,
        username=user_in.username,
        password=hashed_password.decode('utf-8')  # Store the hashed password
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
    Login endpoint that accepts username and password only
    """
    try:
        # Parse the request body
        body = await request.json()
        username = body.get("username")
        password = body.get("password")
        
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
        
        # Verify password (compare with 'password' column)
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            logger.error(f"Invalid password for user: {username}")
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password"
            )
        
        logger.info(f"Successful login for user: {username}")
        return {
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