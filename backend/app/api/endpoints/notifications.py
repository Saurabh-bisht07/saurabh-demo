from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ... import models
from ...services.matching import find_best_donors
from ...services.notify import notify_donor

router = APIRouter()


@router.post("/alert/{patient_id}")
def alert_donors(patient_id: int, top_n: int = 5, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    matches = find_best_donors(
        db=db,
        patient_blood_group=patient.blood_group_needed,
        patient_lat=patient.latitude,
        patient_lng=patient.longitude,
        donation_type=patient.donation_type,
        organ=patient.organ,
        limit=top_n,
    )

    sent = 0
    for m in matches:
        ok = notify_donor(m["donor"], patient)
        if ok:
            sent += 1
    return {"requested": top_n, "sent": sent}