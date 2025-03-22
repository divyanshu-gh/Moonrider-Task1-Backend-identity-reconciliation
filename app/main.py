# app/main.py

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from app.schemas import IdentifyRequest, IdentifyResponse
from app.database import SessionLocal
from app import crud

tags_metadata = [
    {
        "name": "Identity",
        "description": "Operations related to contact identity resolution.",
    },
    {
        "name": "System",
        "description": "System-level health and diagnostics.",
    },
]

app = FastAPI(
    title="Moonrider Identity Reconciliation API",
    description="API for resolving user identity using email and phone numbers. Built for Zamazon.com 🚀",
    version="1.0.0",
    openapi_tags=tags_metadata
)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Identity service is running"}

# Identify endpoint
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "message": "Identity service is running"}

@app.post("/identify", response_model=IdentifyResponse, tags=["Identity"])
def identify(payload: IdentifyRequest, db: Session = Depends(get_db)):
    if not payload.email and not payload.phoneNumber:
        raise HTTPException(
        status_code=403,
        detail="🔒 Request blocked. Identity verification checkpoint not satisfied."
    )
    response = crud.identify_contact(db, payload)
    return response
