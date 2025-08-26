from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
import json

class DonorBase(BaseModel):
    blood_group: str
    can_donate_blood: bool = True
    can_donate_organs: bool = False
    organs_available: Optional[str] = None
    latitude: float
    longitude: float
    city: str
    state: str
    country: str = "India"
    age: int
    weight: Optional[float] = None
    height: Optional[float] = None
    medical_conditions: Optional[str] = None
    medications: Optional[str] = None
    is_available: bool = True
    availability_notes: Optional[str] = None

    @validator('blood_group')
    def validate_blood_group(cls, v):
        valid_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        if v not in valid_groups:
            raise ValueError(f'Blood group must be one of {valid_groups}')
        return v

    @validator('organs_available', 'medical_conditions', 'medications')
    def validate_json_fields(cls, v):
        if v is not None:
            try:
                json.loads(v)
            except json.JSONDecodeError:
                raise ValueError('Must be valid JSON string')
        return v

class DonorCreate(DonorBase):
    pass

class DonorUpdate(BaseModel):
    blood_group: Optional[str] = None
    can_donate_blood: Optional[bool] = None
    can_donate_organs: Optional[bool] = None
    organs_available: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None
    state: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    medical_conditions: Optional[str] = None
    medications: Optional[str] = None
    is_available: Optional[bool] = None
    availability_notes: Optional[str] = None

class DonorSearch(BaseModel):
    blood_group: Optional[str] = None
    request_type: Optional[str] = None  # blood, organ, both
    organ_needed: Optional[str] = None
    latitude: float
    longitude: float
    radius_km: float = 50.0
    max_results: int = 10

class DonorResponse(DonorBase):
    id: int
    user_id: int
    reliability_score: float
    last_donation_date: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    
    # User information
    user_full_name: str
    user_email: str
    user_phone: str
    
    class Config:
        from_attributes = True