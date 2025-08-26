import os
import smtplib
from email.mime.text import MIMEText
from .. import models
from twilio.rest import Client

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT") or 0) or 587
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@donation.local")

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM")


def _send_email(to_email: str, subject: str, body: str) -> bool:
    if not SMTP_HOST or not SMTP_USER or not SMTP_PASS:
        return False
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_FROM
        msg["To"] = to_email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(EMAIL_FROM, [to_email], msg.as_string())
        return True
    except Exception:
        return False


def _send_sms(to_phone: str, body: str) -> bool:
    if not TWILIO_SID or not TWILIO_TOKEN or not TWILIO_FROM:
        return False
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        client.messages.create(to=to_phone, from_=TWILIO_FROM, body=body)
        return True
    except Exception:
        return False


def notify_donor(donor: models.Donor, patient: models.Patient) -> bool:
    subject = "Urgent: Donation Request Match"
    body = (
        f"Hello {donor.name},\n\n"
        f"A patient needs your help. Needed blood group: {patient.blood_group_needed}.\n"
        f"Location: ({patient.latitude}, {patient.longitude}).\n"
        f"If you are available, please respond to this message.\n\nThank you!"
    )
    email_ok = False
    sms_ok = False
    if donor.email:
        email_ok = _send_email(donor.email, subject, body)
    if donor.phone:
        sms_ok = _send_sms(donor.phone, body)
    return email_ok or sms_ok