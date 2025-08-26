from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_db
from ...services.ml import train_reliability_model, predict_reliability_for_all
from typing import Dict, List

router = APIRouter()


@router.post("/train", response_model=Dict[str, str])
def train(db: Session = Depends(get_db)):
    trained, info = train_reliability_model(db)
    return {"status": "trained" if trained else "skipped", "info": info}


@router.get("/predict", response_model=List[Dict[str, float]])
def predict(db: Session = Depends(get_db)):
    return predict_reliability_for_all(db)