from fastapi import APIRouter
from .endpoints import donors, patients, matches, ml, notifications

api_router = APIRouter()

api_router.include_router(donors.router, prefix="/donors", tags=["donors"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(matches.router, prefix="/matches", tags=["matches"])
api_router.include_router(ml.router, prefix="/ml", tags=["ml"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])