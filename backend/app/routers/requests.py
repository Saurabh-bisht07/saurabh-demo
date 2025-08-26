from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Any
from datetime import datetime

from app.database import get_db
from app.core.security import verify_token
from app.models.user import User
from app.models.request import DonationRequest, RequestStatus
from app.schemas.request import RequestCreate, RequestResponse, RequestUpdate, RequestSearch
from app.services.matching_service import find_best_donor_match
from app.services.notification_service import send_donation_request_notifications

router = APIRouter()

def get_current_user(token: str = Depends(verify_token)):
    return token

@router.post("/create", response_model=RequestResponse)
def create_donation_request(
    request_data: RequestCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Create a new donation request.
    """
    requester_id = current_user.get("user_id")
    
    # Create donation request
    db_request = DonationRequest(
        requester_id=requester_id,
        **request_data.dict()
    )
    
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    
    # Try to find a match immediately
    if request_data.urgency_level in ["high", "critical"]:
        best_match = find_best_donor_match(db_request, db)
        if best_match:
            db_request.matched_donor_id = best_match.id
            db_request.status = RequestStatus.MATCHED
            db_request.matched_at = datetime.utcnow()
            db.commit()
            db.refresh(db_request)
            
            # Send notifications
            send_donation_request_notifications(db_request, best_match, db)
    
    # Get requester information for response
    requester = db.query(User).filter(User.id == requester_id).first()
    response_data = db_request.__dict__.copy()
    response_data.update({
        "requester_name": requester.full_name,
        "requester_email": requester.email
    })
    
    return RequestResponse(**response_data)

@router.get("/my-requests", response_model=List[RequestResponse])
def get_my_requests(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get current user's donation requests.
    """
    requester_id = current_user.get("user_id")
    
    requests = db.query(DonationRequest).filter(
        DonationRequest.requester_id == requester_id
    ).order_by(DonationRequest.created_at.desc()).all()
    
    requester = db.query(User).filter(User.id == requester_id).first()
    
    response_list = []
    for req in requests:
        response_data = req.__dict__.copy()
        response_data.update({
            "requester_name": requester.full_name,
            "requester_email": requester.email
        })
        response_list.append(RequestResponse(**response_data))
    
    return response_list

@router.get("/search", response_model=List[RequestResponse])
def search_requests(
    blood_group: str = Query(None, description="Filter by blood group"),
    request_type: str = Query(None, description="Filter by request type"),
    status: str = Query(None, description="Filter by status"),
    city: str = Query(None, description="Filter by city"),
    limit: int = Query(20, description="Number of results"),
    offset: int = Query(0, description="Offset for pagination"),
    db: Session = Depends(get_db)
) -> Any:
    """
    Search for donation requests.
    """
    query = db.query(DonationRequest).join(User)
    
    if blood_group:
        query = query.filter(DonationRequest.blood_group == blood_group)
    if request_type:
        query = query.filter(DonationRequest.request_type == request_type)
    if status:
        query = query.filter(DonationRequest.status == status)
    if city:
        query = query.filter(DonationRequest.city.ilike(f"%{city}%"))
    
    requests = query.order_by(DonationRequest.created_at.desc()).offset(offset).limit(limit).all()
    
    response_list = []
    for req in requests:
        response_data = req.__dict__.copy()
        response_data.update({
            "requester_name": req.requester.full_name,
            "requester_email": req.requester.email
        })
        response_list.append(RequestResponse(**response_data))
    
    return response_list

@router.get("/{request_id}", response_model=RequestResponse)
def get_request_details(
    request_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """
    Get details of a specific donation request.
    """
    request = db.query(DonationRequest).filter(DonationRequest.id == request_id).first()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        )
    
    response_data = request.__dict__.copy()
    response_data.update({
        "requester_name": request.requester.full_name,
        "requester_email": request.requester.email
    })
    
    return RequestResponse(**response_data)

@router.put("/{request_id}", response_model=RequestResponse)
def update_request(
    request_id: int,
    request_data: RequestUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Update a donation request.
    """
    requester_id = current_user.get("user_id")
    request = db.query(DonationRequest).filter(
        DonationRequest.id == request_id,
        DonationRequest.requester_id == requester_id
    ).first()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found or access denied"
        )
    
    # Update fields
    update_data = request_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(request, field, value)
    
    db.commit()
    db.refresh(request)
    
    response_data = request.__dict__.copy()
    response_data.update({
        "requester_name": request.requester.full_name,
        "requester_email": request.requester.email
    })
    
    return RequestResponse(**response_data)

@router.post("/{request_id}/match")
def match_request(
    request_id: int,
    donor_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Manually match a request with a donor.
    """
    requester_id = current_user.get("user_id")
    request = db.query(DonationRequest).filter(
        DonationRequest.id == request_id,
        DonationRequest.requester_id == requester_id
    ).first()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found or access denied"
        )
    
    # Verify donor exists and is compatible
    from app.models.donor import Donor
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    
    if not donor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donor not found"
        )
    
    if donor.blood_group != request.blood_group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Blood group mismatch"
        )
    
    # Update request
    request.matched_donor_id = donor_id
    request.status = RequestStatus.MATCHED
    request.matched_at = datetime.utcnow()
    
    db.commit()
    
    # Send notifications
    send_donation_request_notifications(request, donor, db)
    
    return {"message": "Request matched successfully", "donor_id": donor_id}

@router.post("/{request_id}/complete")
def complete_request(
    request_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Mark a request as completed.
    """
    requester_id = current_user.get("user_id")
    request = db.query(DonationRequest).filter(
        DonationRequest.id == request_id,
        DonationRequest.requester_id == requester_id
    ).first()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found or access denied"
        )
    
    if request.status != RequestStatus.MATCHED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request must be matched before completion"
        )
    
    request.status = RequestStatus.COMPLETED
    db.commit()
    
    return {"message": "Request completed successfully"}