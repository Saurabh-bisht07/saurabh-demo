from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Any

from app.database import get_db
from app.core.security import verify_token
from app.models.notification import Notification, NotificationStatus
from app.schemas.notification import NotificationResponse

router = APIRouter()

def get_current_user(token: str = Depends(verify_token)):
    return token

@router.get("/history", response_model=List[NotificationResponse])
def get_notification_history(
    current_user: dict = Depends(get_current_user),
    limit: int = Query(20, description="Number of results"),
    offset: int = Query(0, description="Offset for pagination"),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get notification history for current user.
    """
    user_id = current_user.get("user_id")
    
    notifications = db.query(Notification).filter(
        Notification.user_id == user_id
    ).order_by(Notification.created_at.desc()).offset(offset).limit(limit).all()
    
    return notifications

@router.get("/unread-count")
def get_unread_notifications_count(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get count of unread notifications.
    """
    user_id = current_user.get("user_id")
    
    count = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.status == NotificationStatus.SENT
    ).count()
    
    return {"unread_count": count}

@router.post("/{notification_id}/mark-read")
def mark_notification_read(
    notification_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Mark a notification as read.
    """
    user_id = current_user.get("user_id")
    
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == user_id
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    notification.status = NotificationStatus.SENT  # Mark as read
    db.commit()
    
    return {"message": "Notification marked as read"}

@router.post("/mark-all-read")
def mark_all_notifications_read(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Mark all notifications as read.
    """
    user_id = current_user.get("user_id")
    
    db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.status == NotificationStatus.SENT
    ).update({"status": NotificationStatus.SENT})
    
    db.commit()
    
    return {"message": "All notifications marked as read"}