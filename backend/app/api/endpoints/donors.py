from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database import get_db
from ... import models, schemas
from typing import List

router = APIRouter()


@router.post("/", response_model=schemas.DonorOut, status_code=201)
def create_donor(donor_in: schemas.DonorCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Donor).filter(models.Donor.email == donor_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Donor with this email already exists")
    donor = models.Donor(
        name=donor_in.name,
        email=donor_in.email,
        phone=donor_in.phone,
        blood_group=donor_in.blood_group,
        latitude=donor_in.latitude,
        longitude=donor_in.longitude,
        city=donor_in.city,
        state=donor_in.state,
        country=donor_in.country,
        donation_types=",".join(donor_in.donation_types) if donor_in.donation_types else None,
        is_available=True,
    )
    db.add(donor)
    db.commit()
    db.refresh(donor)
    return donor


@router.get("/{donor_id}", response_model=schemas.DonorOut)
def get_donor(donor_id: int, db: Session = Depends(get_db)):
    donor = db.get(models.Donor, donor_id)
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    return donor


@router.put("/{donor_id}", response_model=schemas.DonorOut)
def update_donor(donor_id: int, donor_update: schemas.DonorUpdate, db: Session = Depends(get_db)):
    donor = db.get(models.Donor, donor_id)
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")

    update_data = donor_update.dict(exclude_unset=True)
    if "donation_types" in update_data and update_data["donation_types"] is not None:
        update_data["donation_types"] = ",".join(update_data["donation_types"]) if update_data["donation_types"] else None

    for key, value in update_data.items():
        setattr(donor, key, value)
    db.add(donor)
    db.commit()
    db.refresh(donor)
    return donor


@router.get("/", response_model=List[schemas.DonorOut])
def list_donors(db: Session = Depends(get_db)):
    return db.query(models.Donor).order_by(models.Donor.created_at.desc()).all()