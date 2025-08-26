from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .session import Base

class Donor(Base):
	__tablename__ = "donors"

	id = Column(Integer, primary_key=True, index=True)
	full_name = Column(String(255), nullable=False)
	email = Column(String(255), nullable=True, index=True)
	phone = Column(String(32), nullable=True, index=True)

	blood_group = Column(String(3), nullable=False, index=True)  # A, B, AB, O
	rh_factor = Column(String(1), nullable=False, index=True)     # + or -

	latitude = Column(Float, nullable=False)
	longitude = Column(Float, nullable=False)
	city = Column(String(255), nullable=True, index=True)
	country = Column(String(255), nullable=True, index=True)

	available_organs = Column(String(255), nullable=True)  # comma-separated organ names
	is_active = Column(Boolean, default=True)

	# Reliability-related fields
	last_donation_at = Column(DateTime, nullable=True)
	donations_count = Column(Integer, default=0)
	no_show_count = Column(Integer, default=0)
	responses_count = Column(Integer, default=0)
	requests_count = Column(Integer, default=0)

	created_at = Column(DateTime, default=datetime.utcnow)
	updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

	history = relationship("DonationHistory", back_populates="donor", cascade="all, delete-orphan")

class DonationHistory(Base):
	__tablename__ = "donation_history"

	id = Column(Integer, primary_key=True)
	donor_id = Column(Integer, ForeignKey("donors.id", ondelete="CASCADE"), index=True, nullable=False)
	date = Column(DateTime, default=datetime.utcnow)
	outcome = Column(String(32), default="completed")  # completed, cancelled, no_show
	notes = Column(String(512), nullable=True)

	donor = relationship("Donor", back_populates="history")