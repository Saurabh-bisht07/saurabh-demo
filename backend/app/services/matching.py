from typing import List, Optional, Dict
from math import radians, sin, cos, asin, sqrt
from sqlalchemy.orm import Session
from .. import models, schemas
from .ml import predict_reliability


BLOOD_COMPATIBILITY = {
    "O-": set(["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]),
    "O+": set(["O+", "A+", "B+", "AB+"]),
    "A-": set(["A-", "A+", "AB-", "AB+"]),
    "A+": set(["A+", "AB+"]),
    "B-": set(["B-", "B+", "AB-", "AB+"]),
    "B+": set(["B+", "AB+"]),
    "AB-": set(["AB-", "AB+"]),
    "AB+": set(["AB+"]),
}


def can_donate(donor_bg: str, patient_bg: str) -> bool:
    donors_for_patient = {d for d, recipients in BLOOD_COMPATIBILITY.items() if patient_bg in recipients}
    return donor_bg in donors_for_patient


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c


def find_best_donors(
    db: Session,
    patient_blood_group: str,
    patient_lat: float,
    patient_lng: float,
    donation_type: Optional[str] = None,
    organ: Optional[str] = None,
    limit: int = 10,
) -> List[Dict]:
    query = db.query(models.Donor).filter(models.Donor.is_available == True)
    donors: List[models.Donor] = query.all()

    results: List[Dict] = []

    for donor in donors:
        if not can_donate(donor.blood_group, patient_blood_group):
            continue
        if donation_type:
            if not donor.donation_types:
                continue
            types = set([t.strip().lower() for t in donor.donation_types.split(",") if t.strip()])
            if donation_type.lower() not in types:
                continue
        if organ and donation_type and donation_type.lower() == "organ":
            # Optional: in future, filter by specific organ capability
            pass

        distance = haversine_km(patient_lat, patient_lng, donor.latitude, donor.longitude)
        reliability = predict_reliability(donor)
        score = 0.6 * (1.0 / (1.0 + distance)) + 0.4 * reliability
        results.append({
            "donor": donor,
            "distance_km": round(distance, 2),
            "reliability": float(round(reliability, 3)),
            "_score": score,
        })

    results.sort(key=lambda x: x["_score"], reverse=True)
    return [{k: v for k, v in r.items() if k != "_score"} for r in results[:limit]]