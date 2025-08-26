from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict
from ..db.session import get_db
from ..db import models
from ..schemas import AlertRequest
from ..services.notify import Notifier

router = APIRouter()

@router.post("/send")
def send_alerts(payload: AlertRequest, db: Session = Depends(get_db)) -> Dict[str, int]:
	donors = db.query(models.Donor).filter(models.Donor.id.in_(payload.donor_ids)).all()
	if not donors:
		raise HTTPException(status_code=404, detail="No donors found for given ids")
	notifier = Notifier()
	sent = 0
	for d in donors:
		ok_sms = ok_email = False
		if payload.via_sms and d.phone:
			ok_sms = notifier.send_sms(d.phone, payload.message)
		if payload.via_email and d.email:
			ok_email = notifier.send_email(d.email, "Urgent Donation Match", payload.message)
		if ok_sms or ok_email:
			sent += 1
	return {"requested": len(payload.donor_ids), "notified": sent}