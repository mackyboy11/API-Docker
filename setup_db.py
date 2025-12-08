from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base, DBRole
import crud

# Create tables (safe to call even if already created)
Base.metadata.create_all(bind=engine)


def init_db():
    db: Session = SessionLocal()
    try:
        # Create roles if they don't exist
        if not db.query(DBRole).filter(DBRole.name == "user").first():
            crud.create_role(db, "user", "Regular user")
        if not db.query(DBRole).filter(DBRole.name == "admin").first():
            crud.create_role(db, "admin", "Administrator")
        if not db.query(DBRole).filter(DBRole.name == "moderator").first():
            crud.create_role(db, "moderator", "Moderator")
    finally:
        db.close()
    print("Database initialized successfully!")


if __name__ == "__main__":
    init_db()
