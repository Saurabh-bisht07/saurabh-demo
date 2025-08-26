from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/donation_matcher"
    
    # JWT
    JWT_SECRET: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Twilio SMS
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None
    
    # SendGrid Email
    SENDGRID_API_KEY: Optional[str] = None
    FROM_EMAIL: str = "noreply@donationmatcher.com"
    
    # ML Model
    ML_MODEL_PATH: str = "ml_model/donor_reliability_model.pkl"
    
    # API
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Blood & Organ Donation Matcher"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()