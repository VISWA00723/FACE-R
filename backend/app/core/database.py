"""
Database connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """
    Database dependency for FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables
    """
    # Ensure model metadata is registered before table creation
    from app.models.employee import Employee  # noqa: F401
    from app.models.attendance import AttendanceLog  # noqa: F401
    from app.models.user import User  # noqa: F401

    Base.metadata.create_all(bind=engine)
    ensure_default_users()


def ensure_default_users():
    """Ensure example admin and user accounts exist."""
    from app.models.user import User
    from app.core.security import get_password_hash

    db = SessionLocal()
    try:
        defaults = [
            {"username": "admin", "password": "Admin@12345", "role": "admin"},
            {"username": "user", "password": "User@12345", "role": "user"},
        ]

        for item in defaults:
            existing = db.query(User).filter(User.username == item["username"]).first()
            if existing:
                continue
            db.add(User(username=item["username"], password_hash=get_password_hash(item["password"]), role=item["role"], is_active=True))

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
