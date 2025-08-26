from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any


class DonorBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    blood_group: str
    latitude: float
    longitude: float
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    donation_types: Optional[List[str]] = None


class DonorCreate(DonorBase):
    pass


class DonorUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    blood_group: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    donation_types: Optional[List[str]] = None
    is_available: Optional[bool] = None


class DonorOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    blood_group: str
    latitude: float
    longitude: float
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    donation_types: Optional[List[str]] = None
    is_available: bool
    total_donations: int
    reliability_score: float

    class Config:
        from_attributes = True


class PatientCreate(BaseModel):
    name: str
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    blood_group_needed: str
    donation_type: Optional[str] = None
    organ: Optional[str] = None
    latitude: float
    longitude: float
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None


class PatientOut(BaseModel):
    id: int
    name: str
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    blood_group_needed: str
    donation_type: Optional[str] = None
    organ: Optional[str] = None
    latitude: float
    longitude: float
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

    class Config:
        from_attributes = True


class MatchResult(BaseModel):
    donor: DonorOut
    distance_km: float
    reliability: float


class DonationEventCreate(BaseModel):
    donor_id: int
    patient_id: Optional[int] = None
    outcome: str
    notes: Optional[str] = None


class DonationEventOut(BaseModel):
    id: int
    donor_id: int
    patient_id: Optional[int]
    outcome: str
    notes: Optional[str]

    class Config:
        from_attributes = True