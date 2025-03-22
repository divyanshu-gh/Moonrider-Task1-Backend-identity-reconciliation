# app/crud.py

from sqlalchemy.orm import Session
from app.models import Contact, LinkPrecedence
from app.schemas import IdentifyRequest
from typing import List
from sqlalchemy import or_

def identify_contact(db: Session, payload: IdentifyRequest):
    email = payload.email
    phone = payload.phoneNumber

    # Step 1: Find all existing contacts with matching email or phone number
    existing_contacts = db.query(Contact).filter(
        or_(Contact.email == email, Contact.phoneNumber == phone),
        Contact.deletedAt.is_(None)  # 👈 Ignore soft-deleted contacts
    ).all()

    print(f"[MATCH] Found {len(existing_contacts)} active contact(s) matching email/phone.")

    if not existing_contacts:
        # No match found → create new primary contact
        new_contact = Contact(
            email=email,
            phoneNumber=phone,
            linkPrecedence=LinkPrecedence.primary
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)

        print(f"[CREATE] New PRIMARY contact created: ID={new_contact.id}, Email={email}, Phone={phone}")

        return {
            "primaryContactId": new_contact.id,
            "emails": [new_contact.email] if new_contact.email else [],
            "phoneNumbers": [new_contact.phoneNumber] if new_contact.phoneNumber else [],
            "secondaryContactIds": []
        }

    # Step 2: Separate contacts into primary and secondary
    all_contacts = set()
    primary_contact = None

    for contact in existing_contacts:
        all_contacts.add(contact)
        if contact.linkPrecedence == LinkPrecedence.primary:
            if not primary_contact or contact.createdAt < primary_contact.createdAt:
                primary_contact = contact

    # Step 3: If no primary found, pick earliest and mark it as primary
    if not primary_contact:
        primary_contact = sorted(existing_contacts, key=lambda x: x.createdAt)[0]
        primary_contact.linkPrecedence = LinkPrecedence.primary
        primary_contact.linkedId = None
        db.commit()
        print(f"[REASSIGN] Promoted contact ID={primary_contact.id} to PRIMARY")

    # Step 4: Link any new contact info not in existing
    new_data_exists = True
    for contact in all_contacts:
        if contact.email == email and contact.phoneNumber == phone:
            new_data_exists = False
            break

    if new_data_exists:
        new_secondary = Contact(
            email=email,
            phoneNumber=phone,
            linkedId=primary_contact.id,
            linkPrecedence=LinkPrecedence.secondary
        )
        db.add(new_secondary)
        db.commit()
        db.refresh(new_secondary)
        all_contacts.add(new_secondary)

        print(f"[LINK] New SECONDARY contact created: ID={new_secondary.id}, linked to PRIMARY ID={primary_contact.id}")

    # Step 5: Collect final consolidated info
    emails = set()
    phones = set()
    secondary_ids = []

    for contact in all_contacts:
        if contact.linkPrecedence == LinkPrecedence.secondary:
            secondary_ids.append(contact.id)
        emails.add(contact.email)
        phones.add(contact.phoneNumber)

    print(f"[RESPONSE] Consolidated info → Primary ID={primary_contact.id}, Emails={emails}, Phones={phones}, Secondary IDs={secondary_ids}")

    return {
        "primaryContactId": primary_contact.id,
        "emails": list(filter(None, emails)),
        "phoneNumbers": list(filter(None, phones)),
        "secondaryContactIds": secondary_ids
    }
