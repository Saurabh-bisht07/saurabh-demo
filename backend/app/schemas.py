from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class ORMBase(BaseModel):
	model_config = {
		"from_attributes": True
	}

class DonorBase(BaseModel):
	full_name: str = Field(..., min_length=2, max_length=255)
	email: Optional[EmailStr] = None
	phone: Optional[str] = None
	blood_group: str = Field(..., pattern=r"^(A|B|AB|O)$")
	rh_factor: str = Field(..., pattern=r"^[\+\-]$")
	latitude: float
	longitude: float
	city: Optional[str] = None
	country: Optional[str] = None
	available_organs: Optional[str] = None
	is_active: Optional[bool] = True

class DonorCreate(DonorBase):
	pass

class DonorUpdate(BaseModel):
	full_name: Optional[str] = None
	email: Optional[EmailStr] = None
	phone: Optional[str] = None
	blood_group: Optional[str] = Field(None, pattern=r"^(A|B|AB|O)$")
	rh_factor: Optional[str] = Field(None, pattern=r"^[\+\-]$")
	latitude: Optional[float] = None
	longitude: Optional[float] = None
	city: Optional[str] = None
	country: Optional[str] = None
	available_organs: Optional[str] = None
	is_active: Optional[bool] = None

class DonorOut(ORMBase):
	id: int
	full_name: str
	email: Optional[EmailStr]
	phone: Optional[str]
	blood_group: str
	rh_factor: str
	latitude: float
	longitude: float
	city: Optional[str]
	country: Optional[str]
	available_organs: Optional[str]
	is_active: bool
	last_donation_at: Optional[datetime]
	donations_count: int
	no_show_count: int
	responses_count: int
	requests_count: int
	created_at: datetime
	updated_at: datetime
	reliability_score: Optional[float] = None
	distance_km: Optional[float] = None

class DonationHistoryCreate(BaseModel):
	donor_id: int
	date: Optional[datetime] = None
	outcome: str = Field(default="completed", pattern=r"^(completed|cancelled|no_show)$")
	notes: Optional[str] = None

class MatchQuery(BaseModel):
	patient_blood_group: str = Field(..., pattern=r"^(A|B|AB|O)$")
	patient_rh_factor: str = Field(..., pattern=r"^[\+\-]$")
	latitude: float
	longitude: float
	max_km: float = 50.0
	organ: Optional[str] = None
	limit: int = 20

class AlertRequest(BaseModel):
	donor_ids: List[int]
	message: str = Field(..., min_length=2, max_length=600)
	via_sms: bool = True
	via_email: bool = True