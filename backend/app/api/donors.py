from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..db import models
from ..schemas import DonorCreate, DonorOut, DonorUpdate
from typing import List, Optional

router = APIRouter()

@router.post("/register", response_model=DonorOut)
def register_donor(payload: DonorCreate, db: Session = Depends(get_db)) -> DonorOut:
	donor = models.Donor(
		full_name=payload.full_name,
		email=payload.email,
		phone=payload.phone,
		blood_group=payload.blood_group,
		rh_factor=payload.rh_factor,
		latitude=payload.latitude,
		longitude=payload.longitude,
		city=payload.city,
		country=payload.country,
		available_organs=payload.available_organs,
		is_active=payload.is_active if payload.is_active is not None else True,
	)
	db.add(donor)
	db.commit()
	db.refresh(donor)
	out = DonorOut.model_validate(donor)
	return out

@router.get("/{donor_id}", response_model=DonorOut)
def get_donor(donor_id: int, db: Session = Depends(get_db)) -> DonorOut:
	donor = db.query(models.Donor).filter(models.Donor.id == donor_id).first()
	if not donor:
		raise HTTPException(status_code=404, detail="Donor not found")
	return DonorOut.model_validate(donor)

@router.patch("/{donor_id}", response_model=DonorOut)
def update_donor(donor_id: int, payload: DonorUpdate, db: Session = Depends(get_db)) -> DonorOut:
	donor = db.query(models.Donor).filter(models.Donor.id == donor_id).first()
	if not donor:
		raise HTTPException(status_code=404, detail="Donor not found")
	for field, value in payload.model_dump(exclude_unset=True).items():
		setattr(donor, field, value)
	db.add(donor)
	db.commit()
	db.refresh(donor)
	return DonorOut.model_validate(donor)

@router.get("/", response_model=List[DonorOut])
def list_donors(
	blood_group: Optional[str] = None,
	rh_factor: Optional[str] = None,
	city: Optional[str] = None,
	country: Optional[str] = None,
	only_active: bool = True,
	db: Session = Depends(get_db),
) -> List[DonorOut]:
	q = db.query(models.Donor)
	if blood_group:
		q = q.filter(models.Donor.blood_group == blood_group)
	if rh_factor:
		q = q.filter(models.Donor.rh_factor == rh_factor)
	if city:
		q = q.filter(models.Donor.city == city)
	if country:
		q = q.filter(models.Donor.country == country)
	if only_active:
		q = q.filter(models.Donor.is_active.is_(True))
	return [DonorOut.model_validate(d) for d in q.limit(100).all()]