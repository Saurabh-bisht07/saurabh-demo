from __future__ import annotations
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from .. import models
import os
import pickle
import math

MODEL_PATH = os.getenv("MODEL_PATH", "/app/app/data/reliability_model.pkl")


def _extract_features_for_donor(donor: models.Donor) -> List[float]:
    total = donor.total_donations or 0
    reliability = donor.reliability_score or 0.5
    # Features: bias, total donations (log scaled), current reliability estimate
    return [1.0, math.log1p(total), reliability]


def train_reliability_model(db: Session) -> Tuple[bool, str]:
    donors = db.query(models.Donor).all()
    if len(donors) < 5:
        return False, "Insufficient donors to train. Using heuristic fallback."

    # Pseudo training: compute average completed rate from events and map to reliability
    # To keep lightweight without complex deps, we compute per-donor empirical reliability
    donor_scores: Dict[int, float] = {}
    for d in donors:
        events = d.donation_events
        if not events:
            donor_scores[d.id] = d.reliability_score or 0.5
            continue
        completed = sum(1 for e in events if e.outcome == "completed")
        total = len(events)
        donor_scores[d.id] = (completed + 1) / (total + 2)  # Laplace smoothing

    with open(MODEL_PATH, "wb") as f:
        pickle.dump({"version": 1, "scores": donor_scores}, f)

    # Update donors with latest reliability estimate
    for d in donors:
        d.reliability_score = donor_scores.get(d.id, d.reliability_score or 0.5)
        db.add(d)
    db.commit()

    return True, f"Trained with {len(donors)} donors."


def _load_model() -> Dict:
    if not os.path.exists(MODEL_PATH):
        return {"version": 1, "scores": {}}
    try:
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    except Exception:
        return {"version": 1, "scores": {}}


def predict_reliability(donor: models.Donor) -> float:
    model = _load_model()
    score = model.get("scores", {}).get(donor.id)
    if score is not None:
        return float(score)
    # Fallback heuristic
    features = _extract_features_for_donor(donor)
    # Weighted sum to [0,1]
    raw = 0.2 * features[1] + 0.8 * features[2]
    return max(0.05, min(0.99, raw))


def predict_reliability_for_all(db: Session) -> List[Dict[str, float]]:
    donors = db.query(models.Donor).all()
    out = []
    for d in donors:
        out.append({"donor_id": float(d.id), "reliability": predict_reliability(d)})
    return out