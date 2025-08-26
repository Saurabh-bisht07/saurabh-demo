from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database import get_db
from ... import models, schemas

router = APIRouter()


@router.post("/", response_model=schemas.PatientOut, status_code=201)
def create_patient(patient_in: schemas.PatientCreate, db: Session = Depends(get_db)):
    patient = models.Patient(
        name=patient_in.name,
        contact_email=patient_in.contact_email,
        contact_phone=patient_in.contact_phone,
        blood_group_needed=patient_in.blood_group_needed,
        latitude=patient_in.latitude,
        longitude=patient_in.longitude,
        city=patient_in.city,
        state=patient_in.state,
        country=patient_in.country,
        donation_type=patient_in.donation_type,
        organ=patient_in.organ,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.get("/{patient_id}", response_model=schemas.PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.get(models.Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient