from fastapi import FastAPI, HTTPException, Query, Body, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, MetaData, Table, select, cast, Date, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime, timedelta
import logging
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")  # Will be set in Azure
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://admin:admin@52.168.133.23:5432/postgres")

engine = create_engine(DATABASE_URL)
metadata = MetaData()
audit_logs = Table('audit_logs', metadata, autoload_with=engine, schema='fnb')
users = Table('users', metadata, 
    Column('id', Integer, primary_key=True),
    Column('username', String(50), unique=True, nullable=False),
    Column('email', String(100), unique=True, nullable=False),
    Column('password', String(100), nullable=False),
    schema='fnb'
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

class AuditLogBase(BaseModel):
    date: Optional[date]
    entitlement_type: Optional[str]
    name: Optional[str]
    registration_id: Optional[int]
    lunch: Optional[int]
    dinner: Optional[int]
    lunch_takenon: Optional[datetime]
    dinner_takenon: Optional[datetime]

class AuditLogCreate(AuditLogBase):
    pass

class AuditLog(AuditLogBase):
    id: int
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    with engine.connect() as conn:
        user = conn.execute(
            select(users).where(users.c.username == token_data.username)
        ).first()
        if user is None:
            raise credentials_exception
        # Convert Row to dict and add token
        user_dict = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "token": token
        }
        return user_dict

@app.get("/audit_logs", response_model=List[AuditLog])
def get_audit_logs(limit: int = 100):
    with engine.connect() as conn:
        result = conn.execute(select(audit_logs).limit(limit))
        return [dict(row) for row in result]

@app.get("/audit_logs/{log_id}", response_model=AuditLog)
def get_audit_log(log_id: int):
    with engine.connect() as conn:
        result = conn.execute(select(audit_logs).where(audit_logs.c.id == log_id)).first()
        if not result:
            raise HTTPException(status_code=404, detail="Audit log not found")
        return dict(result)

@app.post("/audit_logs", response_model=AuditLog)
def create_audit_log(log: AuditLogCreate):
    with engine.connect() as conn:
        ins = audit_logs.insert().values(**log.dict())
        result = conn.execute(ins)
        conn.commit()
        new_id = result.inserted_primary_key[0]
        new_log = conn.execute(select(audit_logs).where(audit_logs.c.id == new_id)).first()
        return dict(new_log)

@app.get("/api/v1/user/search")
def search_user(
    registrationid: int = Query(..., alias="registrationid"), 
    date: date = Query(..., alias="date"),
    current_user: dict = Depends(get_current_user)
):
    logging.info(f"Received registrationid: {registrationid} (type: {type(registrationid)})")
    logging.info(f"Received date: {date} (type: {type(date)})")
    with engine.connect() as conn:
        # Print all rows with this registration_id
        rows = conn.execute(
            select(audit_logs).where(audit_logs.c.registration_id == registrationid)
        ).fetchall()
        logging.info(f"Rows with registration_id={registrationid}: {rows}")
        for row in rows:
            logging.info(f"Row date: {row.date} (type: {type(row.date)})")
        # Now do the original query
        result = conn.execute(
            select(audit_logs).where(
                audit_logs.c.registration_id == registrationid,
                cast(audit_logs.c.date, Date) == date
            )
        ).first()
        logging.info(f"Query result: {result}")
        if not result:
            raise HTTPException(status_code=404, detail="Audit log not found")
        # Convert the result to a dictionary using the column names
        response_data = {
            "id": result.id,
            "date": result.date,
            "entitlement_type": result.entitlement_type,
            "name": result.name,
            "registration_id": result.registration_id,
            "lunch": result.lunch,
            "dinner": result.dinner,
            "lunch_takenon": result.lunch_takenon,
            "dinner_takenon": result.dinner_takenon,
            "token": current_user["token"]  # Use the token from current_user
        }
        return response_data

class AuditLogUpdate(BaseModel):
    registration_id: int
    date: str
    lunch: Optional[int] = None
    dinner: Optional[int] = None
    lunch_takenon: Optional[datetime] = None
    dinner_takenon: Optional[datetime] = None
    # Add other fields as needed

@app.post("/api/v1/user/update")
def update_user(
    update: AuditLogUpdate = Body(...),
    current_user: dict = Depends(get_current_user)
):
    update_data = update.dict(exclude_unset=True)
    registration_id = update_data.pop("registration_id")
    date = update_data.pop("date")
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update.")
    with engine.connect() as conn:
        result = conn.execute(
            audit_logs.update()
            .where(audit_logs.c.registration_id == registration_id)
            .where(audit_logs.c.date == date)
            .values(**update_data)
        )
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Audit log not found to update.")
        # Return the updated row
        updated = conn.execute(
            select(audit_logs).where(
                audit_logs.c.registration_id == registration_id,
                audit_logs.c.date == date
            )
        ).first()
        return {
            "id": updated.id,
            "date": updated.date,
            "entitlement_type": updated.entitlement_type,
            "name": updated.name,
            "registration_id": updated.registration_id,
            "lunch": updated.lunch,
            "dinner": updated.dinner,
            "lunch_takenon": updated.lunch_takenon,
            "dinner_takenon": updated.dinner_takenon,
            "updated_at": datetime.utcnow().isoformat(),
            "token": current_user["token"]  # Add token to response
        }

@app.post("/api/v1/register", response_model=User)
def register_user(user: UserCreate):
    with engine.connect() as conn:
        # Check if username already exists
        existing_user = conn.execute(
            select(users).where(users.c.username == user.username)
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # Check if email already exists
        existing_email = conn.execute(
            select(users).where(users.c.email == user.email)
        ).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        hashed_password = get_password_hash(user.password)
        result = conn.execute(
            users.insert().values(
                username=user.username,
                email=user.email,
                password=hashed_password
            )
        )
        conn.commit()
        
        # Get the created user
        new_user = conn.execute(
            select(users).where(users.c.id == result.inserted_primary_key[0])
        ).first()
        
        return {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }

@app.post("/api/v1/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    with engine.connect() as conn:
        user = conn.execute(
            select(users).where(users.c.username == form_data.username)
        ).first()
        
        if not user or not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/v1/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }

# Example of adding a new API endpoint
@app.get("/api/v1/status")
def get_status():
    return {
        "status": "active",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    } 