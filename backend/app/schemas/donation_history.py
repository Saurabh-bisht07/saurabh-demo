from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.donation_history import DonationType, DonationOutcome

class DonationHistoryBase(BaseModel):
    donation_type: DonationType
    scheduled_date: datetime
    actual_date: Optional[datetime] = None
    outcome: DonationOutcome
    feedback_rating: Optional[int] = None
    feedback_comment: Optional[str] = None
    hemoglobin_level: Optional[float] = None
    blood_pressure: Optional[str] = None
    pulse_rate: Optional[int] = None
    medical_notes: Optional[str] = None
    response_time_hours: Optional[float] = None
    punctuality_score: Optional[float] = None
    communication_score: Optional[float] = None

class DonationHistoryCreate(DonationHistoryBase):
    donor_id: int
    request_id: int

class DonationHistoryResponse(DonationHistoryBase):
    id: int
    donor_id: int
    request_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True