from sqlalchemy.orm import Session
from db.session import SessionLocal, engine
from db.base import Base  # Import Base correctly
from models.user import User
from models.file import File  # Ensure models are imported to register with SQLAlchemy

def init_db(db: Session) -> None:
    # Create tables
    Base.metadata.create_all(bind=engine)

# Example of initializing the DB, usually called from an external script or startup script
if __name__ == "__main__":
    db = SessionLocal()
    init_db(db)
    db.close()
