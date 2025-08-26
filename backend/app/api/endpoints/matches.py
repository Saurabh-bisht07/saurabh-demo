from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ... import models, schemas
from ...services.matching import find_best_donors

router = APIRouter()


@router.post("/by-patient/{patient_id}", response_model=List[schemas.MatchResult])
def match_by_patient(patient_id: int, limit: int = 10, db: Session = Depends(get_db)):
    patient = db.get(models.Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    donors = find_best_donors(
        db=db,
        patient_blood_group=patient.blood_group_needed,
        patient_lat=patient.latitude,
        patient_lng=patient.longitude,
        donation_type=patient.donation_type,
        organ=patient.organ,
        limit=limit,
    )
    return donors


@router.get("/search", response_model=List[schemas.MatchResult])
def match_by_params(
    blood_group: str = Query(...),
    latitude: float = Query(...),
    longitude: float = Query(...),
    donation_type: Optional[str] = Query(None),
    organ: Optional[str] = Query(None),
    limit: int = 10,
    db: Session = Depends(get_db),
):
    donors = find_best_donors(
        db=db,
        patient_blood_group=blood_group,
        patient_lat=latitude,
        patient_lng=longitude,
        donation_type=donation_type,
        organ=organ,
        limit=limit,
    )
    return donors