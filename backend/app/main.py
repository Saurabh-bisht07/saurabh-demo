from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .api.routes import api_router

import os

app = FastAPI(title="Blood & Organ Donation Matcher API", version="0.1.0")

# CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(api_router, prefix="/api")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}