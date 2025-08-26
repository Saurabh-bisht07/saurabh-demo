from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..db.session import get_db
from ..db import models
from ..schemas import MatchQuery, DonorOut
from ..services.geo import haversine_km, is_blood_compatible
from ..services.ml import ml_service

router = APIRouter()

@router.post("/search", response_model=List[DonorOut])
def search_donors(payload: MatchQuery, db: Session = Depends(get_db)) -> List[DonorOut]:
	candidates = db.query(models.Donor).filter(models.Donor.is_active.is_(True)).all()
	# Filter by blood compatibility and optional organ
	filtered = []
	for d in candidates:
		if not is_blood_compatible(d.blood_group, d.rh_factor, payload.patient_blood_group, payload.patient_rh_factor):
			continue
		if payload.organ:
			if not d.available_organs:
				continue
			orgs = {o.strip().lower() for o in d.available_organs.split(',') if o.strip()}
			if payload.organ.strip().lower() not in orgs:
				continue
		dist_km = haversine_km(payload.latitude, payload.longitude, d.latitude, d.longitude)
		if dist_km <= payload.max_km:
			filtered.append((d, dist_km))
	# Rank by ML reliability, then distance
	if not filtered:
		return []
	donors_only = [d for d, _ in filtered]
	ranked = ml_service.rank_donors(donors_only)
	score_map = {d.id: score for d, score in ranked}
	# Merge with distance and sort: higher score first, then nearer
	merged = []
	for d, dist_km in filtered:
		score = score_map.get(d.id, 0.0)
		merged.append((d, score, dist_km))
	merged.sort(key=lambda x: (-x[1], x[2]))
	results: List[DonorOut] = []
	for d, score, dist_km in merged[: payload.limit]:
		out = DonorOut.model_validate(d)
		out.reliability_score = float(score)
		out.distance_km = float(dist_km)
		results.append(out)
	return results