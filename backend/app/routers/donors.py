from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Any
import math

from app.database import get_db
from app.core.security import verify_token
from app.models.user import User
from app.models.donor import Donor
from app.schemas.donor import DonorCreate, DonorResponse, DonorUpdate, DonorSearch
from app.services.ml_service import predict_donor_reliability

router = APIRouter()

def get_current_user(token: str = Depends(verify_token)):
    return token

@router.post("/register", response_model=DonorResponse)
def register_donor(
    donor_data: DonorCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Register as a blood/organ donor.
    """
    user_id = current_user.get("user_id")
    
    # Check if user already has a donor profile
    existing_donor = db.query(Donor).filter(Donor.user_id == user_id).first()
    if existing_donor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a donor profile"
        )
    
    # Create donor profile
    db_donor = Donor(
        user_id=user_id,
        **donor_data.dict()
    )
    
    # Calculate initial reliability score
    db_donor.reliability_score = predict_donor_reliability(db_donor)
    
    db.add(db_donor)
    db.commit()
    db.refresh(db_donor)
    
    # Get user information for response
    user = db.query(User).filter(User.id == user_id).first()
    response_data = db_donor.__dict__.copy()
    response_data.update({
        "user_full_name": user.full_name,
        "user_email": user.email,
        "user_phone": user.phone
    })
    
    return DonorResponse(**response_data)

@router.get("/search", response_model=List[DonorResponse])
def search_donors(
    blood_group: str = Query(..., description="Blood group required"),
    request_type: str = Query(..., description="Type of donation needed: blood, organ, both"),
    organ_needed: str = Query(None, description="Specific organ needed"),
    latitude: float = Query(..., description="Search latitude"),
    longitude: float = Query(..., description="Search longitude"),
    radius_km: float = Query(50.0, description="Search radius in kilometers"),
    max_results: int = Query(10, description="Maximum number of results"),
    db: Session = Depends(get_db)
) -> Any:
    """
    Search for compatible donors within a radius.
    """
    # Build query
    query = db.query(Donor).join(User).filter(
        Donor.is_available == True,
        Donor.blood_group == blood_group
    )
    
    # Filter by donation type
    if request_type == "blood":
        query = query.filter(Donor.can_donate_blood == True)
    elif request_type == "organ":
        query = query.filter(Donor.can_donate_organs == True)
        if organ_needed:
            query = query.filter(Donor.organs_available.contains(organ_needed))
    
    # Calculate distance and filter by radius
    # Using Haversine formula for distance calculation
    distance_formula = func.acos(
        func.cos(func.radians(latitude)) * 
        func.cos(func.radians(Donor.latitude)) * 
        func.cos(func.radians(longitude) - func.radians(Donor.longitude)) + 
        func.sin(func.radians(latitude)) * 
        func.sin(func.radians(Donor.latitude))
    ) * 6371  # Earth's radius in km
    
    query = query.add_columns(distance_formula.label('distance'))
    query = query.filter(distance_formula <= radius_km)
    query = query.order_by('distance', Donor.reliability_score.desc())
    query = query.limit(max_results)
    
    results = query.all()
    
    # Format response
    donor_responses = []
    for donor, distance in results:
        response_data = donor.__dict__.copy()
        response_data.update({
            "user_full_name": donor.user.full_name,
            "user_email": donor.user.email,
            "user_phone": donor.user.phone,
            "distance_km": round(distance, 2)
        })
        donor_responses.append(DonorResponse(**response_data))
    
    return donor_responses

@router.get("/profile", response_model=DonorResponse)
def get_donor_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get current user's donor profile.
    """
    user_id = current_user.get("user_id")
    donor = db.query(Donor).filter(Donor.user_id == user_id).first()
    
    if not donor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donor profile not found"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    response_data = donor.__dict__.copy()
    response_data.update({
        "user_full_name": user.full_name,
        "user_email": user.email,
        "user_phone": user.phone
    })
    
    return DonorResponse(**response_data)

@router.put("/profile", response_model=DonorResponse)
def update_donor_profile(
    donor_data: DonorUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Update donor profile.
    """
    user_id = current_user.get("user_id")
    donor = db.query(Donor).filter(Donor.user_id == user_id).first()
    
    if not donor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donor profile not found"
        )
    
    # Update fields
    update_data = donor_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(donor, field, value)
    
    # Recalculate reliability score if needed
    if update_data:
        donor.reliability_score = predict_donor_reliability(donor)
    
    db.commit()
    db.refresh(donor)
    
    user = db.query(User).filter(User.id == user_id).first()
    response_data = donor.__dict__.copy()
    response_data.update({
        "user_full_name": user.full_name,
        "user_email": user.email,
        "user_phone": user.phone
    })
    
    return DonorResponse(**response_data)

@router.get("/stats")
def get_donor_stats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get donor statistics and reliability metrics.
    """
    user_id = current_user.get("user_id")
    donor = db.query(Donor).filter(Donor.user_id == user_id).first()
    
    if not donor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donor profile not found"
        )
    
    # Get donation history
    from app.models.donation_history import DonationHistory
    history = db.query(DonationHistory).filter(
        DonationHistory.donor_id == donor.id
    ).all()
    
    total_donations = len(history)
    successful_donations = len([h for h in history if h.outcome == "successful"])
    success_rate = (successful_donations / total_donations * 100) if total_donations > 0 else 0
    
    return {
        "total_donations": total_donations,
        "successful_donations": successful_donations,
        "success_rate": round(success_rate, 2),
        "reliability_score": donor.reliability_score,
        "last_donation_date": donor.last_donation_date,
        "is_available": donor.is_available
    }