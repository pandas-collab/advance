"""Database configuration and connection management."""
import os
from contextlib import contextmanager
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# Database URL from environment or default to SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./age_calculator.db")

# Create engine with appropriate settings
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
metadata = MetaData()

@contextmanager
def get_db_session() -> Session:
    """Get database session with proper cleanup."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def get_db() -> Session:
    """Dependency for FastAPI endpoints."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables."""
    from ...auth.models import Base
    Base.metadata.create_all(bind=engine)

def get_db_health() -> dict:
    """Check database connectivity."""
    try:
        with get_db_session() as db:
            db.execute("SELECT 1")
            return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": f"error: {str(e)}"}
