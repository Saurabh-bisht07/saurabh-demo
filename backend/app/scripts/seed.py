from sqlalchemy.orm import Session
from ..db.session import SessionLocal
from ..db import models

SAMPLE_DONORS = [
	{"full_name": "Alice Johnson", "email": "alice@example.com", "phone": "+15550001", "blood_group": "O", "rh_factor": "+", "latitude": 37.7749, "longitude": -122.4194, "city": "San Francisco", "country": "USA", "available_organs": "blood"},
	{"full_name": "Bob Smith", "email": "bob@example.com", "phone": "+15550002", "blood_group": "A", "rh_factor": "+", "latitude": 37.3382, "longitude": -121.8863, "city": "San Jose", "country": "USA", "available_organs": "blood"},
	{"full_name": "Carol Lee", "email": "carol@example.com", "phone": "+15550003", "blood_group": "B", "rh_factor": "-", "latitude": 37.8044, "longitude": -122.2711, "city": "Oakland", "country": "USA", "available_organs": "blood"},
	{"full_name": "David Kim", "email": "david@example.com", "phone": "+15550004", "blood_group": "AB", "rh_factor": "+", "latitude": 37.7749, "longitude": -122.4194, "city": "San Francisco", "country": "USA", "available_organs": "blood"},
]

def run() -> None:
	session: Session = SessionLocal()
	try:
		for data in SAMPLE_DONORS:
			donor = models.Donor(**data)
			session.add(donor)
		session.commit()
	finally:
		session.close()

if __name__ == "__main__":
	run()