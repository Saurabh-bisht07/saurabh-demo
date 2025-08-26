from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import Optional, List
import math

from app.models.donor import Donor
from app.models.request import DonationRequest
from app.services.ml_service import predict_donor_reliability

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points using Haversine formula."""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_lat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def find_best_donor_match(request: DonationRequest, db: Session, max_distance_km: float = 50.0) -> Optional[Donor]:
    """
    Find the best donor match for a donation request using ML-based scoring.
    """
    # Build base query for compatible donors
    query = db.query(Donor).filter(
        and_(
            Donor.is_available == True,
            Donor.blood_group == request.blood_group
        )
    )
    
    # Filter by donation type
    if request.request_type.value == "blood":
        query = query.filter(Donor.can_donate_blood == True)
    elif request.request_type.value == "organ":
        query = query.filter(Donor.can_donate_organs == True)
        if request.organ_needed:
            query = query.filter(Donor.organs_available.contains(request.organ_needed))
    
    # Get all potential donors
    potential_donors = query.all()
    
    if not potential_donors:
        return None
    
    # Calculate scores for each donor
    donor_scores = []
    
    for donor in potential_donors:
        # Calculate distance
        distance = calculate_distance(
            request.latitude, request.longitude,
            donor.latitude, donor.longitude
        )
        
        # Skip if too far
        if distance > max_distance_km:
            continue
        
        # Calculate composite score
        # Factors: distance (30%), reliability (40%), urgency multiplier (30%)
        distance_score = max(0, 1 - (distance / max_distance_km))  # 0 to 1, closer is better
        reliability_score = donor.reliability_score  # Already 0 to 1
        
        # Urgency multiplier
        urgency_multiplier = {
            "low": 1.0,
            "normal": 1.2,
            "high": 1.5,
            "critical": 2.0
        }.get(request.urgency_level, 1.0)
        
        # Composite score
        composite_score = (
            distance_score * 0.3 +
            reliability_score * 0.4 +
            (1 - distance_score) * 0.3  # Additional weight for reliability
        ) * urgency_multiplier
        
        donor_scores.append({
            'donor': donor,
            'distance': distance,
            'composite_score': composite_score,
            'distance_score': distance_score,
            'reliability_score': reliability_score
        })
    
    if not donor_scores:
        return None
    
    # Sort by composite score (highest first)
    donor_scores.sort(key=lambda x: x['composite_score'], reverse=True)
    
    # Return the best match
    return donor_scores[0]['donor']

def find_multiple_donor_matches(
    request: DonationRequest, 
    db: Session, 
    max_distance_km: float = 50.0,
    max_results: int = 5
) -> List[dict]:
    """
    Find multiple donor matches for a donation request.
    """
    # Build base query for compatible donors
    query = db.query(Donor).filter(
        and_(
            Donor.is_available == True,
            Donor.blood_group == request.blood_group
        )
    )
    
    # Filter by donation type
    if request.request_type.value == "blood":
        query = query.filter(Donor.can_donate_blood == True)
    elif request.request_type.value == "organ":
        query = query.filter(Donor.can_donate_organs == True)
        if request.organ_needed:
            query = query.filter(Donor.organs_available.contains(request.organ_needed))
    
    # Get all potential donors
    potential_donors = query.all()
    
    if not potential_donors:
        return []
    
    # Calculate scores for each donor
    donor_scores = []
    
    for donor in potential_donors:
        # Calculate distance
        distance = calculate_distance(
            request.latitude, request.longitude,
            donor.latitude, donor.longitude
        )
        
        # Skip if too far
        if distance > max_distance_km:
            continue
        
        # Calculate composite score
        distance_score = max(0, 1 - (distance / max_distance_km))
        reliability_score = donor.reliability_score
        
        # Urgency multiplier
        urgency_multiplier = {
            "low": 1.0,
            "normal": 1.2,
            "high": 1.5,
            "critical": 2.0
        }.get(request.urgency_level, 1.0)
        
        # Composite score
        composite_score = (
            distance_score * 0.3 +
            reliability_score * 0.4 +
            (1 - distance_score) * 0.3
        ) * urgency_multiplier
        
        donor_scores.append({
            'donor': donor,
            'distance': distance,
            'composite_score': composite_score,
            'distance_score': distance_score,
            'reliability_score': reliability_score
        })
    
    # Sort by composite score and return top results
    donor_scores.sort(key=lambda x: x['composite_score'], reverse=True)
    return donor_scores[:max_results]

def update_donor_reliability_scores(db: Session):
    """
    Update reliability scores for all donors based on their donation history.
    """
    donors = db.query(Donor).all()
    
    for donor in donors:
        new_reliability_score = predict_donor_reliability(donor)
        donor.reliability_score = new_reliability_score
    
    db.commit()

def get_donor_match_analytics(request: DonationRequest, db: Session) -> dict:
    """
    Get analytics about potential donor matches for a request.
    """
    # Get all compatible donors
    query = db.query(Donor).filter(
        and_(
            Donor.is_available == True,
            Donor.blood_group == request.blood_group
        )
    )
    
    if request.request_type.value == "blood":
        query = query.filter(Donor.can_donate_blood == True)
    elif request.request_type.value == "organ":
        query = query.filter(Donor.can_donate_organs == True)
    
    compatible_donors = query.all()
    
    if not compatible_donors:
        return {
            "total_compatible": 0,
            "within_radius": 0,
            "avg_reliability": 0,
            "best_match_score": 0
        }
    
    # Calculate statistics
    distances = []
    reliability_scores = []
    
    for donor in compatible_donors:
        distance = calculate_distance(
            request.latitude, request.longitude,
            donor.latitude, donor.longitude
        )
        distances.append(distance)
        reliability_scores.append(donor.reliability_score)
    
    within_radius = len([d for d in distances if d <= 50.0])
    avg_reliability = sum(reliability_scores) / len(reliability_scores) if reliability_scores else 0
    
    # Get best match score
    best_match = find_best_donor_match(request, db)
    best_match_score = 0
    if best_match:
        distance = calculate_distance(
            request.latitude, request.longitude,
            best_match.latitude, best_match.longitude
        )
        distance_score = max(0, 1 - (distance / 50.0))
        best_match_score = (
            distance_score * 0.3 +
            best_match.reliability_score * 0.4 +
            (1 - distance_score) * 0.3
        )
    
    return {
        "total_compatible": len(compatible_donors),
        "within_radius": within_radius,
        "avg_reliability": round(avg_reliability, 3),
        "best_match_score": round(best_match_score, 3),
        "avg_distance": round(sum(distances) / len(distances), 2) if distances else 0
    }