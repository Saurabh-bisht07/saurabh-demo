from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.notification import NotificationType, NotificationStatus

class NotificationBase(BaseModel):
    notification_type: NotificationType
    title: str
    message: str
    recipient_email: Optional[str] = None
    recipient_phone: Optional[str] = None

class NotificationCreate(NotificationBase):
    user_id: int
    request_id: Optional[int] = None

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    request_id: Optional[int] = None
    status: NotificationStatus
    sent_at: Optional[datetime] = None
    delivery_confirmation: Optional[str] = None
    retry_count: int
    max_retries: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True