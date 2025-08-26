from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class RequestStatus(str, enum.Enum):
    PENDING = "pending"
    MATCHED = "matched"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

class RequestType(str, enum.Enum):
    BLOOD = "blood"
    ORGAN = "organ"
    BOTH = "both"

class DonationRequest(Base):
    __tablename__ = "donation_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Request details
    request_type = Column(Enum(RequestType), nullable=False)
    blood_group = Column(String, nullable=False)
    organ_needed = Column(String)  # Only for organ requests
    
    # Location
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, default="India")
    
    # Urgency and details
    urgency_level = Column(String, default="normal")  # low, normal, high, critical
    required_by_date = Column(DateTime)
    description = Column(Text)
    
    # Status and matching
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDING)
    matched_donor_id = Column(Integer, ForeignKey("donors.id"))
    matched_at = Column(DateTime)
    
    # Contact information
    contact_person = Column(String, nullable=False)
    contact_phone = Column(String, nullable=False)
    hospital_name = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    requester = relationship("User", back_populates="donation_requests")
    matched_donor = relationship("Donor")