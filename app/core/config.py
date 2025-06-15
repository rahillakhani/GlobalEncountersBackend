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
    
    # JWT settings
    SECRET_KEY: str = Field(default="your-secret-key-here", alias="JWT_SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # 15 minutes
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    REFRESH_TOKEN_SECRET_KEY: str = Field(default="your-refresh-secret-key-here", alias="JWT_REFRESH_SECRET_KEY")
    
    # Optional settings for other environment variables (if they exist in .env)
    port: Optional[int] = Field(8000, alias="PORT")

    @property
    def get_database_url(self) -> str:
        return self.database_url

settings = Settings() 