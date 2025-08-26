import os
from functools import lru_cache
from pydantic import BaseModel
from pydantic import Field
from pydantic import computed_field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
	APP_ENV: str = Field(default=os.getenv("APP_ENV", "development"))
	API_HOST: str = Field(default=os.getenv("API_HOST", "0.0.0.0"))
	API_PORT: int = Field(default=int(os.getenv("API_PORT", "8000")))

	POSTGRES_HOST: str = Field(default=os.getenv("POSTGRES_HOST", "db"))
	POSTGRES_PORT: int = Field(default=int(os.getenv("POSTGRES_PORT", "5432")))
	POSTGRES_DB: str = Field(default=os.getenv("POSTGRES_DB", "donations"))
	POSTGRES_USER: str = Field(default=os.getenv("POSTGRES_USER", "postgres"))
	POSTGRES_PASSWORD: str = Field(default=os.getenv("POSTGRES_PASSWORD", "postgres"))

	SMTP_HOST: str = Field(default=os.getenv("SMTP_HOST", ""))
	SMTP_PORT: int = Field(default=int(os.getenv("SMTP_PORT", "587")))
	SMTP_USER: str = Field(default=os.getenv("SMTP_USER", ""))
	SMTP_PASSWORD: str = Field(default=os.getenv("SMTP_PASSWORD", ""))
	SMTP_FROM: str = Field(default=os.getenv("SMTP_FROM", "noreply@example.com"))

	TWILIO_ACCOUNT_SID: str = Field(default=os.getenv("TWILIO_ACCOUNT_SID", ""))
	TWILIO_AUTH_TOKEN: str = Field(default=os.getenv("TWILIO_AUTH_TOKEN", ""))
	TWILIO_FROM_NUMBER: str = Field(default=os.getenv("TWILIO_FROM_NUMBER", ""))

	@computed_field
	@property
	def DATABASE_URL(self) -> str:
		user = self.POSTGRES_USER
		password = self.POSTGRES_PASSWORD
		host = self.POSTGRES_HOST
		port = self.POSTGRES_PORT
		db = self.POSTGRES_DB
		return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

@lru_cache
def get_settings() -> Settings:
	return Settings()

settings = get_settings()