# Moonrider Task 1: Backend Identity Reconciliation API

This project is a FastAPI-based backend microservice built as part of Task 1 for Moonrider's technical assignment.  
It is designed to resolve user identities based on multiple contact inputs (email and phone number), handling linking of primary and secondary contacts based on overlaps.

---

## Features

- Identify and consolidate users by email or phone number
- Automatically manage `primary` and `secondary` contact relationships
- Filter out deleted records (`deletedAt`)
- Smart logging for traceability
- `/health` endpoint for service monitoring
- Clean UI with tags
- Error masking for stealth operations
- Sorted response fields, batch testing script

---

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- MySQL
- Uvicorn
- Pydantic

---

## Setup & Execution Steps

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/moonrider-task1-identity-reconciliation.git
cd moonrider-task1-identity-reconciliation
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # On Windows
# OR
source venv/bin/activate  # On Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` File
Create a `.env` file in the root folder:

```
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=identity_db
MYSQL_HOST=localhost
MYSQL_PORT=3306
```

### 5. Setup Database
Make sure your MySQL server is running and execute:
```sql
CREATE DATABASE identity_db;
```

### 6. Create Tables
```bash
python create_tables.py
```

### 7. Run the App
```bash
uvicorn app.main:app --reload
```

Visit Swagger UI at:
```
http://127.0.0.1:8000/docs
```

---

## Testing

Use `test.py` to send a sequence of sample requests:

```bash
python test.py
```

---

## Sample Request

```json
{
  "email": "doc@future.com",
  "phoneNumber": "1234567890"
}
```

## Sample Response

```json
{
  "primaryContactId": 1,
  "emails": ["doc@future.com", "cooldoc@future.com"],
  "phoneNumbers": ["1234567890"],
  "secondaryContactIds": [2]
}
```

---

## Folder Structure

```
Task1_ backend-identity-reconciliation/
├── app/
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── test.py
├── create_tables.py
├── requirements.txt
└── .env.example
```



