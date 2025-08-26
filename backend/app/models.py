from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Donor(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(50), nullable=True)

    blood_group = Column(String(5), index=True, nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city = Column(String(120), nullable=True)
    state = Column(String(120), nullable=True)
    country = Column(String(120), nullable=True)

    donation_types = Column(Text, nullable=True)  # comma-separated like "blood,organ"

    is_available = Column(Boolean, default=True, index=True)

    total_donations = Column(Integer, default=0)
    reliability_score = Column(Float, default=0.5)
    last_donation_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    donation_events = relationship("DonationEvent", back_populates="donor")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)

    blood_group_needed = Column(String(5), index=True, nullable=False)
    donation_type = Column(String(50), nullable=True)  # blood or organ
    organ = Column(String(80), nullable=True)  # e.g., kidney, liver

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city = Column(String(120), nullable=True)
    state = Column(String(120), nullable=True)
    country = Column(String(120), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DonationEvent(Base):
    __tablename__ = "donation_events"

    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("donors.id"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)

    outcome = Column(String(30), nullable=False)  # completed, no_show, cancelled
    notes = Column(Text, nullable=True)
    event_at = Column(DateTime(timezone=True), server_default=func.now())

    donor = relationship("Donor", back_populates="donation_events")