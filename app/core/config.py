from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=True)

    PROJECT_NAME: str = "Global Encounters API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database settings - explicitly mapped from DATABASE_URL in .env
    database_url: str = Field(alias="DATABASE_URL") # Using alias to map to DATABASE_URL in .env
    
    # Optional settings for other environment variables (if they exist in .env)
    jwt_secret_key: Optional[str] = Field(None, alias="JWT_SECRET_KEY")
    port: Optional[int] = Field(8000, alias="PORT")

settings = Settings() 