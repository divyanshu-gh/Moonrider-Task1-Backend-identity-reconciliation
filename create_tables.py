# create_tables.py

from app.database import engine
from app.models import Base

# This creates all tables defined with SQLAlchemy models
Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully.")

