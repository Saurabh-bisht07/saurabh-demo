from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .db.session import Base, engine
from .api.donors import router as donors_router
from .api.matching import router as matching_router
from .api.alerts import router as alerts_router
from .services.ml import ml_service

app = FastAPI(title="Blood & Organ Donation Matcher API", version="0.1.0")

# Allow local dev frontend
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.on_event("startup")
def on_startup() -> None:
	# Create database tables if they do not exist
	Base.metadata.create_all(bind=engine)
	# Warm up the ML model from existing data
	ml_service.train_if_needed()

app.include_router(donors_router, prefix="/donors", tags=["donors"])
app.include_router(matching_router, prefix="/match", tags=["match"])
app.include_router(alerts_router, prefix="/alerts", tags=["alerts"])

@app.get("/health")
def health() -> dict:
	return {"status": "ok", "app": app.title, "env": settings.APP_ENV}