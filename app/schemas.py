# app/schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional, List

# Request schema
class IdentifyRequest(BaseModel):
    email: Optional[EmailStr] = None
    phoneNumber: Optional[str] = None

# Response schema
class IdentifyResponse(BaseModel):
    primaryContactId: int
    emails: List[str]
    phoneNumbers: List[str]
    secondaryContactIds: List[int]

