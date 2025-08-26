from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
import json
import os

from app.models.notification import Notification, NotificationType, NotificationStatus
from app.models.user import User
from app.core.config import settings

# Twilio SMS
try:
    from twilio.rest import Client
    from twilio.base.exceptions import TwilioException
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False

# SendGrid Email
try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False

def send_sms(phone_number: str, message: str) -> bool:
    """Send SMS using Twilio."""
    if not TWILIO_AVAILABLE or not settings.TWILIO_ACCOUNT_SID:
        return False
    
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return True
    except TwilioException as e:
        print(f"Twilio SMS error: {e}")
        return False

def send_email(to_email: str, subject: str, message: str) -> bool:
    """Send email using SendGrid."""
    if not SENDGRID_AVAILABLE or not settings.SENDGRID_API_KEY:
        return False
    
    try:
        sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        mail = Mail(
            from_email=settings.FROM_EMAIL,
            to_emails=to_email,
            subject=subject,
            html_content=message
        )
        response = sg.send(mail)
        return response.status_code == 202
    except Exception as e:
        print(f"SendGrid email error: {e}")
        return False

def create_notification_record(
    db: Session,
    user_id: int,
    notification_type: NotificationType,
    title: str,
    message: str,
    recipient_email: Optional[str] = None,
    recipient_phone: Optional[str] = None,
    request_id: Optional[int] = None
) -> Notification:
    """Create a notification record in the database."""
    notification = Notification(
        user_id=user_id,
        request_id=request_id,
        notification_type=notification_type,
        title=title,
        message=message,
        recipient_email=recipient_email,
        recipient_phone=recipient_phone
    )
    
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def send_donation_request_notifications(request, donor, db: Session):
    """Send notifications for a new donation request."""
    # Get donor user information
    donor_user = db.query(User).filter(User.id == donor.user_id).first()
    
    # Create notification message
    urgency_emoji = {
        "low": "🟢",
        "normal": "🟡", 
        "high": "🟠",
        "critical": "🔴"
    }
    
    urgency_text = urgency_emoji.get(request.urgency_level, "🟡")
    
    sms_message = f"""
{urgency_text} URGENT: Blood/Organ Donation Request

Blood Group: {request.blood_group}
Location: {request.city}, {request.state}
Urgency: {request.urgency_level.upper()}
Contact: {request.contact_person} - {request.contact_phone}

Please respond if you can help!
    """.strip()
    
    email_subject = f"Urgent Donation Request - {request.blood_group} Blood Group"
    email_message = f"""
    <h2>{urgency_text} Urgent Donation Request</h2>
    <p><strong>Blood Group:</strong> {request.blood_group}</p>
    <p><strong>Location:</strong> {request.city}, {request.state}</p>
    <p><strong>Urgency Level:</strong> {request.urgency_level.upper()}</p>
    <p><strong>Contact Person:</strong> {request.contact_person}</p>
    <p><strong>Contact Phone:</strong> {request.contact_phone}</p>
    <p><strong>Hospital:</strong> {request.hospital_name or 'Not specified'}</p>
    <p><strong>Description:</strong> {request.description or 'No additional details'}</p>
    <br>
    <p>Please respond immediately if you can help with this donation request.</p>
    """
    
    # Send SMS
    sms_success = False
    if donor_user.phone:
        sms_success = send_sms(donor_user.phone, sms_message)
    
    # Send Email
    email_success = False
    if donor_user.email:
        email_success = send_email(donor_user.email, email_subject, email_message)
    
    # Create notification record
    notification_type = NotificationType.BOTH if (sms_success and email_success) else \
                       NotificationType.SMS if sms_success else \
                       NotificationType.EMAIL if email_success else NotificationType.EMAIL
    
    notification = create_notification_record(
        db=db,
        user_id=donor.user_id,
        notification_type=notification_type,
        title="New Donation Request",
        message=sms_message,
        recipient_email=donor_user.email,
        recipient_phone=donor_user.phone,
        request_id=request.id
    )
    
    # Update notification status
    if sms_success or email_success:
        notification.status = NotificationStatus.SENT
        notification.sent_at = datetime.utcnow()
        notification.delivery_confirmation = json.dumps({
            "sms_sent": sms_success,
            "email_sent": email_success,
            "timestamp": datetime.utcnow().isoformat()
        })
    else:
        notification.status = NotificationStatus.FAILED
    
    db.commit()
    
    return notification

def send_match_confirmation_notifications(request, donor, db: Session):
    """Send notifications when a request is matched with a donor."""
    # Get user information
    requester = db.query(User).filter(User.id == request.requester_id).first()
    donor_user = db.query(User).filter(User.id == donor.user_id).first()
    
    # Notify requester
    requester_sms = f"""
✅ Donation Request Matched!

Your request for {request.blood_group} blood has been matched with a donor.

Donor: {donor_user.full_name}
Contact: {donor_user.phone}

Please coordinate with the donor for donation details.
    """.strip()
    
    requester_email_subject = "Donation Request Matched Successfully"
    requester_email = f"""
    <h2>✅ Donation Request Matched!</h2>
    <p>Your request for <strong>{request.blood_group}</strong> blood has been successfully matched with a donor.</p>
    <p><strong>Donor Name:</strong> {donor_user.full_name}</p>
    <p><strong>Donor Phone:</strong> {donor_user.phone}</p>
    <p><strong>Donor Email:</strong> {donor_user.email}</p>
    <br>
    <p>Please coordinate with the donor to arrange the donation details.</p>
    """
    
    # Send notifications to requester
    if requester.phone:
        send_sms(requester.phone, requester_sms)
    if requester.email:
        send_email(requester.email, requester_email_subject, requester_email)
    
    # Notify donor
    donor_sms = f"""
🎯 You've been matched with a donation request!

Blood Group: {request.blood_group}
Location: {request.city}, {request.state}
Contact: {request.contact_person} - {request.contact_phone}

Please contact them to arrange donation details.
    """.strip()
    
    donor_email_subject = "You've been matched with a donation request"
    donor_email = f"""
    <h2>🎯 You've been matched with a donation request!</h2>
    <p><strong>Blood Group Required:</strong> {request.blood_group}</p>
    <p><strong>Location:</strong> {request.city}, {request.state}</p>
    <p><strong>Contact Person:</strong> {request.contact_person}</p>
    <p><strong>Contact Phone:</strong> {request.contact_phone}</p>
    <p><strong>Hospital:</strong> {request.hospital_name or 'Not specified'}</p>
    <br>
    <p>Please contact them to arrange the donation details.</p>
    """
    
    # Send notifications to donor
    if donor_user.phone:
        send_sms(donor_user.phone, donor_sms)
    if donor_user.email:
        send_email(donor_user.email, donor_email_subject, donor_email)