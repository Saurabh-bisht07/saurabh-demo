import os
import smtplib
from email.mime.text import MIMEText
from typing import Optional
from ..core.config import settings

try:
	from twilio.rest import Client as TwilioClient
except Exception:
	TwilioClient = None  # type: ignore

class Notifier:
	def __init__(self) -> None:
		self.smtp_host = settings.SMTP_HOST
		self.smtp_port = settings.SMTP_PORT
		self.smtp_user = settings.SMTP_USER
		self.smtp_password = settings.SMTP_PASSWORD
		self.smtp_from = settings.SMTP_FROM
		self.twilio_sid = settings.TWILIO_ACCOUNT_SID
		self.twilio_token = settings.TWILIO_AUTH_TOKEN
		self.twilio_from = settings.TWILIO_FROM_NUMBER
		self.twilio_client = None
		if self.twilio_sid and self.twilio_token and TwilioClient is not None:
			self.twilio_client = TwilioClient(self.twilio_sid, self.twilio_token)

	def send_email(self, to_email: str, subject: str, body: str) -> bool:
		if not self.smtp_host:
			return False
		msg = MIMEText(body)
		msg['Subject'] = subject
		msg['From'] = self.smtp_from
		msg['To'] = to_email
		try:
			with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
				server.starttls()
				if self.smtp_user:
					server.login(self.smtp_user, self.smtp_password)
				server.sendmail(self.smtp_from, [to_email], msg.as_string())
			return True
		except Exception:
			return False

	def send_sms(self, to_number: str, body: str) -> bool:
		if not self.twilio_client or not self.twilio_from:
			return False
		try:
			self.twilio_client.messages.create(
				to=to_number,
				from_=self.twilio_from,
				body=body,
			)
			return True
		except Exception:
			return False