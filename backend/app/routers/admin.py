from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Any, Dict
from datetime import datetime, timedelta

from app.database import get_db
from app.core.security import verify_token
from app.models.user import User
from app.models.donor import Donor
from app.models.request import DonationRequest, RequestStatus
from app.models.donation_history import DonationHistory
from app.services.ml_service import train_model
from app.services.matching_service import update_donor_reliability_scores

router = APIRouter()

def get_current_user(token: str = Depends(verify_token)):
    return token

def verify_admin(current_user: dict = Depends(get_current_user)):
    """Verify that the current user is an admin."""
    if current_user.get("user_type") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

@router.get("/dashboard")
def get_admin_dashboard(
    current_user: dict = Depends(verify_admin),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get admin dashboard statistics.
    """
    # User statistics
    total_users = db.query(User).count()
    total_donors = db.query(Donor).count()
    active_donors = db.query(Donor).filter(Donor.is_available == True).count()
    
    # Request statistics
    total_requests = db.query(DonationRequest).count()
    pending_requests = db.query(DonationRequest).filter(
        DonationRequest.status == RequestStatus.PENDING
    ).count()
    matched_requests = db.query(DonationRequest).filter(
        DonationRequest.status == RequestStatus.MATCHED
    ).count()
    completed_requests = db.query(DonationRequest).filter(
        DonationRequest.status == RequestStatus.COMPLETED
    ).count()
    
    # Recent activity (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_users = db.query(User).filter(User.created_at >= thirty_days_ago).count()
    recent_requests = db.query(DonationRequest).filter(
        DonationRequest.created_at >= thirty_days_ago
    ).count()
    
    # Blood group distribution
    blood_group_stats = db.query(
        Donor.blood_group,
        func.count(Donor.id).label('count')
    ).group_by(Donor.blood_group).all()
    
    blood_group_distribution = {
        stat.blood_group: stat.count for stat in blood_group_stats
    }
    
    return {
        "users": {
            "total": total_users,
            "donors": total_donors,
            "active_donors": active_donors,
            "recent_registrations": recent_users
        },
        "requests": {
            "total": total_requests,
            "pending": pending_requests,
            "matched": matched_requests,
            "completed": completed_requests,
            "recent": recent_requests
        },
        "blood_group_distribution": blood_group_distribution,
        "success_rate": round((completed_requests / total_requests * 100), 2) if total_requests > 0 else 0
    }

@router.get("/analytics/requests")
def get_request_analytics(
    current_user: dict = Depends(verify_admin),
    days: int = 30,
    db: Session = Depends(get_db)
) -> Any:
    """
    Get detailed request analytics.
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Daily request counts
    daily_requests = db.query(
        func.date(DonationRequest.created_at).label('date'),
        func.count(DonationRequest.id).label('count')
    ).filter(
        DonationRequest.created_at >= start_date
    ).group_by(
        func.date(DonationRequest.created_at)
    ).order_by(
        func.date(DonationRequest.created_at)
    ).all()
    
    # Request type distribution
    request_type_stats = db.query(
        DonationRequest.request_type,
        func.count(DonationRequest.id).label('count')
    ).filter(
        DonationRequest.created_at >= start_date
    ).group_by(DonationRequest.request_type).all()
    
    # Urgency level distribution
    urgency_stats = db.query(
        DonationRequest.urgency_level,
        func.count(DonationRequest.id).label('count')
    ).filter(
        DonationRequest.created_at >= start_date
    ).group_by(DonationRequest.urgency_level).all()
    
    return {
        "daily_requests": [
            {"date": str(stat.date), "count": stat.count} 
            for stat in daily_requests
        ],
        "request_types": {
            stat.request_type.value: stat.count for stat in request_type_stats
        },
        "urgency_levels": {
            stat.urgency_level: stat.count for stat in urgency_stats
        }
    }

@router.get("/analytics/donors")
def get_donor_analytics(
    current_user: dict = Depends(verify_admin),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get donor analytics and reliability statistics.
    """
    # Reliability score distribution
    reliability_ranges = [
        (0.0, 0.2, "Low"),
        (0.2, 0.4, "Below Average"),
        (0.4, 0.6, "Average"),
        (0.6, 0.8, "Above Average"),
        (0.8, 1.0, "High")
    ]
    
    reliability_stats = {}
    for min_score, max_score, label in reliability_ranges:
        count = db.query(Donor).filter(
            and_(
                Donor.reliability_score >= min_score,
                Donor.reliability_score < max_score
            )
        ).count()
        reliability_stats[label] = count
    
    # Age distribution
    age_ranges = [
        (18, 25, "18-25"),
        (26, 35, "26-35"),
        (36, 45, "36-45"),
        (46, 55, "46-55"),
        (56, 65, "56-65"),
        (66, 100, "65+")
    ]
    
    age_stats = {}
    for min_age, max_age, label in age_ranges:
        count = db.query(Donor).filter(
            and_(
                Donor.age >= min_age,
                Donor.age <= max_age
            )
        ).count()
        age_stats[label] = count
    
    # Top donors by reliability
    top_donors = db.query(Donor).order_by(
        Donor.reliability_score.desc()
    ).limit(10).all()
    
    return {
        "reliability_distribution": reliability_stats,
        "age_distribution": age_stats,
        "top_donors": [
            {
                "id": donor.id,
                "name": donor.user.full_name,
                "blood_group": donor.blood_group,
                "reliability_score": donor.reliability_score,
                "total_donations": len(donor.donation_history)
            }
            for donor in top_donors
        ],
        "avg_reliability": db.query(func.avg(Donor.reliability_score)).scalar() or 0
    }

@router.post("/ml/train")
def train_ml_model(
    current_user: dict = Depends(verify_admin),
    db: Session = Depends(get_db)
) -> Any:
    """
    Train the ML model for donor reliability prediction.
    """
    try:
        success = train_model(db)
        if success:
            return {"message": "ML model trained successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to train ML model"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error training ML model: {str(e)}"
        )

@router.post("/donors/update-reliability")
def update_all_donor_reliability(
    current_user: dict = Depends(verify_admin),
    db: Session = Depends(get_db)
) -> Any:
    """
    Update reliability scores for all donors.
    """
    try:
        update_donor_reliability_scores(db)
        return {"message": "Donor reliability scores updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating reliability scores: {str(e)}"
        )

@router.get("/users")
def get_all_users(
    current_user: dict = Depends(verify_admin),
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
) -> Any:
    """
    Get all users (admin only).
    """
    users = db.query(User).offset(offset).limit(limit).all()
    
    return [
        {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "user_type": user.user_type,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "has_donor_profile": user.donor_profile is not None
        }
        for user in users
    ]

@router.get("/requests")
def get_all_requests(
    current_user: dict = Depends(verify_admin),
    status: str = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
) -> Any:
    """
    Get all donation requests (admin only).
    """
    query = db.query(DonationRequest)
    
    if status:
        query = query.filter(DonationRequest.status == status)
    
    requests = query.offset(offset).limit(limit).all()
    
    return [
        {
            "id": req.id,
            "blood_group": req.blood_group,
            "request_type": req.request_type.value,
            "urgency_level": req.urgency_level,
            "status": req.status.value,
            "city": req.city,
            "state": req.state,
            "created_at": req.created_at,
            "requester_name": req.requester.full_name,
            "matched_donor_id": req.matched_donor_id
        }
        for req in requests
    ]