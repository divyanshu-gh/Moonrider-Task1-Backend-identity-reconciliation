# app/models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

# Enum to represent if a contact is primary or secondary
class LinkPrecedence(str, enum.Enum):
    primary = "primary"
    secondary = "secondary"

# Contact table definition
class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)

    phoneNumber = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)

    # If this is a secondary contact, this links to the primary contact's ID
    linkedId = Column(Integer, ForeignKey("contacts.id"), nullable=True)

    # Either 'primary' or 'secondary' to define contact type
    linkPrecedence = Column(Enum(LinkPrecedence), default=LinkPrecedence.primary)

    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deletedAt = Column(DateTime(timezone=True), nullable=True)

