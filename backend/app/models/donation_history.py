from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class DonationType(str, enum.Enum):
    BLOOD = "blood"
    ORGAN = "organ"

class DonationOutcome(str, enum.Enum):
    SUCCESSFUL = "successful"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
    MEDICAL_DECLINE = "medical_decline"

class DonationHistory(Base):
    __tablename__ = "donation_history"
    
    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("donors.id"), nullable=False)
    request_id = Column(Integer, ForeignKey("donation_requests.id"), nullable=False)
    
    # Donation details
    donation_type = Column(Enum(DonationType), nullable=False)
    scheduled_date = Column(DateTime, nullable=False)
    actual_date = Column(DateTime)
    
    # Outcome and feedback
    outcome = Column(Enum(DonationOutcome), nullable=False)
    feedback_rating = Column(Integer)  # 1-5 rating from recipient
    feedback_comment = Column(Text)
    
    # Medical information
    hemoglobin_level = Column(Float)  # For blood donations
    blood_pressure = Column(String)
    pulse_rate = Column(Integer)
    medical_notes = Column(Text)
    
    # Reliability metrics
    response_time_hours = Column(Float)  # Time from request to response
    punctuality_score = Column(Float)  # 0-1 score based on punctuality
    communication_score = Column(Float)  # 0-1 score based on communication
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    donor = relationship("Donor", back_populates="donation_history")