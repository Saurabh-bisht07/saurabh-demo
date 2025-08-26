from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from app.models.request import RequestStatus, RequestType

class RequestBase(BaseModel):
    request_type: RequestType
    blood_group: str
    organ_needed: Optional[str] = None
    latitude: float
    longitude: float
    city: str
    state: str
    country: str = "India"
    urgency_level: str = "normal"
    required_by_date: Optional[datetime] = None
    description: Optional[str] = None
    contact_person: str
    contact_phone: str
    hospital_name: Optional[str] = None

    @validator('blood_group')
    def validate_blood_group(cls, v):
        valid_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        if v not in valid_groups:
            raise ValueError(f'Blood group must be one of {valid_groups}')
        return v

    @validator('urgency_level')
    def validate_urgency_level(cls, v):
        valid_levels = ['low', 'normal', 'high', 'critical']
        if v not in valid_levels:
            raise ValueError(f'Urgency level must be one of {valid_levels}')
        return v

class RequestCreate(RequestBase):
    pass

class RequestUpdate(BaseModel):
    request_type: Optional[RequestType] = None
    blood_group: Optional[str] = None
    organ_needed: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None
    state: Optional[str] = None
    urgency_level: Optional[str] = None
    required_by_date: Optional[datetime] = None
    description: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    hospital_name: Optional[str] = None
    status: Optional[RequestStatus] = None

class RequestSearch(BaseModel):
    blood_group: Optional[str] = None
    request_type: Optional[RequestType] = None
    organ_needed: Optional[str] = None
    status: Optional[RequestStatus] = None
    urgency_level: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    limit: int = 20
    offset: int = 0

class RequestResponse(RequestBase):
    id: int
    requester_id: int
    status: RequestStatus
    matched_donor_id: Optional[int] = None
    matched_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime]
    
    # Requester information
    requester_name: str
    requester_email: str
    
    class Config:
        from_attributes = True