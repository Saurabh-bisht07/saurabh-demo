from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geography
from app.database import Base

class Donor(Base):
    __tablename__ = "donors"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Blood and organ information
    blood_group = Column(String, nullable=False)  # A+, A-, B+, B-, AB+, AB-, O+, O-
    can_donate_blood = Column(Boolean, default=True)
    can_donate_organs = Column(Boolean, default=False)
    organs_available = Column(Text)  # JSON string of available organs
    
    # Location
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location = Column(Geography(geometry_type='POINT', srid=4326))
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, default="India")
    
    # Medical information
    age = Column(Integer, nullable=False)
    weight = Column(Float)  # in kg
    height = Column(Float)  # in cm
    medical_conditions = Column(Text)  # JSON string of medical conditions
    medications = Column(Text)  # JSON string of current medications
    last_donation_date = Column(DateTime)
    
    # Availability
    is_available = Column(Boolean, default=True)
    availability_notes = Column(Text)
    
    # Reliability score (ML predicted)
    reliability_score = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="donor_profile")
    donation_history = relationship("DonationHistory", back_populates="donor")